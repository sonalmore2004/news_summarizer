import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables (optional)
# load_dotenv()

# Gemini model setup
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# Prompt template
summarize_prompt = PromptTemplate(
    template="Summarize the following news article:\n\n{article}\n\nSummary:",
    input_variables=["article"]
)

# LLMChain
summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)

# Function to extract text from URL
def extract_news(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        return f"❌ Failed to fetch news from {url}: {e}"

# 🌈 Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .title {
        color: #4a4a8a;
        text-align: center;
    }
    .footer {
        text-align: center;
        font-size: 13px;
        color: gray;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 🌟 UI setup
st.markdown('<h1 class="title">📰 Gemini-Powered News Summarizer</h1>', unsafe_allow_html=True)
st.markdown("Get a quick summary of any news article using **Google Gemini AI**.")

# 🚀 Input
user_url = st.text_input("🔗 Enter the news article URL:")

# 🧾 Show full article?
show_full_article = st.checkbox("📖 Show full article text")

# 🔘 Button
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
    else:
        st.warning("⚠️ Please enter a valid URL.")

# 📍 Footer
st.markdown('<div class="footer">Made with ❤️ by Sonal | Powered by Gemini</div>', unsafe_allow_html=True)
