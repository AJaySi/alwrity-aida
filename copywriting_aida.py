import time #Iwish
import os
import json
import openai
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity Copywriting",
        layout="wide",
    )
    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f"""
      <style>
      [class="st-emotion-cache-7ym5gk ef3psqc12"]{{
            display: inline-block;
            padding: 5px 20px;
            background-color: #4681f4;
            color: #FBFFFF;
            width: 300px;
            height: 35px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border-radius: 8px;’
      }}
      </style>
    """
    , unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    # Title and description
    st.title("✍️ Alwrity - AI Generator for CopyWriting AIDA Formula")
    
    # Input section
    with st.expander("**PRO-TIP** - Campaign's Key features and benefits to build **Interest & Desire**", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            aida_brand_about = st.text_input('**Enter Brand/Person/Company Name**')
        with col2:
            aida_brand_details = st.text_input(f'**Describe What {aida_brand_about} Does ?** (In 5-6 words)')

        aida_interest = st.text_input(f'**Provide *Attention* grabbing details of {aida_brand_about} campaign ?** (Grab the audiences attention with a catchy headline or opening statement. Create a sense of want or need for the product/service by emphasizing benefits.)')
        aida_target_audience = st.text_input(f"**Enter {aida_brand_about} Target Audience:** (Example: Wellness, Yoga, IT professionals, Senior Citizen, Adventure seekers, GenZ etc)")

        aida_cta = st.text_input(f"**Call To Action (CTA):** Prompt {aida_brand_about} audience to take action, such as Buy now, Register, Know more etc")

        col1, col2, space, col3 = st.columns([5, 5, 0.5, 5])
        with col1:
            aida_platform = st.selectbox('Copywriting Type:', ('Social media copy', 'Email copy', 
                    'Website copy', 'Ad copy', 'Product copy'), index=0)
        with col2:
            aida_url = st.text_input(f'**Landing Page URL**: Provide {aida_brand_about} web url to use (Optional).')
        with col3:
            aida_language = st.selectbox('Choose Language', ('English', 'Hindustani',
                'Chinese', 'Hindi', 'Spanish'), index=0)

        # Generate Blog FAQ button
        if st.button('**Get AIDA Copy**'):
            # Validate input fields
            if validate_input(aida_brand_about, "Brand/Person/Company Name") and \
                validate_input(aida_brand_details, "Description") and \
                validate_input(aida_interest, "Attention grabbing details") and \
                validate_input(aida_target_audience, "Target Audience") and \
                validate_input(aida_cta, "Call to Action"):

                # Proceed with further processing
                with st.spinner("You have been patient, wait a little longer for AIDA Magic.."):
                    aida_content = generate_aida_copywrite(aida_brand_about, aida_brand_details,
                            aida_interest, aida_target_audience, aida_cta, aida_url, aida_language)
                    if aida_content:
                        st.subheader('**👩🔬👩🔬 Your Human Sounding Content**')
                        st.markdown(aida_content)
                    else:
                        st.error("💥**Failed to AIDA your Content. Please try again!**")



# Function to validate if the input field is not empty
def validate_input(input_text, field_name):
    if not input_text:
        st.error(f"{field_name} is required!")
        return False
    return True


# Function to generate blog metadesc
def generate_aida_copywrite(aida_brand_about, aida_brand_details,
                            aida_interest, aida_target_audience, aida_cta, aida_url, aida_language):
    """ Function to call upon LLM to get the work done. """

    prompt = f"""As an Expert AIDA copywriter, I need your help in creating a marketing campaign for {aida_brand_about}, 
        which is a {aida_brand_details}, targeting {aida_target_audience}. Your task is to incorporate the AIDA framework,
        by providing a headline or hook to grab attention, key features and benefits to build interest and desire, 
        and a call-to-action for {aida_cta}.
        """
    if aida_url and aida_language:
        prompt = f"""As an Expert AIDA copywriter, I need your help in creating a marketing campaign for {aida_brand_about},
            which is a {aida_brand_details}, targeting {aida_target_audience}. Your task is to incorporate the AIDA framework,
            by providing a headline or hook to grab attention, key features and benefits to build interest and desire,
            and a call-to-action for {aida_cta}.
            Include {aida_url} in CTA. Your response should be in {aida_language} language.
            """
    # Exception Handling.
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        api_key (str): Your Google Generative AI API key.
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None



if __name__ == "__main__":
    main()
