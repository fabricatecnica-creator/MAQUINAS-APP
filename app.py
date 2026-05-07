import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cerebro Central Maquinaria", page_icon="🏗️", layout="centered")

# Estilo CSS para mejorar la apariencia en móviles
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #004280; color: white; font-weight: bold; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Cerebro Central de Maquinaria")
st.caption("Asistente Técnico Inteligente para Femcor y Baw Robotics")

# --- 2. CONFIGURACIÓN DE SEGURIDAD (API KEY) ---
raw_api_key = st.secrets.get("GOOGLE_API_KEY")

if not raw_api_key:
    st.error("🚨 Falta la configuración de GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Limpieza de la llave para evitar errores de cabecera (Illegal Header)
clean_api_key = raw_api_key.strip().replace('"', '').replace("'", "")
genai.configure(api_key=clean_api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- 3. DEFINICIÓN DEL CEREBRO (SYSTEM PROMPT) ---
SYSTEM_PROMPT = """
Eres el "Cerebro Central de Gestión de Maquinaria". Tu objetivo es guiar al usuario por la jerarquía técnica.

JERARQUÍA ESTRICTA:
1. MARCAS: Femcor, Baw Robotics.
2. FEMCOR DIVISIONES: Plasma, Laser.
3. MODELOS PLASMA: Lineacord X, Minicord, Versacord, Alfa, Lineacord, Lineacord 4.0, Agile.
4. MODELOS LASER: Laser Golden 3000, Laser Golden 6000, Laser Golden Cabinado 6000, Gira Tubos.
5. ESPECIFICACIONES LINEACORD X: 2000x6000, 2000x12000, 2500x6000, 2500x12000, 3000x6000, 3000.

PROTOCOLO DE RESPUESTA:
- Siempre responde usando menús visuales con negritas y corchetes, ej: **[ SELECCIONAR ]**.
- Si el usuario elige una máquina final, ofrece:
  a) [ VER PROCEDIMIENTO ] (Extraer de tus documentos).
  b) [ DESCARGAR PDF ] (Simular link de Drive).
  c) [ LISTADO DE INSUMOS ] (Mostrar tabla de piezas).
- Tono: Profesional, técnico y preciso.
"""

# --- 4. GESTIÓN DEL HISTORIAL DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. LÓGICA DE INTERACCIÓN ---
if prompt := st.chat_input("Escribe tu marca o modelo de máquina..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta de la IA
    with st.chat_message("assistant"):
        try:
            # Construimos el envío combinando el System Prompt y la consulta actual
            full_query = f"{SYSTEM_PROMPT}\n\nUsuario dice: {prompt}"
            response = model.generate_content(full_query)
            
            respuesta_texto = response.text
            
            # Mostrar respuesta y guardar en historial
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
        except Exception as e:
            st.error(f"Hubo un error al conectar con el cerebro de IA: {e}")
            st.info("Revisa que tu API Key sea válida y no tenga espacios.")
