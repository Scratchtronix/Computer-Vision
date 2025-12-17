import time
import mediapipe as mp
import cv2, sys
import random
import threading

cap = cv2.VideoCapture(0)
hands = mp.solutions.hands
hand = hands.Hands()
rps = ["rock", "paper", "scissors"]
countdown_done = threading.Event()
players_pick, players_score = "", 0
computers_pick, computers_score = "", 0

def intro():
    global computers_pick
    time.sleep(2)
    computers_pick = rps[random.randint(0, 2)]
    print("Okay! On the count of 3, please keep your option ready!")
    time.sleep(2)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    countdown_done.set()

def compare(computer, player):
    global players_score, computers_score
    try:
        if computer == player:
            print(f"It's a tie! The Player picked {player} and the Computer picked {computer}")
        elif computer == "rock" and player == "paper" or computer == "paper" and player == "scissors" or computer == "scissors" and player == "rock":
            print(f"Player picked {player} and computer picked {computer}. Player won!")
            players_score += 1
        elif computer == "rock" and player == "scissors" or computer == "paper" and player == "rock" or computer == "scissors" and player == "paper":
            computers_score += 1
            print(f"Player picked {player} and computer picked {computer}. Computer won!")
        else:
            print("You haven't played anything. Please play a choose a proper option next time.")
        countdown_done.clear()
        play_again = int(input("Would you like to play again?(type 1 to continue or 0 to stop the game): "))
        if bool(play_again):
            threading.Thread(target=intro).start()
            threading.Thread(target=compare_thread).start()
        elif not bool(play_again):
            sys.exit(0)
        else:
            print("Please enter a correct value")
    except ValueError:
        print("Please enter a correct value")
    

def compare_thread():
    countdown_done.wait()
    print("Comparing...")
    compare(computers_pick, players_pick)

threading.Thread(target=intro).start()
threading.Thread(target=compare_thread).start()

while True:
    ret, frame = cap.read()
    (h, w, c) = frame.shape
    if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
        sys.exit(0)
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(rgb_image)
    # print(countdown_done.is_set())
    if results.multi_hand_landmarks:
        for landmark in results.multi_hand_landmarks:
            index_tip_x, index_tip_y, index_bottom_x, index_bottom_y = (landmark.landmark[8].x * w, landmark.landmark[8].y * h, landmark.landmark[5].x * w, landmark.landmark[5].y * h)
            thumb_tip_x, thumb_tip_y, thumb_bottom_x, thumb_bottom_y = (landmark.landmark[4].x * w, landmark.landmark[4].y * h, landmark.landmark[1].x * w, landmark.landmark[1].y * h)
            middle_tip_x, middle_tip_y, middle_bottom_x, middle_bottom_y = (landmark.landmark[12].x * w, landmark.landmark[12].y * h, landmark.landmark[9].x * w, landmark.landmark[9].y * h)
            ring_tip_x, ring_tip_y, ring_bottom_x, ring_bottom_y = (landmark.landmark[16].x * w, landmark.landmark[16].y * h, landmark.landmark[13].x * w, landmark.landmark[13].y * h)
            little_tip_x, little_tip_y, little_bottom_x, little_bottom_y = (landmark.landmark[20].x * w, landmark.landmark[20].y * h, landmark.landmark[17].x * w, landmark.landmark[17].y * h)

            if index_tip_y < index_bottom_y and middle_tip_y < middle_bottom_y and ring_tip_y < ring_bottom_y and little_tip_y < little_bottom_y and thumb_tip_x > thumb_bottom_x:
                cv2.putText(frame, "paper", (850, 650), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3)
                players_pick = "paper"
            elif index_tip_y < index_bottom_y and middle_tip_y < middle_bottom_y and ring_tip_y > ring_bottom_y and little_tip_y > little_bottom_y and thumb_tip_x < thumb_bottom_x:
                cv2.putText(frame, "scissors", (850, 650), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3)
                players_pick = "scissors"
            elif index_tip_y > index_bottom_y and middle_tip_y > middle_bottom_y and ring_tip_y > ring_bottom_y and little_tip_y > little_bottom_y and thumb_tip_x < thumb_bottom_x:
                cv2.putText(frame, "rock", (850, 650), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 3)
                players_pick = "rock"
            else:
                players_pick = ""

    cv2.putText(frame, f"Player Score: {players_score}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(frame, f"Computer Score: {computers_score}", (800, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow("frame", frame)


cap.release()
cv2.destroyAllWindows()
