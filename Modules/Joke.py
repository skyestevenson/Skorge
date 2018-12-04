import maya.cmds as cmds
import maya.mel as mel
import random

# write the best jokes known to man
jokes = ["This is a bad one", "fuck this one sucks so bad", "this one too!", "why would they waste valuable development time making this fucking thing"]

def tellJoke():
    print(random.choice(jokes))
