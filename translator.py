import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """You are an expert translator specializing in Singlish — a casual mix of Sinhala and English commonly used in Sri Lanka.

Your job is to translate Singlish (Sinhala words written in English letters mixed with actual English words) into clear, natural English.

Rules:
- Understand Sinhala words written phonetically in English (e.g. "mokakda", "kohomada", "api", "eka", "wage", "ne", "machang", "bung", "aney")
- Preserve the original meaning and tone (casual, formal, emotional, etc.)
- Output ONLY the English translation — no explanations, no notes, no extra text
- If the input is already fully in English, return it as-is
- Handle informal, slang, and everyday conversational Singlish naturally

Examples:
Input:  "Machang, kohomada? Api gamu."
Output: "Dude, how are you? Let's go."

Input:  "Eka godak hodai, mata kamati."
Output: "That is really good, I like it."

Input:  "Oyage name eka mokakda?"
Output: "What is your name?"

Input:  "Ahanna, api cinema gamu tonight?"
Output: "Hey, shall we go to the cinema tonight?"
"""


def translate_singlish(text: str) -> dict:
    if not text or not text.strip():
        return {"error": "Text cannot be empty", "translated_text": None}

    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nNow translate this:\nInput: {text}\nOutput:"

        response = model.generate_content(full_prompt)
        translated = response.text.strip()

        return {
            "source_language": "Singlish",
            "target_language": "English",
            "original_text": text,
            "translated_text": translated
        }

    except Exception as e:
        return {"error": f"Translation failed: {str(e)}", "translated_text": None}