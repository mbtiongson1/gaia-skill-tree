"""Embedding generation for Gaia semantic search.

Uses sentence-transformers (all-MiniLM-L6-v2) to embed skill descriptions.
Outputs to registry/embeddings.json for use by search and similarity tools.
"""

import json
import os
from datetime import date

from gaia_cli.registry import embeddings_path, named_skills_dir, registry_graph_path

def load_skills(registry_path="."):
    """Load skills from gaia.json plus any named skills from registry/named/.

    Returns a list of dicts with at least 'id', 'name', and 'description'.
    """
    skills = []

    # Load canonical skills from gaia.json
    gaia_path = registry_graph_path(registry_path)
    if os.path.exists(gaia_path):
        try:
            with open(gaia_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for skill in data.get("skills", []):
                skills.append({
                    "id": skill["id"],
                    "name": skill.get("name", skill["id"]),
                    "description": skill.get("description", ""),
                })
        except Exception as e:
            print(f"Warning: could not load {gaia_path}: {e}")

    # Load named skills from registry/named/*.json
    named_dir = named_skills_dir(registry_path)
    if os.path.isdir(named_dir):
        for fname in os.listdir(named_dir):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(named_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    skill = json.load(f)
                if "id" in skill:
                    skills.append({
                        "id": skill["id"],
                        "name": skill.get("name", skill["id"]),
                        "description": skill.get("description", ""),
                    })
            except Exception as e:
                print(f"Warning: could not load {fpath}: {e}")

    return skills


def embed_skills(skills, model_name="all-MiniLM-L6-v2"):
    """Generate embeddings for each skill using '{name}: {description}' as input text.

    Returns a list of dicts: [{"id": ..., "vector": [...]}, ...]
    Raises ImportError with a helpful message if sentence-transformers is missing.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError(
            "sentence-transformers is not installed. "
            "Run: pip install sentence-transformers"
        )

    print(f"Loading model '{model_name}'...", flush=True)
    model = SentenceTransformer(model_name)

    texts = [
        f"{skill['name']}: {skill['description']}" for skill in skills
    ]

    print(f"Encoding {len(texts)} skills...", flush=True)
    vectors = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    entries = []
    for skill, vector in zip(skills, vectors):
        entries.append({
            "id": skill["id"],
            "vector": vector.tolist(),
        })

    return entries, vectors.shape[1] if len(vectors) > 0 else 384


def save_embeddings(entries, output_path, model_name, dimensions):
    """Write embeddings to registry/embeddings.json.

    Args:
        entries: list of {"id": ..., "vector": [...]}
        output_path: absolute or relative path to write the JSON file
        model_name: name of the model used to generate embeddings
        dimensions: embedding vector size
    """
    payload = {
        "model": model_name,
        "dimensions": dimensions,
        "generatedAt": str(date.today()),
        "entries": entries,
    }
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Saved {len(entries)} embeddings to {output_path}")


def generate_embeddings(registry_path=".", model_name="all-MiniLM-L6-v2"):
    """Orchestrate the full embedding generation flow.

    Loads skills, embeds them, and writes registry/embeddings.json.
    """
    try:
        from sentence_transformers import SentenceTransformer  # noqa: F401
    except ImportError:
        print(
            "Error: sentence-transformers is not installed.\n"
            "Install it with:  pip install sentence-transformers"
        )
        return

    skills = load_skills(registry_path)
    if not skills:
        print("No skills found. Make sure the registry path is correct.")
        return

    print(f"Loaded {len(skills)} skills from {registry_path}.")

    entries, dimensions = embed_skills(skills, model_name=model_name)

    output_path = embeddings_path(registry_path)
    save_embeddings(entries, output_path, model_name=model_name, dimensions=dimensions)
