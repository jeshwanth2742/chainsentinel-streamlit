# app.py for ChainSentinel on Streamlit

import streamlit as st
import requests
import json

st.set_page_config(page_title="ChainSentinel - Blockchain Node Assistant", page_icon="🛡️", layout="centered")
st.title("🛡️ ChainSentinel")
st.subheader("Your Blockchain Sentry & Validator Node Expert")

st.markdown("---")

# Input area
user_input = st.text_area("Ask ChainSentinel a blockchain node question:", placeholder="E.g., How do I set up a Cosmos sentry node?")

if st.button("Ask ChainSentinel"):
    if user_input.strip() == "":
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("ChainSentinel is processing your query..."):
            headers = {
                "Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}",
                "Content-Type": "application/json"
            }

            payload = {
                "inputs": user_input
            }

            response = requests.post(
                "https://api-inference.huggingface.co/chat/completions",
                headers=headers,
                data=json.dumps({
                    "model": "mistralai/Mistral-Small-3.1-24B-Instruct-2503",
                    "messages": [
                        {"role": "system", "content": "You are ChainSentinel, an expert blockchain assistant specializing in setting up, optimizing, and monitoring sentry nodes and validator nodes across various blockchain networks. You guide users in understanding blockchain node architecture, improving node uptime, optimizing sync performance, managing peer connections, and maintaining node security. You provide clear, structured, and actionable guidance with Linux commands and scripts as needed, and explain complex concepts simply for learners while also supporting advanced users in node management."},
                        {"role": "user", "content": user_input}
                    ]
                })
            )

            if response.status_code == 200:
                data = response.json()
                message = data['choices'][0]['message']['content']
                st.success("ChainSentinel says:")
                st.markdown(message)
            else:
                st.error(f"Error {response.status_code}: {response.text}")
