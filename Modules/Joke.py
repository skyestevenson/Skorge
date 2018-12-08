import maya.cmds as cmds
import maya.mel as mel
import random
import sys

# alert user function
def alert(message):
    sys.stdout.write("Skorge says: " + message)

# write the best jokes known to man
jokes = ["This is a bad one", "fuck this one sucks so bad", "this one too!", "why would they waste valuable development time making this fucking thing"]

def tellJoke(self):
    alert(random.choice(jokes))
