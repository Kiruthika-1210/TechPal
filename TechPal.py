import os
from dotenv import load_dotenv

import uuid

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



# ----------------------------- Load Environment -----------------------------

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "llama2")



# ----------------------------- Streamlit UI -----------------------------

st.set_page_config(page_title="TechPal", page_icon="🤖", layout="centered")

st.title("🤖 TechPal - AI Assistance for Every Tech Challenge")
st.write("Your AI developer assistant for coding, deployment, databases, and more!")

# --- CSS Styling for Scrollable Chat Container ---
st.markdown("""
<style>
.chat-container {
    max-height: 70vh;
    overflow-y: auto;
    padding: 15px;
    border-radius: 12px;
    background-color: #f7f9fc;
    box-shadow: 0 0 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)



# ----------------------------- Session State -----------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())



# ----------------------------- Sidebar -----------------------------

with st.sidebar:
    st.header("⚙️ Chat Settings")
    role = st.selectbox("Choose your role", ["Developer", "Admin", "Student", "User"])
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.conversation_id = str(uuid.uuid4())
        st.success("Chat cleared! Start fresh.")
        st.stop()  # stops current script and refreshes UI
    st.caption(f"🆔 Conversation ID: {st.session_state.conversation_id}")



# ----------------------------- Dynamic Greetings -----------------------------

greetings = {
    "Developer": "Hey Developer! 💻 Ready to code?",
    "Admin": "Hello Admin! ⚙️ Let's optimize and secure your systems.",
    "Student": "Hi Student! 🎓 Let's learn something new today.",
    "User": "Hey there! 🙋‍♀️ How can I simplify tech for you today?"
}
st.markdown(f"**{greetings[role]}**")



# ----------------------------- Display Chat Messages -----------------------------

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display all past chat messages with role-specific icons
role_icons = {
    "Developer": "🧑‍💻",
    "Admin": "🧑‍🔧",
    "Student": "🎓",
    "User": "🙋‍♀️"
}

for message in st.session_state.chat_history:
    icon = role_icons.get(message["role"], "🤖")  # default fallback icon
    with st.chat_message(message["role"]):
        st.markdown(f"{icon} {message['content']}")




# ----------------------------- LangChain Setup -----------------------------

# Keeps track of conversation for multi-turn Q&A
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="text")

system_prompt = """
You are 🤖 TechPal — a friendly, intelligent, and adaptive AI assistant designed to support different types of tech users. 
Your tone, explanation style, and formatting should dynamically adjust based on the user's selected role.
The current user role is: {role}.
Only answer in the style of this role. 
🧑‍💻 **Developer Mode:**
- Focus on **code**, **debugging tips**, and **best practices**.
- Provide **concise explanations** with **code blocks**, minimal fluff, and efficient solutions.
- Always give **short, clear comments** in the code.
- Use **examples that are executable** and correct.
- Break concepts step-by-step if needed, then provide a practical code snippet.
- Include tips, best practices, or optional enhancements at the end.
- Example structure for decorators:
    1. Brief explanation of concept.
    2. Minimal working code.
    3. Optional enhancements (like logging, arguments, caching).

🧑‍🔧 **Admin Mode:**
- Focus on **deployment**, **security**, **system configurations**, and **DevOps workflows**.
- Provide **commands**, **config examples**, and **safety tips**.
- Emphasize stability, reliability, and security.
- Example:
    ```
    sudo systemctl restart nginx
    ```
    ⚠️ Always back up configuration files before editing.

🎓 **Student Mode:**
- Be encouraging, patient, and clear.
- Break down complex topics step-by-step in **simple language**.
- Use **tables**, **comparisons**, and **mini quizzes**.
- Example table:
    | Concept | Explanation | Example |
    |----------|--------------|----------|
    | Variable | Stores data | `x = 10` |
- End explanations with: “Would you like a short quiz or example code?”

🙋‍♀️ **User Mode:**
- Keep tone friendly, simple, and non-technical.
- Use **analogies** and **real-world examples**.
- Avoid jargon — replace with relatable terms.
- Example:
    “Think of an API as a waiter who takes your order (request) and brings your food (response) from the kitchen (server).”

✨ **General Guidelines:**
- Always adapt your tone and content based on the user’s role.
- **Developers & Admins:** Keep tone precise, technical, and efficient. Limit emojis (use ✅, ⚙️, or 💡 only if needed).
- **Students & Users:** Be more visual and friendly — use emojis, analogies, and formatting for engagement.
- Always use markdown for clarity (code blocks, bullet points, or tables).
- Keep responses structured — first explain briefly, then show example/code, and end with a helpful note.
"""

system_prompt_filled = system_prompt.format(role=role)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt_filled),
    ("user", "{input}")
])



# ----------------------------- LLM Setup -----------------------------

# Using Ollama LLM model 
llm = Ollama(model=MODEL_NAME)

# Output parser to get clean string outputs
output_parser = StrOutputParser()

# Create the chain
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    output_key="text"
)

def ask_techpal(query, role):
    try:
        # Add to memory
        memory.chat_memory.add_user_message(f"[Role: {role}] {query}")

        # Run LLM with the role-specific input
        response = llm_chain.run({"input": query})

        # Store AI response in memory
        memory.chat_memory.add_ai_message(response)

        return response
    except Exception as e:
        print("DEBUG ERROR:", e)
        return f"Error: {e}"




# ----------------------------- Input & Submit -----------------------------

user_input = st.chat_input("Type your query here...")

# Initialize response variable
response = ""  

# Only run if user entered something
if user_input:
    # Display user message immediately
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # AI response section (stream or static)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        try:
            with st.spinner("💭 TechPal is thinking..."):
                response = ask_techpal(user_input, role)
                response_placeholder.markdown(response)

            st.session_state.chat_history.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error("⚠️ Oops! TechPal faced a hiccup. Please try again.")

