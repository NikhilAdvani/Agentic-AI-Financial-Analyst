import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

# Set page config
st.set_page_config(
    page_title="AI Financial Research Assistant",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize agents (cached for performance)
@st.cache_resource
def get_agents():
    # Web search agent
    web_search_agent = Agent(
        name="Web Search Agent",
        role="Search the web for the information",
        model=Groq(id="deepseek-r1-distill-llama-70b"),
        tools=[DuckDuckGo()],
        instructions=[
            "Search the web for current information",
            "Always include sources in your response",
            "If a search fails, explain why it might have failed"
            ],
        show_tools_calls=True,
        markdown=True,
    )

    # Financial agent
    finance_agent = Agent(
        name="Finance AI Agent",
        model=Groq(id="deepseek-r1-distill-llama-70b"),
        tools=[
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                stock_fundamentals=True,
                company_news=True
            ),
        ],
        instructions=[
            "Provide financial data in clear tables when possible",
            "If data isn't available, explain why"
            ],
        show_tool_calls=True,
        markdown=True,
    )

    # Multi-agent team
    multi_ai_agent = Agent(
        model = Groq(id="deepseek-r1-distill-llama-70b"),
        team=[web_search_agent, finance_agent],
        instructions=[
            "Analyze the query to determine if it requires financial data or web search",
            "Delegate to the appropriate agent",
            "Combine results if needed",
            "If any operation fails, explain what went wrong to the user"
            ],
        show_tool_calls=True,
        markdown=True,
    )
    
    return multi_ai_agent

# App title and description
st.title("AI Financial Research Assistant")
st.markdown("""
This assistant can:
- Retrieve financial data (stock prices, analyst recommendations, fundamentals)
- Find the latest company news
- Search the web for additional information
""")

# Sidebar for settings
with st.sidebar:
    # st.header("Settings")
    example_queries = [
        "Summarize analyst recommendation and share the latest news for Nvidia's stock",
        "What's the current stock price of Apple and its P/E ratio?",
        "Find recent news about Tesla and summarize the key points",
        "Compare Microsoft and Google's stock performance"
    ]
    
    st.subheader("Example Queries")
    for query in example_queries:
        if st.button(query):
            st.session_state.user_query = query

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask about stocks or companies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# Process query
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_query = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            # Get the agent
            agent = get_agents()
            
            # Create a container for the response
            response_container = st.empty()
            
            # Collect the response chunks
            full_response = ""

            try:
                response_stream = agent.run(user_query, stream=True)
                for chunk in response_stream:
                    if hasattr(chunk, 'content'):
                        chunk_content = chunk.content
                    else:
                        chunk_content = str(chunk)
                    
                    full_response += chunk_content
                    response_container.markdown(full_response)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.stop()




