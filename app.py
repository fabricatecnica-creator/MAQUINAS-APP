import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cerebro Central Industrial", page_icon="🤖", layout="centered")

# Estilo personalizado para que parezca una App Industrial
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004280; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Cerebro Central de Maquinaria")
st.subheader("Soporte Técnico: Femcor & Baw Robotics")

# --- CONEXIÓN CON GOOGLE AI (GEMINI) ---
# Intentamos obtener la API KEY desde los secretos de Streamlit
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("⚠️ Configura la 'GOOGLE_API_KEY' en los Secrets de Streamlit.")

model = genai.GenerativeModel('gemini-1.5-flash')

# --- DEFINICIÓN DEL SYSTEM PROMPT ---
SYSTEM_PROMPT = """
Eres el Cerebro Central de Gestión de Maquinaria de Femcor y Baw Robotics.
Tu interfaz se basa en menús visuales de texto. 
JERARQUÍA:
1. Marca (Femcor / Baw Robotics)
2. Tecnología (Plasma / Laser)
3. Modelo (Lineacord X, etc.)
4. Medidas (2000x6000, etc.)

REGLAS:
- Entrega enlaces de Google Drive para descargas cuando se soliciten.
- Muestra los insumos en tablas Markdown.
- Mantén un tono técnico y preciso.
"""

# --- GESTIÓN DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe el nombre de la máquina o una consulta..."):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta de la IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # Construimos el contexto completo
        contexto = f"{SYSTEM_PROMPT}\n\nHistorial:\n"
        for m in st.session_state.messages:
            contexto += f"{m['role']}: {m['content']}\n"
        
        response = model.generate_content(contexto)
        full_response = response.text
        message_placeholder.markdown(full_response)
    
    # Agregar respuesta de la IA al historial
    st.session_state.messages.append({"role": "assistant", "content": full_response})
