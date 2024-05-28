from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import face_recognition
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['DATABASE_FOLDER'] = 'static/database_images/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        matches = find_face_matches(filepath)
        return render_template('results.html', matches=matches)
    return redirect(request.url)


def find_face_matches(uploaded_image_path):
    uploaded_image = face_recognition.load_image_file(uploaded_image_path)
    uploaded_face_encodings = face_recognition.face_encodings(uploaded_image)

    if len(uploaded_face_encodings) == 0:
        return []

    uploaded_face_encoding = uploaded_face_encodings[0]

    matches = []
    for image_name in os.listdir(app.config['DATABASE_FOLDER']):
        image_path = os.path.join(app.config['DATABASE_FOLDER'], image_name)
        database_image = face_recognition.load_image_file(image_path)
        database_face_encodings = face_recognition.face_encodings(database_image)

        if len(database_face_encodings) > 0:
            database_face_encoding = database_face_encodings[0]
            result = face_recognition.compare_faces([uploaded_face_encoding], database_face_encoding)
            if result[0]:
                matches.append(image_name)

    return matches


if __name__ == '__main__':
    app.run(debug=True)
