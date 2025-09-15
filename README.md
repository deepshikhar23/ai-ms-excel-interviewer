# 🤖 Excel Pro-Sim: AI-Powered Interviewer

A fully autonomous, multimodal AI agent that conducts practical mock interviews for Microsoft Excel skills.

**[Live Demo Link Here]** <- (Your Hugging Face Spaces URL)

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

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    ```
2.  Install dependencies:
    ```bash
    cd YOUR_REPO_NAME
    pip install -r requirements.txt
    ```
3.  Set up your environment variables by creating a `.env` file and adding your `GEMINI_API_KEY`.
4.  Run the application:
    ```bash
    streamlit run app.py
    ```