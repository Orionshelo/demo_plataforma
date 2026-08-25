import pandas as pd
import json
import os
import math

def clean_str(val):
    if pd.isna(val):
        return ""
    return str(val).strip()

# Marcador que usa el tablero ArCo para "sin dato".
SIN_DATO = "—"

def split_str(val):
    """Parte una celda multi-valor por comas.

    Las comas dentro de parentesis no separan: un objetivo como
    "I+D+i (Investigacion, Desarrollo e Innovacion)" es un solo item.
    """
    if pd.isna(val):
        return []
    partes, buf, nivel = [], [], 0
    for ch in str(val):
        if ch == "(":
            nivel += 1
        elif ch == ")":
            nivel = max(0, nivel - 1)
        if ch == "," and nivel == 0:
            partes.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    partes.append("".join(buf))
    return [p.strip() for p in partes if p.strip() and p.strip() != SIN_DATO]

def run():
    # El tablero vive junto al proyecto: <Analisis empresarial y de oferta>/Resultados ArCo/
    # Se puede sobreescribir con la variable de entorno ARCO_XLSX.
    default_xlsx = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "Resultados ArCo", "Tablero_ArCo_PowerBI.xlsx"
    ))
    excel_path = os.environ.get("ARCO_XLSX", default_xlsx)
    if not os.path.exists(excel_path):
        raise SystemExit(
            f"No se encontro el tablero ArCo en:\n  {excel_path}\n"
            "Indique la ruta con la variable de entorno ARCO_XLSX."
        )
    out_path = os.path.join(os.path.dirname(__file__), "arco_instruments.json")
    
    df = pd.read_excel(excel_path, sheet_name='6_Perfil_Vigentes2026')
    
    instruments = []
    id_counts = {}
    
    for _, row in df.iterrows():
        base_id = clean_str(row['InstrumentoID'])
        if not base_id:
            continue
            
        id_counts[base_id] = id_counts.get(base_id, 0) + 1
        count = id_counts[base_id]
        
        final_id = base_id if count == 1 else f"{base_id}-{count}"
        
        entidad = clean_str(row['Entidad'])
        nombre = clean_str(row['Instrumento'])
        objetivos = split_str(row['Objetivos'])
        usuarios = split_str(row['Usuarios'])
        apoyos = split_str(row['Apoyos'])
        
        # Synthetic description for NLP
        obj_txt = ", ".join(objetivos) if objetivos else "no especificados"
        apo_txt = ", ".join(apoyos) if apoyos else "no especificados"
        desc = f"Instrumento ofrecido por {entidad}. Objetivos: {obj_txt}. Apoyos: {apo_txt}."
        
        inst = {
            "id": final_id,
            "entidad": entidad,
            "nombre": nombre,
            "objetivos": objetivos,
            "usuarios": usuarios,
            "apoyos": apoyos,
            "descripcion": desc
        }
        instruments.append(inst)
        
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(instruments, f, ensure_ascii=False, indent=2)
        
    print(f"Exportados {len(instruments)} instrumentos a {out_path}")

if __name__ == "__main__":
    run()
