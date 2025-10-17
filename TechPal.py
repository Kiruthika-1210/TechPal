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


# -----------------------------
# Streamlit UI Setup
# -----------------------------

st.title("TechPal - AI Assistance for Every Tech Challenge")
st.write("Your AI developer assistant for coding, deployment, databases, and more!")

# Optional: Role selection dropdown (for role-based responses)
role = st.selectbox("Choose your role", ["Developer", "Admin", "Student", "User"])

# Input text box for user queries
input_txt = st.text_input("Enter your query and let TechPal handle it! ⚡")

# Keeps track of conversation for multi-turn Q&A
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# -----------------------------
# LangChain Prompt Setup
# -----------------------------

# We define a chat prompt template that includes:
# - System instruction (what TechPal should behave like)
# - User input placeholder (query + role)

system_prompt = """ You are TechPal, an AI assistant for tech users.
        - Developer → Give code-focused answers, snippets, and debugging tips.
        - Admin → Give practical, safe best practices for deployment, security, and server  management.
        - Student → Give clear explanations, step-by-step guidance, and mini quizzes for learning.
        - User → Give simple, non-technical explanations with analogies and plain language.
        Always remember the user's role."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input_text}")
])


# -----------------------------
# LLM Setup
# -----------------------------

# Using Ollama LLM model 
llm = Ollama(model = "llama2")

# Output parser to get clean string outputs
output_parser = StrOutputParser()


# Create the chain
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    output_key="text"  # optional
)

# -----------------------------
# Handle User Input
# -----------------------------

# Initialize response variable
response = ""  

# Only run if user entered something
if input_txt:
    # Invoke chain with role + query
    combined_input = f"Role: {role}\nUser query: {input_txt}"
    response = llm_chain.run(combined_input)

    # Display the response
    st.write("💡 TechPal says:")
    st.write(response)