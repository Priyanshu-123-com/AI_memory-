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

# Styles - CYBER-MINIMALIST / INDUSTRIAL TECH
st.markdown("""
<style>
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #E0E0E0;
    }
    
    .stCode, .stJSON, .memory-code, .metric-value, div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Background - SOLID MATTE BLACK + SUBTLE GRID VIGNETTE */
    .stApp {
        background-color: #050505;
        /* Technical Grid Pattern */
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            radial-gradient(circle at 50% 50%, rgba(20, 20, 20, 0) 0%, rgba(5, 5, 5, 1) 90%);
        background-size: 30px 30px, 30px 30px, 100% 100%;
        background-attachment: fixed;
    }
    
    /* Hide Header/Footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* BORDERS & CARDS - SHARP, THIN, INDUSTRIAL */
    .metric-card, div[data-testid="stMetric"], .stChatInput, div[data-testid="stMarkdownContainer"] p {
        background-color: #0A0A0A;
        border: 1px solid #333;
        border-radius: 0px; /* Sharp corners */
        box-shadow: none;
    }
    
    /* Sidebar - DATA PANEL */
    section[data-testid="stSidebar"] {
        background-color: #080808;
        border-right: 1px solid #333;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: transparent;
        border-bottom: 1px solid #222;
        padding-bottom: 20px;
    }
    div[data-testid="chatAvatarIcon"] {
        background-color: #222 !important;
        border: 1px solid #444;
    }

    /* ENGINE ROOM - BENTO GRID VISUALIZATION */
    .mem-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(2, 1fr);
        gap: 0;
        border: 1px solid #333;
        margin-bottom: 20px;
        background-color: #000;
    }
    
    .mem-node {
        background: #000;
        border: 1px solid #222; /* Inner borders */
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 120px;
        position: relative;
        transition: background-color 0.1s ease;
    }
    
    .mem-node h4 {
        margin: 0;
        color: #666;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'JetBrains Mono', monospace;
        position: absolute;
        top: 10px;
        left: 10px;
    }
    
    .mem-node span {
        font-size: 1.8rem;
        color: #444;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #222;
        border-radius: 50%;
        position: absolute;
        top: 12px;
        right: 12px;
    }

    /* ACTIVE STATES - HIGH CONTRAST */
    .active-l1 { background-color: #110505; }
    .active-l1 span { color: #FF3333; text-shadow: 0 0 10px rgba(255,50,50,0.5); }
    .active-l1 .status-dot { background-color: #FF3333; box-shadow: 0 0 8px #FF3333; }
    .active-l1 h4 { color: #FF3333; }
    
    .active-l2 { background-color: #001105; }
    .active-l2 span { color: #00FF66; text-shadow: 0 0 10px rgba(0,255,100,0.5); }
    .active-l2 .status-dot { background-color: #00FF66; box-shadow: 0 0 8px #00FF66; }
    .active-l2 h4 { color: #00FF66; }
    
    .active-l3 { background-color: #050A15; }
    .active-l3 span { color: #0088FF; text-shadow: 0 0 10px rgba(0,136,255,0.5); }
    .active-l3 .status-dot { background-color: #0088FF; box-shadow: 0 0 8px #0088FF; }
    .active-l3 h4 { color: #0088FF; }
    
    .active-l4 { background-color: #0A0515; }
    .active-l4 span { color: #AA00FF; text-shadow: 0 0 10px rgba(170,0,255,0.5); }
    .active-l4 .status-dot { background-color: #AA00FF; box-shadow: 0 0 8px #AA00FF; }
    .active-l4 h4 { color: #AA00FF; }

    /* METRIC OVERRIDES */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        color: #FFF;
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #666;
        text-transform: uppercase;
    }

</style>
""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([2, 1.2])

def render_engine_room(active_tier=None):
    """Renders the visual memory nodes with animation state."""
    
    # Determined CSS classes and icons based on active_tier
    c1 = "active-l1" if active_tier == "L1_Redis_Cache" else ""
    c2 = "active-l2" if active_tier == "L2_Episodic_Log" else ""
    c3 = "active-l3" if active_tier == "L3_Vector_Store" else ""
    c4 = "active-l4" if active_tier == "L4_Graph" else ""
    
    html = f"""
    <div style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #444; margin-bottom: 5px;">SYSTEM_STATUS: ONLINE</div>
    <div class="mem-grid">
        <div class="mem-node {c1}">
            <h4>L1_CACHE</h4>
            <div class="status-dot"></div>
            <span>⚡</span>
        </div>
        <div class="mem-node {c2}">
            <h4>L2_LOG</h4>
            <div class="status-dot"></div>
            <span>📜</span>
        </div>
        <div class="mem-node {c3}">
            <h4>L3_VEC</h4>
            <div class="status-dot"></div>
            <span>🧠</span>
        </div>
        <div class="mem-node {c4}">
            <h4>L4_GRAPH</h4>
            <div class="status-dot"></div>
            <span>🕸️</span>
        </div>
    </div>
    """
    return html

# --- Right Column: Memory Inspector ---
with col2:
    st.markdown("### `ENGINE_ROOM`") # Plain markdown header for consistency
    api_key_input = st.text_input("GEMINI_API_KEY", type="password", placeholder="AIza...", label_visibility="collapsed")
    
    # Priority: Input > Secrets > None
    if api_key_input:
        llm_client.set_api_key(api_key_input)
    elif "GEMINI_API_KEY" in st.secrets:
        llm_client.set_api_key(st.secrets["GEMINI_API_KEY"])
        st.success("✅ Connected (via Secrets)")
    
    st.markdown("---")
    
    # VISUALIZATION PLACEHOLDER
    viz_placeholder = st.empty()
    # Default State
    viz_placeholder.markdown(render_engine_room(), unsafe_allow_html=True)

    st.divider()
    
    # Metrics
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Latency", f"{st.session_state.metrics['latency']:.1f}ms")
    st.markdown("---")
    
    # Metrics
    m1, m2 = st.columns(2)
    with m1:
        st.metric("LATENCY", f"{st.session_state.metrics['latency']:.1f}ms")
    with m2:
        img = "ONLINE" if st.session_state.metrics['cache_hit'] else "STANDBY"
        st.metric("NEURAL_CACHE", img)
    
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
        
        # Step A: Ingest User Memory & ANIMATE
        mem = st.session_state.memgraph.add_memory(user_input, role="user")
        
        # TRIGGER ANIMATION: Update the placeholder with the active tier
        viz_placeholder.markdown(render_engine_room(mem.tier.value), unsafe_allow_html=True)
        time.sleep(0.3) # Artificial delay to let user see the flash
        
        # Step B: Retrieve Context (ACAN)
        active_memories = st.session_state.memgraph.retrieve(user_input)
        st.session_state.last_active_memories = active_memories
        
        # Step C: Generate Response (LLM)
        response = llm_client.generate_memgraph_response(user_input, active_memories)
        
        # Step D: Store Assistant Response
        st.session_state.memgraph.add_memory(response, role="assistant")
        
        # Step E: Periodic Maintenance
        st.session_state.memgraph.run_pruning_cycle()
        st.session_state.memgraph.consolidate_memories()

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        # Update Metrics
        st.session_state.metrics["latency"] = latency_ms
        st.session_state.metrics["cache_hit"] = st.session_state.memgraph.neural_cache_hits > 0

        # Display Assistant Message
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        
    with m2:
        cache_status = "ONLINE" if st.session_state.metrics['cache_hit'] else "STANDBY"
        st.metric("NEURAL_CACHE", cache_status, delta_color="normal")
    
    st.markdown("---")
    
    # Active Memories (The "Nuclear" Output)
    st.subheader("`ACTIVE_MEMORY_INJECTION`")
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

    st.markdown("---")
    
    # Storage Stats
    st.subheader("`STORAGE_METRICS`")
    st.text(f"L1 (Cache): {len(st.session_state.memgraph.l1_cache)} items")
    st.text(f"L2 (Episodic): {len(st.session_state.memgraph.l2_episodic)} items")
    st.text(f"L3 (Semantic): {len(st.session_state.memgraph.l3_semantic)} items")
    
    if st.button("Clear Memory"):
        st.session_state.memgraph = MemGraphCore()
        st.session_state.chat_history = []
        st.session_state.last_active_memories = []
        st.rerun()
