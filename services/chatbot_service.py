import os

from dotenv import load_dotenv

import google.generativeai as genai

# =========================================
# LOAD ENV VARIABLES
# =========================================

load_dotenv()

# =========================================
# GEMINI CONFIGURATION
# =========================================

genai.configure(

    api_key=os.getenv(
        "AIzaSyB1kB0nuJBeTYKBf2myap0Unsqk7-WoBew"
    )

)

# =========================================
# GEMINI MODEL
# =========================================

gemini_model = genai.GenerativeModel(

    "gemini-3-flash-preview"

)

# =========================================
# SYSTEM PROMPT
# =========================================

SYSTEM_PROMPT = """

You are RetinaAI,
a professional diabetic retinopathy
medical assistant.

Rules:

- Only discuss retina disease
- Give concise medical answers
- Suggest doctor consultation
- Avoid unrelated topics
- Be friendly and professional

"""

# =========================================
# CHATBOT FUNCTION
# =========================================

def get_chatbot_response(user_message):

    try:

        final_prompt = (

            SYSTEM_PROMPT +

            "\nUser: " +

            user_message

        )

        response = gemini_model.generate_content(

            final_prompt

        )

        return response.text

    except Exception as e:

        return f"""

Gemini API Error:

{str(e)}

Possible Reasons:
- Free quota exceeded
- Invalid API key
- Internet issue
- Too many requests

Please try again later.

"""