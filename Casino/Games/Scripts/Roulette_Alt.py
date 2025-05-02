from turtle import Turtle, mainloop, clear
from random import Random
import json


# === Funktionen ===

def Spinner():
    Ball.color(1, 1, 1)
    Ball.penup()
    Ball.left(-15)
    Ball.forward(280)
    Ball.left(90)


def Round():
    global e
    if e <= h:
        Ball.circle(280, 9.729729729729729729729729729729729729)
        e += 1
        Round()


def Black():
    Blackfield.begin_fill()
    Blackfield.forward(300)
    Blackfield.left(90)
    Blackfield.circle(300, 9.729729729729)
    Blackfield.left(90)
    Blackfield.forward(300)
    Blackfield.right(170.270270270)
    Blackfield.color(0, 0, 0)
    Blackfield.end_fill()


def Red():
    Redfield.begin_fill()
    Redfield.forward(300)
    Redfield.left(90)
    Redfield.circle(300, 9.729729729729)
    Redfield.left(90)
    Redfield.forward(300)
    Redfield.right(170.270270270)
    Redfield.color(1, 0, 0)
    Redfield.end_fill()


def Green():
    Redfield.begin_fill()
    Redfield.forward(300)
    Redfield.left(90)
    Redfield.circle(300, 9.729729729729)
    Redfield.left(90)
    Redfield.forward(300)
    Redfield.right(170.270270270)
    Redfield.color(0, 1, 0)
    Redfield.end_fill()
    Redfield.hideturtle()


def colormatch():
    global coins
    win = False

    if p == green_p and bet == "green":
        print("You win! (green)")
        coins += einsatz * 10
        win = True
    elif p % 2 == 0 and bet == "black":
        print("You win! (black)")
        coins += einsatz
        win = True
    elif p % 2 != 0 and bet == "red" and p != 37:
        print("You win! (red)")
        coins += einsatz
        win = True
    else:
        print("You lost.")
        coins -= einsatz

    print(f"The number was: {p}")
    print(f"Remaining coins: {coins}")

    # Coins speichern
    daten["coin"] = coins
    with open("../../Bank/Data/coin.json", "w") as f:
        json.dump(daten, f)


# === Hauptprogramm ===

# Lade Coins
with open("../../Bank/Data/coin.json", "r") as f:
    daten = json.load(f)
coins = daten["coin"]

# Turtles vorbereiten
Ball = Turtle()
Ball.speed(10)
Blackfield = Turtle()
Blackfield.speed(-1)
Redfield = Turtle()
Redfield.speed(-1)
Redfield.right(9.729729729729)

for _ in range(18):
    Black()
    Red()
Green()

# Spielschleife
while coins > 0:
    print(f"\nYou have {coins} coins.")

    # Einsatz
    while True:
        try:
            einsatz = int(input("How many coins do you want to bet? "))
            if einsatz <= 0:
                print("Bet must be more than 0.")
            elif einsatz > coins:
                print("You don't have enough coins.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    # Farbe setzen
    bet = input("Choose your color: red / black / green: ").strip().lower()
    while bet not in ["red", "black", "green"]:
        print("Invalid color.")
        bet = input("Choose red, black, or green: ").strip().lower()

    # Kugel drehen
    rand = Random()
    p = rand.randint(1, 37)
    green_p = 37
    e = 1
    h = p
    Ball.clear()
    Spinner()
    Round()
    colormatch()

    if coins <= 0:
        print("Game over – you're out of coins")
        exit()

    again = input("Do you want to play again? (yes/no): ").strip().lower()
    if again != "yes":
        print("Thanks for playing!")
        exit()
    else:
        Ball.penup()
        Ball.goto(0,0)
        Ball.setheading(0)
        Ball.pendown()

mainloop()

def random_number():

    global ball_spinning, ball_total_rotation, ball_rotation_done, final_ball_angle
    rand = random.randint(0, 36)

    final_ball_angle = (360 / (1 + rand))  # Hier speicherst du den Wert
    full_rotations = random.randint(3, 6)
    ball_total_rotation = full_rotations * 360 + final_ball_angle
    ball_rotation_done = 0
    ball_spinning = True

    print(rand)

    if rand == 0:
        print("ZERO")
    else:
        # gerade/ungerade
        if rand % 2 == 0:
            print("EVEN")
        else:
            print("ODD")

        def is_red(number):
            return number in {
                1, 3, 5, 7, 9, 12, 14, 16, 18,
                19, 21, 23, 25, 27, 30, 32, 34, 36
            }

        def is_2(number):
            return number in {
                2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35
            }

        # Schwarz/Rot
        if is_red(rand):
            print("Rot")
        else:
            print("Schwarz")

        # /2
        if rand in range(1, 18):
            print("1 to 18")
        elif rand in range(19, 36):
            print("19 to 36")

        # /3
        if rand in range(1, 12):
            print("1 to 12")
        elif rand in range(13, 24):
            print("13 to 24")
        elif rand in range(25, 36):
            print("25 to 36")

        # Rows
        if rand % 3 == 0:
            print("3rd")
        elif is_2(rand):
            print("2nd")
        else:
            print("1st")
