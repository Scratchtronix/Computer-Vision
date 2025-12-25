import cv2, face_recognition, firebase_admin, threading
from firebase_admin import credentials, firestore
import numpy as np

cap = cv2.VideoCapture(0)
known_encodings = []
known_names = []
firebase_api = "/Users/scratcherssubramaniyam/Documents/Computer-Vision-1/face-authentication-13710-firebase-adminsdk-fbsvc-6e64bec10b.json"
cred = credentials.Certificate(firebase_api)
firebase_admin.initialize_app(cred)
db = firestore.client()

def comparing():
    for hi in db.collection("users").stream():
        data = hi.to_dict()["encoding"]
        data = np.array(data)
        if face_encodings:
            match = face_recognition.compare_faces(face_encodings, data)
            print(match)

threading.Thread(target=comparing).start()
while True:
    ret, frame = cap.read()
    if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
        break
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_location = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_location)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        encoding = face_recognition.face_encodings(rgb_image)
        if encoding:
            name = input("What would you like your name to be?: ")

            for encode in encoding:
                doc_ref = db.collection("users").add({"encoding" : (list(encode)), "name" : name})
    cv2.waitKey(1)
    cv2.imshow('frame', frame)

cap.release()
cv2.destroyAllWindows()
