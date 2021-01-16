import textwrap, os
from PIL import Image, ImageDraw, ImageFont
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

class CreatePost:
    
    def __init__(self): # initialize landscape [0] / portrait [1]

        self.postFolder = "C:\\Users\\ZM\\Desktop\\CODE\\pystabot\\"
        self.totalPost = len(os.listdir(f"{self.postFolder}posts"))
        self.num = self.totalPost % 2
        print(f"[POST {self.totalPost+1}]")

        self.fileName = f"{self.postFolder}posts\\instapost_{self.totalPost+1}.jpg"

        self.winW = self.winH = 1000
        self.colors = [(240,240,240), (40,40,40)]

        if self.num == 0: # PORTRAIT
            self.bgColor = self.colors[self.num+1]
            self.accentColor = self.colors[self.num]
            print("The New Post will be in Portrait Mode..")
        else: # LANDSCAPE
            self.bgColor = self.colors[self.num-1]
            self.accentColor = self.colors[self.num]
            print("The New Post will be in Landscape Mode..")

        self.img = Image.new("RGB", (self.winW,self.winH), color=self.bgColor)
        self.draw = ImageDraw.Draw(self.img)

    def requestText(self, scrapeURL): # use Request library to access quote website

        print(f"Scraping Quote from [{scrapeURL}]..")
        req = Request(scrapeURL, headers={'User-Agent': 'Mozilla/5.0'})
        page_html = urlopen(req).read()
        urlopen(req).close()
        self.page_soup = soup(page_html, "html.parser")

    def checkQuote(self):

        try: # check if file exist, if it doesn't, create it
            readquotes = open(f"{self.postFolder}assets\\allquotes.txt", "r", errors="ignore")
            allquoteslist = readquotes.read().split("\n")
            readquotes.close()
        except:
            createtxt = open(f"{self.postFolder}assets\\allquotes.txt", "a")
            createtxt.close()

        self.fulltext = f"{self.quote} - {self.author}"
        
        if len(self.quote) > 120 or self.fulltext in allquoteslist: # if quote too long or used before
            print("QUOTE UNUSABLE, RETRYING..")
            raise Exception ("scraped quote is unusable")
        else:
            print("SUCCESSFULLY SCRAPED QUOTE")
            print(f"[{self.fulltext}]")
            appendquotes = open(f"{self.postFolder}assets\\allquotes.txt", "a", errors="ignore")
            appendquotes.write(f"{self.fulltext}\n")
            appendquotes.close()

    def scrapeText(self): # scrape quote & author from web

        try: # try to scrape from eduro
            scrapeURL = "https://www.eduro.com/"
            self.requestText(scrapeURL)
            eduroquote = self.page_soup.findAll("dailyquote")
            self.quote = "\"{}\"".format(eduroquote[0].findAll("p")[0].text)
            self.author = eduroquote[0].findAll("p")[1].text[4:].strip().upper()
            self.source = "E"
            self.checkQuote()
        except:
            try: # try to scrape from brainyquote
                scrapeURL = "https://www.brainyquote.com/quote_of_the_day"
                self.requestText(scrapeURL)
                brainyquote = self.page_soup.findAll("img")[0].get("alt").split(" - ")
                self.quote = "\"{}\"".format(brainyquote[0])
                self.author = brainyquote[1].upper()
                self.source = "B"
                self.checkQuote()
            except: # if all else fails, retrieve random quote from quotes.toscrape
                while True:
                    try:
                        scrapeURL = "http://quotes.toscrape.com/random"
                        self.requestText(scrapeURL)
                        self.quote = self.page_soup.find(itemprop="text").text
                        self.author = self.page_soup.find(itemprop="author").text.upper()
                        self.source = "TS"
                        self.checkQuote()
                        break
                    except:
                        continue

        # self.quote = "\"I do not know how to teach philosophy without becoming a disturber of established religion.\""
        # self.author = "Thomas Jefferson".upper()

        # self.quote = "\"Perfection is the child of time.\""
        # self.author = "Joseph Hall".upper()

    def writeQuote(self): # draw quote text

        quotewrap = textwrap.wrap(self.quote, width=30)

        if len(self.quote) > 110:
            quotefontsize = 45
        else:
            quotefontsize = 55

        quotefont = ImageFont.truetype("BELLI.TTF", quotefontsize)
        totalW,totalH = quotefont.getsize(self.quote)
        originalH = totalH
        padding = 20
        totalH *= len(quotewrap)+2
        totalH += (len(quotewrap)+1)*padding
        currentH = self.winH/2 - totalH/2

        for line in quotewrap:
            lineW,lineH = quotefont.getsize(line)
            self.draw.text( ((self.winW/2 - lineW/2), currentH), f"{line} ", font=quotefont, fill=self.accentColor)
            currentH += originalH + padding

    def drawLogo(self): # draw dash

        # dash = 80
        # self.draw.rectangle([self.winW/2-dash/2, self.winH-275, self.winW/2+dash/2, self.winH-275+3], fill=self.accentColor)

        if self.num == 0: # PORTRAIT
            logo = Image.open(f"{self.postFolder}assets\\hourglass_portrait.png", "r")
        else: # LANDSCAPE
            logo = Image.open(f"{self.postFolder}assets\\hourglass_landscape.png", "r")
        
        logo = logo.resize((50,85), Image.ANTIALIAS)
        logoW,logoH = logo.size
        self.img.paste(logo, (int(self.winW/2-logoW/2),self.winH-340), mask=logo)

    def writeAuthor(self): # draw author text

        authorfont = ImageFont.truetype("REFSAN.TTF", 24)
        w,h = authorfont.getsize(self.author)
        self.draw.text(((self.winW/2 - w/2), (self.winH - 200)), self.author, font=authorfont, fill=self.accentColor)

    def drawWhitespace(self): # draw whitespace & border

        whitespace = 75
        border = 50
        if self.num == 0: # PORTRAIT
            self.draw.rectangle([0,0,whitespace,self.winH], fill=(255,255,255))
            self.draw.rectangle([self.winW-whitespace,0,self.winW,self.winH], fill=(255,255,255))

            self.draw.rectangle([border+whitespace,border,self.winW-border-whitespace,self.winH-border], width=3, outline=self.accentColor)
        else: # LANDSCAPE
            self.draw.rectangle([0,0,self.winW,whitespace], fill=(255,255,255))
            self.draw.rectangle([0,self.winH-whitespace,self.winW,self.winH], fill=(255,255,255))

            self.draw.rectangle([border,border+whitespace,self.winW-border,self.winH-border-whitespace], width=3, outline=self.accentColor)

    def drawEverything(self):

        self.scrapeText()
        print("Drawing everything onto the Image..")
        self.writeQuote()
        self.drawLogo()
        self.writeAuthor()
        self.drawWhitespace()
        #self.draw.rectangle([self.winW/2, 0, self.winW/2, self.winH], fill=self.accentColor)
        print("IMAGE COMPLETED")

    def showImg(self): # display drawn image without saving

        self.drawEverything()
        self.img.show()
        print("IMAGE SHOWN / PYSTABOT CANNOT CONTINUE WITHOUT SAVED IMAGE")
        exit()

    def saveImg(self): # save drawn image in the postFolder directory

        self.drawEverything()
        print(f"Saving the Image as [instapost_{self.totalPost+1}.jpg]..")
        self.img.save(self.fileName)

        return self.fileName, self.source

if __name__ == "__main__":

    CreatePost().showImg()

    # for i in range(2):
    #     CreatePost().saveImg()