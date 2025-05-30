import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
import os

# Optional: load_dotenv()

# ✅ Gemini model setup
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# ✅ Prompt template
summarize_prompt = PromptTemplate(
    template="Summarize the following news article:\n\n{article}\n\nSummary:",
    input_variables=["article"]
)

# ✅ LLMChain
summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)

# ✅ Function to extract text
def extract_news(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        return f"❌ Failed to fetch news from {url}: {e}"

# ✅ Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background-color: #f8f9fa;
    }
    .title {
        color: #2c3e50;
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #ccc;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton > button {
        background-color: #4a4a8a;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #30306d;
        transform: scale(1.02);
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .footer {
        text-align: center;
        font-size: 13px;
        color: gray;
        margin-top: 30px;
    }
    .stCheckbox {
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ UI
st.markdown('<h1 class="title">📰 Gemini-Powered News Summarizer</h1>', unsafe_allow_html=True)
st.markdown("Get a quick summary of any news article using **Google Gemini AI**.")

user_url = st.text_input("🔗 Enter the news article URL:")

show_full_article = st.checkbox("📖 Show full article text")

if st.button("✨ Summarize Now"):
    if user_url:
        with st.spinner("⏳ Summarizing... Please wait..."):
            article = extract_news(user_url)
            if article.lower().startswith("❌ failed to fetch"):
                st.error(article)
            else:
                summary = summarize_chain.run(article=article)
                st.success("✅ Summary generated successfully!")

                if show_full_article:
                    st.subheader("📝 Full Article:")
                    st.write(article)

                st.subheader("📌 Summary:")
                st.markdown(f"<div class='main'>{summary}</div>", unsafe_allow_html=True)
                st.balloons()
    else:
        st.warning("⚠️ Please enter a valid URL.")

# ✅ Footer
st.markdown('<div class="footer">Made with ❤️ by Sonal | Powered by Gemini</div>', unsafe_allow_html=True)
