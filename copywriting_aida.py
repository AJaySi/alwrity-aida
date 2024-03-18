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
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
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

    # Sidebar input for OpenAI API Key
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown(f"🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")
    
    # Title and description
    st.title("✍️ Alwrity - AI Generator for CopyWriting AIDA Formula")
    with st.expander("What is **Copywriting AIDA formula** & **Howto Use**? 📝❗"):
        st.markdown('''
           ### What's AIDA copywriting Formula, Howto use this AI generator 🗣️
    ---
    #### AIDA Copywriting Formula

    AIDA is a classic and widely used copywriting formula in marketing and advertising. It stands for:

    1. **Attention**: Grab the audience's attention with a catchy headline or opening statement.
    2. **Interest**: Generate interest by providing compelling information or addressing pain points.
    3. **Desire**: Create a sense of want or need for the product/service by emphasizing benefits.
    4. **Action**: Prompt the audience to take action, such as making a purchase or signing up.

    The AIDA formula guides copywriters in structuring their content to lead the audience through a logical sequence of steps, 
    ultimately resulting in a desired action.

    #### AIDA Copywriting Formula: Simple Example

    **Headline (Attention):**  Transform Your Smile Today!
    **Body (Interest):** "Sick of hiding your smile? Our teeth whitening kit delivers professional results at home.
    **Body (Desire):** Imagine flashing a dazzling smile that lights up the room. With our kit, you'll have whiter teeth in just days.
    **Call to Action (Action):** Ready for a radiant smile? Order now and start your journey to brighter, happier teeth!
    --- ''')
    
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

    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")
    st.markdown('''
                Copywrite using AIDA formula - powered by AI (OpenAI, Gemini Pro).
                Implemented by [Alwrity](https://alwrity.netlify.app).
                Know more: [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know)
                ''')


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
    copywrite_aida = openai_chatgpt(prompt)
    return copywrite_aida


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", temperature=0.2, max_tokens=4096, top_p=0.9, n=1):
    """
    Wrapper function for OpenAI's ChatGPT completion.

    Args:
        prompt (str): The input text to generate completion for.
        model (str, optional): Model to be used for the completion. Defaults to "gpt-4-1106-preview".
        temperature (float, optional): Controls randomness. Lower values make responses more deterministic. Defaults to 0.2.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 8192.
        top_p (float, optional): Controls diversity. Defaults to 0.9.
        n (int, optional): Number of completions to generate. Defaults to 1.

    Returns:
        str: The generated text completion.

    Raises:
        SystemExit: If an API error, connection error, or rate limit error occurs.
    """
    # Wait for 10 seconds to comply with rate limits
    for _ in range(10):
        time.sleep(1)

    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
            # Additional parameters can be included here
        )
        return response.choices[0].message.content

    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"OpenAI error: {err}")



# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url


if __name__ == "__main__":
    main()
