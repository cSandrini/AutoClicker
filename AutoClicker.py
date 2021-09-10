from tkinter import *
from pynput import mouse
from pynput.keyboard import Key, Listener
import pyautogui, tkinter.messagebox, threading, time, os

#VARS
clicks=0

### GETTING THE PATH OF THE ICON ###
current_path = os.path.dirname(__file__)
####################################

try: 
    open(str(current_path+"/config.cfg"))
    pathConfig = str(current_path+"/config.cfg")
except:
    pathConfig = "config.cfg"
file = open(pathConfig)
content = file.readlines()

###--
cooldown = 0
paused = True
started = False
alternate = 1

try:
    definedButton = content[0][:-1]
    definedDelay = float(content[1])
except:
    pass

#FUNCTIONS
def on_click(x, y, button, pressed):
    global paused, started, verify, alternate, definedDelay, definedButton
    if(pressed):
        if(not started):
            b1.config(text=button)
            listenerMouse.stop()
            listenerKeyboard.stop()
            b1.config(state="active")
        else:
            if(str(button) == definedButton):
                if(alternate==1):
                    paused = False
                    alternate*=-1
                else:
                    paused = True
                    alternate*=-1

def on_press(key):
    global paused, started, verify, alternate, definedDelay, definedButton
    if(not started):
        b1.config(text=key)
        listenerMouse.stop()
        listenerKeyboard.stop()
        b1.config(state="active")
    else:
        if str(key) == definedButton:
            if(alternate==1):
                paused = False
                alternate*=-1
            else:
                paused = True
                alternate*=-1

def threadAutoClick():
    while started:
        if not paused:
            pyautogui.click()
            pyautogui.PAUSE = definedDelay

def startAc():
    global listenerMouseClicker, listenerKeyboardClicker, started
    if(b01.cget("text")=="Stop"):
        started = False
        b01.config(text="Start")
        listenerMouseClicker.stop()
        listenerKeyboardClicker.stop()
    else:
        started = True
        b01.config(text="Stop")
        listenerMouseClicker = mouse.Listener(on_click=on_click)
        listenerKeyboardClicker = Listener(on_press=on_press)
        threading.Thread(target=threadAutoClick).start()
        listenerMouseClicker.start()
        listenerKeyboardClicker.start()

def turnOn():
    if(not started):
        b1.config(text="Press the Button")
        b1.config(state="disable")
        global listenerMouse, listenerKeyboard
        listenerMouse = mouse.Listener(on_click=on_click)
        listenerKeyboard = Listener(on_press=on_press)
        listenerMouse.start()
        listenerKeyboard.start()
    else:
        tkinter.messagebox.showerror("Error","Stop auto clicker to change")

def restart():
    global clicks, cooldown
    clicks=0
    b3.config(text="Click Counter")
    b4.place(width=0, height=0)
    cooldown=0
    b3.config(state="active")

def timer():
    global cooldown, alternate
    b4.config(state="disable")
    for i in range(5):
        time.sleep(1)
        cooldown+=1
    b4.config(state="active")
    b3.config(state="disable")
    print("\nTime: " + str(cooldown))
    print("Total of Clicks: " + str(b3.cget("text")))
    print("Clicks por Secound: " + str(int(b3.cget("text"))/cooldown) + "\n")

def ccounter():
    global clicks, tempo, cooldown
    clicks+=1
    b3.config(text=clicks)
    if(clicks==1):
        b4.place(x=255,y=75, width=135, height=22)
        threading.Thread(target=timer).start()

def apply():
    global definedButton, definedDelay
    if(str(b1.cget("text"))=="Choose a Button"):
        if(str(e2.get())==""):
            tkinter.messagebox.showerror("Error","Change the button and delay")
        else:
            tkinter.messagebox.showerror("Error","Change the button")
    elif(str(e2.get())==""):
        tkinter.messagebox.showerror("Error","Change the delay")
    elif(started==True):
        tkinter.messagebox.showerror("Error","Stop auto clicker to change")
    else:
        open(pathConfig,"w").write(str(b1.cget("text"))+"\n"+str(e2.get()))
        definedButton =  str(b1.cget("text"))
        definedDelay = float(e2.get())

def closeWindow():
    global listenerKeyboard, listenerMouse, listenerMouseClicker, listenerKeyboardClicker, started
    started=False
    try:
        listenerMouse.stop()
    except:
        pass
    try:
        listenerKeyboard.stop()
    except:
        pass
    try:
        listenerKeyboardClicker.stop()
    except:
        pass
    try:
        listenerMouseClicker.stop()
    except:
        pass
    window.destroy()

#WINDOW CONFIG
window=Tk()
window.protocol("WM_DELETE_WINDOW", closeWindow)
try:
    icon = PhotoImage(file = str(current_path + "/icon.png"))
except:
    icon = PhotoImage(file = "icon.png")
window.iconphoto(False, icon)
window.title("AutoClicker")
window.geometry("400x144")
window.resizable(False, False)
window.configure(background="#7b6887")

########
l1=Label(window, text="Button", background="#7b6887", foreground="#FFF", anchor=W)
l1.place(x=10,y=15,width=100,height=20)
b1=Button(window, command=turnOn, text="Choose a Button", background="#4b4151", activebackground="#574d5e", borderwidth=0, foreground="#FFF", highlightthickness=0, bd=0, relief="sunken", activeforeground="#FFF", anchor=CENTER)
b1.place(x=70,y=10, width=175, height=30)
try:
    b1.config(text=content[0][:-1])
except:
    pass

########
l2=Label(window, text="Delay", background="#7b6887", foreground="#FFF", anchor=W)
l2.place(x=10,y=50,width=100,height=20)
e2=Entry(window, bd=0, highlightthickness=0, borderwidth=10, relief="flat")
try:
    e2.insert(0, content[1])
except:
    pass
e2.place(x=70,y=45, width=175, height=30)

########
b3=Button(window, command=ccounter, text="Click Counter", background="#4b4151", activebackground="#574d5e", borderwidth=0, foreground="#FFF", highlightthickness=0, bd=0, relief="sunken", activeforeground="#FFF", anchor=CENTER)
b3.place(x=255,y=10, width=135, height=65)
b4=Button(window, command=restart, text="Restart", background="#4b4151", activebackground="#574d5e", borderwidth=0, foreground="#FFF", highlightthickness=0, bd=0, relief="sunken", activeforeground="#FFF", anchor=CENTER)
b4.place(width=0, height=0)

########
b0=Button(window, command=apply, text="Apply", background="#4b4151", activebackground="#574d5e", borderwidth=0, foreground="#FFF", highlightthickness=0, bd=0, relief="sunken", activeforeground="#FFF", anchor=CENTER, pady=10)
b0.place(x=200,y=105, width=200)
b01=Button(window, command=startAc, text="Start", background="#4b4151", activebackground="#574d5e", borderwidth=0, foreground="#FFF", highlightthickness=0, bd=0, relief="sunken", activeforeground="#FFF", anchor=CENTER, pady=10)
b01.place(x=0,y=105, width=200)

#RUN THE WINDOW
window.mainloop()