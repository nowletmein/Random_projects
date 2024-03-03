import random
import time
import cv2
import cvzone
from tensorflow.keras.models import Sequential
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = HandDetector(maxHands=1)

# Q-learning initialization
Q = {}  # Q-table
actions = ['rock', 'paper', 'scissors']
learning_rate = 0.1
discount_factor = 0.9
exploration_prob = 0.3


# Rock, Paper, Scissors logic
def play_rps(hand_detector):
    global stateResults

    if stateResults is False:
        timer = time.time() - initialTime
        cv2.putText(img, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 0), 4)
        if timer > 3:
            print("timer up")
            if hands:
                print("hand detected")
                hand = hands[0]
                playerMove = None
                fingers = hand_detector.fingersUp(hand)
                if fingers == [0, 0, 0, 0, 0]:
                    playerMove = "rock"
                if fingers == [1, 1, 1, 1, 1]:
                    playerMove = "paper"
                if fingers == [0, 1, 1, 0, 0]:
                    playerMove = "scissors"

                if playerMove == None:
                    print("nincs lépés")
                else:
                    print(playerMove)

                # Q-learning update
                if stateResults:
                    reward = calculate_reward(playerMove, myAI)
                    update_q_value(playerMove, reward)

                options = ['rock', 'paper', 'scissors']
                myAI = choose_action()
                stateResults = True
                print("lefutott")

                print(f"AI Move: {myAI}")
                print("Updated Q-table:", Q)


def choose_action():
    if random.uniform(0, 1) < exploration_prob:
        return random.choice(actions)  # Explore
    else:
        return max(actions, key=lambda a: Q.get((a, myAI), 1.0))  # Exploit


def calculate_reward(playerMove, myAI):
    if playerMove == myAI:
        return 0
    elif (playerMove == "rock" and myAI == "scissors") or \
            (playerMove == "paper" and myAI == "rock") or \
            (playerMove == "scissors" and myAI == "paper"):
        return 1
    else:
        return -1


def update_q_value(action, reward):
    if (action, myAI) not in Q:
        Q[(action, myAI)] = 0
    max_next_q = max(Q.get((a, myAI), 0) for a in actions)
    Q[(action, myAI)] += learning_rate * (reward + discount_factor * max_next_q - Q[(action, myAI)])


# Main loop
while True:
    success, img = cap.read()

    # Find hands
    hands, img = detector.findHands(img)

    if startGame:
        play_rps(detector)

    cv2.imshow("image", img)
    cv2.waitKey(1)

    key = cv2.waitKey(1)
    if key == ord('a'):
        startGame = True
        initialTime = time.time()
    stateResults = False