import os
import json
# import openai # Uncomment if using OpenAI directly, or use requests for Ollama/Local

# Mocking LLM for now to ensure portability and no API key dependency for the immediate demo unless user keys are provided.
# In a real hackathon, you'd replace this with actual API calls.

class LLMInterface:
    def __init__(self, provider="mock", model="llama3"):
        self.provider = provider
        self.model = model
        print(f"[LLM] Initialized with provider={provider}, model={model}")

    def generate_memgraph_response(self, user_query, relevant_memories):
        """
        Generates a response based on the user query and injected memory context.
        """
        # Construct Context String
        context_str = "\n".join([f"[{m.internal_code}] (Turn {m.metadata.get('turn_id', '?')}): {m.content}" for m in relevant_memories])
        
        system_prompt = f"""You are MemGraph AI. Use the following Active Memories to answer the user. 
Do NOT explicitly mention "I found this memory", just use the information naturally.
If the memories contradict, trust the one with the higher confidence score.

Active Memories:
{context_str}
"""
        
        # Mock Response Logic
        if "name" in user_query.lower() and "Priranshu" in context_str:
             return f"Your name is Priranshu. I recall this from memory {relevant_memories[0].internal_code}."
        
        return f"This is a generated response for '{user_query}' based on {len(relevant_memories)} active memories."

    def summarize_intent(self, interaction_history):
        """
        HIAGENT: Summarizes a list of interactions into a single 'Goal' or 'Subgoal'.
        """
        # interaction_history is a list of memory content strings
        joined_history = " ".join(interaction_history)
        
        # Mock Summarization
        summary = f"User goal intent derived from: {joined_history[:50]}..."
        return summary

# Singleton instance
llm_client = LLMInterface()
