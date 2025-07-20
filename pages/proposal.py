import streamlit as st
from db import get_proposal_by_id

query_params = st.query_params
client = query_params.get("client", [None])[0]

st.set_page_config(page_title="Proposal Generator", layout="wide", initial_sidebar_state="collapsed")

# ------------------- STYLES -------------------
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a;
        background: #ffffff;
    }
    [data-testid="stSidebar"] { display: none; }
    .hero { text-align: center; margin-bottom: 2rem; }
    .hero img { width: auto; max-height: 150px; margin-bottom: 1rem; }
    .hero h1 { color: #003566; font-size: 2.2rem; }
    .hero p { color: #333; font-size: 1.1rem; }
    .columns, .bottom-columns {
        display: flex; gap: 2rem; margin-bottom: 2rem;
    }
    .col, .section {
        flex: 1;
        background: #f9f9f9;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .section h3 { color: #003566; }
</style>
""", unsafe_allow_html=True)

# ------------------- CLIENT VIEW MODE -------------------
if not client:
    st.error("❌ No client ID found in URL.")
    st.stop()

proposal_data = get_proposal_by_id(client)
if not proposal_data or len(proposal_data.strip()) < 20:
    st.error("⚠️ No proposal content found for this client. Please check the link.")
    st.stop()

st.image("delhidigitalco_cover.jpg", use_column_width=True)

cleaned_data = proposal_data.replace("```markdown", "").replace("```", "")
sections = cleaned_data.split("## ")
get_section = lambda key: next((s for s in sections if key in s.lower()), None)

# --- Columns: Objective & Timeline ---
st.markdown("<div class='columns'>", unsafe_allow_html=True)
objective = get_section("objective")
timeline = get_section("timeline")

if objective:
    heading, *content = objective.split("\n")
    st.markdown(f"""
        <div class='col'>
            <h3>🎯 {heading.strip()}</h3>
            <p>{' '.join(content)}</p>
        </div>
    """, unsafe_allow_html=True)

if timeline:
    heading, *content = timeline.split("\n")
    st.markdown(f"""
        <div class='col'>
            <h3>📅 {heading.strip()}</h3>
            <p>{' '.join(content)}</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- Proposal Section ---
proposal = get_section("proposal")
if proposal:
    heading, *content = proposal.split("\n")
    st.markdown(f"""
        <div class='section'>
            <h3>📝 {heading.strip()}</h3>
            <p>{' '.join(content)}</p>
        </div>
    """, unsafe_allow_html=True)

# --- Investment + Contact ---
st.markdown("<div class='bottom-columns'>", unsafe_allow_html=True)

st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("## 💸 Investment Breakdown")
data = {
    "Phase": ["Design", "Development", "Marketing"],
    "Cost ($)": [3000, 5000, 2000]
}
st.dataframe(data, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='section'>
        <h3>📞 Contact</h3>
        <p>For questions or next steps, email: <strong>contact@yourcompany.com</strong></p>
    </div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# WhatsApp Widget
st.markdown("""
<script>
  window.onload = function () {
    var wa = document.createElement("script");
    wa.src = "https://wati-integration-service.clare.ai/ShopifyWidget/shopifyWidget.js?47203";
    document.head.appendChild(wa);
  }
</script>
""", unsafe_allow_html=True)
