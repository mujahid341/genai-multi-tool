import streamlit as st
from utils import detect_intent, log_event, save_output
from prompts import build_prompt
import google.generativeai as genai
import google.api_core.exceptions

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# App UI
st.set_page_config(page_title="Gemini Assistant", page_icon="")
st.title("Gemini All-in-One Assistant")

query = st.text_area("Ask anything (code, translate, text, summarize...)")

col1, col2 = st.columns(2)
mode_override = col1.selectbox("Force mode (optional)", ["Auto", "Code", "Text", "Translate", "Summarize"])
lang_output = col2.selectbox("Output Language", ["English", "Hindi", "Spanish", "French", "Auto"])

if st.button("Generate"):
    if not query.strip():
        st.warning("Please enter a prompt.")
    else:
        try:
            intent = detect_intent(query, mode_override)
            prompt = build_prompt(query, intent, lang_output)

            with st.spinner("Generating..."):
                response = model.generate_content(prompt)
                result = response.text

            # Show result
            st.subheader("Output:")
            if intent == "code":
                st.code(result, language="python")
            else:
                st.write(result)

            # Download
            save_output(result)
            st.download_button("Download Result", result, file_name="gemini_output.txt")

            log_event(query, intent, lang_output)

        except google.api_core.exceptions.ResourceExhausted:
            st.error("Daily quota exceeded. Try again tomorrow.")
        except Exception as e:
            st.error("Error occurred.")
            log_event(query, "error", lang_output, error=str(e))
