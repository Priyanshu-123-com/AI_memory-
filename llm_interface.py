import os
import json
import requests
from typing import List, Optional

class LLMInterface:
    def __init__(self, provider="openai", model="gpt-3.5-turbo"):
        self.provider = provider.lower()
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        
        # Provider-specific configurations
        if self.provider == "openai":
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
                print(f"[LLM] Initialized OpenAI with model={model}")
            except ImportError:
                print("[LLM] OpenAI package not installed. Installing...")
                self._install_openai()
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
                print(f"[LLM] Initialized OpenAI with model={model}")
                
        elif self.provider == "ollama":
            self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            print(f"[LLM] Initialized Ollama with model={model} at {self.ollama_url}")
            
        elif self.provider == "huggingface":
            self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY", "")
            print(f"[LLM] Initialized Hugging Face with model={model}")
            
        else:
            print(f"[LLM] Using mock provider with model={model}")
            
    def _install_openai(self):
        """Install openai package if not available"""
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
        
    def _call_openai(self, messages: List[dict], temperature: float = 0.7) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[LLM] OpenAI API error: {e}")
            return self._get_mock_response(messages)
            
    def _call_ollama(self, prompt: str, temperature: float = 0.7) -> str:
        """Call Ollama API"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json()["response"].strip()
            else:
                print(f"[LLM] Ollama API error: {response.status_code}")
                return self._get_mock_response_from_prompt(prompt)
        except Exception as e:
            print(f"[LLM] Ollama API error: {e}")
            return self._get_mock_response_from_prompt(prompt)
            
    def _call_huggingface(self, prompt: str, temperature: float = 0.7) -> str:
        """Call Hugging Face Inference API"""
        try:
            headers = {"Authorization": f"Bearer {self.hf_api_key}"}
            API_URL = f"https://api-inference.huggingface.co/models/{self.model}"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_new_tokens": 300
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0]["generated_text"].strip()
                elif isinstance(result, dict) and "generated_text" in result:
                    return result["generated_text"].strip()
            print(f"[LLM] Hugging Face API error: {response.status_code}")
            return self._get_mock_response_from_prompt(prompt)
        except Exception as e:
            print(f"[LLM] Hugging Face API error: {e}")
            return self._get_mock_response_from_prompt(prompt)
            
    def _get_mock_response(self, messages: List[dict]) -> str:
        """Generate mock response based on messages"""
        user_message = ""
        for msg in messages:
            if msg["role"] == "user":
                user_message = msg["content"]
                break
                
        return self._get_mock_response_from_prompt(user_message)
        
    def _get_mock_response_from_prompt(self, prompt: str) -> str:
        """Generate mock response based on prompt content"""
        prompt_lower = prompt.lower()
        
        # More interactive and conversational mock responses
        if "hello" in prompt_lower or "hi" in prompt_lower or "hey" in prompt_lower:
            greetings = [
                "Hello there! I'm MemGraph AI, your intelligent memory assistant. I'm excited to help you explore the fascinating world of memory architectures!",
                "Hi! I'm MemGraph AI - your guide to understanding advanced memory systems. What would you like to know about the four-tier memory architecture?",
                "Hey there! I'm MemGraph AI, designed to work with cutting-edge memory technologies. I can help you understand how neural caches, episodic matrices, and semantic monoliths work together!"
            ]
            import random
            return random.choice(greetings)
            
        elif "name" in prompt_lower:
            return "I'm MemGraph AI, your interactive memory assistant! I'm built on the MemGraph nuclear memory architecture - a sophisticated four-tier system that mimics human memory patterns. I can help you understand how memories are stored, retrieved, and processed across different memory layers."
            
        elif "memory" in prompt_lower:
            return "The MemGraph system is fascinating! It uses a four-tier architecture: L1 Neural Cache for immediate access, L2 Episodic Matrix for temporal patterns, L3 Semantic Monolith for long-term knowledge, and L4 Relationship Graph for connections between concepts. Each tier has unique properties and retrieval mechanisms. Would you like me to explain any specific tier in detail?"
            
        elif "help" in prompt_lower:
            return "I'd be happy to help! I can assist you with understanding memory architectures, explaining how different memory tiers work, demonstrating the retrieval process, or answering questions about the MemGraph system. What aspect of memory systems interests you most?"
            
        elif "what is" in prompt_lower or "what are" in prompt_lower:
            if "neural cache" in prompt_lower:
                return "The L1 Neural Cache is the fastest memory tier! It's like your brain's immediate recall - storing recently accessed information with hyper-fast retrieval times. Think of it as your working memory that keeps frequently used data readily available."
            elif "episodic" in prompt_lower:
                return "The L2 Episodic Matrix handles temporal memory patterns! It's like your autobiographical memory, storing experiences and their contextual details in time-based sequences. It's brilliant for session continuity and pattern recognition."
            elif "semantic" in prompt_lower:
                return "The L3 Semantic Monolith is your long-term knowledge base! It stores factual information, concepts, and general knowledge with high persistence. Think of it as your encyclopedia that builds up over time."
            elif "relationship" in prompt_lower:
                return "The L4 Relationship Graph maps connections between entities and concepts! It's like your brain's association network, linking related memories and enabling complex reasoning through connected knowledge."
            else:
                return f"That's an interesting question about '{prompt}'! The MemGraph system processes queries through its multi-tier architecture, analyzing context and retrieving relevant information from the appropriate memory layers. Each tier specializes in different types of knowledge storage and retrieval."
                
        elif "how does" in prompt_lower or "how do" in prompt_lower:
            return f"Great question about '{prompt}'! The MemGraph system uses sophisticated algorithms to process your query. It analyzes the context, determines which memory tiers are most relevant, retrieves appropriate information, and synthesizes a coherent response. The process involves pattern matching, similarity scoring, and contextual weighting across all four tiers."
            
        elif "tell me" in prompt_lower or "explain" in prompt_lower:
            return f"I'd be happy to explain '{prompt}'! The MemGraph architecture is designed to mimic human memory processes. It uses a hierarchical approach where different types of information are stored in specialized tiers, each optimized for specific retrieval patterns and access speeds."
            
        elif "example" in prompt_lower or "demo" in prompt_lower:
            return "Here's a quick demonstration! When you ask me something, I search through multiple memory layers: first checking my immediate cache for recent conversations, then looking through episodic memories for similar contexts, consulting my semantic knowledge base for facts, and finally mapping relationships between concepts. This multi-layered approach makes responses more comprehensive and contextually aware."
            
        else:
            # More engaging default response
            return f"I've processed your query: '{prompt}'. This is handled by the MemGraph memory system, which searches through its four specialized memory tiers to find the most relevant information. Each tier contributes different types of knowledge - from immediate recall to deep semantic understanding. What specific aspect of this process would you like to explore further?"

    def generate_memgraph_response(self, user_query: str, relevant_memories: List) -> str:
        """
        Generates a response based on the user query and injected memory context.
        """
        # Construct Context String
        context_str = "\n".join([
            f"[{m.internal_code}] (Turn {m.metadata.get('creation_turn', '?')}): {m.content}" 
            for m in relevant_memories
        ])
        
        # Create more engaging system prompt
        if context_str:
            system_prompt = f"""You are MemGraph AI, an advanced interactive assistant powered by a four-tier memory architecture. 
You have access to relevant memories that inform your responses. Use this context naturally without explicitly mentioning memory codes.

Active Memories:
{context_str}

Your task is to provide helpful, conversational responses that demonstrate understanding of the context while being engaging and informative. Ask follow-up questions when appropriate, and make the conversation feel natural and interactive."""
        else:
            system_prompt = """You are MemGraph AI, an advanced interactive assistant. 
You're designed to be helpful, engaging, and conversational. Ask questions, provide detailed explanations, and make the interaction feel natural and interesting."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        # Call appropriate provider
        if self.provider == "openai" and self.api_key:
            return self._call_openai(messages)
        elif self.provider == "ollama":
            return self._call_ollama(system_prompt + "\n\nUser: " + user_query)
        elif self.provider == "huggingface" and self.hf_api_key:
            return self._call_huggingface(system_prompt + "\n\nUser: " + user_query)
        else:
            # Fallback to enhanced mock response
            return self._get_mock_response(messages)
            
    def summarize_intent(self, interaction_history: List[str]) -> str:
        """
        HIAGENT: Summarizes a list of interactions into a single 'Goal' or 'Subgoal'.
        """
        joined_history = " ".join(interaction_history)
        
        prompt = f"""Summarize the following interaction history into a concise goal or intent:
        
{joined_history}

Provide a single sentence summary of the user's main objective or intent."""

        if self.provider == "openai" and self.api_key:
            messages = [
                {"role": "system", "content": "You are a helpful assistant that summarizes user intents."},
                {"role": "user", "content": prompt}
            ]
            return self._call_openai(messages, temperature=0.3)
        elif self.provider == "ollama":
            return self._call_ollama("Summarize this user intent: " + joined_history, temperature=0.3)
        else:
            # Mock summarization
            if len(joined_history) > 100:
                return f"User intent: exploring {joined_history[:50]}..."
            else:
                return f"User goal: {joined_history}"

# Initialize with environment variables or defaults
provider = os.getenv("LLM_PROVIDER", "openai")
model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
llm_client = LLMInterface(provider=provider, model=model)
