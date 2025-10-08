import torch
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from retrieve import get_menu_info
from config import CONFIG
import json

def create_llm():
    """
    Loads a non-quantized Hugging Face model (Phi-3-mini).
    """
    model_id = "microsoft/Phi-3-mini-4k-instruct"

    # Check for Apple Silicon GPU (MPS)
    if torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map=device,
        trust_remote_code=True,
        torch_dtype=torch.float16, 
        attn_implementation="eager"
    )
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=200,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
        return_full_text=False,
        )
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm



def main():
    with open('model/prompt_pref.txt', 'r', encoding='utf-8') as f:
        prompt_pref = f.read()

    with open('model/prompt_task.txt', 'r', encoding='utf-8') as f:
        prompt_task = f.read()

    bruin_plate_url = CONFIG['restaurants_url']['BRUIN_PLATE_URL']
    de_neve_url = CONFIG['restaurants_url']['DE_NEVE_URL']
    epicuria_url = CONFIG['restaurants_url']['EPICURIA_URL']

    print("Fetched menu information from all restaurants.")
    
    menus = [
        get_menu_info(bruin_plate_url),
        get_menu_info(de_neve_url),
        get_menu_info(epicuria_url)    
    ]
    print("Fetch LLM model")
    
    llm = create_llm()
    prompt = PromptTemplate(
        template = prompt_task,
        input_variables = ["preferences", "menus"],
    )

    chain = prompt | llm | StrOutputParser()

    print("Generating recommendation...\n")

    response = chain.invoke({
        "preferences": prompt_pref,
        "menus": json.dumps(menus, ensure_ascii=False)
    })
    print("\n--- AI Dining Recommendation ---")
    print(response)

if __name__ == "__main__":
    main()