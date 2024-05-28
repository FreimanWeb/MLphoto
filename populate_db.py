import os
import face_recognition
from app import db, Photo

# Ensure app is imported after db to avoid circular imports
from app import app

photos_dir = 'static/uploads/initial_photos/'

# Create the initial_photos directory if it does not exist
if not os.path.exists(photos_dir):
    os.makedirs(photos_dir)

# Add initial photos to the database
for filename in os.listdir(photos_dir):
    file_path = os.path.join(photos_dir, filename)
    image = face_recognition.load_image_file(file_path)
    encodings = face_recognition.face_encodings(image)

    if encodings:  # Ensure at least one face encoding is found
        encoding = encodings[0]
        new_photo = Photo(file_path=file_path, encoding=encoding)
        db.session.add(new_photo)

db.session.commit()
print("Database populated with initial photos.")
