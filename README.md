# Smart ATS CV Generator

![alt text](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

![alt text](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)

![alt text](https://img.shields.io/badge/Pandoc-FF0000?style=for-the-badge&logo=pandoc&logoColor=white)

Este proyecto es una herramienta de automatización creada con Python, Ollama y Pandoc para generar currículums en formato Word (.docx) altamente optimizados para sistemas ATS (Applicant Tracking Systems).

## ¿Cómo funciona?
1. **Base de Datos Maestra:** Toda la experiencia se almacena en `master_cv.yaml`.
2. **IA Local:** Utiliza [Ollama](https://ollama.com/) (modelo Llama 3) para analizar una oferta laboral y extraer automáticamente las palabras clave (skills) más relevantes.
3. **Filtrado:** El script filtra la experiencia en el YAML basándose en los tags extraídos por la IA.
4. **Exportación:** Genera un documento Word con formato profesional (estilo Harvard) utilizando Pandoc.

## Tecnologías utilizadas
- Python (PyYAML, Jinja2, Requests)
- Ollama (LLM local)
- Pandoc
