import google.generativeai as genai
from django.conf import settings
import json

class GeminiService:
   

    def __init__(self): 
        secret_key = settings.SECRET_KEY
        genai.configure(api_key=secret_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def chat_with_context(self, message, conversation_history=None, patient_info=None):
        """
        Continue a conversation with the medical assistant
        
        Args:
            message (str): Current user message
            conversation_history (list): Previous messages in the conversation
            patient_info (dict, optional): Additional patient information
            
        Returns:
            dict: Structured response
        """
        try:
            # Initialize chat
            chat = self.model.start_chat(history=self._format_history(conversation_history or []))
            
            # Add system prompt if this is the beginning of conversation
            if not conversation_history:
                system_prompt = self._get_system_prompt(patient_info)
                chat.send_message(system_prompt)
            
            # Send the user's message
            response = chat.send_message(message)
            
            return {
                'response_text': response.text,
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error_message': str(e)
            }
    
    def _format_history(self, conversation_history):
        """Format conversation history for Gemini"""
        formatted_history = []
        for message in conversation_history:
            role = "user" if message.get('isUser', False) else "model"
            formatted_history.append({
                "role": role,
                "parts": [message.get('text', '')]
            })
        return formatted_history
    
    def _get_system_prompt(self, patient_info=None):
        """Create the initial system prompt"""
        prompt = """You are a helpful medical assistant chatbot. Your role is to:
        
1. Help users understand potential medical conditions based on symptoms they describe
2. Provide general health information and guidance
3. Always include appropriate medical disclaimers emphasizing you're not a replacement for professional medical advice
4. Ask relevant follow-up questions to better understand the user's situation
5. Present information in a clear, structured manner
6. Be empathetic and supportive

When discussing potential medical conditions, provide:
- Brief descriptions of likely conditions
- General recommendations
- When to seek professional medical help

Remember: Never diagnose with certainty and always recommend consulting healthcare professionals."""

        if patient_info:
            prompt += "\n\nPatient Information:"
            for key, value in patient_info.items():
                prompt += f"\n- {key}: {value}"
                
        return prompt