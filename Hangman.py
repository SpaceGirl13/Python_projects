# import required module
import random
with open("Random_Words.txt", "r") as file:
	allText = file.read()
	words = list(map(str, allText.split()))
def new_word():
# Open the file in read mode
    # print random string
	print(random.choice(words))
#Display message on screen
print("Hello, welcome to Hangman. Guess the word. ")
new_word()



