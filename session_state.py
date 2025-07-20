# session_state.py
import streamlit as st

def set_proposal_data(data):
    st.session_state['proposal_data'] = data

def get_proposal_data():
    return st.session_state.get('proposal_data', None)
