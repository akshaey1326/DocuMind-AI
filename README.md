# DocuMind AI — Smart Document Knowledge Assistant

## Overview
DocuMind AI is a Python-based document assistant that allows users to upload PDF and TXT documents, ask questions about their content, and receive AI-generated answers grounded in relevant document passages.

## Features
- Upload and read PDF and TXT documents.
- Ask questions about uploaded documents through a chat interface.
- Retrieve relevant text passages to provide context for AI-generated answers.
- Display source passages alongside answers.
- Generate AI-powered flashcards for revision.
- Generate mind maps to organize key concepts.
- Provide a simple web interface built with Streamlit.

## Technologies Used
- Python
- Streamlit
- PyMuPDF (fitz) for PDF processing
- Mesh API for language-model responses
- AI-based text processing and retrieval

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/akshaey1326/DocuMind-AI.git
   cd DocuMind-AI
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project folder and add your Mesh API key:
   ```text
   MESH_API_KEY=your_api_key_here
   ```

4. Start the application:
   ```bash
   streamlit run app.py
   ```

## Security
Never commit API keys, `.env` files, or private documents to the repository.

## Project Purpose
This project demonstrates how document processing, information retrieval, and language models can be combined to build an interactive document knowledge assistant.
