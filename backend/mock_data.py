import random
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

MOCK_USERS = {
    "900123456-1": {
        "nombre": "Tech Solutions SAS",
        "tamaño": "Pequeña",
        "sector": "Tecnología",
        "ciiu": "6201 - Desarrollo de programas informáticos",
        "empleados": 15,
        "activos": "$150,000,000",
        "departamento": "Bogotá D.C.",
        "perfil": "PyMEs en Consolidación (Track B - Consolidar)",
        "perfil_id": 3
    },
    "800987654-2": {
        "nombre": "Agro Exportaciones S.A.",
        "tamaño": "Mediana",
        "sector": "Agricultura",
        "ciiu": "0111 - Cultivo de cereales",
        "empleados": 50,
        "activos": "$500,000,000",
        "departamento": "Valle del Cauca",
        "perfil": "Expansión Internacional (Track B - Crecer)",
        "perfil_id": 5
    },
    "901234567-3": {
        "nombre": "Café Artesanal del Eje SAS",
        "tamaño": "Micro",
        "sector": "Alimentos y Bebidas",
        "ciiu": "1063 - Trilla de café",
        "empleados": 3,
        "activos": "$25,000,000",
        "departamento": "Risaralda",
        "perfil": "Microempresa Tradicional (Track B - Consolidar)",
        "perfil_id": 2
    }
}

# ──────────────────────────────────────────────────────────────────────
# Oferta Institucional REAL – Extraída de arco_instruments.json
# ──────────────────────────────────────────────────────────────────────

_DATA_FILE = os.path.join(os.path.dirname(__file__), 'arco_instruments.json')
with open(_DATA_FILE, 'r', encoding='utf-8') as f:
    ARCO_INSTRUMENTS = json.load(f)

# Pre-compute TF-IDF for all instruments
_corpus = [inst.get('descripcion', '') for inst in ARCO_INSTRUMENTS]
_vectorizer = TfidfVectorizer(stop_words=None)
_tfidf_matrix = _vectorizer.fit_transform(_corpus) if _corpus else None


# ──────────────────────────────────────────────────────────────────────
# Mapeo perfil ↔ dimensiones (basado en el cuestionario de Radar de Madurez)
# A=1, B=2, C=3, D=4.  Promedio simple → perfil_id.
# ──────────────────────────────────────────────────────────────────────
ANSWER_SCORES = {"A": 1, "B": 2, "C": 3, "D": 4}

PERFIL_RANGES = [
    (1.0, 1.5, "Explorador (Track A – Nacer)", 1),
    (1.5, 2.25, "Microempresa Tradicional (Track B – Consolidar)", 2),
    (2.25, 3.0, "PyMEs en Consolidación (Track B – Consolidar)", 3),
    (3.0, 3.5, "Emprendimiento de Alto Impacto (Track B – Crecer)", 4),
    (3.5, 5.0, "Expansión Internacional (Track B – Crecer)", 5),
]

def _compute_perfil(respuestas):
    """Calcula el perfil a partir de las respuestas A-D del cuestionario y devuelve puntajes por pilar."""
    pilares = ["operacion", "financiamiento", "mercado", "innovacion"] # Excluir objetivo para el radar
    
    # Puntajes individuales para el radar (escala 1 a 4)
    # A=1, B=2, C=3, D=4
    puntajes_radar = {
        p: ANSWER_SCORES.get(respuestas.get(p, "B"), 2) for p in pilares
    }
    
    # Para el cálculo del perfil sí usamos el transversal 'objetivo'
    todos_pilares = pilares + ["objetivo"]
    scores = [ANSWER_SCORES.get(respuestas.get(p, "B"), 2) for p in todos_pilares]
    avg = sum(scores) / len(scores)
    
    perfil_resultado = (PERFIL_RANGES[-1][1], PERFIL_RANGES[-1][2], avg)
    for lo, hi, nombre, pid in PERFIL_RANGES:
        if lo <= avg < hi:
            perfil_resultado = (nombre, pid, avg)
            break
            
    return perfil_resultado[0], perfil_resultado[1], perfil_resultado[2], puntajes_radar


def _nlp_similarity(texto, inst_index):
    """Calcula similitud semántica usando TF-IDF y Cosine Similarity."""
    if not texto or _tfidf_matrix is None:
        return 0.0
    
    query_vec = _vectorizer.transform([texto.lower()])
    sim = cosine_similarity(query_vec, _tfidf_matrix[inst_index]).flatten()[0]
    return sim

def calcular_match(respuestas):
    """
    Calcula el emparejamiento entre el perfil del usuario y los
    instrumentos vigentes 2026 de ArCo.
    """
    perfil_nombre, perfil_id, avg_score, puntajes_radar = _compute_perfil(respuestas)
    nlp_text = respuestas.get("necesidad_nlp", "").strip()

    matches = []
    for idx, inst in enumerate(ARCO_INSTRUMENTS):
        score = 0.0

        # 1. Score por perfil (40% del total)
        usuarios_list = inst.get("usuarios", [])
        usuarios_str = " ".join(usuarios_list).lower()
        if perfil_id <= 2 and ("personas naturales" in usuarios_str or "emprendedores" in usuarios_str):
            score += 0.4
        elif perfil_id == 3 and "mipymes" in usuarios_str:
            score += 0.4
        elif perfil_id >= 4 and ("mipymes" in usuarios_str or "grandes empresas" in usuarios_str):
            score += 0.4
        elif "mipymes" in usuarios_str:
            score += 0.2  # partial

        # 2. Score por NLP (35% del total)
        if nlp_text:
            sim_score = _nlp_similarity(nlp_text, idx)
            score += 0.35 * sim_score

        # 3. Score por diversidad de apoyos (15%)
        diversity = min(len(inst.get("apoyos", [])) / 5.0, 1.0)
        score += 0.15 * diversity

        # 4. Variabilidad controlada (10%) para que no sea idéntico entre instrumentos
        score += 0.10 * random.uniform(0.3, 1.0)

        match_pct = round(score * 100)
        match_pct = max(40, min(match_pct, 99))  # clamp

        if match_pct >= 50:
            matches.append({
                "programa": {
                    "id": inst["id"],
                    "nombre": inst["nombre"],
                    "entidad": inst["entidad"],
                    "descripcion": inst.get("descripcion", ""),
                    "objetivos": inst.get("objetivos", []),
                    "usuarios": inst.get("usuarios", []),
                    "apoyos": inst.get("apoyos", [])[:3]
                },
                "match_score": match_pct
            })

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches[:15], perfil_nombre, puntajes_radar
