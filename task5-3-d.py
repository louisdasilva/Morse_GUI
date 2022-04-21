# A GUI to take in a word <= 12 characters and power an LED to signal the word in morse code
# REFERENCES: code made with reference to
# https://python-course.eu/tkinter/entry-widgets-in-tkinter.php
# https://docs.python.org/3/library/tkinter.messagebox.html

import RPi.GPIO as GPIO
from time import sleep
from tkinter import *
from tkinter import messagebox

GPIO.setmode(GPIO.BCM) # BCM pinout rather than Board pinout
LED = 21
GPIO.setup(LED, GPIO.OUT)

# set only the time for the dot, 
# all other units are calculated as per international morse code timing
# https://morsecode.world/international/morse2.html
dot = 0.1
dash = 3 * dot
ccs = dot # ccs = character component space, space between dot or dash for one character
character_space = dash # space between complete characters (letters)
word_space = 7 * dot # space between words

alpha = [".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--",
         "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."]

def power_character_component(component):
    GPIO.output(LED, GPIO.HIGH)
    if(component == "."):
        sleep(dot)
    if(component == "-"):
        sleep(dash)
    GPIO.output(LED, GPIO.LOW)
    print(component)

def signal_out(dot_dash):
    count = len(dot_dash) - 1
    for i in range(0, count):
        power_character_component(dot_dash[i])
        sleep(ccs) # character component space
    power_character_component(dot_dash[count])

def get_morse(character):
    alpha_index = ord(character) - ord("a")
    character_code = alpha[alpha_index]
    return character_code

def send_morse(message):
    count = len(message) - 1
    for i in range(0, count):
        print(message[i])
        alpha_code = get_morse(message[i])
        signal_out(alpha_code)
        sleep(character_space)
    
    print(message[count])
    alpha_code = get_morse(message[count])
    signal_out(alpha_code)

def morse_gui():
    root = Tk()
    root.title("Morse GUI")
    root.geometry("400x100")

    # create main window
    main_menu = Frame(root)
    main_menu.pack()
    
    entry_box_label = Label(main_menu, text = "Enter Word (max 12 letters)")
    entry_box_label.grid(row=0, column=0, pady=10)
    
    entry_box = Entry(main_menu)
    entry_box.grid(row=0, column=1, padx=50)

    user_word = StringVar()
    def signal():
        message = entry_box.get()
        if(not(message.isalpha())):
            messagebox.showerror("Error", "Alphabet letters only, no special characters or numbers")
            clear()
        if (len(message) > 12):
            messagebox.showerror("Error", "Max word length 12 characters")
            clear()
        else:
            message_out = message.lower()
            send_morse(message_out)
            
    def clear():
        entry_box.delete(0,END)

    submit_button = Button(main_menu, text="Signal in Morse", command=signal)
    submit_button.grid(row=1)

    clear_button = Button(main_menu, text="Clear", command=clear)
    clear_button.grid(row=1, column=1)

    root.mainloop()

try:
    morse_gui()
finally:
    GPIO.output(LED, GPIO.LOW)
    GPIO.cleanup()
    exit()
