
import re
import unicodedata


STOPWORDS = {
    "quel", "quelle", "quels", "quelles",
    "est", "sont", "comment", "pourquoi",
    "combien", "que", "qui", "quoi",
    "le", "la", "les", "un", "une", "des",
    "du", "de", "dans", "pour", "par",
    "a", "au", "aux", "en", "et", "ou",
    "sur", "avec", "mon", "ma", "mes",
    "son", "sa", "ses", "ce", "cette",
    "ces", "je", "tu", "il", "elle",
    "nous", "vous", "ils", "elles",
    "me", "te", "se", "y", "ne", "pas"
}


def normalize_text(text):
    """Supprime les accents et met le texte en minuscules."""

    text = unicodedata.normalize("NFD", text.lower())

    return "".join(
        char for char in text
        if unicodedata.category(char) != "Mn"
    )


def tokenize(text):
    """Transforme un texte en mots normalisés."""

    normalized = normalize_text(text)
    words = re.findall(r"\b[a-z0-9]+\b", normalized)

    terms = set()

    for word in words:
        if word in STOPWORDS or len(word) < 3:
            continue

        if word.endswith("s") and len(word) > 4:
            if word not in {"frais", "plus", "tous", "sans"}:
                word = word[:-1]

        terms.add(word)

    return terms


def calculate_relevance_score(question_terms, content):
    """
    Calcule un score lexical avec une priorité
    aux passages contenant une information précise.
    """

    normalized_content = normalize_text(content)
    content_terms = tokenize(content)

    matched_terms = question_terms.intersection(content_terms)

    # Nombre de termes correspondants
    score = len(matched_terms) * 2

    # Proportion des termes de la question retrouvés
    coverage = len(matched_terms) / len(question_terms)
    score += coverage

    # Bonus si le passage contient un délai chiffré
    if "delai" in question_terms:
        has_duration = re.search(
            r"\b\d+\s*(?:a|-|et)\s*\d+\s*(?:jours?|semaines?|heures?)\b",
            normalized_content
        )

        if has_duration:
            score += 2

    return score, matched_terms


def filter_relevant_chunks(question, retrieved_chunks):
    """
    Filtre les passages insuffisamment pertinents,
    puis les classe du meilleur au moins pertinent.
    """

    question_terms = tokenize(question)

    if not question_terms:
        return retrieved_chunks

    minimum_matches = min(2, len(question_terms))

    relevant_chunks = []

    for chunk in retrieved_chunks:
        content = chunk.get("content", "")

        score, matched_terms = calculate_relevance_score(
            question_terms,
            content
        )

        if len(matched_terms) >= minimum_matches:
            filtered_chunk = chunk.copy()

            filtered_chunk["relevance_score"] = round(score, 3)
            filtered_chunk["matched_terms"] = sorted(matched_terms)

            relevant_chunks.append(filtered_chunk)

    # Classement du score le plus élevé au plus faible
    relevant_chunks.sort(
        key=lambda chunk: chunk["relevance_score"],
        reverse=True
    )

    return relevant_chunks

import re
import unicodedata


STOPWORDS = {
    "quel", "quelle", "quels", "quelles",
    "est", "sont", "comment", "pourquoi",
    "combien", "que", "qui", "quoi",
    "le", "la", "les", "un", "une", "des",
    "du", "de", "dans", "pour", "par",
    "a", "au", "aux", "en", "et", "ou",
    "sur", "avec", "mon", "ma", "mes",
    "son", "sa", "ses", "ce", "cette",
    "ces", "je", "tu", "il", "elle",
    "nous", "vous", "ils", "elles",
    "me", "te", "se", "y", "ne", "pas"
}


def normalize_text(text):
    """Supprime les accents et met le texte en minuscules."""

    text = unicodedata.normalize("NFD", text.lower())

    return "".join(
        char for char in text
        if unicodedata.category(char) != "Mn"
    )


def tokenize(text):
    """Transforme un texte en mots normalisés."""

    normalized = normalize_text(text)
    words = re.findall(r"\b[a-z0-9]+\b", normalized)

    terms = set()

    for word in words:
        if word in STOPWORDS or len(word) < 3:
            continue

        if word.endswith("s") and len(word) > 4:
            if word not in {"frais", "plus", "tous", "sans"}:
                word = word[:-1]

        terms.add(word)

    return terms


def calculate_relevance_score(question_terms, content):
    """
    Calcule un score lexical avec une priorité
    aux passages contenant une information précise.
    """

    normalized_content = normalize_text(content)
    content_terms = tokenize(content)

    matched_terms = question_terms.intersection(content_terms)

    # Nombre de termes correspondants
    score = len(matched_terms) * 2

    # Proportion des termes de la question retrouvés
    coverage = len(matched_terms) / len(question_terms)
    score += coverage

    # Bonus si le passage contient un délai chiffré
    if "delai" in question_terms:
        has_duration = re.search(
            r"\b\d+\s*(?:a|-|et)\s*\d+\s*(?:jours?|semaines?|heures?)\b",
            normalized_content
        )

        if has_duration:
            score += 2

    return score, matched_terms


def filter_relevant_chunks(question, retrieved_chunks):
    """
    Filtre les passages insuffisamment pertinents,
    puis les classe du meilleur au moins pertinent.
    """

    question_terms = tokenize(question)

    if not question_terms:
        return retrieved_chunks

    minimum_matches = min(2, len(question_terms))

    relevant_chunks = []

    for chunk in retrieved_chunks:
        content = chunk.get("content", "")

        score, matched_terms = calculate_relevance_score(
            question_terms,
            content
        )

        if len(matched_terms) >= minimum_matches:
            filtered_chunk = chunk.copy()

            filtered_chunk["relevance_score"] = round(score, 3)
            filtered_chunk["matched_terms"] = sorted(matched_terms)

            relevant_chunks.append(filtered_chunk)

    # Classement du score le plus élevé au plus faible
    relevant_chunks.sort(
        key=lambda chunk: chunk["relevance_score"],
        reverse=True
    )

    return relevant_chunks

import re
import unicodedata


STOPWORDS = {
    "quel", "quelle", "quels", "quelles",
    "est", "sont", "comment", "pourquoi",
    "combien", "que", "qui", "quoi",
    "le", "la", "les", "un", "une", "des",
    "du", "de", "dans", "pour", "par",
    "a", "au", "aux", "en", "et", "ou",
    "sur", "avec", "mon", "ma", "mes",
    "son", "sa", "ses", "ce", "cette",
    "ces", "je", "tu", "il", "elle",
    "nous", "vous", "ils", "elles",
    "me", "te", "se", "y", "ne", "pas"
}


def normalize_text(text):
    """Supprime les accents et met le texte en minuscules."""

    text = unicodedata.normalize("NFD", text.lower())

    return "".join(
        char for char in text
        if unicodedata.category(char) != "Mn"
    )


def tokenize(text):
    """Transforme un texte en mots normalisés."""

    normalized = normalize_text(text)
    words = re.findall(r"\b[a-z0-9]+\b", normalized)

    terms = set()

    for word in words:
        if word in STOPWORDS or len(word) < 3:
            continue

        if word.endswith("s") and len(word) > 4:
            if word not in {"frais", "plus", "tous", "sans"}:
                word = word[:-1]

        terms.add(word)

    return terms


def calculate_relevance_score(question_terms, content):
    """
    Calcule un score lexical avec une priorité
    aux passages contenant une information précise.
    """

    normalized_content = normalize_text(content)
    content_terms = tokenize(content)

    matched_terms = question_terms.intersection(content_terms)

    # Nombre de termes correspondants
    score = len(matched_terms) * 2

    # Proportion des termes de la question retrouvés
    coverage = len(matched_terms) / len(question_terms)
    score += coverage

    # Bonus si le passage contient un délai chiffré
    if "delai" in question_terms:
        has_duration = re.search(
            r"\b\d+\s*(?:a|-|et)\s*\d+\s*(?:jours?|semaines?|heures?)\b",
            normalized_content
        )

        if has_duration:
            score += 2

    return score, matched_terms


def filter_relevant_chunks(question, retrieved_chunks):
    """
    Filtre les passages insuffisamment pertinents,
    puis les classe du meilleur au moins pertinent.
    """

    question_terms = tokenize(question)

    if not question_terms:
        return retrieved_chunks

    minimum_matches = min(2, len(question_terms))

    relevant_chunks = []

    for chunk in retrieved_chunks:
        content = chunk.get("content", "")

        score, matched_terms = calculate_relevance_score(
            question_terms,
            content
        )

        if len(matched_terms) >= minimum_matches:
            filtered_chunk = chunk.copy()

            filtered_chunk["relevance_score"] = round(score, 3)
            filtered_chunk["matched_terms"] = sorted(matched_terms)

            relevant_chunks.append(filtered_chunk)

    # Classement du score le plus élevé au plus faible
    relevant_chunks.sort(
        key=lambda chunk: chunk["relevance_score"],
        reverse=True
    )

    return relevant_chunks
