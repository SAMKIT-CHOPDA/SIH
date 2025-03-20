import os
from flask import Flask, request, render_template, session, flash, redirect, url_for
from PIL import Image
from transformers import pipeline, BlipProcessor, BlipForQuestionAnswering
import wikipediaapi

app = Flask(__name__)
app.secret_key = "some_secure_secret_key"

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize BLIP model for Visual Question Answering (VQA)
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
blip_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

# Initialize question-answering model for general (non-image) questions
qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Wikipedia API setup
wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='ImageRecognitionBot/1.0')

# Helper function to classify the question type
def classify_question(question):
    image_keywords = ['color', 'wearing', 'see', 'appear', 'hold', 'visible', 'pose', 'background', 'person', 'animal', 'bird', 'creature', 'shirt', 'clothing', 'wears', 'sunglasses']
    for keyword in question.lower().split():
        if keyword in image_keywords:
            return "image"
    return "general"

# Function to retrieve Wikipedia summary for a famous person
def get_wikipedia_summary(object_name):
    try:
        page = wiki_wiki.page(object_name)
        if page.exists():
            return page.summary
        else:
            return f"No information found for {object_name} on Wikipedia."
    except Exception as e:
        print(f"Error retrieving Wikipedia content for {object_name}: {e}")
        return None

# Function to handle visual question answering (using BLIP)
def answer_image_question(question, image_path):
    image = Image.open(image_path)
    inputs = blip_processor(image, question, return_tensors="pt")
    outputs = blip_model.generate(**inputs)
    answer = blip_processor.decode(outputs[0], skip_special_tokens=True)
    return answer

# Function to handle general question answering using Wikipedia and QA model
def answer_general_question(question, famous_person=None):
    if famous_person:
        # Retrieve the Wikipedia summary for the detected famous person
        summary = get_wikipedia_summary(famous_person)
        if summary:
            # Use the question-answering model to extract a relevant answer from the Wikipedia summary
            qa_input = {"question": question, "context": summary}
            answer = qa_model(qa_input)
            return answer['answer']
    return "The question does not seem relevant to the detected objects."

# Helper function to generate the correct image URL for rendering
def get_image_url(image_path):
    # Normalize the path by replacing backslashes with forward slashes
    relative_path = os.path.relpath(image_path, "static").replace("\\", "/")
    return url_for('static', filename=relative_path)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Reset session on new image upload
        if "image" in request.files:
            file = request.files["image"]
            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            
            # Start a new session with the uploaded image
            session.clear()  # This resets everything, including chat history and context
            session["uploaded_image_path"] = filename
            session["chat_history"] = []  # Reset chat history
            session["famous_person"] = None  # Clear detected famous person
            flash("Image uploaded successfully! Ask your questions below.")
        
        # Handle question input
        if "question" in request.form:
            image_path = session.get("uploaded_image_path")
            if not image_path:
                flash("Please upload an image first.")
                return redirect(url_for("index"))

            question = request.form["question"]
            try:
                # Classify the question to determine if it's image-based or general
                question_type = classify_question(question)

                if question_type == "image":
                    # Answer image-based question using BLIP
                    answer = answer_image_question(question, image_path)
                    
                    # If the famous person is detected, store the name for follow-up questions
                    if "albert einstein" in answer.lower():
                        session["famous_person"] = "Albert Einstein"

                else:
                    # General question-answering using Wikipedia
                    famous_person = session.get("famous_person")
                    answer = answer_general_question(question, famous_person)

                # Store the question and answer in session for display
                chat_history = session.get("chat_history", [])
                chat_history.append({"question": question, "answer": answer})
                session["chat_history"] = chat_history

            except Exception as e:
                flash(f"Error analyzing the image: {e}")
                return redirect(url_for("index"))

    # Pass the correct image URL to the template
    image_url = None
    if "uploaded_image_path" in session:
        image_url = get_image_url(session["uploaded_image_path"])

    return render_template("index.html", chat_history=session.get("chat_history", []), image_url=image_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
