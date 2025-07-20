import streamlit as st
import os

# --- Get query parameter ---
query_params = st.experimental_get_query_params()
client = query_params.get("client", [None])[0]

st.set_page_config(page_title="Proposal Generator", layout="wide", initial_sidebar_state="collapsed")

# --- Proposal save/load helpers ---
def save_client_proposal(client_id, content):
    os.makedirs("proposals", exist_ok=True)
    with open(f"proposals/{client_id}.txt", "w", encoding="utf-8") as f:
        f.write(content)

def load_client_proposal(client_id):
    path = f"proposals/{client_id}.txt"
    if client_id and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# ------------------- STYLES -------------------
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a;
        background: #ffffff;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .hero {
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero img {
        width: auto;
        max-height: 150px;
        margin-bottom: 1rem;
    }
    .hero h1 {
        color: #003566;
        font-size: 2.2rem;
    }
    .hero p {
        color: #333;
        font-size: 1.1rem;
    }

    .columns, .bottom-columns {
        display: flex;
        gap: 2rem;
        margin-bottom: 2rem;
    }

    .col, .section {
        flex: 1;
        background: #f9f9f9;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .section h3 {
        color: #003566;
    }
</style>
""", unsafe_allow_html=True)

# ------------------- ADMIN FORM (if no ?client= param) -------------------
if not client:
    st.image("delhidigitalco_logo.jpg", use_column_width=True)
    st.title("📄 Generate New Proposal")
    client_id = st.text_input("Client ID (used in shareable link):")
    proposal_text = st.text_area("Proposal content:", height=400)
    if st.button("Save Proposal"):
        if client_id and proposal_text.strip():
            save_client_proposal(client_id, proposal_text)
            st.success(f"✅ Saved! Share this link: `?client={client_id}`")
        else:
            st.error("Please provide both Client ID and Proposal text.")
    st.stop()

# ------------------- CLIENT VIEW MODE -------------------
proposal_data = load_client_proposal(client)
if not proposal_data or len(proposal_data.strip()) < 20:
    st.error("⚠️ No proposal content found for this client. Please check the link.")
    st.stop()

st.image("delhidigitalco_cover.jpg", use_column_width=True)

# st.markdown("""
# # <div class="hero">
# #     <h1>🚀 Client Proposal</h1>
# #     <p>Your customized business proposal, crafted for clarity and impact.</p>
# # </div>
# """, unsafe_allow_html=True)

# Cleanup
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

# Investment Table
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("## 💸 Investment Breakdown")
data = {
    "Phase": ["Design", "Development", "Marketing"],
    "Cost ($)": [3000, 5000, 2000]
}
st.dataframe(data, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Contact
st.markdown("""
    <div class='section'>
        <h3>📞 Contact</h3>
        <p>For questions or next steps, email: <strong>contact@yourcompany.com</strong></p>
    </div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# WhatsApp
st.markdown("""
<script>
  window.onload = function () {
    var wa = document.createElement("script");
    wa.src = "https://wati-integration-service.clare.ai/ShopifyWidget/shopifyWidget.js?47203";
    document.head.appendChild(wa);
  }
</script>
""", unsafe_allow_html=True)
