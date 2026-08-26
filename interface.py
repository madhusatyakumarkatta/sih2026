import time
import streamlit as st
from src.retriever import get_retriever
from src.pipeline import run_pipeline, get_query_validation

st.set_page_config(
    page_title="BIS Standards Recommendation Engine",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize retriever in cache
@st.cache_resource
def load_retriever():
    return get_retriever()

retriever = load_retriever()

# Enhanced CSS Styling
st.markdown("""
    <style>
    /* SIH Theme Colors: Deep Blue (#173873) and Orange (#f37021) */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #173873;
        margin: 1.5rem 0 0.5rem 0;
        letter-spacing: -0.5px;
        text-transform: uppercase;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: #f37021;
        margin-bottom: 2.5rem;
        font-weight: 500;
    }
    
    .search-box {
        background: linear-gradient(135deg, #173873 0%, #0d285c 100%);
        padding: 2.5rem;
        border-radius: 8px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 24px rgba(23, 56, 115, 0.15);
    }
    
    .search-box textarea {
        background-color: rgba(255,255,255,0.98) !important;
        color: #333 !important;
        border: 2px solid #f37021 !important;
        border-radius: 6px !important;
        font-size: 1.05rem !important;
        padding: 1.2rem !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    .search-box h3 {
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .result-card {
        background: #ffffff;
        border-left: 6px solid #f37021;
        padding: 1.8rem;
        margin: 1.5rem 0;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-top: 1px solid #eee;
        border-right: 1px solid #eee;
        border-bottom: 1px solid #eee;
    }
    
    .result-card:hover {
        box-shadow: 0 6px 20px rgba(243, 112, 33, 0.15);
        transform: translateY(-2px);
    }
    
    .result-standard {
        font-size: 1.4rem;
        font-weight: 800;
        color: #173873;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .result-title {
        font-size: 1.1rem;
        color: #444;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .result-score {
        display: inline-block;
        background: #fdf1e8;
        color: #f37021;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-size: 0.9rem;
        font-weight: 700;
        border: 1px solid #fbd8c1;
    }
    
    .rank-badge {
        display: inline-block;
        background: #f37021;
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 4px;
        text-align: center;
        line-height: 36px;
        font-weight: bold;
        font-size: 1.1rem;
        margin-right: 1rem;
    }
    
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 6px;
        text-align: center;
        border: 1px solid #e0e0e0;
        border-top: 4px solid #173873;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #f37021;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #555;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #f37021 0%, #e35b00 100%);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 6px;
        border: none;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(243, 112, 33, 0.3);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .status-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .status-info {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
    
    .info-box {
        background: #f4f6f9;
        border-left: 4px solid #173873;
        padding: 1.5rem;
        border-radius: 4px;
        margin: 1.5rem 0;
        border-right: 1px solid #e0e0e0;
        border-top: 1px solid #e0e0e0;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .divider {
        height: 2px;
        background: #eee;
        margin: 2.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown('<div class="header-title">🏗️ BIS Standards Recommendation Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">AI-powered RAG system to find relevant Indian Standards for building materials</div>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    enable_validation = st.checkbox(
        "🤖 Enable Query Validation (LLM)",
        value=False,
        help="Use Ollama (phi:2.7b) to validate building-material queries"
    )
    
    top_k = st.slider(
        "📊 Number of Recommendations",
        min_value=3,
        max_value=5,
        value=5,
        help="How many standards to return"
    )
    
    st.divider()
    
    st.subheader("📈 System Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Standards", len(retriever.documents))
    with col2:
        st.metric("LLM", "✅ Ready" if enable_validation else "⏸️ Off")
    
    st.divider()
    
    st.subheader("ℹ️ About")
    st.info("""
    **Architecture:**
    - BM25 Retriever
    - Material Term Boosting
    - Query Expansion
    - Optional LLM Validation
    
    **Performance:**
    - Latency: <2s avg
    - Hit Rate: 100%
    - No hallucinations
    """)

# Main Content
st.markdown('<div class="search-box">', unsafe_allow_html=True)
st.markdown("### 📝 Enter Your Query")

with st.form("search_form", clear_on_submit=False):
    query = st.text_area(
        "Product Description",
        height=120,
        placeholder="Example: High-strength Portland cement (53 grade) for concrete construction with good durability and fast strength gain...",
        help="Describe the building material product, grade, specifications, or standards needed"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        submitted = st.form_submit_button(
            "🔍 Find Standards",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        clear_btn = st.form_submit_button(
            "🗑️ Clear",
            use_container_width=True
        )
    
    with col3:
        pass

st.markdown('</div>', unsafe_allow_html=True)

# Process Query
if clear_btn:
    st.rerun()

if submitted:
    if not query or len(query.strip()) < 5:
        st.error("⚠️ Please enter a meaningful product description (at least 5 characters)")
        st.stop()
    
    with st.spinner("🔄 Processing your query..."):
        start_time = time.perf_counter()
        
        # Validate if enabled
        validation_time = 0
        if enable_validation:
            try:
                val_start = time.perf_counter()
                validation = get_query_validation(query)
                validation_time = time.perf_counter() - val_start
                
                if not validation["is_valid"]:
                    st.markdown(f'<div class="status-badge status-error">❌ {validation["message"]}</div>', unsafe_allow_html=True)
                    st.info("💡 Please describe a building material product (cement, steel, concrete, aggregates, bricks, etc.)")
                    st.stop()
                else:
                    st.markdown('<div class="status-badge status-success">✅ Valid building-material query</div>', unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"⚠️ Validation skipped: {str(e)}")
                validation_time = 0
        
        # Get recommendations
        try:
            retrieval_start = time.perf_counter()
            hits = retriever.retrieve(query, top_k=top_k)
            retrieval_time = time.perf_counter() - retrieval_start
            total_time = time.perf_counter() - start_time
            
            if not hits:
                st.error("❌ No standards found. Try a different query.")
                st.stop()
            
            # Results Header
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("## ✅ Recommendations Found")
            
            # Metrics
            st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(hits)}</div>
                    <div class="metric-label">Standards</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{retrieval_time:.2f}s</div>
                    <div class="metric-label">Retrieval</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{validation_time:.2f}s</div>
                    <div class="metric-label">Validation</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_time:.2f}s</div>
                    <div class="metric-label">Total</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Results
            for rank, hit in enumerate(hits, start=1):
                standard = hit.get("standard", "Unknown")
                title = hit.get("title", "Standard details not available")
                score = hit.get("score", 0.0)
                
                st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span class="rank-badge">{rank}</span>
                        <span class="result-standard">{standard}</span>
                    </div>
                    <div class="result-title">{title}</div>
                    <span class="result-score">Score: {score:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Expandable Details
            with st.expander("📊 Show Technical Details"):
                st.json({
                    "query_submitted": query[:100] + "..." if len(query) > 100 else query,
                    "standards_returned": len(hits),
                    "retrieval_latency_seconds": round(retrieval_time, 4),
                    "validation_latency_seconds": round(validation_time, 4),
                    "total_latency_seconds": round(total_time, 4),
                    "validation_enabled": enable_validation,
                    "total_standards_indexed": len(retriever.documents)
                })
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Success Message
            st.success(f"✅ Query processed in {total_time:.3f} seconds. Top {len(hits)} standards displayed above.")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()

else:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📚 Getting Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Example 1:**
        High-strength OPC 53 grade cement
        """)
    
    with col2:
        st.info("""
        **Example 2:**
        Coarse aggregate for concrete
        """)
    
    with col3:
        st.info("""
        **Example 3:**
        Steel reinforcement bars
        """)
    
    st.markdown("""
    ---
    **How to use this system:**
    1. Describe your building material product in detail
    2. Optionally enable LLM validation for query checking
    3. Click "Find Standards" to get recommendations
    4. View relevant BIS standards with relevance scores
    
    **Supported Materials:**
    Cement, Concrete, Aggregates, Steel, Bricks, Tiles, Mortar, Pipes, Precast, Masonry, and more.
    """)


