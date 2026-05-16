# import os
# import random
# from urllib import response

# from flask import (
#     Flask,
#     render_template,
#     request,
#     jsonify
# )

# from werkzeug.utils import secure_filename

# from dotenv import load_dotenv

# import google.generativeai as genai

# # =========================================
# # LOAD ENV VARIABLES
# # =========================================

# load_dotenv()

# GEMINI_API_KEY = os.getenv(
#     "GEMINI_API_KEY"
# )

# # =========================================
# # GEMINI CONFIGURATION
# # =========================================

# genai.configure(
#     api_key=GEMINI_API_KEY
# )

# # gemini_model = genai.GenerativeModel(
# #     "gemini-1.5-flash"
# # )
# gemini_model = genai.GenerativeModel(
#     "gemini-1.5-pro"
# )

# # =========================================
# # FLASK APP
# # =========================================

# app = Flask(__name__)

# UPLOAD_FOLDER = "static/uploads"

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# os.makedirs(
#     UPLOAD_FOLDER,
#     exist_ok=True
# )

# # =========================================
# # MOCK DATA
# # =========================================

# severity_levels = [

#     "No DR",
#     "Mild",
#     "Moderate",
#     "Severe",
#     "Proliferative DR"

# ]

# recommendations = {

#     "No DR":
#     "Maintain healthy blood sugar and regular retina checkups.",

#     "Mild":
#     "Schedule regular retina screening and monitor glucose levels carefully.",

#     "Moderate":
#     "Consult ophthalmologist for advanced retinal monitoring and treatment.",

#     "Severe":
#     "Immediate retinal specialist consultation recommended.",

#     "Proliferative DR":
#     "Urgent treatment required to avoid permanent vision loss."

# }

# # =========================================
# # HOME PAGE
# # =========================================

# @app.route("/")
# def home():

#     return render_template(
#         "index.html"
#     )

# # =========================================
# # PREDICTION PAGE
# # =========================================

# @app.route(
#     "/predict",
#     methods=["POST"]
# )

# def predict():

#     file = request.files["image"]

#     if file:

#         filename = secure_filename(
#             file.filename
#         )

#         filepath = os.path.join(
#             app.config["UPLOAD_FOLDER"],
#             filename
#         )

#         file.save(filepath)

#         # MOCK RESULT

#         prediction = random.choice(
#             severity_levels
#         )

#         confidence = round(
#             random.uniform(85, 99),
#             2
#         )

#         recommendation = recommendations[
#             prediction
#         ]

#         return render_template(

#             "result.html",

#             image_path=filepath,

#             prediction=prediction,

#             confidence=confidence,

#             recommendation=recommendation

#         )

# # =========================================
# # CHATBOT PAGE
# # =========================================

# @app.route("/chatbot")
# def chatbot():

#     return render_template(
#         "chatbot.html"
#     )

# # =========================================
# # GEMINI CHAT API
# # =========================================

# @app.route(
#     "/chat",
#     methods=["POST"]
# )

# def chat():

#     data = request.json

#     user_message = data.get(
#         "message"
#     )

#     SYSTEM_PROMPT = """

#     You are RetinaAI,
#     an advanced diabetic retinopathy
#     medical assistant.

#     Rules:

#     - Only discuss diabetic retinopathy
#     - Give concise professional answers
#     - Suggest doctor consultation
#     - Avoid unrelated topics
#     - Be accurate and medical

#     """

#     final_prompt = (
#         SYSTEM_PROMPT +
#         "\nUser: " +
#         user_message
#     )

#     try:

#         # response = gemini_model.generate_content(
#         #     final_prompt
#         # )
#         from services.chatbot_service import (
#             get_chatbot_response
#         )

#         reply = get_chatbot_response(
#             user_message
#         )

#         return jsonify({

#             "response":
#             response.text

#         })

#     except Exception as e:

#         return jsonify({

#             "response":
#             str(e)

#         })

# # =========================================
# # RUN SERVER
# # =========================================

# if __name__ == "__main__":

#     app.run(
#         debug=True
#     )


import os
import random

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from werkzeug.utils import secure_filename

from dotenv import load_dotenv

# =========================================
# LOAD ENV VARIABLES
# =========================================

load_dotenv()

# =========================================
# FLASK APP
# =========================================

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# =========================================
# MOCK DATA
# =========================================

severity_levels = [

    "No DR",
    "Mild",
    "Moderate",
    "Severe",
    "Proliferative DR"

]

recommendations = {

    "No DR":
    "Maintain healthy blood sugar and regular retina checkups.",

    "Mild":
    "Schedule regular retina screening and monitor glucose levels carefully.",

    "Moderate":
    "Consult ophthalmologist for advanced retinal monitoring and treatment.",

    "Severe":
    "Immediate retinal specialist consultation recommended.",

    "Proliferative DR":
    "Urgent treatment required to avoid permanent vision loss."

}

# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

# =========================================
# PREDICTION PAGE
# =========================================

@app.route(
    "/predict",
    methods=["POST"]
)

def predict():

    file = request.files["image"]

    if file:

        filename = secure_filename(
            file.filename
        )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        prediction = random.choice(
            severity_levels
        )

        confidence = round(
            random.uniform(85, 99),
            2
        )

        recommendation = recommendations[
            prediction
        ]

        return render_template(

            "result.html",

            image_path=filepath,

            prediction=prediction,

            confidence=confidence,

            recommendation=recommendation

        )

# =========================================
# CHATBOT PAGE
# =========================================

@app.route("/chatbot")
def chatbot():

    return render_template(
        "chatbot.html"
    )

# =========================================
# GEMINI CHAT API
# =========================================

@app.route(
    "/chat",
    methods=["POST"]
)

def chat():

    from services.chatbot_service import (
        get_chatbot_response
    )

    try:

        data = request.json

        user_message = data.get(
            "message"
        )

        reply = get_chatbot_response(
            user_message
        )

        return jsonify({

            "response": reply

        })

    except Exception as e:

        return jsonify({

            "response": str(e)

        })

# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )