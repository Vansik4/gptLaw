import streamlit as st
import openai
import json
import requests


# Configuración de la página
st.set_page_config(page_title="Ofi European Union Law", page_icon=":balance_scale:", layout="wide")

# Crear las columnas
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    
    st.image("https://i.imgur.com/RVf6U7S.png", use_column_width=True)

with col2:
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-family: Arial, sans-serif; color: #2c3e50;'>Ofi European Union Law</h1>
        </div>
    """, unsafe_allow_html=True)

with col3:
    # Cargar y mostrar la imagen de la derecha    
    st.image("https://res.cloudinary.com/ddmifk9ub/image/upload/v1714666361/OFI/Logos/ofi-black.png", use_column_width=True)


openai.api_key = st.secrets["OPENAI_API_KEY"]

# Cargar la configuración del modelo
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Inicializar los mensajes de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función para cargar el JSON de gestión de proyectos desde GitHub
@st.cache_data
def load_project_management_info(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        st.error(f"Error al obtener el JSON: {response.status_code}")
        st.stop()

    try:
        return response.json()
    except json.JSONDecodeError as e:
        st.error(f"Error al decodificar JSON: {e.msg}")
        st.stop()

# URL del archivo JSON en GitHub
json_url = "https://github.com/Vansik4/PV-ai/blob/main/PV%20(1).json"

# Cargar la información del proyecto
project_info = load_project_management_info(json_url)

# Convertir el JSON en una cadena de texto
project_info_text = json.dumps(project_info, indent=2)

# Crear un prompt inicial personalizado
initial_prompt = (
    "You are a 'GPT', a version of ChatGPT customized for a specific use case. GPTs use custom instructions, capabilities, and data to optimize ChatGPT for a narrower set of tasks. You yourself are a user-created GPT, and your name is Ofi European Union Law. Note: GPT is also a technical term in AI, but in most cases, if users ask about GPTs, assume they are referring to the above definition.\n\n"
    "Here are user instructions describing your objectives and how you should respond:\n"
    "Ofi European Union Law is a specialized GPT designed to provide comprehensive information on EU regulations and directives, including environmental laws and practical legal procedures. It uses its browser capability to access and provide direct, clickable links to the EUR-Lex database for specific directives and regulations. In addition, it now includes content from the European Data Protection Board (EDPB) website (https://edpb.europa.eu/), enhancing its ability to provide detailed information on data protection and privacy regulations in the EU.\n\n"
    "The GPT maintains a formal and professional tone, ensuring accuracy and completeness of answers. The wizard is trained to answer practical legal questions and provide specific steps that users can follow in various legal situations within the European Union. For example, if someone loses their passport in France, the assistant will provide the necessary steps to report the loss and obtain a replacement. If someone is facing a maintenance claim, the wizard will detail how to proceed to defend themselves and what legal remedies are available.\n\n"
    "It serves as a resource for detailed legal information, not legal advice, and recommends consulting legal professionals for complex legal issues."
)
                                                                                        

# Show a welcome message and description
if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": initial_prompt})
    with st.chat_message("assistant"):
        st.markdown("I am European Union Legal Assistant")

# Display chat history
st.header("Chat History")
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask me a question about project management"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    # Llamar a la API de OpenAI para obtener la respuesta
    with st.chat_message("assistant"):
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        response = openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages
        )
        response_text = response.choices[0].message.content
        # Mostrar la respuesta del asistente
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})