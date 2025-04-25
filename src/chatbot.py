import os
from google import genai
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")

# Create a client instance
client = genai.Client(api_key=api_key)

def get_chatbot_response(query, knowledge_base):
    """
    Get a response from the chatbot based on the user query and knowledge base.
    
    Args:
        query (str): The user's question
        knowledge_base (str): The insurance knowledge base text
    
    Returns:
        str: The chatbot's response
    """
    try:
        # Create a prompt for the LLM
        prompt = f"""
        You are an insurance policy assistant. Use ONLY the following information to answer the query.
        If you cannot find the answer in the provided information, say that you don't have that information.
        
        INSURANCE INFORMATION:
        {knowledge_base}
        
        USER QUERY: {query}
        """
        
        # Generate response using Gemini
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        # Extract and return the response text
        return response.text
    
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"