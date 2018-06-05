# DON'T CHANGE ANYTHING IN THIS FILE!!

from random import *
MAX_ATTEMPTS = 5

# Set up instructions to be sent to client
INSTRUCTIONS = """\nThis is hangman. You will guess one letter at a time. If the letter is in
the hidden word, the "-" will be replaced by the correct letter. Guessing multiple letters at
a time will be considered as guessing the entire word (which will result in either a win
or loss automatically - win if correct, loss if incorrect). You win if you either guess all of
the correct letters or guess the word correctly. You lose if you run out of attempts. Attempts
will be decremented in the case of an incorrect or repeated letter guess.\n\n"""


def open_file():
  fp = open("words.txt")
  fp_list = fp.read().split('\n')
  fp.close()
  return fp_list


def checkGuessCh(word, word_blanks, guess):
  for i, ch in enumerate(word):
    if guess == ch and word_blanks[i] == "-":
      word_blanks = word_blanks[:i] + ch + word_blanks[i+1:]

  return word_blanks


def checkGuessWord(word, guess):
  if word == guess:
    return 1
  return 0


def gameSetup(args):
  if args[1] == '-r':
    # get random word
    fp_list = open_file()
    word = sample(fp_list, 1)[0]
    while len(word) == 1:
      word = sample(fp_list, 1)
  else:
    word = args[1]

  word_blanks = "-"*len(word)
  attempts = MAX_ATTEMPTS
  win = False

  return word, word_blanks, attempts, win


def checkGuess(word, word_blanks, attempts, guess, win):
    # Whole word? Win or lose
    if len(guess) > 1:
      print("Guess was more than 1 char - win/lose only")
      win = checkGuessWord(word, guess)
      print("Win status: {}".format(win))
      return word_blanks, attempts, win
      #break

    # Otherwise check letter and update word_blanks
    word_blanks_check = checkGuessCh(word, word_blanks, guess)
    if word_blanks_check == word_blanks:
      # wrong letter
      print("Incorrectly or already guessed char")
      attempts -= 1
      print("Attempts left: {}".format(attempts))

    else:
      print("Correctly guessed char")
      # correct letter
      word_blanks = word_blanks_check
      print("Attempts left: {}".format(attempts))

    if word == word_blanks:
      print("Correctly guessed word")
      win = True

    print("Win status: {}".format(win))

    return word_blanks, attempts, win
