import os
import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Create a directory for storing patient images if it doesn't exist
IMAGE_UPLOAD_FOLDER = 'uploads'
if not os.path.exists(IMAGE_UPLOAD_FOLDER):
    os.makedirs(IMAGE_UPLOAD_FOLDER)

def photo_quality_accessor(left_image, right_image):
    # Simulate enhancing photo quality
    print(f"Enhancing quality for images: {left_image}, {right_image}")
    enhanced_left = f"enhanced_{left_image}"
    enhanced_right = f"enhanced_{right_image}"
    return enhanced_left, enhanced_right

def cancer_risk_prediction(left_image, right_image, gender):
    # Simulate risk calculation for cancer
    print(f"Calculating cancer risk for images: {left_image}, {right_image} with gender: {gender}")
    return "Risk percentage for Cancer: 60%"


def diabetes_risk_prediction(left_image, right_image):
    # Simulate risk calculation for diabetes
    print(f"Calculating diabetes risk for images: {left_image}, {right_image}")
    return "Risk percentage for Diabetes: 40%"


def results_output(risk):
    # Output results
    print(f"Final risk assessment: {risk}")
    return risk

def choosing_disease(disease, gender=None):
    # Log disease choice and gender
    print(f"Disease chosen: {disease}, Gender: {gender}")
    return disease, gender

def generate_unique_id():
    # Generate a unique ID using UUID
    return str(uuid.uuid4())

def save_images(patient_id, left_eye, right_eye):
    # Create a directory for the patient using their unique ID
    patient_folder = os.path.join(IMAGE_UPLOAD_FOLDER, patient_id)
    if not os.path.exists(patient_folder):
        os.makedirs(patient_folder)

    # Save the images in the patient's folder
    left_image_path = os.path.join(patient_folder, left_eye.filename)
    right_image_path = os.path.join(patient_folder, right_eye.filename)
    left_eye.save(left_image_path)
    right_eye.save(right_image_path)

    return left_image_path, right_image_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle patient name and generate a unique ID
        patient_name = request.form['patient_name']
        patient_id = generate_unique_id()

        # Store the patient ID and redirect to the upload page
        return redirect(url_for('upload', patient_id=patient_id))
    return render_template('index.html')


@app.route('/upload/<patient_id>', methods=['GET', 'POST'])
def upload(patient_id):
    if request.method == 'POST':
        # Handle image upload and form data
        left_eye = request.files['left_eye']
        right_eye = request.files['right_eye']
        disease = request.form['disease_choice']
        gender = request.form.get('gender')  # This might be None if not provided

        # Save the images using the patient ID as folder name
        uploaded_left, uploaded_right = save_images(patient_id, left_eye, right_eye)

        enhanced_left, enhanced_right = photo_quality_accessor(uploaded_left, uploaded_right)
        choosing_disease(disease, gender)

        if disease == 'Cancer':
            risk = cancer_risk_prediction(enhanced_left, enhanced_right, gender)
        elif disease == 'Diabetes':
            risk = diabetes_risk_prediction(enhanced_left, enhanced_right)

        results_output(risk)

        return redirect(url_for('results', risk=risk))
    return render_template('upload.html', patient_id=patient_id)


@app.route('/results')
def results():
    risk = request.args.get('risk', type=str)
    return render_template('results.html', risk=risk)


if __name__ == '__main__':
    app.run(debug=True)
