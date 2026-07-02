import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from mock_data import MOCK_USERS, ARCO_INSTRUMENTS, calcular_match

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)


# ── API Routes ─────────────────────────────────────────────────────────

@app.route('/api/auth', methods=['POST'])
def auth():
    """Fase 0: Ingreso – Autenticación por Cédula (Track A) o NIT (Track B)."""
    data = request.json
    identificador = data.get('identificador', '').strip()
    tipo = data.get('tipo')

    if tipo == 'cedula':
        return jsonify({
            "status": "success",
            "perfil": "Explorador (Track A – Nacer)",
            "mensaje": "Se ha generado una Llave Temporal vinculada a su documento de identidad.",
            "datos_basicos": {
                "nombre": "Emprendedor",
                "estado": "Ideación / Pre-formalización",
                "departamento": "—",
            }
        })

    elif tipo == 'nit':
        user_info = MOCK_USERS.get(identificador)
        if user_info:
            return jsonify({
                "status": "success",
                "perfil": user_info['perfil'],
                "mensaje": "Interoperabilidad exitosa: datos validados vía RUES, PILA y Superintendencia de Sociedades.",
                "datos_basicos": user_info
            })
        else:
            return jsonify({
                "status": "error",
                "mensaje": "NIT no encontrado en el registro simulado. NITs de prueba: 900123456-1, 800987654-2, 901234567-3."
            }), 404

    return jsonify({"status": "error", "mensaje": "Tipo de identificación no válido."}), 400


@app.route('/api/diagnostico', methods=['POST'])
def diagnostico():
    """Fase 2: Autodiagnóstico – Radar de Madurez Empresarial."""
    data = request.json
    respuestas = data.get('respuestas', {})

    match_results, perfil_calculado, puntajes_radar = calcular_match(respuestas)

    return jsonify({
        "status": "success",
        "mensaje": "Diagnóstico completado. Motor de emparejamiento semántico (NLP) activo.",
        "perfil_calculado": perfil_calculado,
        "puntajes_radar": puntajes_radar,
        "total_instrumentos_arco": len(ARCO_INSTRUMENTS),
        "matches": match_results
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Health check para Render."""
    return jsonify({"status": "ok", "service": "Ruta Integral – API", "instrumentos_arco": len(ARCO_INSTRUMENTS)})


# ── Serve React Frontend ───────────────────────────────────────────────

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve the React SPA – any non-API route returns index.html."""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
