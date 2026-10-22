
import streamlit as st
from groq import Groq
import os

st.set_page_config(
    page_title="RIO - AI Biology Tutor",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 RIO - AI Biology Tutor")
st.caption("Your personal AI Biology Teacher | Class 10")

st.write(
    "Enter any Biology topic and RIO will explain it "
    "with definitions, examples, diagrams and practice questions."
)

language = st.selectbox(
    "Choose your answer language",
    ["English + Roman Urdu", "English", "Roman Urdu"]
)

topic = st.text_input(
    "Enter your Biology topic",
    placeholder="e.g. Cell, Photosynthesis, Human Heart"
)

if st.button("Generate Explanation"):
    if not topic.strip():
        st.warning("Please enter a Biology topic first.")
    else:
        api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

        if not api_key:
            st.error("Groq API key is missing. Please configure it in app secrets.")
        else:
            try:
                client = Groq(api_key=api_key)

                prompt = f"""
                You are RIO, a friendly Class 10 Biology tutor.

                Explain this Biology topic: {topic}
                Answer language: {language}

                Include:
                1. Topic name
                2. Clear definition
                3. Detailed explanation in easy words
                4. Daily-life examples
                5. A simple labelled text diagram where suitable
                6. Important points
                7. Five practice questions with answers

                Keep the information scientifically accurate
                and suitable for a Class 10 student.
                If using English + Roman Urdu, provide both.
                """

                with st.spinner("RIO is preparing your lesson..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are RIO, an expert Biology teacher."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.5,
                        max_tokens=3500
                    )

                st.markdown("---")
                st.subheader(f"📘 Topic: {topic}")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
