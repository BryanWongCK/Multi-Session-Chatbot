from google import genai
from google.genai import types
import config

# Initialize the official Gemini Client using the key from config
client = genai.Client(api_key=config.GEMINI_API_KEY)

def _convert_to_gemini_contents(messages):
    """
    Helper Function (Internal):
    Translates database chat history dictionaries into the specific 
    Content types required by the google-genai SDK.
    """
    formatted_contents = []
    
    for msg in messages:
        # Map roles: Streamlit uses 'assistant', Gemini uses 'model'
        gemini_role = "model" if msg['role'] == "assistant" else "user"
        
        # Build the structured content object required by the SDK
        content_obj = types.Content(
            role=gemini_role,
            parts=[types.Part.from_text(text=msg['content'])]
        )
        formatted_contents.append(content_obj)
        
    return formatted_contents

def get_gemini_stream(model_name, conversation_history, fresh_prompt):
    """
    Combines database history with the new prompt, translates the payload,
    and returns a live text stream coming back from Google cloud servers.
    """
    # 1. Append the new incoming prompt to past history
    full_history = conversation_history + [{"role": "user", "content": fresh_prompt}]
    
    # 2. Transform the message history format into Gemini Content Objects
    gemini_payload = _convert_to_gemini_contents(full_history)
    
    # 3. Call the cloud streaming service
    return client.models.generate_content_stream(
        model=model_name,
        contents=gemini_payload
    )

def parse_stream_chunks(raw_stream):
    """
    A generator function that cleanly extracts text from Gemini's response chunks.
    """
    for chunk in raw_stream:
        # Extract the text property from the current stream packet if available
        if chunk.text:
            yield chunk.text