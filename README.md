# 🤖 Excel Pro-Sim: AI-Powered Interviewer

A fully autonomous, multimodal AI agent that conducts practical mock interviews for Microsoft Excel skills.

**[[HuggingFace Link Here](https://huggingface.co/spaces/deepshikhar23/ai-ms-excel-interviewer)]** <- (Your Hugging Face Spaces URL)

---
## About The Project

This project is an AI-powered assessment tool designed to automate the technical screening of candidates for Excel proficiency. Instead of a simple Q&A, this agent presents candidates with real-world tasks, provides them with unique datasets, and evaluates their solutions by analyzing both their written explanation and visual proof in the form of screenshots.

## Key Features

* **🤖 Multi-Agent System:** Built with LangGraph, the application uses a robust, stateful agentic architecture to manage the interview flow.
* **👁️ Multimodal Evaluation:** Leverages Google's Gemini Vision model to analyze screenshots of the user's work (formulas, Pivot Tables, etc.) providing undeniable proof of skill.
* **⚙️ Dynamic Task Generation:** Each interview session generates unique CSV datasets to ensure a novel challenge for every user.
* **🗣️ Interactive Experience:** A web-based, conversational interface built with Streamlit.
* **🧠 Adaptive Logic:** The graph is designed to be easily scalable with an adaptive engine that can adjust question difficulty in the future.

## Tech Stack

* **Orchestration:** LangGraph
* **LLM:** Google Gemini 2.5 Flash Lite
* **Frontend:** Streamlit
* **Core Libraries:** LangChain, Pandas
* **Deployment:** Hugging Face Spaces

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/deepshikhar23/ai-excel-interviewer.git](https://github.com/deepshikhar23/ai-excel-interviewer.git)
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd YOUR_REPO_NAME
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your Gemini API key:
    `GEMINI_API_KEY="YOUR_API_KEY_HERE"`

5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
