import streamlit as st
from openai import OpenAI
from mem0 import Memory
import os
from playwright.sync_api import sync_playwright
import json
import docker

# Initialize Streamlit App
st.title("OC Digital Bank  🏦")
st.caption("Always here to help you.")

# Set up OpenAI API Key
openai_api_key = st.text_input("Enter OpenAI API Key", type="password")

if openai_api_key:
    os.environ['OPENAI_API_KEY'] = openai_api_key
    client = OpenAI()

    # Initialize Qdrant via Docker
    docker_client = docker.from_env()
    try:
        qdrant_container = docker_client.containers.run("qdrant/qdrant", detach=True, ports={"6333/tcp": 6333, "6334/tcp": 6334})
    except Exception as e:
        st.error(f"Error starting Qdrant container: {e}")

    memory = Memory.from_config({
        "vector_store": {
            "provider": "qdrant",
            "config": {"host": "localhost", "port": 6333}
        }
    })
    
    # Define AI Agents
    AGENTS = {
        "cards": "Handles credit card-related queries.",
        "accounts": "Handles account-related queries.",
        "faq": "Handles general banking FAQs.",
        "trading": "Handles stock trading and investment queries."
    }
    
    def classify_intent(query):
        """Classify query intent using GPT-4."""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Classify the user's query into one of these categories: cards, accounts, faq, trading."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content.lower()
    
    def scrape_ocbc(url):
        """Scrape OCBC website using Playwright."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_extra_http_headers({"User-Agent": "Mozilla/5.0"})
            page.goto(url, timeout=60000)
            content = page.content()
            browser.close()
        return content
    
    def handle_query(query, user_id):
        """Route query to the correct agent and retrieve response."""
        intent = classify_intent(query)
        
        if intent not in AGENTS:
            intent = "faq"
        
        urls = {
            "cards": "https://www.ocbc.com/personal-banking/cards",
            "accounts": "https://www.ocbc.com/personal-banking/accounts",
            "faq": "https://www.ocbc.com/personal-banking/help-and-support",
            "trading": "https://www.iocbc.com/index.page"
        }
        
        scraped_content = scrape_ocbc(urls[intent])
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize the following banking information for a customer:"},
                {"role": "user", "content": query + "\n\n" + scraped_content[:2000]}
            ],
            max_tokens=200  # Limit output tokens to prevent large responses
        )
        
        answer = response.choices[0].message.content
        
        memory.add(query, user_id=user_id, metadata={"role": "user"})
        memory.add(answer, user_id=user_id, metadata={"role": "assistant"})
        
        return answer
    
    # Streamlit Chat Interface
    st.sidebar.title("Askme Chatbot")
    customer_id = st.sidebar.text_input("Please input your ID")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    query = st.chat_input("How can I assist you today?")
    
    if query and customer_id:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        with st.spinner("Retrieving information..."):
            response = handle_query(query, customer_id)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    
    elif not customer_id:
        st.warning("Please enter a Customer ID to start the chat.")

