import streamlit as st
import time
import json
import pandas as pd
from memgraph_core import MemGraphCore
from llm_interface import llm_client

# Page Config
st.set_page_config(layout="wide", page_title="MemGraph: Nuclear Memory Architecture")

# Initialize Session State
if "memgraph" not in st.session_state:
    st.session_state.memgraph = MemGraphCore()
    # Seed with some initial data for demo
    st.session_state.memgraph.add_memory("My name is Priranshu.", role="user", entities=["Priranshu"])
    st.session_state.memgraph.add_memory("I am participating in an IIT Guwahati Hackathon.", role="user", entities=["IIT Guwahati", "Hackathon"])
    st.session_state.memgraph.add_memory("I need a memory system that scales to 1,000 turns.", role="user", entities=["Memory System"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_active_memories" not in st.session_state:
    st.session_state.last_active_memories = []

if "metrics" not in st.session_state:
    st.session_state.metrics = {"latency": 0, "cache_hit": False}

# Styles
st.markdown("""
<style>
    .stTextArea textarea { font-size: 16px; }
    .metric-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        margin-bottom: 10px;
    }
    .memory-code {
        font-family: 'Courier New', monospace;
        color: #00FF7F;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([2, 1])

# --- Left Column: Chat Interface ---
with col1:
    st.title("🧠 MemGraph Core")
    st.caption("Real-Time Long-Form Memory System | L1-L4 Hierarchy | ACAN Retrieval")

    # Display Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    user_input = st.chat_input("Enter your message/query...")

    if user_input:
        # 1. Display User Message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # 2. Process with MemGraph
        start_time = time.time()
        st.session_state.memgraph.increment_turn()
        current_turn = st.session_state.memgraph.global_turn
        
        # Step A: Ingest User Memory
        st.session_state.memgraph.add_memory(user_input, role="user")
        
        # Step B: Retrieve Context (ACAN)
        active_memories = st.session_state.memgraph.retrieve(user_input)
        st.session_state.last_active_memories = active_memories
        
        # Step C: Generate Response (LLM)
        response = llm_client.generate_memgraph_response(user_input, active_memories)
        
        # Step D: Store Assistant Response
        st.session_state.memgraph.add_memory(response, role="assistant")
        
        # Step E: Periodic Maintenance (Pruning + Chunking)
        st.session_state.memgraph.run_pruning_cycle()
        st.session_state.memgraph.consolidate_memories()

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        # Update Metrics
        st.session_state.metrics["latency"] = latency_ms
        # Basic check if L1 was hit (mock logic from core)
        st.session_state.metrics["cache_hit"] = st.session_state.memgraph.neural_cache_hits > 0 # This is a cumulative counter in mock, effectively shows activity

        # Display Assistant Message
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Force rerun to update sidebar
        st.rerun()

# --- Right Column: Memory Inspector ---
with col2:
    st.header("⚙️ Engine Room")
    
    # Metrics
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Latency", f"{st.session_state.metrics['latency']:.1f}ms")
    with m2:
        cache_status = "ACTIVE" if st.session_state.metrics['cache_hit'] else "IDLE"
        st.metric("L1 Cache", cache_status, delta_color="normal")
    
    st.divider()
    
    # Active Memories (The "Nuclear" Output)
    st.subheader("🔋 Active Memory Injection")
    if st.session_state.last_active_memories:
        memory_data = []
        for mem in st.session_state.last_active_memories:
            memory_data.append({
                "ID": mem.internal_code,
                "Tier": mem.tier.value,
                "Score": f"{mem.half_life_score:.2f}",
                "Origin": mem.metadata.get("creation_turn", "N/A"),
                "Last Used": mem.metadata.get("last_access_turn", "N/A")
            })
        
        st.table(pd.DataFrame(memory_data))
        
        st.caption("Detailed Dump:")
        st.json([m.to_dict() for m in st.session_state.last_active_memories])
    else:
        st.info("No active memories injected for this turn.")

    st.divider()
    
    # Storage Stats
    st.subheader("💾 Storage Stats")
    st.text(f"L1 (Cache): {len(st.session_state.memgraph.l1_cache)} items")
    st.text(f"L2 (Episodic): {len(st.session_state.memgraph.l2_episodic)} items")
    st.text(f"L3 (Semantic): {len(st.session_state.memgraph.l3_semantic)} items")
    
    if st.button("Clear Memory"):
        st.session_state.memgraph = MemGraphCore()
        st.session_state.chat_history = []
        st.session_state.last_active_memories = []
        st.rerun()
