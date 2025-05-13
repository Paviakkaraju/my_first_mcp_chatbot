import streamlit as st
from chatbot import generate_response
import base64

# --- Function to encode image to base64 ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- Company logo and link ---
image_base64 = get_base64_image("codework_logo.jpg")  
homepage_url = "https://codework.ai"  

# --- Display clickable logo ---
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 10px;'>
        <a href="{homepage_url}" target="_blank">
            <img src="data:image/png;base64,{image_base64}" alt="Codework Logo" style="width:200px;" />
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# --- App Title ---
st.title("CODEWORK PAL")

# --- User Input and Bot Response ---
user_input = st.text_input("You:", placeholder="Ask me anything about codework")
if user_input:
    with st.spinner("Thinking..."):
        answer = generate_response(user_input)
        st.markdown(f"**Codework Pal:** {answer}")

