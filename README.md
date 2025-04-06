# Agentic-AI-Financial-Analyst

# AI Financial Research Assistant 🤖📈



[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

A Streamlit web app that combines Groq's Deepseek R1 with financial data (Yahoo Finance) and web search (DuckDuckGo) capabilities.

![Demo Screenshot](demo.gif) *(Replace with actual screenshot)*

## Features ✨

- **Real-time stock data** (prices, P/E ratios, market caps)
- **Analyst recommendations** summary
- **Company news** aggregation
- **Web search integration** for latest information
- **Multi-agent architecture** for specialized tasks
- **Error-resilient design** with fallback mechanisms

## Tech Stack 🛠️

| Component       | Technology |
|----------------|------------|
| Frontend       | Streamlit  |
| LLM            | Groq (Deepseek R1 70B) |
| Financial Data | Yahoo Finance API |
| Web Search     | DuckDuckGo API |
| Backend        | Python 3.10+ |
| Orchestration  | Phi Library |

## Installation ⚙️

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/financial-research-assistant.git
   cd financial-research-assistant

2. ## Step 2: Set Up Environment

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

3. ## Step 3: Install Dependencies

   ```bash
   pip install -r requirements.txt

4. ## Step 4: Configure Environment

   ```bash
   GROQ_API_KEY=your_api_key_here

5. ## Step 5: Launch Application

   ```bash
   streamlit run financial_assistant.py



