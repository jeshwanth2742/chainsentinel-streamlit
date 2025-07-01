import streamlit as st
import requests
import json

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="ChainSentinel - Blockchain Node Assistant",
    page_icon="🛡️",
    layout="centered"
)

# -------------------- UI Elements --------------------
st.title("🛡️ ChainSentinel")
st.subheader("Your Blockchain Sentry & Validator Node Expert")
st.markdown("---")

user_input = st.text_area(
    "Ask ChainSentinel a blockchain node question:",
    placeholder="E.g., How do I set up a Cosmos sentry node?"
)

# -------------------- Hugging Face Model --------------------
API_URL = "https://api-inference.huggingface.co/models/google/gemma-3-7b-it"

# -------------------- Inference Call on Submit --------------------
if st.button("Ask ChainSentinel"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a question before submitting.")
    else:
        with st.spinner("⏳ ChainSentinel is processing your query..."):
            headers = {
                "Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}",
                "Content-Type": "application/json"
            }

            # Prepare the prompt for generation
            full_prompt = (
                "You are ChainSentinel, an expert blockchain assistant specializing in setting up, "
                "optimizing, and monitoring sentry nodes and validator nodes across various blockchain networks. "
                "You guide users in understanding node architecture, improving uptime, optimizing sync performance, "
                "managing peer connections, and maintaining node security. Provide clear, structured, actionable guidance "
                "with Linux commands and scripts when needed. Explain complex concepts simply for learners and assist advanced users "
                "in node management.\n\n"
                f"User question: {user_input}"
            )

            payload = {
                "inputs": full_prompt
            }

            try:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=90
                )

                if response.status_code == 200:
                    data = response.json()
                    generated_text = data[0]['generated_text']
                    st.success("✅ ChainSentinel says:")
                    st.markdown(generated_text)
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("🔗 [Open ChainSentinel in a new tab](https://chainsentinel-app-xxxxx.streamlit.app)")

