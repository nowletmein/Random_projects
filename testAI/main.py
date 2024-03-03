import random
import time
import cv2
import cvzone
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

# Initialize game variables
timer = 0
stateResults = False
gameActive = False  # Initialize gameActive here
winner = ""  # Initialize the winner
roundStartTime = 0  # Initialize the round start time


# Rock, Paper, Scissors logic
def play_rps(hand_detector, myAI):
    global stateResults, winner, roundStartTime


    if hands:

        hand = hands[0]
        playerMove = None
        fingers = hand_detector.fingersUp(hand)
        print(fingers)

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
        reward = calculate_reward(playerMove, myAI)
        update_q_value(playerMove, reward, myAI)


        myAI = choose_action(myAI)
        stateResults = True
        winner = ""  # Reset the winner for the new round

        print(f"AI Move: {myAI}")
        print("Updated Q-table:", Q)

        # Determine the winner
        winner = determine_winner(playerMove, myAI)
        if fingers == [1, 0, 1, 0, 0]:
            winner = "A kurva anyád"

    timer = 0
    # Display the winner




def choose_action(myAI):
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


def update_q_value(action, reward, myAI):
    if (action, myAI) not in Q:
        Q[(action, myAI)] = 0
    max_next_q = max(Q.get((a, myAI), 0) for a in actions)
    Q[(action, myAI)] += learning_rate * (reward + discount_factor * max_next_q - Q[(action, myAI)])


def determine_winner(playerMove, myAI):
    if playerMove == myAI:
        return "Tie"
    elif (playerMove == "rock" and myAI == "scissors") or \
            (playerMove == "paper" and myAI == "rock") or \
            (playerMove == "scissors" and myAI == "paper"):
        return "Player"
    else:
        return "AI"


# Main loop
myAI = random.choice(actions)  # Initialize AI's move
while True:
    success, img = cap.read()

    # Find hands
    hands, img = detector.findHands(img)
    key = cv2.waitKey(1)
      # Check if 'a' is pressed and the game is not active
    if key == ord('a'):
        winner = None
        play_rps(detector, myAI)
        roundStartTime = time.time()

    if winner:
        if winner == "A kurva anyád":
            cv2.putText(img, f"{winner}", (100, 200), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 255), 4)
        else:
            cv2.putText(img, f"Winner: {winner}", (70, 140), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 4)

    cv2.imshow("image", img)

    if key == 27:  # Press 'Esc' key to exit the program
        break

cap.release()
cv2.destroyAllWindows()