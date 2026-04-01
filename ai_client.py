import google.generativeai as genai
from config import GEMINI_API_KEY

#ai
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def classify_file_sample(sample_text, sector_hint="Unknown"):
    prompt = f"""
    Analyze this file sample from the {sector_hint} sector:
    "{sample_text}"
    
    Task:
    1. Categorize the file (e.g., Invoice, Medical Record, Public Flyer).
    2. Give a Risk Score from 1 to 10 (10 being most sensitive/private).
    
    Return ONLY a JSON-style response like this:
    {{"category": "category_name", "risk_score": 5}}
    """
    
    try:
        response = model.generate_content(prompt)
       
       
        result = eval(response.text)
        return result.get("category", "Unknown"), result.get("risk_score", 1)
    except:
        return "Analysis Failed", 1
