import streamlit as st
import requests
import json

st.set_page_config(page_title="ChainSentinel - Blockchain Node Assistant", page_icon="🛡️")

st.title("🛡️ ChainSentinel")
st.subheader("Your Blockchain Sentry & Validator Node Expert")

st.markdown("---")

user_input = st.text_area(
    "Ask ChainSentinel a blockchain node question:",
    placeholder="E.g., How do I set up a Cosmos sentry node?"
)

# ✅ Correct LLaMA 3.3 70B endpoint
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct"

if st.button("Ask ChainSentinel"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a question before submitting.")
    else:
        with st.spinner("⏳ ChainSentinel is processing your query..."):
            headers = {
                "Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}",
                "Content-Type": "application/json"
            }

            # LLaMA models use 'inputs' key with text
            payload = {
                "inputs": (
                    "You are ChainSentinel, an expert blockchain assistant specializing in setting up, "
                    "optimizing, and monitoring sentry nodes and validator nodes across various blockchain networks. "
                    "Provide clear, structured, actionable guidance with Linux commands and scripts if needed.\n\n"
                    f"User question: {user_input}"
                )
            }

            try:
                response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=120)

                if response.status_code == 200:
                    data = response.json()
                    generated_text = data[0]["generated_text"]
                    st.success("✅ ChainSentinel says:")
                    st.markdown(generated_text)
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")
