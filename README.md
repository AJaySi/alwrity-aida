# Alwrity - AI Generator for CopyWriting AIDA Formula

Alwrity is a web application built with Streamlit that utilizes OpenAI's GPT-3.5 model to generate marketing copy using the AIDA (Attention-Interest-Desire-Action) formula. This application enables users to create compelling marketing content by inputting key details about their brand and incorporating the AIDA framework to structure their copy effectively.

## AIDA Copywriting Formula

The AIDA formula is a classic and widely used approach in marketing and advertising. It stands for:

1. **Attention**: Grab the audience's attention with a catchy headline or opening statement.
2. **Interest**: Generate interest by providing compelling information or addressing pain points.
3. **Desire**: Create a sense of want or need for the product/service by emphasizing benefits.
4. **Action**: Prompt the audience to take action, such as making a purchase or signing up.

The AIDA formula guides copywriters in leading the audience through a logical sequence of steps, ultimately resulting in a desired action.

### AIDA Copywriting Formula: Simple Example

- **Headline (Attention)**: Transform Your Smile Today!
- **Body (Interest)**: "Sick of hiding your smile? Our teeth whitening kit delivers professional results at home."
- **Body (Desire)**: Imagine flashing a dazzling smile that lights up the room. With our kit, you'll have whiter teeth in just days.
- **Call to Action (Action)**: Ready for a radiant smile? Order now and start your journey to brighter, happier teeth!

## Features

- **AIDA Formula**: Utilizes the Attention-Interest-Desire-Action framework to guide users in creating persuasive marketing copy.
- **AI-Powered**: Employs OpenAI's GPT-3.5 model to generate high-quality marketing content based on user inputs.
- **User-Friendly Interface**: Offers an intuitive interface for users to input campaign details and view generated copy.
- **Retry Logic**: Implements retry logic using the Tenacity library to handle potential errors when communicating with the OpenAI API.

## How to Use

1. Clone the repository to your local machine.
2. Install the required dependencies listed in the `requirements.txt` file.
3. Set up your OpenAI API key as an environment variable named `OPENAI_API_KEY`.
4. Run the `app.py` file.

## Dependencies

- Streamlit
- OpenAI
- Streamlit Lottie
- Tenacity


## Acknowledgements

- Special thanks to OpenAI for providing access to the GPT-3.5 model.
- This project was inspired by the need for efficient and effective marketing copy generation.
