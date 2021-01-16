import datetime, time, pyautogui, pyperclip, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from hashbrowns import RandomCaption

class ShareInstaPost:

    def __init__(self, profilename, mypassword, hashtags, filename, source):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Linux; Android 9; SM-G955F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36"')
        chrome_options.add_argument("user-data-dir=C:\\Users\\ZM\\AppData\\Local\\Google\\Chrome\\User Data Auto\\Profile 1")
        
        self.driver = webdriver.Chrome(executable_path="C:\\Users\\ZM\\Desktop\\CODE\\pystabot\\assets\\chromedriver.exe", options=chrome_options)

        #self.driver.set_window_position(-2000,0)

        self.profilename = profilename
        self.mypassword = mypassword
        self.hashtags = hashtags
        self.filename = filename
        self.source = source
        self.correctpassword = None

    def postMockup(self):

        while True:
            try:
                self.timeout = 0
                print("Accessing Instagram..")
                self.driver.get("https://instagram.com/perennialquotes")

                time.sleep(2)
                self.checkInternet()
                self.checkIfLoggedIn()
                self.checkUploadWindow()
                self.writeCaption()
                print("Preparing to Post..")
                break
            except:
                print("MOCKUP TIMEOUT : RESTARTING SCRIPT")
                continue

    def checkInternet(self):

        print("Checking for Internet Connection..")
        nointernet = None
        while not nointernet:
            try:
                nointernet = self.driver.find_element_by_xpath("//span[contains(text(), 'No internet')]")
                print("NO INTERNET")
                break
            except:
                print("Internet Connection Established")
                return

        raise Exception

    def checkIfLoggedIn(self):

        newpostbtn = None
        while not newpostbtn:
            try:
                print("Checking if Logged In by finding the New Post Button..")
                newpostbtn = self.driver.find_element_by_xpath("//span[@aria-label='New Post']")
                print("LOGGED IN : FOUND THE NEW POST BUTTON")
                newpostbtn.click()
                return
            except:
                if self.timeout == 20:
                    print("TIMEOUT : UNABLE TO FIND NEW POST BUTTON")
                    raise Exception
                else:
                    time.sleep(1)
                    self.timeout += 1
                    self.newLogin()

    def newLogin(self):

        print("NOT LOGGED IN YET")
        try:
            print("Trying to find Login Button..")
            login = self.driver.find_element_by_link_text("Log in")
            print("FOUND LOGIN BUTTON")
            login.click()
        except:
            print("Can't find Login Button")
            return

        loginURL = self.driver.current_url
        usernamebtn = passwordbtn = None
        try:
            print("Trying to find Username/Password Fields..")
            usernamebtn = self.driver.find_element_by_name("username")
            passwordbtn = self.driver.find_element_by_name("password")
            print("FOUND USERNAME/PASSWORD FIELDS")
            usernamebtn.send_keys(self.profilename)

            if len(self.correctpassword) > 0:
                self.mypassword = self.correctpassword

            passwordbtn.send_keys(self.mypassword)
            passwordbtn.send_keys(Keys.ENTER)
            time.sleep(2)
        except:
            print("Can't find the fields")
            time.sleep(1)
            return

        if self.driver.current_url == loginURL:
            try:
                passwordbtn = self.driver.find_element_by_name("password")
                print("WRONG PASSWORD")
                self.correctpassword = input("Type in the Correct Password >> ")
            except:
                print("PASSWORD ACCEPTED")

        return

    def checkUploadWindow(self):

        postnextbtn = None
        while not postnextbtn:
            try:
                postnextbtn = self.driver.find_element_by_xpath("//button[contains(text(), 'Next')]")
                print("FILE UPLOADED SUCCESSFULLY")
                postnextbtn.click()
                return
            except:
                if self.timeout == 20:
                    print("TIMEOUT : UNABLE TO UPLOAD IMAGE")
                    raise Exception
                else:
                    time.sleep(1)
                    self.timeout += 1

                print("Trying to Upload the File, make sure the Window is in Focus..")
                time.sleep(1.5)
                pyautogui.typewrite(str(self.filename))
                time.sleep(.5)
                pyautogui.press('enter')
                time.sleep(3)

    def writeCaption(self):

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
                print("Trying to find Caption Textbox..")
                captionbtn = self.driver.find_element_by_tag_name("textarea")
                print("FOUND THE CAPTION TEXTBOX")
                captionbtn.send_keys(Keys.CONTROL, "v")
                return
            except:
                if self.timeout == 20:
                    print("TIMEOUT : UNABLE TO FIND CAPTION BOX")
                    raise Exception
                else:
                    time.sleep(1)
                    self.timeout += 1

    def sharePost(self):
        
        while True:
            try:
                self.timeout = 0
                self.postMockup()
                self.checkShareBtn()
                self.checkSuccess()

                print("Shutting Down Browser..")
                self.driver.quit()
                print("CODE SELF-DESTRUCTED")
                break
            except:
                print("POST TIMEOUT : RESTARTING SCRIPT")
                continue

    def checkShareBtn(self):

        postsharebtn = None
        while not postsharebtn:
            try:
                print("Trying to find the Share button..")
                postsharebtn = self.driver.find_element_by_xpath("//button[contains(text(), 'Share')]")
                print("FOUND THE SHARE BUTTON")
                self.sharepageURL = self.driver.current_url
                postsharebtn.click()
                return
            except:
                if self.timeout == 20:
                    print("TIMEOUT : UNABLE TO FIND THE SHARE BUTTON")
                    raise Exception
                else:
                    time.sleep(1)
                    self.timeout += 1

    def checkSuccess(self):

        while True:
            if self.timeout == 20:
                print("TIMEOUT : UNABLE TO POST ON INSTAGRAM")
                raise Exception

            if self.driver.current_url == self.sharepageURL:
                print("Posting to Instagram..")
                time.sleep(1)
                self.timeout += 1
                continue
            else:
                print("POST SHARED SUCCESSFULLY")
                return


if __name__ == "__main__":
    #postFolder = "C:\\Users\\ZM\\Desktop\\CODE\\pystabot\\"
    totalPost = len(os.listdir(f"C:\\Users\\ZM\\Desktop\\CODE\\pystabot\\posts"))
    num = totalPost % 2
    print(f"[POST {totalPost+1}]")

    fileName = f"C:\\Users\\ZM\\Desktop\\CODE\\pystabot\\posts\\instapost_{totalPost+1}.jpg"
    myCaption = RandomCaption().getCaption()
    ShareInstaPost("antivnti", "", myCaption, fileName, "SELF").sharePost()