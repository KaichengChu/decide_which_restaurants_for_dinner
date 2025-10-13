from model.llm_model import get_response_from_llm
from service.email_service import send_email
def main():
    response = get_response_from_llm()
    result = send_email(response)
    print(result)

if __name__ == "__main__":
    main()