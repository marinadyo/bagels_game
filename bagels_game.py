import random
# from bagels_db import bagels_user, bagels_score
import sqlite3
from sqlite3 import Error


def create_connection(path):
    connect = None
    try:
        connect = sqlite3.connect(path)
        print('Connected to Data Base')
    except Error as e:
        print(f"The error '{e}' occurred.")
    return connect


connection = create_connection('/Users/marinade/programming/python/bagel_game/bagels_db.db')


def execute_query(connect, query):
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        connect.commit()
        # connect.close()
        print('Query executed successfully')
    except Error as e:
        print(f"The error '{e}' occurred.")


def bagels_user(name, age):
    execute_query(connection, query=f'INSERT INTO users (name, age) VALUES ("{name}", "{age}")')


def bagels_score(score):
    execute_query(connection, query=f'INSERT INTO result (score) VALUES ({score})')


num_dig = 3
max_moves = 10


def getSecretNum():
    numbers = list('0123456789')
    random.shuffle(numbers)
    secretNum = ''
    for i in range(num_dig):
        secretNum += str(numbers[i])
    return secretNum


def getClues(guess, secretNum):
    if guess == secretNum:
        return 'You got it!'

    clues = []

    for i in range(len(guess)):
        if guess[i] == secretNum[i]:
            clues.append('Fermi')
        elif guess[i] in secretNum:
            clues.append('Pico')
    if len(clues) == 0:
        return 'Bagels'
    else:
        clues.sort()
        return ' '.join(clues)


def main():
    print(f"Let's play Bagels! I am thinking of a {num_dig}-digit. You have {max_moves}-guesses.\n Clues:\n"
          f"When I say: This means:\n"
          f" Pico       One digit is correct but in the wrong position.\n"
          f" Fermi      One digit is correct in the right position.\n"
          f" Bagel      No digit is correct.\n")

    user_name = input('Please, enter your name ')
    user_age = input('Please enter your age ')
    bagels_user(user_name, user_age)

    while True:
        secretNum = getSecretNum()
        print("I've thought up a number.\n You've got {max_moves} guesses to get it.")

        num_moves = 1
        while num_moves <= max_moves:
            guess = ''
            while len(guess) != num_dig or not guess.isdecimal():
                print(f"Guess #{num_moves}")
                guess = input("> ")

            clues = getClues(guess, secretNum)
            print(clues)
            num_moves += 1

            if guess == secretNum:
                break
            if num_moves > max_moves:
                print('You ran out of guesses')
                print(f"The answer was {secretNum}.")
        print(f'You used {num_moves} moves.')
        print('Do you want to play again? (yes or no)')
        if not input('> ').lower().startswith('y'):
            break
    print('Thanks for playing')
    bagels_score(score=num_moves)


if __name__ == '__main__':
    main()
