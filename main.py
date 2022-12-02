import random
import discord
from Listes import *
from random import *
from discord import *
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
import os
from Echangeur import echangeur

# App part -------------------------------------------------------------------------------------

client = discord.Client()
default_intents = discord.Intents.default()
default_intents.members = True
client = discord.Client(intents=default_intents)

chemin = os.getcwd()
system = client.get_channel(960202685183836170)


@client.event
async def on_ready():
    print("The FireAspect vient de se réveiller !")
    system = client.get_channel(960202685183836170)
    await system.send("The FireAspect vient de se réveiller !")


@client.event
async def on_message(message):
    msg = message.content
    mot_msg = msg.split(" ")
    already_answer = False
    fin = len(reponse_hello) - 1
    if (message.author.bot):
        return
    else:
        if message.content in salutations:
            num_message = randint(0, fin)
            await message.channel.send(f"{reponse_hello[num_message]} ! ")
        elif message.content == "Ping":
            await message.channel.send("Pong")
        i = 0
        salut_here = False
        Hesta_here = False
        for i in range(len(mot_msg)):
            if mot_msg[i] in salutations:
                salut_here = True
            elif mot_msg[i] in Hesta:
                Hesta_here = True
        if salut_here and Hesta_here:
            num_message = randint(0, fin)
            await message.channel.send(f"{reponse_hello[num_message]} {message.author.mention} !")
            already_answer = True

        user = message.author
        admin = False
        if discord.utils.get(user.roles, name="Élèves de confiance") or discord.utils.get(user.roles, name="La flamme"):
            admin = True

        if message.content == "Dodo Vestia":
            os.spawnl(os.P_NOWAIT, 'STOPRaspberry.bat')
        user = message.author
        user_ID = message.author.id
        system = client.get_channel(960202685183836170)
        vocaChannel = False
        Voca1 = client.get_channel(963787951320494094)
        Voca2 = client.get_channel(968891072220626964)
        if message.channel == Voca1 or message.channel == Voca2:
            vocaChannel = True
        await echangeur(user_ID, user, message, admin, system, vocaChannel, already_answer)


@client.event
async def on_member_join(member):
    fin_enter = len(enter_member) - 1
    random_enter = randint(0, fin_enter)
    fin_name = len(tell_name) - 1
    random_name = randint(0, fin_name)
    portail = client.get_channel(956979535914606652)
    await portail.send(f"{enter_member[random_enter]} {tell_name[random_name]}***{member.display_name}*** !")
    await portail.send(file=discord.File(f'{chemin}/Image_bot/Arrivee_1.png'))
    role = member.guild.get_role(956977942171369533)
    await member.add_roles(role)


@client.event
async def on_member_remove(member):
    fin_leave = len(leave_member) - 1
    random_leave = randint(0, fin_leave)
    fin_name = len(tell_name) - 1
    random_name = randint(0, fin_name)
    portail = client.get_channel(956979535914606652)
    await portail.send(f"{leave_member[random_leave]} {tell_old_name[random_name]}***{member.display_name}*** !")


@client.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    voiceCreation = False
    voiceDeleting = False
    if before.channel is None and after.channel is not None:
        voiceCreation = True

    elif before.channel is not None and after.channel is None:
        voiceDeleting = True

    elif before.channel is not None and after.channel is not None:
        voiceCreation = True
        voiceDeleting = True

    if voiceDeleting:
        for i in range(len(occuped_name)):
            if before.channel.name == occuped_name[i]:
                deleted_channel = discord.utils.get(guild.voice_channels, name=occuped_name[i], bitrate=64000)
                if len(deleted_channel.members) < 1:
                    await deleted_channel.delete()
                    occuped_name.remove(occuped_name[i])

    if voiceCreation:
        if after.channel.name == "Graine Sacrée":
            ok = False
            while not ok:
                x = randint(0, len(voice_name) - 1)
                if voice_name[x] not in occuped_name:
                    newName = voice_name[x]
                    occuped_name.append(voice_name[x])
                    ok = True
                if len(occuped_name) == len(voice_name):
                    system = client.get_channel(960202685183836170)
                    await system.send("Tout les channels temporaires de la Jungle des Phénix sont occupés et un "
                                      "utilisateur a besoin d'une "
                                      "place, besoin d'urgence de rajouter des noms à la liste !")
                    ok = True
            laJungleDesPhenix = guild.get_channel(954893251662467093)
            await guild.create_voice_channel(newName, category=laJungleDesPhenix)
            generateur1 = guild.get_channel(963119318944600134)
            channel = discord.utils.get(guild.voice_channels, name=newName, bitrate=64000)
            for i in range(len(generateur1.members)):
                await generateur1.members[i].move_to(channel)
        elif after.channel.name == "Puissante Etincelle":
            ok = False
            while not ok:
                x = randint(0, len(voice_name_F) - 1)
                if voice_name_F[x] not in occuped_name:
                    newName = voice_name_F[x]
                    occuped_name.append(voice_name_F[x])
                    ok = True
                if len(occuped_name) == len(voice_name):
                    system = client.get_channel(960202685183836170)
                    await system.send("Tout les channels temporaires des Cieux Spirituels sont occupés et un "
                                      "utilisateur a besoin d'une "
                                      "place, besoin d'urgence de rajouter des noms à la liste !")
                    ok = True
            spiritSky = guild.get_channel(956977713950888029)
            await guild.create_voice_channel(newName, category=spiritSky)
            generateur2 = guild.get_channel(965919089010835466)
            channel = discord.utils.get(guild.voice_channels, name=newName, bitrate=64000)
            for i in range(len(generateur2.members)):
                await generateur2.members[i].move_to(channel)


@client.event
async def on_member_update(before, after):
    print("Ping0")
    streaming_role = after.guild.get_role(966641522760093696)
    enLiveRole = after.guild.get_role(966642628026314772)
    activity = discord.utils.get(after.activities, type=discord.ActivityType.streaming)
    print(activity)


client.run("NjM0MzI3OTU4Njc2NDM5MDcx.Xag58g.jjqYvO8urAWQz0-dkvDr3viu5N0")
