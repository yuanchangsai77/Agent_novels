import google.generativeai as genai
from agents.utils.config import load_api_key, MODEL_NAME

api_key = load_api_key()
genai.configure(api_key=api_key, transport='rest')

def test_gemini_api(prompt):
    model = genai.GenerativeModel(model_name=MODEL_NAME)
    response = model.generate_content(prompt)
    
    print("API Response:")
    print(response.text)

if __name__ == "__main__":
    test_prompt = "Write a short novel about games in Chinese."
    test_gemini_api(test_prompt)