import os
import re

from dotenv import load_dotenv

import google.generativeai as genai

# =========================================
# LOAD ENV VARIABLES
# =========================================

load_dotenv()

# =========================================
# GEMINI CONFIG
# =========================================

genai.configure(

    api_key=os.getenv(
        "GEMINI_API_KEY"
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

- ONLY answer retina and diabetes related questions
- Give short and clean answers
- DO NOT use markdown symbols
- DO NOT use ** or *
- DO NOT repeatedly introduce yourself
- Speak professionally
- Use plain readable English
- Suggest doctor consultation if necessary

"""

# =========================================
# CLEAN RESPONSE
# =========================================

def clean_response(text):

    # Remove markdown symbols

    text = re.sub(r"\*\*", "", text)

    text = re.sub(r"\*", "", text)

    text = re.sub(r"#+", "", text)

    # Remove repeated intro

    text = text.replace(
        "Hello! I am RetinaAI.",
        ""
    )

    text = text.replace(
        "Hello! I am RetinaAI,",
        ""
    )

    text = text.strip()

    return text

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

        cleaned_text = clean_response(

            response.text

        )

        return cleaned_text

    except Exception as e:

        return f"""

Gemini API Error:

{str(e)}

Please try again later.

"""

# =========================================
# DYNAMIC RECOMMENDATION
# =========================================

def get_dynamic_recommendation(severity, confidence):

    prompt = f"""
    The patient's retina scan was analyzed by our AI.
    Result: {severity} Diabetic Retinopathy.
    Confidence: {confidence}%.
    
    Provide a short, professional, 2-sentence medical recommendation for the patient. 
    Do not use markdown. Do not include introductory text. 
    Act as RetinaAI.
    """
    
    try:
        response = gemini_model.generate_content(prompt)
        return clean_response(response.text)
    except Exception as e:
        return "Please consult an ophthalmologist for a thorough eye examination."