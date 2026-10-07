import base64, io
import streamlit as st
from PIL import Image
from openai import OpenAI

st.set_page_config(page_title="TFT Coach", page_icon="⚔️", layout="centered")

if "history" not in st.session_state:
    st.session_state.history = []
if "game_state" not in st.session_state:
    st.session_state.game_state = ""

st.title("⚔️ TFT Coach")
st.caption("Captura → analiza → juega")

with st.expander("⚙️ Configuración", expanded=False):
    api_key = st.text_input("OpenAI API Key", type="password")
    model = st.selectbox("Modelo", ["gpt-5.6", "gpt-5.6-luna"], index=0)
    st.info("Para una versión pública, guarda la clave como secreto del servidor y no la pongas en el código.")

st.subheader("📸 Captura de TFT")
uploaded = st.file_uploader("Sube una captura", type=["png","jpg","jpeg","webp"])

c1, c2 = st.columns(2)
with c1:
    hp = st.number_input("❤️ Vida", 1, 100, 100)
with c2:
    gold = st.number_input("💰 Oro", 0, 1000, 10)

c3, c4 = st.columns(2)
with c3:
    level = st.number_input("⭐ Nivel", 1, 11, 4)
with c4:
    stage = st.text_input("🕐 Etapa", placeholder="Ej. 3-2")

question = st.text_area(
    "🎯 Objetivo",
    "Dime exactamente qué debo hacer ahora para buscar Top 4 o ganar.",
    height=90
)

if uploaded:
    img_bytes = uploaded.getvalue()
    st.image(Image.open(io.BytesIO(img_bytes)), use_container_width=True)

if st.button("🚀 ANALIZAR PARTIDA", type="primary", use_container_width=True):
    if not uploaded:
        st.error("Sube una captura primero.")
        st.stop()
    if not api_key:
        st.error("Introduce tu API Key en Configuración.")
        st.stop()

    b64 = base64.b64encode(img_bytes).decode()
    mime = uploaded.type or "image/png"

    prompt = f"""
Eres TFT Coach, un coach competitivo de Teamfight Tactics.
Analiza la captura con máxima atención. NO inventes campeones, objetos, rasgos,
aumentos ni información que no puedas leer. Si algo no es visible, indícalo.

Datos:
Vida={hp}; Oro={gold}; Nivel={level}; Etapa={stage or "desconocida"}.

Estado previo de la partida:
{st.session_state.game_state or "Es la primera captura."}

Pregunta:
{question}

Responde en español, directo y accionable:

🔥 DECISIÓN AHORA
Una sola acción prioritaria.

🛒 TIENDA/BANCA
Qué comprar, vender o conservar.

⚔️ COMPOSICIÓN
Carry, tanque, unidades a buscar y línea alternativa.

🎒 OBJETOS
Qué objeto hacer y a quién equiparlo.

📍 POSICIONAMIENTO
Cómo colocar las unidades visibles.

💰 ECONOMÍA
Si subir nivel, rolear o ahorrar y hasta cuánto.

🏆 OBJETIVO
Top 4 / Top 2 / victoria y por qué.

➡️ PRÓXIMA RONDA
Qué buscar y qué cambiar.

📊 ESTADO ACTUAL
Resume los datos importantes que hayas podido identificar para poder
compararlos con la siguiente captura.

Prioriza las piezas que ya tiene el jugador y evita forzar una composición.
"""

    client = OpenAI(api_key=api_key)
    with st.spinner("🧠 Analizando tablero..."):
        response = client.responses.create(
            model=model,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": f"data:{mime};base64,{b64}", "detail": "high"}
                ]
            }]
        )

    answer = response.output_text
    st.session_state.history.append(answer)
    # Conservamos el último estado textual para la próxima captura.
    marker = answer.find("📊 ESTADO ACTUAL")
    st.session_state.game_state = answer[marker:] if marker >= 0 else answer[-2500:]

    st.success("Análisis listo")
    st.markdown(answer)

if st.session_state.history:
    st.divider()
    if st.button("🗑️ Nueva partida", use_container_width=True):
        st.session_state.history = []
        st.session_state.game_state = ""
        st.rerun()

st.caption("Consejo: captura donde se vean tablero, banca, tienda, objetos, oro, nivel y rivales.")
