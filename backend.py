from flask import Flask, request, jsonify
import pdfplumber
import re
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_text(file):
    with pdfplumber.open(file) as pdf:
        return ''.join([page.extract_text() for page in pdf.pages])

def parse_resume(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'\b\d{10}\b'
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]  # Example if custom entity is defined
    return {
        "emails": emails,
        "phones": phones,
        "skills": skills
    }

@app.route('/parse', methods=['POST'])
def parse():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['resume']
    text = extract_text(file)
    parsed_data = parse_resume(text)
    return jsonify(parsed_data)

if __name__ == '__main__':
    app.run(debug=True)
