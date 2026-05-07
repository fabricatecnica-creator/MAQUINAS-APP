import streamlit as st
import google.generativeai as genai

# Configuración básica
st.set_page_config(page_title="Cerebro Maquinaria", layout="centered")
st.title("🏗️ Cerebro Central de Maquinaria")

# Configuración Segura de API
raw_api_key = st.secrets.get("GOOGLE_API_KEY")
if not raw_api_key:
    st.error("Falta la API Key en los Secrets.")
    st.stop()

# Limpiamos la llave de espacios o saltos de línea invisibles
clean_api_key = raw_api_key.strip().replace('"', '').replace("'", "")
genai.configure(api_key=clean_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# System Prompt
SYSTEM_PROMPT = "Eres el experto técnico de Femcor y Baw Robotics. Usa menús y tablas."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Enviamos la consulta
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUsuario: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error de conexión: {e}"), "content": full_response})
