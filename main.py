from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
random_word = {}
words_to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")

def next_word():
    global random_word, flip_timer
    window.after_cancel(flip_timer)
    random_word = random.choice(words_to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=random_word["French"], fill="black")
    canvas.itemconfig(card_background, image=front_img)
    flip_timer = window.after(3000, func=flip)

def flip():
    canvas.itemconfig(card_background, image=back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=random_word["English"], fill="white")

def is_known():
    words_to_learn.remove(random_word)
    df = pandas.DataFrame(words_to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_word()

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip)

canvas = Canvas(height=526, width=800)
back_img = PhotoImage(file="images/card_back.png")
front_img = PhotoImage(file="images/card_front.png")
card_background = canvas.create_image(400,263, image=front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
button = Button(image=wrong_img, highlightthickness=0, borderwidth=0, bg=BACKGROUND_COLOR, command=next_word)
button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
button = Button(image=right_img, highlightthickness=0, borderwidth=0, bg=BACKGROUND_COLOR, command=is_known)
button.grid(row=1, column=1)

next_word()

window.mainloop()