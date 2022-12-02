import os
from Listes import *
from discord import *
from discord.utils import get
from random import randint
import discord


client = discord.Client()
default_intents = discord.Intents.default()
default_intents.members = True
client = discord.Client(intents=default_intents)


async def vocalearn(current_id, message):
    statusVocalearn = 1
    system = client.get_channel(960202685183836170)
    lose1 = []
    win1 = []
    lose2 = []
    appris = []
    file = open("listes_existantes.txt", "r", encoding="cp1252")
    available_list = file.readlines()
    file.close()
    if os.path.exists(f"{chemin}/user/{current_id}.txt"):
        file = open(f"{chemin}/user/{current_id}.txt", 'r', encoding="cp1252")
        informations = file.readlines()
        file.close()
    else:
        await message.channel.send("Error : Votre ID s'est perdu en chemin")
    if informations[3].strip() == '0':
        file = open("listes_existantes.txt", "r", encoding="cp1252")
        informations = file.readlines()
        file.close()
        await message.channel.send("Choisi parmi les listes ci-dessous, celle que tu veux travailler !\n")
        for i in range(len(informations)):
            await message.channel.send(f"    {i}.{informations[i]}\n")
        await message.channel.send("Ecris le numéro de la liste que tu choisis")
        if os.path.exists(f"{chemin}/user/{current_id}.txt"):
            file = open(f"{chemin}/user/{current_id}.txt", 'r', encoding="cp1252")
            informations = file.readlines()
            file.close()
            informations[3] = "V.A\n"
            informations = await maj_information_user(informations, current_id)

    elif informations[3].strip() == "V.A":
        reponseInt = int(message.content)
        if reponseInt < len(available_list):
            file = open(f"{chemin}/Listes Vocalearn/{available_list[reponseInt].strip()}.txt", 'r', encoding="cp1252")
            motVoca = file.readlines()
            file.close()
            pair = False
            while not pair:
                x = randint(0, len(motVoca) - 1)
                if (x % 2) == 0:
                    pair = True
                else:
                    pair = False
            await message.channel.send(f"--> {motVoca[x]}")
            file = open(f"{chemin}/user/{current_id}.txt", 'r', encoding="cp1252")
            informations = file.readlines()
            file.close()
            informations[3] = f"V.{reponseInt}.{x}\n"  # Code de la question
            informations = await maj_information_user(informations, current_id)
            return

    splitCode = informations[3].split('.')
    file = open(f"{chemin}/user/{current_id}.txt", 'r', encoding="cp1252")
    informations = file.readlines()
    file.close()
    information = informations[4].strip()
    lose1 = information.split(' ')
    information = informations[5].strip()
    win1 = information.split(' ')
    information = informations[6].strip()
    lose2 = information.split(' ')
    information = informations[7].strip()
    appris = information.split(' ')
    if len(splitCode) == 3:
        if splitCode[1] != 'A' and splitCode[2].strip() != 'A':
            file = open(f"{chemin}/Listes Vocalearn/{available_list[int(splitCode[1])].strip()}.txt", 'r', encoding="ut"
                                                                                                                    "f-"
                                                                                                                    "8")
            motVoca = file.readlines()
            file.close()
            reponse = 0
            if splitCode[2].strip() in lose1:
                reponse = 1
            elif splitCode[2].strip() in win1 or splitCode[2].strip() in lose2:
                reponse = 0
            else:
                reponse = 1
            if message.content == motVoca[int(splitCode[2].strip()) + reponse].strip():
                await delete_msg_channel(message)
                await message.channel.send(
                    "Bien joué ! https://tenor.com/view/friends-joey-chandler-good-job-thumbs-up-gif"
                    "-13961903")
                if splitCode[2].strip() in lose1:
                    lose1.remove(splitCode[2].strip())
                    if win1[0] == '?':
                        win1.remove('?')
                    win1.append(splitCode[2].strip())
                elif splitCode[2].strip() in win1:
                    win1.remove(splitCode[2].strip())
                    if appris[0] == '?':
                        appris.remove('?')
                    appris.append(splitCode[2].strip())
                elif splitCode[2].strip() in lose2:
                    lose2.remove(splitCode[2].strip())
                    if appris[0] == '?':
                        appris.remove('?')
                    appris.append(splitCode[2].strip())
                else:
                    if win1[0] == '?':
                        win1.remove('?')
                    win1.append(splitCode[2].strip())

                information = ' '.join([str(i) for i in lose1])
                informations[4] = f"{information.strip()}\n"
                information = ' '.join([str(i) for i in win1])
                informations[5] = f"{information.strip()}\n"
                information = ' '.join([str(i) for i in lose2])
                informations[6] = f"{information.strip()}\n"
                information = ' '.join([str(i) for i in appris])
                informations[7] = f"{information.strip()}\n"
                informations = await maj_information_user(informations, current_id)

                await gestion_stats(message, lose1, win1, lose2, appris, motVoca, informations, current_id)
                if statusVocalearn == 0:
                    return
                goodOne = False
                while not goodOne:
                    pair = False
                    while not pair:
                        x = randint(0, (len(motVoca)) - 1)
                        if (x % 2) == 0:
                            pair = True
                        else:
                            pair = False
                    xStr = str(x)
                    if xStr in lose1:
                        await message.channel.send(f"Allez {message.author.mention}, celui-là tu l'as loupé l'autre"
                                                   f" fois ! **{motVoca[x].strip()}**") #Question
                        goodOne = True
                    elif xStr in win1:
                        await message.channel.send(f"Maintenant {message.author.mention}, "
                                                   f"celui-là ! **{motVoca[x+1].strip()}**") #Question
                        goodOne = True
                    elif xStr in lose2:
                        await message.channel.send(f"Allez {message.author.mention}, on se concentre, tu l'as déjà eu "
                                                   f"tout à l'heure ! **{motVoca[x+1].strip()}**") #Question
                        goodOne = True
                    elif xStr in appris:
                        goodOne = False
                        print("Déjà appris !")
                    else:
                        await message.channel.send(f"Allez {message.author.mention}, au suivant "
                                                   f"**{motVoca[x].strip()}**") #Question
                        goodOne = True
                    informations[3] = f"V.{splitCode[1].strip()}.{x}\n"
                    informations = await maj_information_user(informations, current_id)
                return

            elif message.content != motVoca[int(splitCode[2].strip()) + reponse].strip():
                await message.channel.send(
                    f"Aie non c'est pas le bon ! {message.author.mention} https://tenor.com/view/dis"
                    f"ney-plus-disney-sad-sad-eyes-sad-face-gif-15549594")
                if splitCode[2].strip() in lose1:
                    await message.channel.send(
                        f"Allez t'inquiètes tu vas y arriver ! {message.author.mention}, la réponse"
                        f"c'était *{motVoca[int(splitCode[2].strip())+1].strip()}*, **réécris le !**")#Réponse
                elif splitCode[2].strip() in win1:
                    win1.remove(splitCode[2].strip())
                    if lose2[0] == '?':
                        lose2.remove('?')
                    lose2.append(splitCode[2].strip())
                    await message.channel.send(
                        f"Allez, on se rapproche de la fin {message.author.mention} ! La bonne répo"
                        f"nse c'était : *{motVoca[int(splitCode[2].strip())].strip()}* **réécris le !**") #Réponse
                elif splitCode[2].strip() in lose2:
                    await message.channel.send(
                        f"Allez t'inquiètes tu vas y arriver ! {message.author.mention}, la réponse "
                        f"c'était *{motVoca[int(splitCode[2].strip())].strip()}*, **réécris le !**") #Réponse

                else:
                    await message.channel.send(
                        f"Bon c'est pas grave c'était la première fois {message.author.mention}, tu "
                        f"vas y arriver. La bonne réponse c'était *{motVoca[int(splitCode[2].strip())+1].strip()}* " #Réponse
                        f"**réécris le !**")
                    if lose1[0] == '?':
                        lose1.remove('?')
                    lose1.append(splitCode[2].strip())

                informations[3] = f"V.{splitCode[1].strip()}.{splitCode[2].strip().strip()}.R\n"

                information = ' '.join([str(i) for i in lose1])
                informations[4] = f"{information.strip()}\n"
                information = ' '.join([str(i) for i in win1])
                informations[5] = f"{information.strip()}\n"
                information = ' '.join([str(i) for i in lose2])
                informations[6] = f"{information.strip()}\n"
                information = ' '.join([str(i) for i in appris])
                informations[7] = f"{information.strip()}\n"
                informations = await maj_information_user(informations, current_id)
                return
    if len(splitCode) == 4:
        file = open(f"{chemin}/Listes Vocalearn/{available_list[int(splitCode[1])].strip()}.txt", "r", encoding="cp1252")
        motVoca = file.readlines()
        file.close()
        if splitCode[3].strip() == "R":
            goodOne = False
            if splitCode[2].strip() in lose1:
                if message.content != motVoca[int(splitCode[2].strip())+1].strip():
                    await message.channel.send(f"Non, toujours pas {message.author.mention}! "
                                               f"Réessais, tu dois réécrire ce mot là : "
                                               f"{motVoca[int(splitCode[2].strip())+1].strip()}")
                elif message.content == motVoca[int(splitCode[2].strip())+1].strip():
                    await delete_msg_channel(message)
                    await message.channel.send(
                        f"Ok nickel {message.author.mention}, maintenant sans la réponse :"
                        f" **{motVoca[int(splitCode[2].strip())].strip()}** !")
                    informations[3] = f"V.{splitCode[1]}.{splitCode[2].strip()}.R2\n"
                    await maj_information_user(informations, current_id)
            elif splitCode[2].strip() in lose2:
                if message.content != motVoca[int(splitCode[2].strip())].strip():
                    await message.channel.send(f"Non, toujours pas {message.author.mention}! Réessais, tu dois "
                                               f"réécrire ce mot là : {motVoca[int(splitCode[2].strip())].strip()}")
                elif message.content == motVoca[int(splitCode[2].strip())].strip():
                    await delete_msg_channel(message)
                    await message.channel.send(
                        f"Ok nickel {message.author.mention}, maintenant sans la réponse :"
                        f" **{motVoca[int(splitCode[2].strip())+1].strip()}** !")
                    informations[3] = f"V.{splitCode[1]}.{splitCode[2].strip()}.R2\n"
                    await maj_information_user(informations, current_id)
            return

        elif splitCode[3].strip() == "R2":
            goodOne = False
            if splitCode[2].strip() in lose2:
                if message.content != motVoca[int(splitCode[2].strip())].strip():
                    await message.channel.send(
                        f"Non, toujours pas {message.author.mention}! Réessais, tu dois réécrire "
                        f"ce mot là : {motVoca[int(splitCode[2].strip())].strip()}") #Réponse
                    informations[3] = f"V.{splitCode[1]}.{splitCode[2].strip()}.R\n"
                    await maj_information_user(informations, current_id)
                elif message.content == motVoca[int(splitCode[2].strip())].strip():
                    lose2.remove(splitCode[2].strip())
                    appris.append(splitCode[2].strip())
                    goodOne = True
            elif splitCode[2].strip() in lose1:
                if message.content != motVoca[int(splitCode[2].strip())+1].strip():
                    await message.channel.send(
                        f"Non, toujours pas {message.author.mention}! Réessais, tu dois réécrire "
                        f"ce mot là : {motVoca[int(splitCode[2].strip()) + 1].strip()}") #Réponse
                    informations[3] = f"V.{splitCode[1]}.{splitCode[2].strip()}.R\n"
                    await maj_information_user(informations, current_id)
                elif message.content == motVoca[int(splitCode[2].strip()) + 1].strip():
                    lose1.remove(splitCode[2].strip())
                    appris.append(splitCode[2].strip())
                    goodOne = True

            if goodOne:
                await delete_msg_channel(message)
                await message.channel.send(f"Nice, celui-là {message.author.mention}, tu l'as ! Allez au suivant !")
                await gestion_stats(message, lose1, win1, lose2, appris, motVoca, informations, current_id)
                if statusVocalearn == 0:
                    return
                goodOne = False
                while not goodOne:
                    pair = False
                    while not pair:
                        x = randint(0, (len(motVoca)) - 1)
                        if (x % 2) == 0:
                            pair = True
                        else:
                            pair = False
                    xStr = str(x)
                    if xStr in lose1:
                        await message.channel.send(
                            f"Allez, celui-là tu l'as loupé l'autre fois {message.author.mention}: **{motVoca[x]}**") #Question
                        goodOne = True
                    elif xStr in win1:
                        await message.channel.send(f"Maintenant {message.author.mention}, celui-là : **{motVoca[x+1]}**") #Question
                        goodOne = True
                    elif xStr in lose2:
                        await message.channel.send(f"Allez on se concentre {message.author.mention}, tu l'as déjà eu "
                                                   f"tout à l'heure : **{motVoca[x + 1]}**") #Question
                        goodOne = True
                    elif xStr in appris:
                        goodOne = False
                    else:
                        await message.channel.send(f"Allez un petit nouveau {message.author.mention}: **{motVoca[x]}**") #Question
                        goodOne = True
                    informations[3] = f"V.{splitCode[1]}.{x}\n"
                    informations = await maj_information_user(informations, current_id)
            return


async def maj_information_user(informations, current_id):
    file = open(f"{chemin}/user/{current_id}.txt", 'w', encoding="cp1252")
    for i in range(len(informations)):
        file.write(f"{informations[i]}")
    file.close()
    if os.path.exists(f"{chemin}/user/{current_id}.txt"):
        file = open(f"{chemin}/user/{current_id}.txt", 'r', encoding="cp1252")
        informations = file.readlines()
        file.close()
        return informations
    else:
        await message.channel.send("Error : Votre ID s'est perdu en chemin")


async def delete_msg_channel(message):
    while message.channel.last_message is not None:
        dead_messages = await message.channel.history(limit=None).flatten()
        for i in range(len(dead_messages)):
            await dead_messages[i].delete()


async def gestion_stats(message, lose1, win1, lose2, appris, motVoca, informations, current_id):
    if len(appris)*2 >= len(motVoca):
        await message.channel.send(f"Bien joué {message.author.mention}, tu as appris toutes la liste de vocabulaire "
                                   f"! :partying_face: :partying_face:")
        informations[3] = '0\n'
        informations[4] = '?\n'
        informations[5] = '?\n'
        informations[6] = '?\n'
        informations[7] = '?\n'
        await maj_information_user(informations, current_id)
        statusVocalearn = 0
    else:
        pNonVu = 100-((len(lose1)+len(lose2)+len(win1)+len(appris))*100/len(motVoca))
        pVuSens = (len(lose1)+len(win1))*100/len(motVoca)
        pAppris = len(appris)*100/len(motVoca)
        pLeft = 100-pAppris
        await message.channel.send(f"Petit point statistiques parce que Firekiking adore ça :\n"
                                   f"Pourcentage restant non vu : **{int(pNonVu)}%**\n"
                                   f"Pourcentage appris (dans un sens uniquement) : **{int(pVuSens)}%**\n"
                                   f"Pourcentage appris : **{int(pAppris)}%**\n"
                                   f"Pourcentage à apprendre : **{int(pLeft)}%**")