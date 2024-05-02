from tkinter import *
import random
import pandas
import time


BACKGROUND_COLOR = "#B1DDC6"


#---------------------READ_CSV AND GENERATE RANDOM WORDS
try:
    data = pandas.read_csv("./data/updated_words.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
except pandas.errors.EmptyDataError:
    data = pandas.read_csv("./data/french_words.csv")


random_word = data.to_dict(orient='records')
word =''
def generate_french_word():
    global word, delay_timer
    window.after_cancel(delay_timer)
    try:
        word = random.choice(random_word)
    except IndexError:
        canvas.itemconfig(current_word, text="COMPLETED", fill="black")
    else:
        canvas.itemconfig(title, text="French", fill="black")
        canvas.itemconfig(current_word, text=word["French"], fill="black")
        canvas.itemconfig(canvas_image, image=card_front)
        delay_timer = window.after(3000, generate_english_word)
def generate_english_word():
    global random_word
    canvas.itemconfig(title, text= "English", fill="white")
    canvas.itemconfig(current_word, text=word["English"], fill="white")
    canvas.itemconfig(canvas_image, image=card_back)
    random_word = [item for item in random_word if item["English"] != word["English"]]


#-----------------------CREATING UI-------------------------------
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50,background=BACKGROUND_COLOR)
delay_timer = window.after(3000, generate_english_word)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=528)
canvas_image = canvas.create_image(400, 263, image=card_front)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
current_word = canvas.create_text(400, 253, text="", font=("Ariel", 60, "bold"))
canvas.config(background=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)



unknown_button_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=unknown_button_image, highlightthickness=0,command=generate_french_word)
unknown_button.grid(row=1, column=0)

known_button_image = PhotoImage(file="./images/right.png")
known_button = Button(image=known_button_image, highlightthickness=0, command=generate_english_word)
known_button.grid(row=1, column=1)

generate_french_word()


window.mainloop()

final_data = pandas.DataFrame(random_word)
final_data.to_csv("./data/updated_words.csv", index=False)