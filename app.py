import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cerebro Industrial", page_icon="🏗️", layout="centered")

# Estilo visual
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 10px; }
    .stButton>button { width: 100%; background-color: #004280; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Cerebro Central de Maquinaria")
st.caption("Soporte Técnico Especializado | Femcor & Baw Robotics")

# --- 2. CONFIGURACIÓN DE LA IA (MODELO UNIVERSAL) ---
# Obtenemos la llave de los Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🚨 Error: No se encontró la 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# Configuración del modelo
try:
    # Limpiamos la llave por si acaso
    genai.configure(api_key=api_key.strip())
    
    # Usamos Gemini 1.5 Pro (Modelo Universal)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
except Exception as e:
    st.error(f"Error al configurar la IA: {e}")
    st.stop()

# --- 3. PROMPT DE SISTEMA ---
SYSTEM_PROMPT = """
Eres el experto técnico de Femcor y Baw Robotics.
Tu función es guiar al usuario por los modelos de máquinas.

MARCAS: Femcor, Baw Robotics.
MODELOS FEMCOR: Plasma (Lineacord X, Agile, etc) y Laser (Golden 3000, 6000, etc).

Reglas: 
1. Responde siempre con opciones claras en negritas y corchetes.
2. Si preguntan por una máquina, ofrece [ VER MANUAL ] y [ LISTADO DE INSUMOS ].
3. Usa tablas para datos técnicos.
"""

# --- 4. GESTIÓN DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta
    with st.chat_message("assistant"):
        try:
            # Enviamos el prompt de sistema + la pregunta del usuario
            full_context = f"{SYSTEM_PROMPT}\n\nPregunta del usuario: {prompt}"
            response = model.generate_content(full_context)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("La IA no devolvió contenido. Intenta otra pregunta.")
                
        except Exception as e:
            st.error(f"Error en la consulta: {e}")
            st.info("Asegúrate de que tu API KEY sea válida y no tenga restricciones de región.")
