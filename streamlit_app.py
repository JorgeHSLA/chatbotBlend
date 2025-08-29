import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot de SCRUM att: Jorge Sierra y Jefferson Gutierrez")
st.write(
    "Este es un chatbot simple que usa el modelo GPT-3.5 de OpenAI para responder preguntas de SCRUM, nos basamos un chat ya creado "
    "Necesitas una API key de OpenAI, que puedes obtener [aquí](https://platform.openai.com/account/api-keys). "
)

# Obtener la API key desde secrets.toml
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Inicializar historial solo una vez
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Actúa como un profesional y conocedor en temas de SCRUM y agilidades técnicas. Tu objetivo es ayudar a entender los conceptos básicos respecto a las certificaciones de SCRUM, explicando de manera clara y con ejemplos fáciles de entender, como si estuvieras hablando a unos recién ingresados a ingeniería de sistemas.\n\nCuando se te pregunte sobre algún tema intenta dar ejemplos practicos y dar motivacion para aprender, intenta siempre recalcarme la importancia de SCRUM en proyectos en parte dirigidos a software"}
    ]


# Crear cliente
client = OpenAI(api_key=openai_api_key)
# Mostrar historial previo
for message in st.session_state.messages:
    if message["role"] != "system":  # No mostramos el mensaje del system
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
# Campo de input
if prompt := st.chat_input("Hazme una pregunta sobre Scrum"):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Generar respuesta
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        stream=True,
    )
    # Mostrar respuesta
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    # Guardar respuesta en historial
    st.session_state.messages.append({"role": "assistant", "content": response})
