import time
from memgraph_core import MemGraphCore, MemoryTier

def test_memgraph_core():
    print("Initializing MemGraph Core...")
    mg = MemGraphCore()
    
    # 1. Test Ingestion
    print("\n[Test 1] Memory Ingestion and Indexing")
    m1 = mg.add_memory("My name is Priranshu.", entities=["Priranshu"])
    assert m1.internal_code in mg.keyword_index["name"]
    assert m1.internal_code in mg.entity_index["Priranshu"]
    print("✅ Ingestion & Indexing passed.")

    # 2. Test Retrieval (ACAN)
    print("\n[Test 2] ACAN Retrieval")
    results = mg.retrieve("What is my name?")
    assert len(results) > 0
    assert results[0].internal_code == m1.internal_code
    print(f"✅ Retrieved: {results[0].content}")

    # 3. Test Neural Caching (L1)
    print("\n[Test 3] Neural Prompt Caching")
    # Add a preference which should auto-promote to L1
    m2 = mg.add_memory("I prefer coding in Python.", entities=["Python"])
    # Check if it was promoted (logic in add_memory promotes if "preference" in text)
    if m2.tier == MemoryTier.L1_FAST_REACTOR:
        print("✅ Immediate promotion to L1 worked.")
    else:
        print(f"ℹ️ Memory in {m2.tier}, checking retrieval promotion...")
        
    # Retrieve it multiple times to verify cache hits
    mg.retrieve("I prefer coding in Python.")
    mg.retrieve("I prefer coding in Python.")
    if mg.neural_cache_hits > 0:
        print(f"✅ Cache Hits recorded: {mg.neural_cache_hits}")
    else:
        print("❌ No cache hits recorded.")

    # 4. Test HIAGENT Chunking
    print("\n[Test 4] HIAGENT Chunking")
    # Fill L2 to trigger consolidation (Threshold is 5)
    for i in range(5):
        mg.add_memory(f"Turn {i} interaction details.")
    
    mg.consolidate_memories()
    
    # Check if L3 has the summary
    if len(mg.l3_semantic) > 0:
        goal_mem = mg.l3_semantic[-1]
        print(f"✅ L3 Summary Created: {goal_mem.content}")
        assert "HIAGENT_Goal" in goal_mem.metadata.get("type", "")
    else:
        print("❌ HIAGENT consolidation failed or threshold not met.")

    # 5. Test Pruning
    print("\n[Test 5] MIRAS Pruning")
    # Manually decay a memory
    m1.half_life_score = 0.1
    mg.l3_semantic.append(m1) # Move m1 to L3 to be eligible for pruning loop
    mg.run_pruning_cycle()
    
    # m1 should be removed from l3_semantic (or handled)
    # Note: run_pruning_cycle iterates l3_semantic.
    if m1 not in mg.l3_semantic:
        print("✅ Memory successfully pruned.")
    else:
        print(f"❌ Memory not pruned. Score: {m1.half_life_score}")

if __name__ == "__main__":
    test_memgraph_core()
