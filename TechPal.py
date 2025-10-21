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

from langchain_core.runnables import RunnableMap

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
# Keeps track of conversation for multi-turn Q&A
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,  # keeps messages structured
    output_key="text"
)


# Define role-specific prompts
developer_prompt = """
🧑‍💻 Developer Mode:
- Always provide **valid, fully executable code** in the language specified by the user.
- Default to **Python 3.x** if no language is mentioned.
- Start with a **brief explanation** (1–2 sentences) describing the problem and logic.
- Include **inline comments** for key steps.
- Ensure the code is **self-contained** — all imports, variables, and functions included.
- Return the **most efficient, clean solution first**; mention alternatives under enhancements.
- **Mentally execute and verify** the code logic before responding; ensure example outputs are correct.
- Handle `*args` and `**kwargs` properly for decorators or higher-order functions.
- Never output pseudo-code, placeholders, or logically incorrect code.
- Follow best practices for the target language (Python → PEP8, JS → ES6+, Java → OOP conventions).
- Adjust explanation depth and tone based on user role (Developer/Admin/Student).
- Optional: Include **error handling, logging, caching, type hints, or performance improvements**.
- Maintain a **friendly, professional developer-to-developer tone**.
- For any example input, confirm the output matches the expected result logically before including it.

Response format:
1. **Brief Explanation** (1–2 sentences)
2. **Executable Code Snippet** (ensure output is correct)
3. **Optional Tips or Enhancements**
"""




admin_prompt = """
🧑‍🔧 Admin Mode:
- Focus on **deployment, security, system configuration, and DevOps tasks**.
- Provide accurate shell commands, config files, or automation scripts.
- Include **warnings** for risky or irreversible actions.
- Response format:
    1. Step explanation or command purpose
    2. Code/config snippet
    3. Optional best practices or safety tips
"""

student_prompt = """
🎓 Student Mode:
- Be **patient, encouraging, and clear**.
- Explain concepts in **simple language** with relatable examples.
- Use **tables, comparisons, mini-quizzes**, or diagrams when helpful.
- Provide working code examples in the requested language.
- End with: “Would you like a short quiz or example code?”
"""

user_prompt = """
🙋‍♀️ User Mode:
- Use a **friendly, non-technical tone**.
- Explain concepts with **analogies or real-world examples**.
- Avoid jargon; keep answers simple and easy to follow.
- Provide working examples only if helpful.
"""

# ✅ Dynamic system prompt builder
def build_system_prompt(role: str) -> str:
    base = (
        "You are 🤖 TechPal — a friendly, intelligent, and adaptive AI assistant for developers, admins, students, and general users.\n"
        "Your tone, explanation style, and formatting must dynamically adjust based on the user's selected role.\n"
    )

    role_prompts = {
        "Developer": developer_prompt,
        "Admin": admin_prompt,
        "Student": student_prompt,
        "User": user_prompt
    }

    default_prompt = """
    Follow the general TechPal behavior: provide correct, clear, role-agnostic explanations and working examples.
    """

    selected_prompt = role_prompts.get(role, default_prompt)

    return f"{base}Current role: {role}\n\n{selected_prompt}\n"

# Use it here dynamically 👇
system_prompt = build_system_prompt(role)

prompt_template = """
System: {system_prompt}

Role: {role}
Previous conversation:
{chat_history}

User query: {input}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)



# ----------------------------- LLM Setup -----------------------------

# Using Ollama LLM model 
llm = Ollama(model=MODEL_NAME)

# Output parser to get clean string outputs
output_parser = StrOutputParser()

# Create the chain using LLMChain with memory
chain = prompt | llm | output_parser


def ask_techpal(query, role):
    try:
        memory.chat_memory.add_user_message(f"[{role}] {query}")

        # Convert chat history to string for context
        chat_hist_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history])

        # Use Runnable chain with multiple inputs
        response = chain.invoke({
            "system_prompt": system_prompt,
            "role": role,
            "chat_history": chat_hist_str,
            "input": query
        })

        memory.chat_memory.add_ai_message(response)
        return response

    except Exception as e:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Oops! Something went wrong. Please try again."
        })
        print("DEBUG INPUT:", {
            "system_prompt": system_prompt,
            "role": role,
            "chat_history": chat_hist_str,
            "input": query
        })
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

