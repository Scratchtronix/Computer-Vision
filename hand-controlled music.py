import pygame
import mediapipe as mp
import os, time, math, cv2

pygame.mixer.init()
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hand = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
files = "/Users/scratcherssubramaniyam/Documents/Computer-Vision-1/sample-songs"
songs = []
for song in os.listdir(files):
    songs.append(f"{files}/{song}")
ind = 0
print(len(songs))
def next_song():
    global ind
    ind+=1
    print(f"Playing {songs[ind]}")
    pygame.mixer.music.load(songs[ind])
    pygame.mixer.music.play()

pygame.mixer.music.load(songs[ind])
pygame.mixer.music.play()
if not pygame.mixer.music.get_busy():
    next_song()
    time.sleep(5)

while True:
    ret, frame = cap.read()
    if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
        break
    h, w, c = frame.shape
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(rgb_image)
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            thumb1_x, thumb1_y = hand_landmark.landmark[4].x * w, hand_landmark.landmark[4].y * h
            index1_x, index1_y = hand_landmark.landmark[6].x * w, hand_landmark.landmark[6].y * h
            thumb2_x, thumb2_y = hand_landmark.landmark[2].x * w, hand_landmark.landmark[2].y * h
            index2_x, index2_y = hand_landmark.landmark[8].x * w, hand_landmark.landmark[8].y * h
            middle1_x, middle1_y = hand_landmark.landmark[12].x * w, hand_landmark.landmark[12].y * h
            middle2_x, middle2_y = hand_landmark.landmark[10].x * w, hand_landmark.landmark[10].y * h
            pinky1_x, pinky1_y = hand_landmark.landmark[16].x * w, hand_landmark.landmark[16].y * h
            pinky2_x, pinky2_y = hand_landmark.landmark[14].x * w, hand_landmark.landmark[14].y * h
            ring1_x, ring1_y = hand_landmark.landmark[20].x * w, hand_landmark.landmark[20].y * h
            ring2_x, ring2_y = hand_landmark.landmark[18].x * w, hand_landmark.landmark[18].y * h
            try:
                if math.dist((thumb1_x, thumb1_y), (thumb2_x, thumb2_y)) > 205 and thumb1_y < thumb2_y and index1_x > index2_x and middle1_x < middle2_x and ring1_x < ring2_x and pinky1_x < pinky2_x:
                    next_song()
                    time.sleep(5)
                if thumb1_y > thumb2_y and index1_x < index2_x and middle1_x < middle2_x and ring1_x < ring2_x and pinky1_x < pinky2_x:
                    print("Moving to previous song.")
                    ind -= 1
                    pygame.mixer.music.load(songs[ind])
                    pygame.mixer.music.play()
                    print(f"Playing {songs[ind]}")
                    time.sleep(5)
                elif index1_x > index2_x and middle1_x < middle2_x and ring1_x < ring2_x and pinky1_x < pinky2_x and thumb1_x > thumb2_x:
                    print("Paused")
                    pygame.mixer.music.pause()
                elif thumb1_x > thumb2_x and index1_y > index2_y and middle1_y < middle2_y and ring1_y < ring2_y and pinky1_y < pinky2_y:
                    print("Unpaused")
                    pygame.mixer.music.unpause()
            except IndexError:
                ind = 0
                pygame.mixer.music.load(songs[ind])
                pygame.mixer.music.play()

    cv2.imshow('frame', frame)

cap.release()
cv2.destroyAllWindows()
