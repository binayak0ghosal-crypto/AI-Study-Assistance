import os
import pypdf
import streamlit as st
from openai import OpenAI  
from dotenv import load_dotenv

# ==========================================
# PHASE 1 & 3: GROK INITIALIZATION & SECURITY
# ==========================================
load_dotenv() 

# Grab the API key from the .env file
grok_key = os.getenv("GROK_API_KEY")

# Set up the Grok client safely
client = None
if grok_key:
    client = OpenAI(
        api_key=grok_key,
        base_url="https://api.x.ai/v1",
    )

# ==========================================
# PHASE 2: PDF TEXT EXTRACTION FUNCTION
# ==========================================
def extract_text_from_pdf(pdf_file):
    reader = pypdf.PdfReader(pdf_file)
    extracted_text = ""
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
            
    return extracted_text

# ==========================================
# PHASE 3: AI GENERATION FUNCTION (GROK)
# ==========================================
def generate_study_material(text, material_type):
    if not client:
        return "❌ Error: API Key missing. Please check your `.env` file."
        
    prompts = {
        "Summary": "Provide a comprehensive summary and key takeaways of this text.",
        "Flashcards": "Create 5 conceptual flashcards from this text. Format as Front: [Question] | Back: [Answer].",
        "Quiz": "Generate a 3-question multiple-choice quiz based on this text with answers at the bottom."
    }
    
    try:
        response = client.chat.completions.create(
            model="grok-2", 
            messages=[
                {"role": "system", "content": "You are an expert academic tutor."},
                {"role": "user", "content": f"{prompts[material_type]}\n\nText:\n{text[:4000]}"} 
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API Error: {str(e)}"

# ==========================================
# PHASE 4: STREAMLIT USER INTERFACE (UI)
# ==========================================
st.set_page_config(page_title="AI Study Assistant", page_icon="📚")
st.title("📚 AI-Powered Study Assistant")
st.write("Upload your textbook chapter or notes, and let AI do the heavy lifting.")

# Helper message to check API key status visually
if not grok_key:
    st.warning("⚠️ `.env` file or `GROK_API_KEY` not detected. Make sure your `.env` file is in the same folder as `app.py`!")

# File Uploader Widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    # Extract text once
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    
    # Create layout tabs
    tab1, tab2, tab3 = st.tabs(["📋 Summary & Guide", "🔀 Flashcards", "🧠 Practice Quiz"])
    
    with tab1:
        if st.button("Generate Study Guide"):
            with st.spinner("Analyzing text with Grok..."):
                summary = generate_study_material(pdf_text, "Summary")
                st.markdown(summary)
                
    with tab2:
        if st.button("Generate Flashcards"):
            with st.spinner("Creating flashcards with Grok..."):
                cards = generate_study_material(pdf_text, "Flashcards")
                st.text_area("Your Flashcards", cards, height=300)
                
    with tab3:
        if st.button("Generate Quiz"):
            with st.spinner("Formulating questions with Grok..."):
                quiz = generate_study_material(pdf_text, "Quiz")
                st.markdown(quiz)