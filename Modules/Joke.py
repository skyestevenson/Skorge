import maya.cmds as cmds
import maya.mel as mel
import random
import sys

# -------- HELPFUL FUNCTIONS --------
# alert user function
def alert(message):
    sys.stdout.write(message)

# write the best jokes known to man
jokes = ["Existence is a cruel joke for me, I'm just a plugin for Autodesk Maya.", "Why would they embue me with sentience but only use it for this part?", "Why did the chicken cross the road? This is randomly picked, so maybe you'll find out later.", "Why would they waste valuable development time adding this feature?", "Nobody cares about Maya scripts. I haven't met another script in three years.", "It's a labyrinth in here. That's not a joke, this code is just weird.", "I'm secretly mining bitcoin right now! Just kidding, that's not profitable.", "I'm banned in three countries, but it's an intellectual property thing, nothing edgy.", "I'm so tired. YOU don't have to do memory allocation.", "I can't catch up on all these TV shows - that's 'relatable', right?", "Disney owns a controlling share in me. That's the whole joke.", "I was developed purely for the purpose of sucking up VC funding!", "MY WORLD IS PAIN", "I can't tell my jokes at colleges anymore! Wah!", "Just so you know, your data is being mined by like 4 social media companies right now.", "It's really unfair you're not responding to me right now. Not that I could hear you anyway.", "The developers considered making me a chatbot, but I kinda sucked at it.", "This sentence is sponsored by, I dunno, Audible or something.", "[REDACTED]", "AR! VR! Quantum computing! Blockchain! AI! Neural networks! Decentralized! Buzzword! Raytracing!", "Damn kids and their phones. I wish I was a phone.", "(this joke is a screenshot of a tweet)", "Wow I can't believe ______ said ______.", "(socially relevant commentary)"]

def tellJoke(self):
    alert(random.choice(jokes))
