import random

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
# Oferta Institucional REAL – Extraída del Tablero_ArCo_PowerBI.xlsx
# Hoja: 6_Perfil_Vigentes2026 (última iteración ArCo)
# Se incluyen los instrumentos vigentes 2026 por entidad.
# ──────────────────────────────────────────────────────────────────────

ARCO_INSTRUMENTS = [
    # ── Bancóldex ──────────────────────────────────────────────────────
    {
        "id": "BANC-05",
        "entidad": "Bancóldex",
        "nombre": "Coberturas Cambiarias",
        "objetivos": ["I+D+i (Investigación, Desarrollo e Innovación)"],
        "usuarios": ["Grandes empresas", "Mipymes"],
        "apoyos": ["Formación de Talento Humano"],
        "descripcion": "Cobertura de riesgo cambiario para empresas exportadoras e importadoras."
    },
    {
        "id": "BANC-04",
        "entidad": "Bancóldex",
        "nombre": "Línea de Crédito Apoyo a la Economía Popular Regional 2025",
        "objetivos": ["Emprendimiento"],
        "usuarios": ["Mipymes", "Personas naturales"],
        "apoyos": ["Apoyo Financiero"],
        "descripcion": "Crédito para unidades de economía popular en regiones."
    },
    {
        "id": "BANC-06",
        "entidad": "Bancóldex",
        "nombre": "neocrédito",
        "objetivos": ["Emprendimiento"],
        "usuarios": ["Mipymes"],
        "apoyos": ["Apoyo Financiero"],
        "descripcion": "Plataforma digital de crédito para Mipymes con procesos ágiles y 100% digitales."
    },
    # ── Colombia Productiva / iNNpulsa ─────────────────────────────────
    {
        "id": "INNP-12",
        "entidad": "iNNpulsa",
        "nombre": "FortaleSER",
        "objetivos": ["Calidad / Productividad y Competitividad", "Clúster / Asociatividad", "Economía Popular", "Formación de Capital Humano", "Formalización", "I+D+i", "Inclusión Financiera"],
        "usuarios": ["Mipymes"],
        "apoyos": ["Asistencia técnica y Consultoría", "Eventos", "Formación de Talento Humano", "Redes de Colaboración"],
        "descripcion": "Programa integral de fortalecimiento empresarial para Mipymes con enfoque en productividad, calidad, y formalización."
    },
    {
        "id": "INNP-04",
        "entidad": "iNNpulsa",
        "nombre": "Ruta ALDEA",
        "objetivos": ["Acceso a financiación", "Acceso a mercados / Comercialización", "Comercio Electrónico", "Desarrollo Sostenible", "Emprendimiento", "I+D+i"],
        "usuarios": ["Entidades de soporte", "Mipymes", "Personas naturales"],
        "apoyos": ["Asistencia técnica y Consultoría", "Bonos o Vouchers", "Eventos", "Formación de Talento Humano", "Redes de Colaboración"],
        "descripcion": "Programa de aceleración para emprendimientos de alto impacto con acceso a mentores, financiación y redes."
    },
    {
        "id": "INNP-14",
        "entidad": "iNNpulsa",
        "nombre": "Oportunidades para Emprender",
        "objetivos": ["Acceso a mercados / Comercialización", "Comercio Electrónico", "Emprendimiento", "Formación de Capital Humano", "I+D+i", "Inclusión Financiera"],
        "usuarios": ["Mipymes", "Personas naturales"],
        "apoyos": ["Asistencia técnica y Consultoría", "Compra Pública", "Eventos", "Formación de Talento Humano", "Redes de Colaboración"],
        "descripcion": "Programa de acompañamiento integral para emprendedores con oportunidades de formación, financiación y conexión con mercados."
    },
    {
        "id": "INNP-32",
        "entidad": "iNNpulsa",
        "nombre": "Crecer Juntos – Desarrollo para la Economía Popular",
        "objetivos": ["Acceso a mercados / Comercialización", "Economía Popular", "Educación económica y financiera", "Formalización", "Inclusión Financiera"],
        "usuarios": ["Emprendedores", "Entidades de soporte", "Mipymes", "Personas naturales"],
        "apoyos": ["Asistencia técnica y Consultoría", "Bonos o Vouchers", "Compra Pública", "Eventos", "Formación de Talento Humano"],
        "descripcion": "Programa de fortalecimiento integral para unidades productivas de la economía popular."
    },
    {
        "id": "INNP-25",
        "entidad": "iNNpulsa",
        "nombre": "Círculos Solidarios",
        "objetivos": ["Acceso a financiación", "Educación económica y financiera", "Inclusión Financiera"],
        "usuarios": ["Entidades de soporte", "Mipymes", "Personas naturales"],
        "apoyos": ["Apoyo Financiero", "Asistencia técnica y Consultoría", "Formación de Talento Humano", "Redes de Colaboración"],
        "descripcion": "Metodología de microfinanzas comunitarias para grupos solidarios de emprendedores."
    },
    {
        "id": "INNP-08",
        "entidad": "iNNpulsa",
        "nombre": "MiLAB – Laboratorio GovTech de Colombia",
        "objetivos": ["Formación de Capital Humano", "I+D+i", "Transferencia de Conocimiento y Tecnología"],
        "usuarios": ["Academia", "Entidades de soporte", "Gobierno", "Mipymes", "Personas naturales"],
        "apoyos": ["Asistencia técnica y Consultoría", "Compra Pública", "Eventos", "Formación de Talento Humano", "Redes de Colaboración"],
        "descripcion": "Laboratorio de innovación pública que conecta startups con retos del sector público."
    },
    {
        "id": "INNP-31",
        "entidad": "iNNpulsa",
        "nombre": "Ventanilla Única Empresarial – VUE",
        "objetivos": ["Emprendimiento", "Formalización"],
        "usuarios": ["Academia", "Entidades de soporte", "Gobierno", "Grandes empresas", "Mipymes"],
        "apoyos": ["Asistencia técnica y Consultoría", "Sistemas de Información"],
        "descripcion": "Portal unificado para la creación y formalización de empresas en Colombia."
    },
    {
        "id": "INNP-13",
        "entidad": "iNNpulsa",
        "nombre": "Emprende-tón",
        "objetivos": ["Educación económica y financiera", "Emprendimiento", "Formación de Capital Humano", "I+D+i"],
        "usuarios": ["Personas naturales"],
        "apoyos": ["Formación de Talento Humano", "Redes de Colaboración"],
        "descripcion": "Maratón de emprendimiento con formación intensiva y mentoría."
    },
    {
        "id": "INNP-27",
        "entidad": "iNNpulsa",
        "nombre": "Programa de Encadenamientos Productivos",
        "objetivos": ["Acceso a mercados / Comercialización", "Calidad / Productividad y Competitividad", "Clúster / Asociatividad", "Desarrollo Digital", "Formalización"],
        "usuarios": ["Entidades de soporte", "Mipymes"],
        "apoyos": ["Apoyo Financiero", "Asistencia técnica y Consultoría", "Eventos", "Redes de Colaboración", "Sistemas de Información"],
        "descripcion": "Articulación de cadenas de valor entre grandes empresas y proveedores Mipymes."
    },
    {
        "id": "INNP-21",
        "entidad": "iNNpulsa",
        "nombre": "Comercializadoras Territoriales",
        "objetivos": ["Acceso a mercados / Comercialización", "Clúster / Asociatividad", "Economía Popular", "Formación de Capital Humano"],
        "usuarios": ["Entidades de soporte", "Mipymes", "Personas naturales"],
        "apoyos": ["Asistencia técnica y Consultoría", "Compra Pública", "Eventos", "Formación de Talento Humano"],
        "descripcion": "Red de comercializadoras para fortalecer la venta de productos de la economía popular."
    },
    {
        "id": "INNP-28",
        "entidad": "iNNpulsa",
        "nombre": "Programa iNNpulsa Crowdlending",
        "objetivos": ["Acceso a financiación", "Educación económica y financiera", "Emprendimiento", "Inclusión Financiera"],
        "usuarios": ["Personas naturales"],
        "apoyos": ["Apoyo Financiero", "Asistencia técnica y Consultoría", "Eventos", "Redes de Colaboración", "Sistemas de Información"],
        "descripcion": "Financiamiento colectivo digital para emprendimientos y Mipymes."
    },
    # ── ProColombia ────────────────────────────────────────────────────
    {
        "id": "PROC-01",
        "entidad": "ProColombia",
        "nombre": "Programas de Formación Exportadora",
        "objetivos": ["Formación de Capital Humano", "Internacionalización"],
        "usuarios": ["Mipymes", "Grandes empresas"],
        "apoyos": ["Formación de Talento Humano", "Asistencia técnica y Consultoría"],
        "descripcion": "Capacitación especializada para la internacionalización de empresas colombianas."
    },
    {
        "id": "PROC-02",
        "entidad": "ProColombia",
        "nombre": "Fábricas de Internacionalización",
        "objetivos": ["Acceso a mercados / Comercialización", "Internacionalización"],
        "usuarios": ["Mipymes"],
        "apoyos": ["Asistencia técnica y Consultoría", "Eventos"],
        "descripcion": "Acompañamiento intensivo para ampliar la base exportadora de Mipymes colombianas."
    },
    {
        "id": "PROC-03",
        "entidad": "ProColombia",
        "nombre": "Ruta Exportadora",
        "objetivos": ["Internacionalización", "Acceso a mercados / Comercialización"],
        "usuarios": ["Mipymes", "Personas naturales"],
        "apoyos": ["Asistencia técnica y Consultoría", "Formación de Talento Humano"],
        "descripcion": "Ruta de 5 pasos para preparar empresas hacia la internacionalización."
    },
    {
        "id": "PROC-04",
        "entidad": "ProColombia",
        "nombre": "Invest in Colombia – Buscador de Oportunidades",
        "objetivos": ["Inversión y Clima de Negocios", "Internacionalización"],
        "usuarios": ["Grandes empresas", "Mipymes"],
        "apoyos": ["Sistemas de Información"],
        "descripcion": "Herramienta digital para identificar oportunidades de inversión en Colombia."
    },
    # ── Fontur ─────────────────────────────────────────────────────────
    {
        "id": "FONT-01",
        "entidad": "Fontur",
        "nombre": "Red Turística de Pueblos Patrimonio",
        "objetivos": ["Turismo", "Desarrollo Sostenible"],
        "usuarios": ["Mipymes", "Gobierno"],
        "apoyos": ["Asistencia técnica y Consultoría", "Eventos"],
        "descripcion": "Red de pueblos patrimonio turísticos con apoyo para el desarrollo territorial."
    },
    {
        "id": "FONT-02",
        "entidad": "Fontur",
        "nombre": "Tarjeta Joven Colombia",
        "objetivos": ["Turismo"],
        "usuarios": ["Personas naturales"],
        "apoyos": ["Bonos o Vouchers"],
        "descripcion": "Beneficios y descuentos turísticos para jóvenes colombianos."
    },
    # ── MinCIT ─────────────────────────────────────────────────────────
    {
        "id": "MINC-01",
        "entidad": "MinCIT",
        "nombre": "Fábricas de Productividad y Sostenibilidad",
        "objetivos": ["Calidad / Productividad y Competitividad", "Desarrollo Sostenible"],
        "usuarios": ["Mipymes"],
        "apoyos": ["Asistencia técnica y Consultoría", "Formación de Talento Humano"],
        "descripcion": "Extensionismo tecnológico para mejorar la productividad y sostenibilidad de Mipymes."
    },
    {
        "id": "MINC-02",
        "entidad": "MinCIT",
        "nombre": "Fábricas de Internacionalización en Calidad",
        "objetivos": ["Internacionalización", "Calidad / Productividad y Competitividad"],
        "usuarios": ["Mipymes"],
        "apoyos": ["Asistencia técnica y Consultoría", "Formación de Talento Humano"],
        "descripcion": "Preparación de empresas con estándares de calidad para mercados internacionales."
    },
    {
        "id": "MINC-03",
        "entidad": "MinCIT",
        "nombre": "Ventanilla Única de Comercio Exterior – VUCE",
        "objetivos": ["Internacionalización", "Comercio Electrónico"],
        "usuarios": ["Mipymes", "Grandes empresas"],
        "apoyos": ["Sistemas de Información"],
        "descripcion": "Trámites y procedimientos de comercio exterior centralizados en una sola ventanilla digital."
    },
    {
        "id": "MINC-04",
        "entidad": "MinCIT",
        "nombre": "Territorios Clúster",
        "objetivos": ["Clúster / Asociatividad", "Calidad / Productividad y Competitividad"],
        "usuarios": ["Mipymes", "Gobierno", "Entidades de soporte"],
        "apoyos": ["Asistencia técnica y Consultoría", "Eventos", "Redes de Colaboración"],
        "descripcion": "Acompañamiento a aglomeraciones clúster para fortalecer la competitividad territorial."
    },
]


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

# Palabras clave por dimensión para emparejamiento simplificado
KEYWORD_MAP = {
    "financiacion": ["Apoyo Financiero", "Inclusión Financiera", "Acceso a financiación"],
    "exportar": ["Internacionalización", "Acceso a mercados / Comercialización"],
    "calidad": ["Calidad / Productividad y Competitividad"],
    "formalizar": ["Formalización", "Emprendimiento"],
    "tecnologia": ["I+D+i", "Desarrollo Digital", "Transferencia de Conocimiento y Tecnología", "Comercio Electrónico"],
    "credito": ["Apoyo Financiero", "Inclusión Financiera", "Acceso a financiación"],
    "capacitacion": ["Formación de Capital Humano", "Formación de Talento Humano"],
    "innovacion": ["I+D+i", "Transferencia de Conocimiento y Tecnología"],
    "turismo": ["Turismo"],
    "mercado": ["Acceso a mercados / Comercialización"],
    "sostenibilidad": ["Desarrollo Sostenible"],
    "productividad": ["Calidad / Productividad y Competitividad"],
}


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


def _nlp_keywords(texto):
    """Extrae keywords de forma simplificada del texto libre del usuario."""
    texto = texto.lower()
    matched_objectives = set()
    for keyword, objectives in KEYWORD_MAP.items():
        if keyword in texto:
            matched_objectives.update(objectives)
    return matched_objectives


def calcular_match(respuestas):
    """
    Calcula el emparejamiento entre el perfil del usuario y los
    instrumentos vigentes 2026 de ArCo.
    """
    perfil_nombre, perfil_id, avg_score, puntajes_radar = _compute_perfil(respuestas)
    nlp_text = respuestas.get("necesidad_nlp", "")
    nlp_objectives = _nlp_keywords(nlp_text)

    matches = []
    for inst in ARCO_INSTRUMENTS:
        score = 0.0

        # 1. Score por perfil (40% del total)
        if perfil_id <= 2 and any(u in inst["usuarios"] for u in ["Personas naturales", "Emprendedores"]):
            score += 0.4
        elif perfil_id == 3 and "Mipymes" in inst["usuarios"]:
            score += 0.4
        elif perfil_id >= 4 and any(u in inst["usuarios"] for u in ["Mipymes", "Grandes empresas"]):
            score += 0.4
        elif "Mipymes" in inst["usuarios"]:
            score += 0.2  # partial

        # 2. Score por NLP (35% del total)
        if nlp_objectives:
            all_inst_tags = set(inst["objetivos"] + inst["apoyos"])
            overlap = nlp_objectives & all_inst_tags
            if overlap:
                score += 0.35 * min(len(overlap) / max(len(nlp_objectives), 1), 1.0)

        # 3. Score por diversidad de apoyos (15%)
        diversity = min(len(inst["apoyos"]) / 5.0, 1.0)
        score += 0.15 * diversity

        # 4. Variabilidad controlada (10%) para que no sea idéntico entre instrumentos
        score += 0.10 * random.uniform(0.3, 1.0)

        match_pct = round(score * 100)
        match_pct = max(40, min(match_pct, 99))  # clamp

        if match_pct >= 60:
            matches.append({
                "programa": {
                    "id": inst["id"],
                    "nombre": inst["nombre"],
                    "entidad": inst["entidad"],
                    "descripcion": inst["descripcion"],
                    "objetivos": inst["objetivos"][:3],
                    "apoyos": inst["apoyos"][:3]
                },
                "match_score": match_pct
            })

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches, perfil_nombre, puntajes_radar
