# AI-Customer-Support-Agent

## 🚀 Project Overview
This Proof of Concept (POC) demonstrates an **AI-powered customer support chatbot** designed to handle **banking-related queries** using real-time data retrieval. The chatbot was developed to:
- Answer customer queries related to **credit cards, accounts, trading, and general banking FAQs**.
- Perform **real-time web scraping** to fetch the latest banking information.
- Use **Qdrant for memory storage**, allowing contextual responses.
- Implement **OpenAI's GPT-4o** for natural language processing.

This POC was built as an experimental model to explore AI-driven banking chatbots and has since been concluded due to **limitations in handling complex queries and response accuracy**.

---

## ⚙️ Tech Stack
- **Python 3.9**
- **Streamlit** - Frontend UI for chatbot interaction
- **OpenAI GPT-4o** - AI-powered response generation
- **Qdrant** - Vector database for memory storage
- **Playwright** - Web scraping for real-time data
- **Docker** - Running Qdrant locally

---

## 🏗️ Features Implemented
✅ **Real-time Web Scraping** - Fetches live banking data from OCBC website using Playwright.  
✅ **Intent Classification** - Categorizes customer queries into predefined banking topics.  
✅ **AI-powered Responses** - Uses OpenAI GPT-4o to generate contextual answers.  
✅ **Memory Storage** - Stores past interactions in Qdrant for better user experience.  

---

## 🛠️ How to Run Locally
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/customer-support-agent.git
cd customer-support-agent
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Run Qdrant in DockerThe app expects Qdrant to be running on localhost:6333. Adjust the configuration in the code if your setup is different.
```sh
docker pull qdrant/qdrant
docker run -d -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant
```

### 4️⃣ Start the Chatbot
```sh
streamlit run customer_support_agentv1.py
```

### 5️⃣ Open in Browser
Visit: **[http://localhost:8501](http://localhost:8501)**  

---

## 📜 License
This project is for **educational and experimental purposes only** and is not intended for production use.

---

## 📌 Conclusion
This POC successfully demonstrated the feasibility of an AI-powered banking chatbot but highlighted critical limitations in handling **complex user queries, accuracy, and scalability**. These learnings will be valuable for future AI implementations in banking environments.

For more information, feel free to contribute or fork this project! 
