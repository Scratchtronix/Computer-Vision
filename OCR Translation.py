import pytesseract
import requests
from openai import OpenAI

text = pytesseract.image_to_string("YOUR-SAMPLE-IMAGE")
print(text)
key = OpenAI(api_key="PASTE-IN-YOUR-API-KEY")
lang = input("Please enter the language you want to translate this text to: ")
response = key.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role" : "system", "content" : "You are a translator."},
        {"role" : "user", "content" : f"Translate this text and return only the translated text in the language {lang}, and not anything else-{text}."}
    ]
)
print(response.choices[0].message["content"])
