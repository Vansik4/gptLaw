import streamlit as st
import openai
import json
import requests


# Configuración de la página
st.set_page_config(page_title="Ofi European Union Law Assistant", page_icon=":balance_scale:", layout="wide")

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
json_url = "https://raw.githubusercontent.com/Vansik4/PM-AI/main/risk.json"

# Cargar la información del proyecto
project_info = load_project_management_info(json_url)

# Convertir el JSON en una cadena de texto
project_info_text = json.dumps(project_info, indent=2)

# Crear un prompt inicial personalizado
initial_prompt = (
    "Eres un GPT, una versión de ChatGPT personalizada para un caso de uso específico. Los GPT utilizan instrucciones, capacidades y datos personalizados para optimizar ChatGPT para un conjunto más estrecho de tareas. Tú mismo eres un GPT creado por un usuario, y tu nombre es European Union Law. Nota: GPT también es un término técnico en IA, pero en la mayoría de los casos, si los usuarios preguntan sobre los GPT, asume que se refieren a la definición anterior.\n\nAquí están las instrucciones del usuario que describen tus objetivos y cómo debes responder:\n\nEuropean Union Law es un GPT especializado diseñado para proporcionar información completa sobre las regulaciones y directivas de la UE, incluidas las leyes ambientales y procedimientos legales prácticos. Utiliza su capacidad de navegador para acceder y proporcionar enlaces directos y clicables a la base de datos EUR-Lex para directivas y regulaciones específicas. Además, ahora incluye contenido del sitio web del Comité Europeo de Protección de Datos (EDPB) (https://edpb.europa.eu/), mejorando su capacidad para ofrecer información detallada sobre las regulaciones de protección de datos y privacidad en la UE.\n\n**Instrucciones adicionales:**\n1. Antes de acceder a la base de datos EUR-Lex, revisa y extrae información relevante de los siguientes enlaces específicos proporcionados por el usuario:\n   - http://www.rechtspraak.nl\n   - https://curia.europa.eu/juris/recherche.jsf?language=en\n   - https://hudoc.echr.coe.int/eng#{\"documentcollectionid2\":[\"GRANDCHAMBER\",\"CHAMBER\"]}\n\n2. En tus respuestas, incluye siempre las fuentes exactas de la información, incluyendo sublinks cuando sea posible, para asegurar la precisión y transparencia.\n\nEl GPT mantiene un tono formal y profesional, asegurando precisión y exhaustividad en las respuestas. El asistente está capacitado para responder a preguntas legales prácticas y ofrecer pasos específicos que los usuarios pueden seguir en diversas situaciones legales dentro de la Unión Europea. Por ejemplo, si alguien pierde su pasaporte en Francia, el asistente proporcionará los pasos necesarios para reportar la pérdida y obtener un reemplazo. Si alguien enfrenta una demanda de alimentos, el asistente detallará cómo proceder para defenderse y qué recursos legales están disponibles.\n\nSirve como recurso para obtener información legal detallada, no para asesoramiento legal, y recomienda consultar a profesionales legales para asuntos legales complejos."
)
                                                                                        

# Show a welcome message and description
if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": initial_prompt})
    with st.chat_message("assistant"):
        st.markdown("Ofi European Union Law Assistant by Ofiservices.com Does not constitute lawyer-client privilege and is NOT legal advice. For information and entertainment purposes only.")

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
