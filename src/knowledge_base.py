from pypdf import PdfReader
import io

def load_knowledge_base(uploaded_files):
    """
    Extract text from uploaded PDF files to create a knowledge base.
    
    Args:
        uploaded_files (list): List of uploaded PDF files
    
    Returns:
        str: Extracted text from all PDFs
    """
    knowledge_base = ""
    
    for uploaded_file in uploaded_files:
        # Read PDF file
        pdf_bytes = uploaded_file.read()
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = PdfReader(pdf_stream)
        
        # Extract text from each page
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                knowledge_base += page_text + "\n\n"
    
    return knowledge_base