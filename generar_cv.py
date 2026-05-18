import yaml
from jinja2 import Template
import subprocess
import os
import requests  # <-- Nueva librería para conectarnos a Ollama local

def cargar_datos(ruta_yaml):
    with open(ruta_yaml, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def extraer_tags_con_ollama(texto_oferta, modelo="gemma3:27b"):
    print(f"🤖 Analizando la oferta laboral con IA ({modelo} vía Ollama)...")
    
    # Este es el 'Prompt Engineering' para que la IA haga exactamente lo que queremos
    prompt = f"""
    Actúa como un sistema ATS de recursos humanos experto en tecnología. 
    Lee la siguiente oferta de trabajo y extrae un máximo de 7 palabras clave técnicas o herramientas.
    
    REGLA ESTRICTA: Tu respuesta debe ser ÚNICAMENTE las palabras clave separadas por comas, todo en minúsculas. 
    NO agregues saludos, NO uses viñetas, NO agregues ninguna otra palabra. Solo la lista.
    Ejemplo de respuesta perfecta: python, sql, machine learning, etl, aws
    
    Oferta de trabajo:
    {texto_oferta}
    """

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": modelo,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        respuesta_llm = response.json()["response"]
        
        # Limpiamos la respuesta y la convertimos en una lista de Python
        tags = [tag.strip().lower() for tag in respuesta_llm.split(',')]
        print(f" La IA extrajo las siguientes palabras clave: {tags}")
        return tags
        
    except requests.exceptions.ConnectionError:
        print(" ERROR: No me pude conectar a Ollama. ¿Está la aplicación de Ollama abierta?")
        return []
    except Exception as e:
        print(f" Error inesperado con la IA: {e}")
        return []

def generar_cv(datos_cv, palabras_clave=None):
    if palabras_clave:
        datos_cv['proyectos'] = [
            p for p in datos_cv['proyectos'] 
            if any(tag.lower() in palabras_clave for tag in p['tags'])
        ]
        datos_cv['habilidades'] = [
            h for h in datos_cv['habilidades'] 
            if any(tag.lower() in palabras_clave for tag in h['tags'])
        ]
        
        # Opcional: Si el filtro deja los proyectos vacíos, avisar.
        if not datos_cv['proyectos']:
            print(" ADVERTENCIA: La IA no encontró proyectos en tu YAML que coincidan con esta oferta.")
    
    with open('plantilla_cv.md', 'r', encoding='utf-8') as file:
        template = Template(file.read())
    
    cv_markdown = template.render(
        personal=datos_cv['personal'],
        perfil=datos_cv['perfil'],
        proyectos=datos_cv['proyectos'],
        habilidades=datos_cv['habilidades'],
        educacion=datos_cv['educacion'],
        extra=datos_cv['extra']
    )
    
    ruta_md = 'cv_temporal.md'
    with open(ruta_md, 'w', encoding='utf-8') as file:
        file.write(cv_markdown)
    
    archivo_salida = 'CV_Fernando_Quiroz_Automatizado.docx'
    print(f" Armando el currículum en Word ({archivo_salida})...")
    
    try:
        subprocess.run(['pandoc', ruta_md, '-o', archivo_salida], check=True)
        print(" ¡Éxito! Tu CV hiper-personalizado está listo.")
    except Exception as e:
        print(f"Error de Pandoc: {e}")
    finally:
        if os.path.exists(ruta_md):
            os.remove(ruta_md)

if __name__ == '__main__':
    # 1. Cargar tu base de datos (tu YAML)
    datos = cargar_datos('master_cv.yaml')
    
    # 2. PEGA AQUÍ LA OFERTA LABORAL (Puede ser de LinkedIn, GetOnBoard, etc.)
    # Prueba copiando cualquier oferta real aquí adentro:
    oferta_de_trabajo = """
    Traducir oportunidades de negocio en casos de uso de IA viables y escalables.
Diseñar, entrenar, probar y evaluar modelos predictivos y soluciones de IA Generativa.
Prototipar y desarrollar soluciones usando prompt engineering, RAG, embeddings, fine-tuning y agentes LLM.
Implementar evaluaciones técnicas, benchmarks y métricas de calidad de modelos.
Colaborar en procesos de gobernanza, ética y gestión de riesgos de IA (sesgos, explicabilidad, cumplimiento).
Trabajar de manera transversal con equipos de negocio, data, compliance y tecnología para asegurar impacto real.
    """
    
    # 3. La IA lee la oferta y saca los tags (Asegúrate de poner el modelo que descargaste en Ollama)
    tags_ia = extraer_tags_con_ollama(oferta_de_trabajo, modelo="llama3")
    
    # 4. Generar el Word
    if tags_ia:
        generar_cv(datos, palabras_clave=tags_ia)
    else:
        print("Generando CV base sin filtros...")
        generar_cv(datos)