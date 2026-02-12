from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from translator import translate_singlish

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslationRequest(BaseModel):
    text: str

    @field_validator("text")
    def text_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        return v


@app.get("/")
def home():
    return {"message": "Singlish → English Translator is running 🚀 (powered by Gemini)"}


@app.post("/translate")
def translate(req: TranslationRequest):
    result = translate_singlish(req.text)

    if "error" in result:
        return {
            "bot_message": "Oops! Something went wrong 😕",
            "error": result["error"]
        }

    return {
        "bot_message": "Here's the English translation 😊",
        "original_text": result["original_text"],
        "translation": result["translated_text"],
        "source_language": result["source_language"],
        "target_language": result["target_language"]
    }