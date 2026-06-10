# AI-Study-Assistance

An intelligent, full-stack desktop tool built in Python that extracts core academic material from PDF notes and textbooks to automatically generate comprehensive study guides, conceptual flashcards, and interactive practice quizzes. 

## Technical Architecture
- **Frontend Framework:** Streamlit (Python-native reactive UI)
- **Data Parsing Engine:** PyPDF (Robust extraction of layout text)
- **Large Language Model Layer:** xAI API integration (`grok-2` orchestrations)
- **Security & Configurations:** Dotenv architecture for isolated pipeline environment keys

## System Features
- **Deterministic Token Chunking:** Sanitizes and scales text extraction inputs to comply with API layer constraints.
- **Asynchronous Parsing States:** Built-in loading UX to prevent application freezing during remote endpoint completion requests.
- **Environment Agnostic Setup:** Completely decoupled API authentication layer for seamless deployment scaling.
