import streamlit as st
from rag_app import ask_rag

st.title("🏦 Bank of Maharashtra Loan Assistant")

question = st.text_input("Ask any loan-related question...")

if st.button("Search"):
    st.write("⏳ Retrieving information...")
    answer, sources = ask_rag(question)

    st.success(answer)

    with st.expander("📄 Sources Used"):
        for i, src in enumerate(sources):
            st.write(f"**Source {i+1}:** {src}")
            st.write("---")
