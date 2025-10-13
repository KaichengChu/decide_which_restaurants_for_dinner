from sentence_transformers import SentenceTransformer, util
from config import CONFIG
from retrieve import get_menu_info
# Load the pre-trained model

if __name__ == "__main__":
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Prepare the preference text
    with open('model/prompt.txt', 'r', encoding='utf-8') as f:
        preference = f.read()

    bruin_plate_url = CONFIG['restaurants_url']['BRUIN_PLATE_URL']
    de_neve_url = CONFIG['restaurants_url']['DE_NEVE_URL']
    epicuria_url = CONFIG['restaurants_url']['EPICURIA_URL']

    menus = [
        get_menu_info(bruin_plate_url),
        get_menu_info(de_neve_url),
        get_menu_info(epicuria_url)
    ]

    pref_embedding = model.encode(preference, convert_to_tensor=True)

    scores = []
    
    for menu in menus:
        menu_text = ' '.join([item for station in menu["dinner_menu"].values() for item in station])
        menu_embedding = model.encode(menu_text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(pref_embedding, menu_embedding).item()
    
        try:
            crowd_level = float(menu.get("activity_level", "0"))
        except ValueError:
            crowd_level = 0.0
        
        adjusted_score = similarity * (1-(crowd_level+1)/100)

        scores.append((menu["restaurant_name"], adjusted_score, menu['dinner_menu']))
    scores.sort(key=lambda x:x[1], reverse=True)

    for name, score, dinner_menu in scores:
        print(f"Restaurant: {name}, Score: {score:.4f}")
        for station, items in dinner_menu.items():
            print(f"  {station}:")
            for item in items:
                print(f"    - {item}")
        print("\n")

