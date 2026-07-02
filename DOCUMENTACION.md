# Documentación Técnica – Demo Ruta Integral de Apoyo Empresarial

## 1. Descripción General

Este prototipo funcional implementa la **Ruta Integral de Servicios de Desarrollo Empresarial** propuesta en el Producto 1 del modelo conceptual para el MinCIT. Permite demostrar, de extremo a extremo, el flujo que seguiría un emprendedor o empresario al interactuar con la plataforma: desde su identificación hasta la visualización de ofertas institucionales recomendadas por un motor de emparejamiento semántico.

### Stack Tecnológico

| Componente   | Tecnología          | Versión     | Rol                                          |
|-------------|---------------------|-------------|----------------------------------------------|
| Backend     | Flask (Python)      | 3.1+        | API REST, lógica de emparejamiento           |
| Frontend    | React + Vite        | React 19+   | Interfaz de usuario (SPA)                    |
| Estilos     | Vanilla CSS         | —           | Sistema de diseño institucional              |
| Despliegue  | Render              | Free tier   | Backend como Web Service, Frontend como Static Site |

---

## 2. Estructura del Proyecto

```
demo_plataforma/
├── backend/
│   ├── app.py                 # Servidor Flask – rutas API
│   ├── mock_data.py           # Datos ArCo reales + algoritmo de emparejamiento
│   ├── requirements.txt       # Dependencias Python
│   └── venv/                  # Entorno virtual
│
└── frontend/
    ├── index.html             # HTML base con meta-tags SEO
    ├── package.json           # Configuración npm
    └── src/
        ├── main.jsx           # Punto de entrada React
        ├── App.jsx            # Enrutamiento y layout (Header/Footer)
        ├── index.css          # Sistema de diseño completo
        └── components/
            ├── Landing.jsx    # Fase 0 – Ingreso
            ├── Diagnostico.jsx # Fase 2 – Radar de Madurez
            └── Dashboard.jsx  # Fases 3-5 – Ofertas y Seguimiento
```

---

## 3. Endpoints de la API (Backend)

### `POST /api/auth`
**Descripción:** Fase 0 – Autenticación por Cédula (Track A) o NIT (Track B).

| Parámetro       | Tipo   | Descripción                         |
|-----------------|--------|-------------------------------------|
| `identificador` | string | Número de cédula o NIT              |
| `tipo`          | string | `"cedula"` o `"nit"`                |

**Respuesta exitosa:**
```json
{
  "status": "success",
  "perfil": "PyMEs en Consolidación (Track B – Consolidar)",
  "mensaje": "Interoperabilidad exitosa: datos validados vía RUES, PILA y Superintendencia de Sociedades.",
  "datos_basicos": {
    "nombre": "Tech Solutions SAS",
    "tamaño": "Pequeña",
    "sector": "Tecnología",
    "empleados": 15,
    "activos": "$150,000,000",
    "departamento": "Bogotá D.C."
  }
}
```

**NITs de prueba:** `900123456-1`, `800987654-2`, `901234567-3`

### `POST /api/diagnostico`
**Descripción:** Fase 2 – Procesa las respuestas del autodiagnóstico y ejecuta el emparejamiento semántico.

| Parámetro       | Tipo   | Descripción                                          |
|-----------------|--------|------------------------------------------------------|
| `identificador` | string | Identificador del usuario                            |
| `respuestas`    | object | Claves: `operacion`, `financiamiento`, `mercado`, `innovacion`, `objetivo`, `necesidad_nlp` |

**Respuesta exitosa:**
```json
{
  "status": "success",
  "perfil_calculado": "PyMEs en Consolidación (Track B – Consolidar)",
  "total_instrumentos_arco": 25,
  "matches": [
    {
      "programa": {
        "id": "INNP-14",
        "nombre": "Oportunidades para Emprender",
        "entidad": "iNNpulsa",
        "descripcion": "...",
        "objetivos": ["..."],
        "apoyos": ["..."]
      },
      "match_score": 82
    }
  ]
}
```

### `GET /api/health`
**Descripción:** Health check para monitoreo en Render.

---

## 4. Datos de Oferta ArCo

### Origen de los datos

Los instrumentos que alimentan el motor de emparejamiento provienen directamente del archivo **`Tablero_ArCo_PowerBI.xlsx`**, específicamente de la hoja **`6_Perfil_Vigentes2026`**, que contiene los instrumentos vigentes en la última iteración del ejercicio ArCo.

### Instrumentos incorporados

Se incorporaron **25 instrumentos** de las siguientes entidades:

| Entidad             | Instrumentos | Ejemplos                                                      |
|---------------------|:------------:|---------------------------------------------------------------|
| **iNNpulsa**        |      14      | FortaleSER, Ruta ALDEA, Oportunidades para Emprender, VUE     |
| **ProColombia**     |       4      | Formación Exportadora, Fábricas de Internacionalización       |
| **MinCIT**          |       4      | Fábricas de Productividad, VUCE, Territorios Clúster          |
| **Bancóldex**       |       3      | Coberturas Cambiarias, neocrédito, Línea Economía Popular     |
| **Fontur**          |       2      | Red Turística de Pueblos Patrimonio, Tarjeta Joven            |

### Campos por instrumento

Cada instrumento contiene:
- `id`: Identificador ArCo (ej. `INNP-04`)
- `entidad`: Entidad que opera el instrumento
- `nombre`: Nombre oficial del instrumento
- `objetivos`: Lista de objetivos de política (ej. "Emprendimiento", "I+D+i")
- `usuarios`: Tipos de usuario objetivo (ej. "Mipymes", "Personas naturales")
- `apoyos`: Tipos de apoyo que ofrece (ej. "Apoyo Financiero", "Asistencia técnica")
- `descripcion`: Descripción del instrumento

---

## 5. Algoritmo de Emparejamiento

El emparejamiento simula el **Pilar 5 (Emparejamiento semántico / NLP)** del modelo conceptual. Se basa en cuatro componentes ponderados:

### Componentes del Score

| Componente                 | Peso | Descripción                                                    |
|----------------------------|:----:|----------------------------------------------------------------|
| **Perfil del usuario**     | 40%  | Coincidencia entre el perfil calculado (Explorador → Expansión Internacional) y los tipos de usuario del instrumento |
| **NLP sobre texto libre**  | 35%  | Extracción de keywords del texto libre del usuario y cruce con los objetivos y apoyos del instrumento |
| **Diversidad de apoyos**   | 15%  | Instrumentos con más tipos de apoyo reciben un score mayor     |
| **Variabilidad controlada** | 10% | Factor estocástico para evitar scores idénticos                |

### Cálculo del Perfil (Radar de Madurez)

Las respuestas del cuestionario (A=1, B=2, C=3, D=4) se promedian sobre los 5 pilares:

| Rango promedio | Perfil resultante                                |
|:--------------:|--------------------------------------------------|
| 1.0 – 1.5     | Explorador (Track A – Nacer)                     |
| 1.5 – 2.25    | Microempresa Tradicional (Track B – Consolidar)  |
| 2.25 – 3.0    | PyMEs en Consolidación (Track B – Consolidar)    |
| 3.0 – 3.5     | Emprendimiento de Alto Impacto (Track B – Crecer)|
| 3.5 – 5.0     | Expansión Internacional (Track B – Crecer)       |

### Extracción de Keywords (NLP simplificado)

El texto libre del usuario se analiza contra un diccionario de 12 categorías de keywords que mapean a los objetivos y apoyos de ArCo:

```
financiacion → Apoyo Financiero, Inclusión Financiera, Acceso a financiación
exportar     → Internacionalización, Acceso a mercados / Comercialización
calidad      → Calidad / Productividad y Competitividad
formalizar   → Formalización, Emprendimiento
tecnologia   → I+D+i, Desarrollo Digital, Transferencia de Conocimiento
credito      → Apoyo Financiero, Inclusión Financiera
capacitacion → Formación de Capital Humano
innovacion   → I+D+i, Transferencia de Conocimiento y Tecnología
turismo      → Turismo
mercado      → Acceso a mercados / Comercialización
sostenibilidad → Desarrollo Sostenible
productividad  → Calidad / Productividad y Competitividad
```

### Umbral de filtrado

Solo se muestran instrumentos con un **match ≥ 60%**, alineado con el umbral mínimo definido en el Pilar 5 del modelo conceptual. Los instrumentos con match ≥ 80% se clasifican como "Alta coincidencia".

---

## 6. Flujo de la Aplicación

```
┌──────────────────────────────────────────────────────────┐
│ Fase 0: INGRESO                                         │
│ - Track A (Cédula) → Llave Temporal                     │
│ - Track B (NIT) → Interoperabilidad RUES/PILA/SuperSoc  │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ Fase 2: AUTODIAGNÓSTICO (Radar de Madurez)              │
│ - 5 preguntas (Operación, Financiamiento, Mercado,      │
│   Innovación, Objetivo Inmediato)                       │
│ - 1 campo de texto libre (input NLP)                    │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ Fase 3: DASHBOARD DE OFERTAS                            │
│ - Perfil empresarial (datos oficiales)                  │
│ - Tracker de interacciones                              │
│ - Instrumentos ArCo ordenados por % de coincidencia     │
│ - Botón "Aplicar – Radicación virtual" (Fase 4)        │
└──────────────────────────────────────────────────────────┘
```

---

## 7. Sistema de Diseño Visual

### Paleta de colores

El diseño utiliza una paleta **navy/gold** institucional, profesional y alineada con estándares de organismos multilaterales (BID, Banco Mundial):

| Token              | Color     | Uso                              |
|---------------------|-----------|----------------------------------|
| `--color-navy-900`  | `#0c1a3a` | Fondos oscuros, header, badges   |
| `--color-navy-800`  | `#112240` | Botones primarios                |
| `--color-gold-500`  | `#d4a843` | Acentos, botones de acción       |
| `--color-gray-50`   | `#f8f9fc` | Fondo general de la aplicación   |
| `--color-success`   | `#059669` | Estados positivos, match alto    |
| `--color-warning`   | `#d97706` | Match medio                      |

### Tipografía
- **Fuente:** Inter (Google Fonts)
- **Pesos:** 300–800
- **Estilo:** Limpio, institucional, sin serifas

### Componentes clave
- **Cards:** Bordes sutiles, sin glassmorphism exagerado, sombras controladas
- **Badges:** Pill-style con colores semánticos (navy, gold, success, warning)
- **Buttons:** Bordes redondeados sutiles (`6px`), estilos primary/accent/outline/ghost
- **Progress Bar:** Barra delgada (4px) con transición animada
- **Score Display:** Número grande + barra de progreso con color semántico

---

## 8. Ejecución Local

### Backend (Terminal 1)
```powershell
cd demo_plataforma/backend
.\venv\Scripts\activate
python app.py
# → Servidor en http://localhost:5000
```

### Frontend (Terminal 2)
```powershell
cd demo_plataforma/frontend
npm run dev
# → Servidor en http://localhost:5173
```

---

## 9. Despliegue en Render

### Backend (Web Service)
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Root Directory:** `demo_plataforma/backend`
- **Agregar a `requirements.txt`:** `gunicorn`

### Frontend (Static Site)
- **Build Command:** `npm install && npm run build`
- **Publish Directory:** `demo_plataforma/frontend/dist`
- **Variable de entorno:** `VITE_API_URL=https://<nombre-backend>.onrender.com`

> **Nota:** El frontend lee `VITE_API_URL` como variable de entorno de Vite para conectarse al backend. Si no se configura, usa `http://localhost:5000` por defecto.

---

## 10. Limitaciones del Prototipo

1. **Interoperabilidad simulada:** Los datos de RUES, PILA y Supersociedades son ficticios. La conexión real requeriría APIs oficiales o X-Road.
2. **NLP simplificado:** El emparejamiento usa extracción de keywords en lugar de un modelo de lenguaje real (ej. embeddings semánticos).
3. **Sin persistencia:** No hay base de datos; toda la información se pierde al reiniciar el servidor.
4. **Sin autenticación real:** El login es simulado con NITs hardcoded.
5. **Radicación no funcional:** El botón "Aplicar" no tiene un flujo de postulación real implementado.
