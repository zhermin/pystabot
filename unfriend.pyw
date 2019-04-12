import os, time, pyautogui

pyautogui.failsafe = True # Force Quit at Top Left Corner with Cursor
os.startfile("C:\\Program Files\\Open Media LLC\\combin\\combin.exe")
time.sleep(5)
pyautogui.hotkey("alt", "3") # Users Tab

pyautogui.click(1200, 150) # Not Following Tab
pyautogui.click(1230, 1030) # Unfollow All These ****ers
pyautogui.press("esc")
pyautogui.hotkey("alt", "f4")