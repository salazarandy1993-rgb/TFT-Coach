# TFT Coach Mobile

Aplicación Streamlit para analizar capturas de Teamfight Tactics con visión.

## Ejecutar en PC

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicarla para Android

1. Crea un repositorio en GitHub.
2. Sube `app.py` y `requirements.txt`.
3. Entra a Streamlit Community Cloud.
4. Conecta el repositorio.
5. Selecciona `app.py`.
6. Configura `OPENAI_API_KEY` como Secret del proyecto.
7. Despliega.
8. Abre la URL desde Android y usa "Agregar a pantalla de inicio".

Para una versión pública es mejor leer la API key desde `st.secrets["OPENAI_API_KEY"]`
y no pedirla al usuario. La versión incluida mantiene el campo para facilitar pruebas.
