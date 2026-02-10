import time
import uuid
import math
import random
import json
from enum import Enum
from collections import deque
from datetime import datetime
from llm_interface import llm_client

class MemoryTier(Enum):
    L1_FAST_REACTOR = "L1_Redis_Cache"
    L2_EPISODIC = "L2_Episodic_Log"
    L3_SEMANTIC = "L3_Vector_Store"
    L4_GRAPH = "L4_Neo4j_Graph"

class Memory:
    def __init__(self, content, role="user", embedding=None, metadata=None):
        self.internal_code = f"MEM_{str(uuid.uuid4())[:8].upper()}"
        self.content = content
        self.role = role
        self.embedding = embedding if embedding else self._mock_embedding()
        self.creation_timestamp = time.time()
        self.last_access_timestamp = self.creation_timestamp
        self.metadata = metadata if metadata else {}
        # Ensure metadata has turn info
        if "creation_turn" not in self.metadata:
            self.metadata["creation_turn"] = 0 # Default, will be overwritten by Core if used properly
        if "last_access_turn" not in self.metadata:
            self.metadata["last_access_turn"] = 0
            
        self.access_count = 1
        self.tier = MemoryTier.L2_EPISODIC
        self.half_life_score = 1.0  # Starts at 100% confidence/relevance
        self.decay_rate = 0.05      # Adjustable decay rate

    def _mock_embedding(self):
        # reliable mock embedding for demonstration
        return [random.random() for _ in range(128)]

    def update_access(self):
        self.last_access_timestamp = time.time()
        self.access_count += 1
        # Boost score on access (Anti-Decay)
        self.half_life_score = min(1.0, self.half_life_score + 0.1)

    def apply_decay(self, current_time=None):
        if current_time is None:
            current_time = time.time()
        
        # Calculate time delta in "turns" or "seconds" (using seconds for demo)
        time_delta = current_time - self.last_access_timestamp
        
        # Exponential decay formula: N(t) = N0 * e^(-lambda * t)
        # Using a simplified version for memory score
        decay_factor = math.exp(-self.decay_rate * (time_delta / 3600)) # Decays over hours in real-time, or we can speed it up
        
        # For Hackathon demo speed, let's say 1 second = 1 hour of decay
        # decay_factor = math.exp(-self.decay_rate * time_delta) 
        
        self.half_life_score *= decay_factor
        return self.half_life_score

    def to_dict(self):
        return {
            "id": self.internal_code,
            "content": self.content,
            "tier": self.tier.value,
            "score": round(self.half_life_score, 4),
            "role": self.role,
            "metadata": self.metadata
        }

class MemGraphCore:
    def __init__(self):
        # 3. Hierarchical Tiers
        self.l1_cache = {}          # O(1) Key-Value (Hash -> Memory) - Redis Simulation
        self.l2_episodic = deque(maxlen=50) # Recent context window
        self.l3_semantic = []       # List of consolidated memories (Vector Store Simulation)
        self.l4_graph = {}          # Adjacency List for Graph connections

        # 2. Decoupled Indexing
        self.keyword_index = {}     # Inverted Index: Word -> Set(IDs)
        self.vector_index = {}      # ID -> Embedding Vector
        self.entity_index = {}      # Entity -> Set(IDs)

        # "Nuclear" Configs
        self.neural_cache_hits = 0
        self.global_turn = 0

    def increment_turn(self):
        self.global_turn += 1

    def add_memory(self, content, role="user", entities=None):
        """
        Ingests a new memory, assigns code, indexes it, and places it in L2.
        """
        # Auto-increment turn on user input (or manual control)
        # For this implementation, we assume external controller calls increment_turn, 
        # OR we just use current global_turn.
        
        meta = {"creation_turn": self.global_turn, "last_access_turn": self.global_turn}
        if entities:
            meta["entities"] = entities

        mem = Memory(content, role=role, metadata=meta)
        
        # 1. Code-Addressable Logic
        print(f"[DEBUG] Created Memory: {mem.internal_code}")

        # Indexing
        self._update_indexes(mem, entities)

        # Storage Deployment (New memories go to L2 initially)
        self.l2_episodic.append(mem)
        mem.tier = MemoryTier.L2_EPISODIC
        
        # Check for L1 Promotion (Hot Memory)
        # In a real system, this would happen on frequent access. 
        # For now, let's cache immediate user preferences/identities.
        if "my name is" in content.lower() or "preference" in content.lower():
            self._promote_to_l1(mem)
        
        return mem

    def _update_indexes(self, memory, entities):
        # Keyword Index
        words = memory.content.lower().split()
        for word in words:
            if word not in self.keyword_index:
                self.keyword_index[word] = set()
            self.keyword_index[word].add(memory.internal_code)

        # Vector Index
        self.vector_index[memory.internal_code] = memory.embedding

        # Entity Index
        if entities:
            for entity in entities:
                if entity not in self.entity_index:
                    self.entity_index[entity] = set()
                self.entity_index[entity].add(memory.internal_code)
                memory.metadata['entities'] = entities

    def _promote_to_l1(self, memory):
        """Neural Prompt Caching / Fast-Reactor"""
        # key could be a hash of the content or the semantic meaning
        # For simplicity, using the content string as key mimicking "semantic hash"
        self.l1_cache[memory.content] = memory
        memory.tier = MemoryTier.L1_FAST_REACTOR
        print(f"[CACHE] Promoted {memory.internal_code} to L1 Fast-Reactor")

    def retrieve(self, query, top_k=3):
        """
        Retrieves memories using ACAN (Auxiliary Cross-Attention Network) logic simulation.
        1. Check L1 Cache (Exact match or high similarity)
        2. Search L2/L3 using Hybrid Search (Keyword + Vector)
        3. Score results
        """
        results = []
        
        # 1. L1 Fast-Reactor Check
        if query in self.l1_cache:
            self.neural_cache_hits += 1
            mem = self.l1_cache[query]
            mem.update_access()
            return [mem]

        # 2. Vector Similarity check (simulated) on L2 and L3
        # In a real app, this would be a dot product of query_emb vs all_embs
        candidates = list(self.l2_episodic) + self.l3_semantic
        
        query_vec = [random.random() for _ in range(128)] # Mock query vector
        
        scored_candidates = []
        for mem in candidates:
            # Mock Similarity Score (0.0 to 1.0)
            sim_score = random.uniform(0.1, 0.9) 
            
            # ACAN: Relevance based on Current Intent (simulated by boosting if keywords match)
            intent_boost = 1.0
            for word in query.lower().split():
                if word in mem.content.lower():
                    intent_boost += 0.5
            
            # Intelligent Pruning: Weight by Half-Life Score
            final_score = sim_score * intent_boost * mem.half_life_score
            scored_candidates.append((final_score, mem))

        # Sort and return top_k
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        results = [x[1] for x in scored_candidates[:top_k]]
        
        # Update access for retrieved memories
        for mem in results:
            mem.update_access()
            mem.metadata["last_access_turn"] = self.global_turn
            
        return results

    def run_pruning_cycle(self):
        """
        MIRAS & Half-Life Pruning
        """
        # Iterate through L2 and L3, decay scores, and remove if threshold met
        kept_memories = []
        for mem in self.l3_semantic:
            mem.apply_decay()
            if mem.half_life_score > 0.2: # Threshold
                kept_memories.append(mem)
            else:
                print(f"[PRUNING] Pruned {mem.internal_code} due to low half-life ({mem.half_life_score:.2f})")
        self.l3_semantic = kept_memories

    def consolidate_memories(self):
        """
        Goal-Oriented Chunking (HIAGENT)
        Move older L2 memories to L3, summarizing them into a "Goal" memory.
        """
        if len(self.l2_episodic) >= 5: # Threshold of 5 for demo
            # Take oldest 3 to chunk
            chunk_batch = []
            for _ in range(3):
                chunk_batch.append(self.l2_episodic.popleft())
            
            # Extract content for summarization
            chunk_texts = [m.content for m in chunk_batch]
            
            # HIAGENT: Generate Subgoal/Summary
            summary_text = llm_client.summarize_intent(chunk_texts)
            
            # Create new L3 Memory
            l3_mem = Memory(summary_text, role="system", metadata={"type": "HIAGENT_Goal", "constituent_codes": [m.internal_code for m in chunk_batch]})
            l3_mem.tier = MemoryTier.L3_SEMANTIC
            
            self._update_indexes(l3_mem, entities=[]) # Re-index the new summary
            self.l3_semantic.append(l3_mem)
            print(f"[HIAGENT] Consolidated {len(chunk_batch)} memories into L3 Goal: {l3_mem.internal_code}")

# Example Usage
if __name__ == "__main__":
    mg = MemGraphCore()
    m1 = mg.add_memory("The user's name is Priranshu.", role="user", entities=["Priranshu"])
    m2 = mg.add_memory("I like coding in Python.", role="user", entities=["Python"])
    
    print("\n-- Retrieval Test --")
    results = mg.retrieve("What is my name?")
    for m in results:
        print(f"Retrieved: {m.content} (Score: {m.half_life_score:.2f})")

