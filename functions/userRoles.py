from files import Files
import json
import discord

def getUserSubject(user, interaction: discord.Interaction):
    with open(Files.subjects) as f:
        subjects = json.load(f)
    f.close()

    for subject in subjects:
        role = interaction.guild.get_role(subjects[subject]["role"])
        if(user.get_role(subjects[subject]["role"]) == role):
            return role
    return None
    
def hasUserAcceptedAlready(user):
    with open(Files.settings) as f:
        settings = json.load(f)
    f.close()

    if(user.get_role(settings["roles"]["accepted"]) != None):
        return True
    else:
        return False