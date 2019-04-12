# PYSTABOT
_A Fully Automated Instagram Bot_\
Follow @perennialquotes to see the bot in action!

---

## DISCLAIMER
* This project is a Proof-of-Concept

---

## Features
* Scrapes Quote of The Day from the Web
* Generates an Image with the Scraped Qutoe
* Retrieves 30 Random Hashtags from a CSV File
* Posts the completed Image and Caption on my Profile
* Sets Up Combin for Automated Instagram Interactions

---

## NERDY STEPS IN DETAIL (LIBRARIES USED)

1. Quote of The Day
    a. [beautifulsoup4 / request / urllib] to scrape quote
    b. [textwrap] to fit the quote onto the image
2. Generated JPG Image
    a. [pillow] to create the image and align everything
3. Random Hashtags in Caption
    a. [pandas] to convert csv file of related hashtags into a dataframe
    b. use pandas' sampling to retrieve 30 random hashtags with the specified categories
4. Posting on Instagram
    a. [selenium / chromedriver] to emulate a mobile phone and access instagram's mobile site, which allows photo posting
5. Automated Instagram Interactions (Fairly hard to do on my own)
    a. [pyautogui] to interact with the limited trial software "combin" that does all the hardwork
    b. that software is able to like, follow and comment on posts and other advaced search features
    c. [tkinter] to set up a popup countdown timer after all the searches have finished and ready for interaction

---

## Notes
* The numbers at the end of the captions indicate the date/time posted and the website the quote was scraped from