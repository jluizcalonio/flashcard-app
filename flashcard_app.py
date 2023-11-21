from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
random_word = {}

# -- ADDING DATA -- #
try:
    data_file = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data_file = pandas.read_csv("./data/german_words.csv")
except pandas.errors.EmptyDataError:
    data_file = pandas.read_csv("./data/german_words.csv")
data_dict = data_file.to_dict(orient="records")

def next_card():
    global random_word, timer
    window.after_cancel(timer)
    canvas.itemconfig(current_card_face, image=card_front_img)
    print(len(data_dict))
    if len(data_dict) > 0:
        random_word = choice(data_dict)
        canvas.itemconfig(language_text, text="Alemão", fill="Black")
        canvas.itemconfig(word_text, text=random_word["Alemão"], fill="Black")
        timer = window.after(3000, func=flip_card)
    else:
        canvas.itemconfig(language_text, text="Parabéns!", fill="Black")
        canvas.itemconfig(word_text, text="Você memorizou todas as palavras!", fill="Black", font=("Arial", 32, "bold"))

def flip_card():
    canvas.itemconfig(current_card_face, image=card_back_img)
    canvas.itemconfig(language_text, text="Português", fill="White")
    canvas.itemconfig(word_text, text=random_word["Português"], fill="White")

def remove_card():
    global random_word
    data_dict.remove(random_word)
    data_dict_df = pandas.DataFrame(data_dict)
    data_dict_df.to_csv("./data/words_to_learn.csv", index=False)

    next_card()

# -- ADDING DATA -- #


# -- UI -- #
# Window
window = Tk()
window.title("Tongues & Cards")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
timer = window.after(3000, func=flip_card)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
current_card_face = canvas.create_image(800 / 2, 526 / 2, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)

# Canvas - text
language_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

# Buttons
wrong_image = PhotoImage(file="./images/wrong.png")
right_image = PhotoImage(file="./images/right.png")
unknown_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
known_button = Button(image=right_image, highlightthickness=0, command=remove_card)
unknown_button.grid(column=0, row=1)
known_button.grid(column=1, row=1)

next_card()

window.mainloop()
