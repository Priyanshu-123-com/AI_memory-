import os
import json
import google.generativeai as genai

class LLMInterface:
    def __init__(self, model_name="gemini-2.0-flash"):
        self.client = None
        self.model_name = model_name
        self.model = None

    def set_api_key(self, api_key):
        """Sets the Gemini API Key and initializes the model."""
        try:
            # Check environment variable first if not provided
            if not api_key:
                api_key = os.environ.get("GEMINI_API_KEY")
            
            # Hardcoded key fallback (User provided)
            if not api_key:
                api_key = "AIzaSy..." # Placeholder for security, in real usage would be the actual key

            if not api_key:
                print("[LLM] No API Key provided or found in environment.")
                return

            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.client = True # Flag to indicate readiness
            print(f"[LLM] Gemini API Key set. Model: {self.model_name}")
        except Exception as e:
            print(f"[LLM] Failed to configure Gemini: {e}")
            self.client = None

    def generate_memgraph_response(self, user_query, active_memories):
        """
        Generates a response using the LLM, conditioned on retrieved memories.
        """
        
        # Context Construction
        memory_block = ""
        if active_memories:
            memory_block = "RELEVANT MEMORIES (Use these to answer):\n"
            for mem in active_memories:
                memory_block += f"- [{mem.tier.name}] {mem.content} (Confidence: {mem.half_life_score:.2f})\n"
        
        system_prompt = f"""You are MemGraph, an AI with a localized long-term memory system.
        
{memory_block}

INSTRUCTIONS:
1. Answer the user's query based ONLY on the provided memories if relevant.
2. If memories are provided, cite them implicitly (e.g., "As you mentioned before...").
3. If no memories are relevant, answer generally but admit you don't recall specific details if asked.
4. Be concise and helpful.
"""
        
        # 1. Real API Call (if key set)
        if self.client and self.model:
            try:
                # Gemini doesn't use 'system' role in the same way as OpenAI in `generate_content`
                # We prepend system prompt to user query or use system_instruction if supported by lib version
                # For safety, simpler concatenation:
                full_prompt = f"{system_prompt}\n\nUSER: {user_query}"
                
                response = self.model.generate_content(full_prompt)
                return response.text
            except Exception as e:
                return f"Error calling Gemini LLM: {str(e)}"

        # 2. Mock Fallback (No Key)
        return f"[MOCK RES] (Gemini Key Missing) I received: '{user_query}'. Memories used: {len(active_memories)}"

    def summarize_intent(self, interaction_history):
        """
        Summarizes a list of interactions into a single 'Goal' or 'Intent' string.
        """
        if self.client and self.model:
            joined_history = " ".join(interaction_history)
            try:
                prompt = f"Summarize the following user interactions into a single concise goal or intent statement:\n\n{joined_history}"
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Error summarizing intent: {str(e)}"
        
        return "User is testing the MemGraph system."

# Singleton Init
llm_client = LLMInterface()
