from tkinter import *
import pandas
import random

# ---------------------------- CREATE CARD ------------------------------- #
random_dict = {}
data_dict = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


def generate_word():
    global random_dict, change_timer
    window.after_cancel(change_timer)
    random_dict = random.choice(data_dict)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=random_dict["French"], fill="black")
    canvas.itemconfig(canvas_image, image=front_img)
    change_timer = window.after(3000, func=change_card)

# ---------------------------- CHANGE CARD ------------------------------- #


def change_card():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=random_dict["English"], fill="white")


# ---------------------------- REMOVE WORD ------------------------------- #

def is_known():
    data_dict.remove(random_dict)
    data2 = pandas.DataFrame(data_dict)
    data2.to_csv("data/words_to_learn.csv", index=False)
    generate_word()


# ---------------------------- UI SETUP ------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

change_timer = window.after(3000, func=change_card)

canvas = Canvas(width=800, height=526, highlightthickness=0)
back_img = PhotoImage(file="images/card_back.png")
front_img = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=front_img)
title = canvas.create_text(400, 150, text="Title", font=('Ariel', 40, 'italic'))
word = canvas.create_text(400, 263, text="Word", font=('Ariel', 60, 'bold'))

canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

language_label = Label(text="French")

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=generate_word)
wrong_button.grid(column=0, row=1)
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

generate_word()

window.mainloop()
