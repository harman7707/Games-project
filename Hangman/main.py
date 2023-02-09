import random
from words import words
import string
# print(words)

def get_valid_word(words):
    word= random.choice(words)
    while "-" in word or " " in word:
        word=random.choice(words)

    return upper.word


def hangman():
    words= get_valid_word(words)
    word_letter = set(words)
    alphabet= set(string.ascii_uppercase)
    used_letters = set() #what user has guessed

    #getting user input
    while len(word_letter) >0:
        #letters used
        # " ".join ["a" , "b", "cd"]--> "a b cd"
        print("you have used these letters: ", "".join(used_letters))
        user_letter = input("guess the letter: ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letter:
                word_letter.remove(user_letter)

        elif user_letter in used_letters:
            print("already guessed please try again: ")

        else:
            print("invalid please try again: ")    

user_input = input("Type the words: ")

print(user_input)
