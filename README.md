# 🤖 TechPal – Role-Adaptive AI Tech Assistant

TechPal is a **role-aware AI assistant** built using **Streamlit, LangChain, and Ollama**.  
It dynamically adapts its responses for **Developers, Admins, Students, and General Users**, making it a smart companion for coding help, system administration, learning, and everyday tech queries.

---

## 🚀 Key Features

- 🧠 **Role-Based Intelligence**
  - **Developer** → Clean, executable, best-practice code
  - **Admin** → DevOps, security, deployment commands
  - **Student** → Beginner-friendly explanations
  - **User** → Simple, non-technical guidance

- 💬 **Multi-Turn Conversational Memory**
  - Maintains chat context using `ConversationBufferMemory`
  - Supports natural, continuous conversations

- ⚡ **Local LLM with Ollama**
  - Runs fully locally using models like `llama2`
  - No cloud dependency or API keys required

- 🎨 **Modern Chat UI**
  - Streamlit-based chat interface
  - Role-specific greetings and icons
  - Scrollable chat container

- 🔄 **Session-Safe Conversations**
  - Unique conversation IDs
  - Clear chat functionality

---

## 🛠 Tech Stack

| Layer | Technology |
|------|-----------|
| Frontend | Streamlit |
| LLM Orchestration | LangChain |
| Model Runtime | Ollama |
| Memory | ConversationBufferMemory |
| Prompt Engineering | ChatPromptTemplate |
| Language | Python 3.x |

---

## 📂 Project Structure

TechPal/
├── app.py # Main Streamlit application
├── .env # Environment variables
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Kiruthika-1210/TechPal.git
cd TechPal
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Install & Run Ollama
```bash
ollama pull llama2
```

### 4️⃣ Configure Environment Variables
Create a .env file:
```bash
MODEL_NAME=llama2
```

### 5️⃣ Run TechPal
```bash
streamlit run app.py
```

---

## 🧩 How TechPal Works

1. User selects a role (**Developer / Admin / Student / User**)
2. A dynamic system prompt is generated based on the selected role
3. LangChain pipeline processes the request:
   - Prompt Template
   - Ollama LLM
   - Output Parser
4. Conversation memory maintains multi-turn context
5. Streamlit UI renders role-aware responses

---

## 🧠 Prompt Engineering Highlights

- Enforces **fully executable code** in Developer mode
- Provides **security warnings and best practices** in Admin mode
- Uses **simple explanations and examples** in Student mode
- Avoids technical jargon in User mode

---

## 📈 Future Enhancements

- API mode using FastAPI
- Conversation export (PDF / JSON)
- Vector-based memory using embeddings
- Cloud deployment (Render / AWS)
- Authentication and role-based access

---

## 🎯 Resume Value

- Demonstrates real-world **LLM orchestration**
- Strong example of **prompt engineering**
- Shows **state management and memory handling**
- Combines **AI, frontend, and UX design**
- Easily extensible to production systems

---

## 📄 License

Open-source project. Free to use, modify, and extend.

---

## 👩‍💻 Author

**Kiruthika (Kittu)**  
Aspiring Software Development Engineer | AI & Full-Stack Enthusiast
