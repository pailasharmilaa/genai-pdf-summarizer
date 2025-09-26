
import streamlit as st
import PyPDF2
import openai
import os

# Set your API key (better: use environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("📄 GenAI PDF Summarizer")
st.write("Upload a PDF and get a concise AI-generated summary.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    if st.button("Summarize"):
        if text.strip() == "":
            st.error("No text found in PDF.")
        else:
            st.info("Generating summary... please wait ⏳")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant that summarizes documents."},
                    {"role": "user", "content": f"Summarize this text:\n{text}"}
                ],
                max_tokens=250
            )

            summary = response["choices"][0]["message"]["content"]
            st.success("Summary:")
            st.write(summary)
