# main.py

import streamlit as st
import requests
from db import save_proposal

st.set_page_config(page_title="Generate Proposal", layout="centered")

# ---------------- Model Config ----------------
MODEL_ENDPOINTS = {
    "GPT 4o mini": "https://payload.vextapp.com/hook/TZ9Z7POAYP/catch/$(10)"
}

API_KEYS = {
    "GPT 4o mini": "Api-Key Ixgvb348.9g9qdwzROoygMc3r2KAE3rljhEec2vNH"
}

def fetch_response(prompt, model):
    headers = {
        "Content-Type": "application/json",
        "Apikey": API_KEYS[model]
    }
    data = {
        "payload": prompt,
        "env": "dev"
    }
    try:
        res = requests.post(MODEL_ENDPOINTS[model], headers=headers, json=data)
        res.raise_for_status()
        return res.json().get("text", "No output")
    except Exception as e:
        return f"Error: {e}"

# ---------------- UI ----------------
st.title("📄 Internal Proposal Generator")
st.markdown("Fill out the form to generate a client-ready proposal with a shareable link.")

client_name = st.text_input("Client Name")
user_prompt = st.text_area("Enter the project or service details:")
domain = st.text_input("Domain (e.g., Web Dev, Branding, etc.):", value="Web Development")

if st.button("Generate Proposal"):
    if user_prompt.strip() and client_name.strip():
        full_prompt = f"""
You are a business consultant. Based on the following input, generate a detailed, structured proposal in markdown format with the following section headings only:

## Executive Summary  
## Objectives  
## Solution Overview  
## Timeline  
## Investment  
## Contact  

Use the following domain: {domain}

Input:
{user_prompt}
"""
        # Fetch proposal from model
        response = fetch_response(full_prompt, "GPT 4o mini")

        # Save to MongoDB
        proposal_id = save_proposal(response, client_name, domain)

        # Shareable link
        base_url = "https://proposalgenerator-4p6ov7seqdthssanhz7jln.streamlit.app"
        share_url = f"{base_url}/proposal?client={proposal_id}"

        st.success("✅ Proposal generated and saved!")
        st.markdown(f"🔗 [Click to view/share proposal]({share_url})")
    else:
        st.error("Please enter all required fields.")
