
from pathlib import Path
import chromadb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_ROOT / "data" / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_DIR))

print("===== VERIFICATION CHROMADB =====")

for name, expected in [
    ("modastyle_a", 67),
    ("modastyle_b", 37)
]:
    collection = client.get_collection(name=name)

    print(f"\nCollection : {name}")
    print("Nombre de chunks :", collection.count())
    print("Nombre attendu :", expected)
    print("Stockage correct :", collection.count() == expected)

    sample = collection.get(limit=1)

    if sample["ids"]:
        print("Exemple ID :", sample["ids"][0])
        print("Texte disponible :", bool(sample["documents"][0]))
        print("Metadonnees disponibles :", bool(sample["metadatas"][0]))

print("\nVerification terminee.")
