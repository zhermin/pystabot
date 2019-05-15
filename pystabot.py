import time, os, random
from src.pillowtalk import CreatePost
from src.hashbrowns import RandomCaption
from src.adamantium import ShareInstaPost
from src.combing import AutoInteraction

starttime = time.time()
os.system("mode con: cols=70 lines=3")
print("[INITIALIZED PYSTABOT]\n")
myPost, mySource = CreatePost().saveImg()
myCaption = RandomCaption().getCaption()
getlogin = open("C:\\Users\\ZM\\Desktop\\CODE\\login.txt", "r")
logindetails = getlogin.read().split("\n")
getlogin.close()
ShareInstaPost(logindetails[0], logindetails[1], myCaption, myPost, mySource).sharePost()

users = random.sample([
    "philosophy.quote",
    "quotesndnotes",
    "quotes.of.thoughts",
    "orion_philosophy",
    "just.lifequotes",
    "tinkling.quotes",
    "life_through_quote",
    "quotewagon",
    "quotesndnotes",
    "quoteswithpositivity",
    "__quotesworld__",
    "quotes_textbook",
    "positive.inspirational.quotes",
    "broken_quotes_143",
],8)

print("Automating Interaction using Combin..")
AutoInteraction(users)
print("COMBIN WILL NOW RUN IN THE BACKGROUND")

print("\n[PYSTABOT TERMINATED]")
print("{} seconds".format(time.time() - starttime))