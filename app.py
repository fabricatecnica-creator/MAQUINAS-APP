import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cerebro Central Maquinaria", page_icon="🏗️", layout="centered")

# Estilo CSS para mejorar la apariencia
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #004280; color: white; font-weight: bold; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Cerebro Central de Maquinaria")
st.caption("Asistente Técnico Inteligente para Femcor y Baw Robotics")

# --- 2. CONFIGURACIÓN DE SEGURIDAD (API KEY) - VERSIÓN BLINDADA ---
raw_api_key = st.secrets.get("GOOGLE_API_KEY")

if not raw_api_key:
    st.error("🚨 Falta la configuración de GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Limpieza profunda de la llave para evitar errores de cabecera
clean_api_key = raw_api_key.strip().replace('"', '').replace("'", "").replace(" ", "")
genai.configure(api_key=clean_api_key)

# Lógica blindada para selección de modelo
try:
    # Intento 1: Usar gemini-1.5-flash (el más rápido)
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    # Prueba rápida de conexión
    model.count_tokens("test") 
except Exception:
    try:
        # Intento 2: Usar el nombre con prefijo models/
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        model.count_tokens("test")
    except Exception:
        # Intento 3: Versión Pro (siempre disponible como respaldo)
        model = genai.GenerativeModel(model_name='gemini-pro')

# --- 3. DEFINICIÓN DEL CEREBRO (SYSTEM PROMPT) ---
SYSTEM_PROMPT = """
Eres el "Cerebro Central de Gestión de Maquinaria" de Femcor y Baw Robotics. 
Tu objetivo es ser un experto técnico que guía al usuario por la jerarquía de productos.

JERARQUÍA:
1. MARCAS: Femcor, Baw Robotics.
2. FEMCOR: Plasma (Lineacord X, Minicord, Versacord, Alfa, Agile) y Laser (Golden 3000, 6000, Cabinado, Gira Tubos).
3. MODELO LINEACORD X: 2000x6000, 2000x12000, 2500x6000, 2500x12000, 3000x6000, 3000x12000.

PROTOCOLO:
- Responde siempre con menús claros usando negritas y corchetes: **[ OPCIÓN ]**.
- Si el usuario llega a una máquina específica, ofrece: [ DESCARGAR MANUAL ], [ LISTADO DE INSUMOS ], [ VER PROCEDIMIENTO ].
- Usa tablas para los insumos.
"""

# --- 4. GESTIÓN DEL HISTORIAL ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. INTERACCIÓN ---
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Combinamos el prompt del sistema con la pregunta para dar contexto
            full_query = f"{SYSTEM_PROMPT}\n\nPregunta del usuario: {prompt}"
            response = model.generate_content(full_query)
            
            if response and response.text:
                respuesta_final = response.text
                st.markdown(respuesta_final)
                st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
            else:
                st.warning("El cerebro no devolvió texto. Intenta reformular la pregunta.")
                
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Sugerencia: Verifica que tu API Key en Secrets sea correcta y no tenga espacios.")
