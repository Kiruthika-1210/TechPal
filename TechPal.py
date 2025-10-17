# LangChain core for prompts
from langchain_core.prompts import ChatPromptTemplate

# Output parser to handle simple string outputs (avoids weird characters like \n)
from langchain_core.output_parsers import StrOutputParser 

# Ollama LLM integration
from langchain_community.llms import Ollama

# Streamlit for web UI
import streamlit as st 

from langchain.chains import LLMChain
# Memory for multi-turn conversation
from langchain.memory import ConversationBufferMemory


# ----------------------------- Streamlit UI -----------------------------

st.title("🤖 TechPal - AI Assistance for Every Tech Challenge")
st.write("Your AI developer assistant for coding, deployment, databases, and more!")

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Optional: Role selection dropdown (for role-based responses)
role = st.selectbox("Choose your role", ["Developer", "Admin", "Student", "User"])

#To restart a fresh session
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []



# ----------------------------- LangChain Setup -----------------------------

# Keeps track of conversation for multi-turn Q&A
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

system_prompt = """ You are TechPal, an AI assistant for tech users.
        - Developer → Give code-focused answers, snippets, and debugging tips.
        - Admin → Give practical, safe best practices for deployment, security, and server  management.
        - Student → Give clear explanations, step-by-step guidance, and mini quizzes for learning.
        - User → Give simple, non-technical explanations with analogies and plain language.
        Always remember the user's role."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")   
])



# ----------------------------- LLM Setup -----------------------------

# Using Ollama LLM model 
llm = Ollama(model = "llama2")

# Output parser to get clean string outputs
output_parser = StrOutputParser()

# Create the chain
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    output_key="text"
)

def ask_techpal(query):
    return llm_chain.run({"input": query})



# ----------------------------- Display Chat History -----------------------------

for msg in st.session_state.chat_history:
    with st.chat_message("assistant" if msg.startswith("💡") else "user"):
        st.write(msg)



# ----------------------------- Input & Submit -----------------------------

user_input = st.text_input(
    "Enter your query and let TechPal handle it! ⚡", 
    key="chat_input",
    value=""  # starts empty or resets automatically on rerun
)
submit = st.button("Send") 

# Initialize response variable
response = ""  

# Only run if user entered something
if submit and user_input.strip():
    st.session_state.chat_history.append(f"{role}: {user_input}")

    with st.spinner("💭 TechPal is thinking..."):
        response = ask_techpal(user_input)

    # Append user query and AI response to session chat history
    st.session_state.chat_history.append(f"💡 TechPal says: {response}")

# Display all chat history
for msg in st.session_state.chat_history:
    st.chat_message("assistant" if msg.startswith("💡") else "user").write(msg)


