import streamlit as st
import requests
import uuid
from db import save_proposal, get_proposal_by_id
from urllib.parse import unquote

st.set_page_config(page_title="Proposal Generator", layout="wide", initial_sidebar_state="collapsed")

query_params = st.query_params
client_id = query_params.get("client", [None])[0]

# ----------------- UI Style -----------------
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a;
        background: #ffffff;
    }
    .hero { text-align: center; margin-bottom: 2rem; }
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
    [data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ----------------- CLIENT MODE -----------------
if client_id:
    from bson import ObjectId
    proposal_data = get_proposal_by_id(str(client_id))
    if not proposal_data:
        st.error("⚠️ No proposal found for this client.")
        st.stop()

    st.image("delhidigitalco_cover.jpg", use_column_width=True)

    markdown = proposal_data.replace("```markdown", "").replace("```", "")
    sections = markdown.split("## ")
    get_section = lambda key: next((s for s in sections if key in s.lower()), None)

    # Objective + Timeline
    st.markdown("<div class='columns'>", unsafe_allow_html=True)
    for label, icon in [("objective", "🎯"), ("timeline", "📅")]:
        section = get_section(label)
        if section:
            heading, *content = section.split("\n")
            st.markdown(f"""
                <div class='col'>
                    <h3>{icon} {heading.strip()}</h3>
                    <p>{' '.join(content)}</p>
                </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Proposal Section
    proposal = get_section("proposal")
    if proposal:
        heading, *content = proposal.split("\n")
        st.markdown(f"""
            <div class='section'>
                <h3>📝 {heading.strip()}</h3>
                <p>{' '.join(content)}</p>
            </div>
        """, unsafe_allow_html=True)

    # Investment + Contact
    st.markdown("<div class='bottom-columns'>", unsafe_allow_html=True)
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("## 💸 Investment Breakdown")
    st.dataframe({"Phase": ["Design", "Development", "Marketing"], "Cost ($)": [3000, 5000, 2000]}, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='section'>
            <h3>📞 Contact</h3>
            <p>Email: <strong>contact@yourcompany.com</strong></p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ----------------- ADMIN FORM -----------------
st.title("📄 Internal Proposal Generator")
st.markdown("Use the form below to generate a new client proposal with a shareable link.")

client_name = st.text_input("Client Name")
user_prompt = st.text_area("Enter the project or service details:")
domain = st.text_input("Domain (e.g., Web Dev, Branding, etc.):", value="Web Development")

def fetch_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "Apikey": "Api-Key Ixgvb348.9g9qdwzROoygMc3r2KAE3rljhEec2vNH"
    }
    data = {
        "payload": prompt,
        "env": "dev"
    }
    try:
        res = requests.post("https://payload.vextapp.com/hook/TZ9Z7POAYP/catch/$(10)", headers=headers, json=data)
        res.raise_for_status()
        return res.json().get("text", "No output")
    except Exception as e:
        return f"Error: {e}"

if st.button("Generate Proposal"):
    if client_name.strip() and user_prompt.strip():
        prompt = f"""
You are a business consultant. Based on the following input, generate a detailed, structured proposal in markdown format with these headings:

## Executive Summary  
## Objectives  
## Solution Overview  
## Timeline  
## Investment  
## Contact  

Domain: {domain}

Input:
{user_prompt}
"""
        result = fetch_response(prompt)
        proposal_id = save_proposal(result, client_name, domain)
        share_url = f"https://your-streamlit-app-url.streamlit.app/?client={proposal_id}"
        st.success("✅ Proposal generated!")
        st.markdown(f"🔗 [Share this proposal]({share_url})")
    else:
        st.error("Please fill in all fields.")
