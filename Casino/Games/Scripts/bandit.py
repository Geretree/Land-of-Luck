from random import randint
from turtle import *
import json

with open("../../Bank/Data/coin.json", "r") as f:
    daten = json.load(f)

coins = daten["coin"]


def start():  # Start the game and set coins
    global coins
    print(f"You have {coins} Coins")
    bet = int(input("How many coins do you want to bet?"))
    if bet <= 0:
        print("You need coins to play")
        return False
    elif bet > coins:
        print("That is not the amount of coins you are able to use")
        return False
    else:
        coins -= bet
        print("Okay, let's go")
        return True


turtle1 = Turtle()
turtle2 = Turtle()
turtle3 = Turtle()
turtle4 = Turtle()
turtle5 = Turtle()

turtle1.hideturtle()
turtle2.hideturtle()
turtle3.hideturtle()
turtle4.hideturtle()
turtle5.hideturtle()

turtle1.penup()
turtle2.penup()
turtle3.penup()
turtle4.penup()
turtle5.penup()

turtle1.goto(-300, 0)
turtle2.goto(-150, 0)
turtle3.goto(0, 0)
turtle4.goto(150, 0)
turtle5.goto(300, 0)

def random_integer():
    global  x, y, z, w,v
    x = randint(3, 7)
    y = randint(3, 7)
    z = randint(3, 7)
    w = randint(3, 7)
    v = randint(3, 7)



def Ecken(): #Um in Turtle die Formen zu zeichnen
    lange = 300 / x
    for i in range(x):
        turtle1.pendown()
        turtle1.forward(lange)
        turtle1.right(-360 / x)


    lange = 300 / y
    for i in range(y):
        turtle2.pendown()
        turtle2.forward(lange)
        turtle2.right(-360 / y)


    lange = 300 / z
    for i in range(z):
        turtle3.pendown()
        turtle3.forward(lange)
        turtle3.right(-360 / z)


    lange = 300 / w
    for i in range(w):
        turtle4.pendown()
        turtle4.forward(lange)
        turtle4.right(-360 / w)


    lange = 300 / v
    for i in range(v):
        turtle5.pendown()
        turtle5.forward(lange)
        turtle5.right(-360 / v)


def printer():  # Recognizes which shapes match and refunds accordingly
    global coins
    rueckerstattung = sum([x == y, x == z, x == w, x == v, y == z, y == w, y == v, z == w, z == v, w == v])

    if rueckerstattung == 5:
        print("Jackpot! All shapes match!")
        coins += coins * 34  # Five times the bet back
    elif rueckerstattung == 4:
        print("You get your bet back.")
        coins += coins * 1  # 1 times the bet back
    elif rueckerstattung == 3:
        print("You get 75% of your bet back.")
        coins += coins * 0.75
    elif rueckerstattung == 1:
        print("Try again!!")

    # Update the JSON file with the new coin count
    daten["coin"] = coins
    with open("../../Bank/Data/coin.json", "w") as f:
        json.dump(daten, f)




def play_again(): #Frage ob weitergespielt wird
    while True:
        antwort = input("Do you wannt to play again [yes/no]")
        if antwort== "yes":
            all_again()
            if coins >0:
                exit()
        elif antwort== "no":
            print("Thanks for Playing")
            exit()
        else:
            print("You have an invalid Input please enter yes or no to the question if you want to keep playing")


def all_again(): #Um spiel wieder zu starten
    global coins
    while coins > 0:
        turtle1.clear()
        turtle2.clear()
        turtle3.clear()
        turtle4.clear()
        turtle5.clear()
        if not start():
            continue

        random_integer()
        Ecken()
        printer()

        if not play_again():
            break
    print("Game over, You cant play anymore")
all_again()
mainloop()
