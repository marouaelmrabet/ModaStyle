
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Clé API introuvable.")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": (
                "Tu es un assistant commercial de ModaStyle. "
                "Tu réponds en français, clairement et poliment."
            )
        },
        {
            "role": "user",
            "content": (
                "Quel est le délai de livraison à Fès ? "
                "Réponds uniquement que tu ne disposes pas "
                "de cette information documentaire."
            )
        }
    ],
    temperature=0.2,
    max_completion_tokens=300
)

print("\n========== REPONSE DU MODELE ==========\n")
print(response.choices[0].message.content)

print("\n========== INFORMATIONS ==========")
print("Modèle :", response.model)
