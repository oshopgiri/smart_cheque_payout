import cv2
import face_recognition
import os
# import webbrowser

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_cheque_payout.settings')
django.setup()

from app.models import User

# Get a reference to web cam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load pictures and learn how to recognize it.
known_face_encodings = []
known_face_ids = []
base_images_file_paths = []

# Read all users from the database
for user in User.objects.all():
    if user.avatar:
        # Store path to the user's profile image
        base_images_file_paths.append('.' + user.avatar.url)
        # Store user's id
        known_face_ids.append(str(user.id))

for base_images_file_path in base_images_file_paths:
    user_image = face_recognition.load_image_file(base_images_file_path)
    user_face_encoding = face_recognition.face_encodings(user_image)[0]
    known_face_encodings.append(user_face_encoding)

face_locations = []
face_encodings = []
face_ids = []
process_this_frame = True

# while True:
# Grab a single frame of video
ret, frame = video_capture.read()

# Resize frame of video to 1/4 size for faster face recognition processing
small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

# Convert the image from BGR color-scheme (which OpenCV uses) to RGB color-scheme (which face-recognition uses)
rgb_small_frame = small_frame[:, :, ::-1]

# Only process every other frame of video to save time
if process_this_frame:
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_ids = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        id = 'Unknown'

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            id = known_face_ids[first_match_index]

        face_ids.append(id)

process_this_frame = not process_this_frame

if face_ids:
    if face_ids[0] != 'Unknown':
        # webbrowser.open('http://localhost:8000/users/view/{0}'.format(face_ids[0]))
        # break
        print(face_ids[0], end='')
    # else:
        # webbrowser.open('http://localhost:8000/users/new')
        # break

print('', end='')

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
