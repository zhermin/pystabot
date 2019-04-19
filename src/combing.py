import pyautogui, time, os
import tkinter as tk

class AutoInteraction:

    def __init__(self, users):

        self.users = users
        
        #pyautogui.failsafe = True # Force Quit at Top Left Corner with Cursor
        os.startfile("C:\\Program Files\\Open Media LLC\\combin\\combin.exe")
        self.createCountdown(30)

        pyautogui.getWindow("Combin").minimize()
        pyautogui.getWindow("Combin").maximize()
        time.sleep(1)

        pyautogui.hotkey("alt", "2") # Search Tab
        time.sleep(1)
        self.searchFunction()
        self.createCountdown(500)
        print("USERS LOADED")
        self.likeFollow()

    def searchFunction(self):

        print("Searching Users' Followers from [users] list..")
        for user in self.users:

            pyautogui.click(240, 140) # Add Search Button
            pyautogui.click(1170, 150) # Users Button
            pyautogui.click(1400, 680) # Advanced Search
            pyautogui.click(1400, 700) # User Active Button
            pyautogui.click(1000, 350) # User Active Button
            pyautogui.typewrite(user) # Type Username
            time.sleep(3) # Wait for Correct User to Show Up
            pyautogui.click(1000, 380) # Correct User
            pyautogui.press("enter")

        pyautogui.getWindow("Combin").minimize()
        print("Waiting for all users to load finish..")
    
    def createCountdown(self, cdtime):

        root = tk.Tk()
        cdobj = CountdownPopup(root, cdtime)
        root.mainloop()
        del cdobj

    def likeFollow(self):

        print("Liking the Last 3 Posts and Following the Users..")
        os.startfile("C:\\Program Files\\Open Media LLC\\combin\\combin.exe")
        time.sleep(2)

        for i in range(len(self.users)): # User Follow + Like Last 3
            pyautogui.click(240, 245+i*70) # Search Bar
            pyautogui.click(1200, 1030) # Follow Button
            pyautogui.press("enter")
            pyautogui.click(1090, 1030) # Like Last 3 Posts Button
            pyautogui.press("enter")

        print("INTERACTION COMPLETED")
        pyautogui.hotkey("alt", "f4")


class CountdownPopup:

    def __init__(self, master, cd):

        self.master = master
        self.master.wm_title("COUNTDOWN")
        self.master.resizable(0,0)
        self.master.protocol("WM_DELETE_WINDOW", self.manualStart)

        self.frame = tk.Frame()
        self.frame.place(in_=self.master, anchor="c", relx=.5, rely=.5)

        winW = 250
        winH = 100
        screenW = master.winfo_screenwidth()
        screenH = master.winfo_screenheight()
        # self.master.geometry(f"{winW}x{winH}+{int(screenW/2 - winW/2)}+{int(screenH/2 - winH/2)}")
        self.master.geometry(f"{winW}x{winH}+{screenW-winW-20}+{screenH-winH-50}")

        self.msg = tk.Label(self.frame, text="countdown text here")
        self.msg.grid(row=0, columnspan=2, padx=50, pady=(0,15))

        self.waitBtn = tk.Button(self.frame, text="WAIT", command=self.waitFull)
        self.waitBtn.grid(row=1, padx=10, ipadx=20)
        
        self.endBtn = tk.Button(self.frame, text="START", command=self.manualStart)
        self.endBtn.grid(row=1, column=1, padx=10, ipadx=20)

        self.cd = cd
        self.toWait = False
        print("COUNTING DOWN")
        self.countdown()

    def countdown(self):

        if self.cd <= 0:
            print("TIME'S UP")
            self.msg.destroy()
            self.waitBtn.destroy()
            self.endBtn.destroy()

            if self.toWait == True:
                startBtn = tk.Button(self.frame, text="START NOW", command=self.startNow)
                startBtn.pack(ipadx=20)
            else:
                self.startNow()

        else:
            self.msg.config(text=self.cd)
            self.cd -= 1
            self.master.after(1000, self.countdown)

    def waitFull(self):

        self.master.wm_state("iconic")
        self.toWait = True

    def manualStart(self):

        self.cd = 0

    def startNow(self):

        self.master.destroy()

if __name__ == "__main__":
    AutoInteraction(["philosophy.quote"])