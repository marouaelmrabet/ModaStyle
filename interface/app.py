
from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

# Ajouter la racine du projet au chemin Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.rag_pipeline import RAGPipeline

# Initialiser l'application
app = FastAPI(
    title="ModaStyle - Assistant Client",
    description="Assistant intelligent basé sur les documents ModaStyle",
    version="1.0.0"
)

# Charger le pipeline RAG avec la configuration B
pipeline = RAGPipeline(config_name="B", top_k=5)


class Question(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def accueil():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ModaStyle - Assistant Client</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f5f1ed;
                color: #333;
            }

            header {
                background: #382b32;
                color: white;
                padding: 22px;
                text-align: center;
            }

            header h1 {
                margin: 0;
            }

            header p {
                margin-bottom: 0;
                color: #eadde3;
            }

            .container {
                max-width: 750px;
                margin: 35px auto;
                background: white;
                border-radius: 14px;
                padding: 25px;
                box-shadow: 0 4px 15px #00000012;
            }

            #messages {
                min-height: 300px;
                max-height: 450px;
                overflow-y: auto;
                padding: 10px;
            }

            .message {
                padding: 13px 16px;
                margin: 12px 0;
                border-radius: 12px;
                line-height: 1.6;
                white-space: pre-wrap;
            }

            .client {
                background: #eee6eb;
                margin-left: 15%;
            }

            .assistant {
                background: #f5f1ed;
                margin-right: 10%;
            }

            .input-area {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }

            input {
                flex: 1;
                padding: 14px;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 15px;
            }

            button {
                background: #382b32;
                color: white;
                border: none;
                padding: 14px 22px;
                border-radius: 8px;
                cursor: pointer;
            }

            button:disabled {
                opacity: 0.6;
                cursor: wait;
            }

            .references {
                font-size: 12px;
                color: #666;
                margin-top: 8px;
            }

            footer {
                text-align: center;
                color: #777;
                font-size: 12px;
                margin-top: 20px;
            }
        </style>
    </head>

    <body>
        <header>
            <h1>ModaStyle</h1>
            <p>Votre assistant intelligent de service client</p>
        </header>

        <div class="container">
            <h2>Bonjour ! Comment pouvons-nous vous aider ?</h2>

            <div id="messages">
                <div class="message assistant">
                    Bonjour ! Je suis l'assistant ModaStyle.
                    Posez-moi vos questions sur nos produits, prix, 
                    livraisons et conditions commerciales.
                </div>
            </div>

            <div class="input-area">
                <input
                    id="question"
                    type="text"
                    placeholder="Écrivez votre question..."
                    onkeydown="if(event.key === 'Enter') envoyerQuestion()"
                >
                <button id="send" onclick="envoyerQuestion()">
                    Envoyer
                </button>
            </div>

            <footer>
                ModaStyle - Assistant basé sur les documents officiels de la boutique
            </footer>
        </div>

        <script>
            async function envoyerQuestion() {
                const input = document.getElementById("question");
                const button = document.getElementById("send");
                const messages = document.getElementById("messages");
                const question = input.value.trim();

                if (!question) return;

                const clientMessage = document.createElement("div");
                clientMessage.className = "message client";
                clientMessage.textContent = question;
                messages.appendChild(clientMessage);

                input.value = "";
                button.disabled = true;
                button.textContent = "Patientez...";

                const loading = document.createElement("div");
                loading.className = "message assistant";
                loading.textContent = "Je recherche les informations...";
                messages.appendChild(loading);

                messages.scrollTop = messages.scrollHeight;

                try {
                    const response = await fetch("/ask", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({question: question})
                    });

                    if (!response.ok) {
                        throw new Error("Erreur du serveur");
                    }

                    const data = await response.json();

                    loading.textContent = data.answer.split("**").join("");

                    if (data.references && data.references.length > 0) {
                        const refs = document.createElement("div");
                        refs.className = "references";
                        refs.textContent = "Sources : " +
                            data.references.map(ref =>
                                ref.document_id + " - " + ref.filename
                            ).join(" ; ");
                        loading.appendChild(refs);
                    }

                } catch (error) {
                    loading.textContent =
                        "Une erreur est survenue. Veuillez réessayer.";
                }

                button.disabled = false;
                button.textContent = "Envoyer";
                input.focus();
                messages.scrollTop = messages.scrollHeight;
            }
        </script>
    </body>
    </html>
    """


@app.post("/ask")
def poser_question(data: Question):
    result = pipeline.ask(data.question)

    return {
        "answer": result["answer"],
        "references": result["references"],
        "configuration": result["configuration"],
        "blocked": result["blocked"]
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": "ModaStyle",
        "configuration": "B"
    }
