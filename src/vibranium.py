import datetime, time, pyautogui, pyperclip, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

pyautogui.failsafe = True # Force Quit at Top Left Corner with Cursor

class ShareInstaPost:

    def __init__(self, profilename, mypassword, hashtags, filename, source):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Linux; Android 9; SM-G955F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.90 Mobile Safari/537.36"')
        chrome_options.add_argument("user-data-dir=C:\\Users\\ZM\\AppData\\Local\\Google\\Chrome\\User Data Auto\\Profile 1")
        
        self.driver = webdriver.Chrome(executable_path="C:\\Users\\ZM\\Desktop\\CODE\\pystabot\\assets\\chromedriver.exe", options=chrome_options)

        self.driver.set_window_position(-2000,0)

        self.profilename = profilename
        self.mypassword = mypassword
        self.hashtags = hashtags
        self.filename = filename
        self.source = source

    def tryLogin(self): # access instagram and find login button

        print("Accessing Instagram..")
        self.driver.get("https://instagram.com/")

        login = None
        noLogin = 0
        while not login:
            try:
                print("Trying to find Login Button..")
                login = self.driver.find_element_by_link_text("Log in")
                print("FOUND LOGIN BUTTON")
                login.click()
                self.loginPage()
            except:
                time.sleep(.5)
                if noLogin != 3:
                    noLogin += 1
                    continue
                else:
                    print("ALREADY LOGGED IN")
                    break

    def loginPage(self): # key in username and password

        loginURL = self.driver.current_url
        while self.driver.current_url == loginURL:

            usernamebtn = passwordbtn = None
            while not usernamebtn or not passwordbtn:
                try:
                    print("Trying to find Username/Password Fields..")
                    usernamebtn = self.driver.find_element_by_name("username")
                    passwordbtn = self.driver.find_element_by_name("password")
                    print("FOUND USERNAME/PASSWORD FIELDS")
                    usernamebtn.send_keys(self.profilename)
                    passwordbtn.send_keys(self.mypassword)
                    passwordbtn.send_keys(Keys.ENTER)
                except:
                    time.sleep(1)
                    continue

                try:
                    time.sleep(2)
                    passwordbtn = self.driver.find_element_by_name("password")
                    print("WRONG PASSWORD")
                    self.tryLogin()
                    continue
                except:
                    print("PASSWORD ACCEPTED")
                    print("Logging In..")

    def newInstaPost(self): # click on new post button

        newpostbtn = None
        while not newpostbtn:
            try:
                print("Redirecting to Profile Page..")
                self.driver.get(f"https://instagram.com/{self.profilename}/")
                print("Finding the New Post Button..")
                newpostbtn = self.driver.find_element_by_xpath("//span[@aria-label='New Post']")
                print("FOUND THE NEW POST BUTTON")
                newpostbtn.click()
            except:
                time.sleep(1)
                continue

    def uploadPost(self): # type in new post's file name and proceed to caption

        postnextbtn = None
        uploadTimeout = 0
        while not postnextbtn:
            try:
                postnextbtn = self.driver.find_element_by_xpath("//button[contains(text(), 'Next')]")
                print("FILE UPLOADED SUCCESSFULLY")
                print("FOUND THE NEXT BUTTON")
                postnextbtn.click()
            except:
                if uploadTimeout < 10:
                    print("Trying to Upload the File, make sure the Window is in Focus..")
                    time.sleep(2)
                    pyautogui.typewrite(str(self.filename))
                    pyautogui.press('enter')
                    time.sleep(.5)
                    continue
                else:


    def writeCaption(self): # key in whole chunk of caption + hashtags

        captionbtn = None
        now = datetime.datetime.now().strftime("%H%M%d%m%y")

        fullCaption = "\U0001F914 Comment 'YES' if you Agree \U0001F914\n"
        fullCaption += "Tag a Friend that needs to see this\n"
        fullCaption += "\u2800\n"
        fullCaption += "- Support My Venture!!! -\n"
        fullCaption += "\u2764 @VYBS.vtg \U0001F64F\n"*3
        fullCaption += "\u2800\n"*5
        fullCaption += self.hashtags
        fullCaption += "\n\u2800\n"
        fullCaption += f"[{now}/{self.source}]"
        pyperclip.copy(fullCaption)

        while not captionbtn:
            try:
                print("Trying to find Caption textbox..")
                captionbtn = self.driver.find_element_by_tag_name("textarea")
                print("FOUND THE CAPTION TEXTBOX")
                captionbtn.send_keys(Keys.CONTROL, "v")
                print("Preparing to Post..")
            except:
                continue

    def findShareBtn(self): # finding the share button

        postsharebtn = None
        while not postsharebtn:
            try:
                print("Trying to find the Share button..")
                postsharebtn = self.driver.find_element_by_xpath("//button[contains(text(), 'Share')]")
                print("FOUND THE SHARE BUTTON")
                self.sharepageURL = self.driver.current_url
                postsharebtn.click()
            except:
                continue

    def postMockup(self):

        self.tryLogin()
        self.newInstaPost()
        self.uploadPost()
        self.writeCaption()
        self.findShareBtn()

    def postSuccess(self): # check and see if the post managed to be shared

        postTimeout = 0
        while True:
            if postTimeout >= self.timeoutValue:
                return postTimeout
            
            if self.driver.current_url == self.sharepageURL:
                print("Posting to Instagram..")
                time.sleep(1)
                postTimeout += 1
                continue
            else:
                return postTimeout

    def sharePost(self):

        while True:
            self.postMockup()

            self.timeoutValue = 30
            postTimeout = self.postSuccess()
            if postTimeout >= self.timeoutValue:
                print("Post Timeout, Retrying..")
                continue
            else:
                print("POST SHARED SUCCESSFULLY")
                break

        print("Shutting Down Browser..")
        self.driver.quit()
        print("CODE SELF-DESTRUCTED")

if __name__ == "__main__":
    ShareInstaPost("antivnti", "", "#test", f"{os.getcwd()}\\posts\\instapost_1.jpg", "O")