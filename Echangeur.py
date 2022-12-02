import os
from Listes import *
from discord import *
from discord.utils import get
from Vocalearn import vocalearn

import discord

client = discord.Client()
default_intents = discord.Intents.default()
default_intents.members = True
client = discord.Client(intents=default_intents)


async def echangeur(current_id, current_user, message, admin, system, vocaChannel, already_answer):
    msg = message.content.split(" ")
    if os.path.exists(f"{chemin}/user/{current_id}.txt"):
        file = open(f"{chemin}/user/{current_id}.txt", 'r', encoding="cp1252")
        informations = file.readlines()
        file.close()
        if admin:
            if informations[2] == "member":
                informations[2] = "admin"
        elif not admin:
            if informations[2] == "admin":
                informations[2] = "member"
        file = open(f"{chemin}/user/{current_id}.txt", 'w', encoding="cp1252")
        for i in range(len(informations)):
            file.write(informations[i])
        file.close()
        information = informations[3].strip()
        splitCode = information.split('.')
        if informations[3] != "0" and splitCode[0] != "V":
            if informations[3] == "R.1.0":
                file = open(f"{chemin}/liste/banwords.txt", "a", encoding="cp1252")
                for i in range(len(msg)):
                    file.write(f"{msg[i]}\n")
                file.close()
                await message.channel.send("Très bien c'est noté !")
                file = open(f"{chemin}/user/{current_id}.txt", 'r', encoding="cp1252")
                informations = file.readlines()
                file.close()
                informations[3] = "0\n"
                file = open(f"{chemin}/user/{current_id}.txt", 'w', encoding="cp1252")
                for i in range(len(informations)):
                    file.write(informations[i])
        elif splitCode[0] == 'V' and vocaChannel:
            if message.content == "STOP":
                await message.channel.send("Abandon de l'apprentissage...")
                informations[3] = '0'
                informations[4] = '?'
                informations[5] = '?'
                informations[6] = '?'
                informations[7] = '?'
                await maj_information_user(informations, current_id)
                await delete_msg_channel(message, system)
                await message.channel.send("Apprentissage abandonné !")
            else:
                await vocalearn(current_id, message)
                return

        # Finir quand la création est fini

    else:
        file = open(f"{chemin}/user/{current_id}.txt", "w+", encoding="cp1252")
        file.write(f"{current_id}\n")  # 0
        file.write(f"{current_user}\n")  # 1
        if admin:
            file.write("admin")  # 2
        else:
            file.write("member")  # 2
        file.write("\n0\n")  # 3
        # Vocalearn space
        file.write("?\n")  # 4 mauvaise réponse définition
        file.write("?\n")  # 5 bonne réponse
        file.write("?\n")  # 6 mauvaise réponse terme
        file.write("?\n")  # 7 termes appris
        file.close()

    cmd = False
    isVouloir = False
    isAjouter = False
    isBanwords = False
    isMot = False
    isInterdit = False
    isVoir = False
    isMontrer = False
    isUser = False
    isHesta = False
    isPouvoir = False
    isFaire = False
    isQuestion = False
    isSupprime = False
    isMessage = False
    isDigit = False
    isChannel = False
    isAneantissement = False
    isVocabulaire = False
    isApprendre = False
    nb_deleting_msg = 0

    file = open(f"{chemin}/liste/banwords.txt", 'r', encoding="cp1252")
    banword = file.readlines()
    file.close()
    for i in range(len(banword)):
        banword[i] = banword[i].strip()

    for i in range(len(msg)):

        SpeCharac = "&'(-_)=][°/\|`#~!?,;.:§*$"
        for x in range(len(SpeCharac)):
            msg[i] = msg[i].replace(SpeCharac[x], "")

        if msg[i] == "Hesta":
            cmd = True
            match = True

        if msg[i] in vouloir:
            isVouloir = True
            match = True

        if msg[i] in ajouter:
            isAjouter = True
            match = True

        if msg[i] in banwords:
            isBanwords = True
            match = True

        if msg[i] in mot:
            isMot = True
            match = True

        if msg[i] in interdit:
            isInterdit = True
            match = True

        if msg[i] in voir:
            isVoir = True
            match = True

        if msg[i] in présenter:
            isMontrer = True
            match = True

        if msg[i] in utilisateur:
            isUser = True
            match = True

        if msg[i].lower() in pouvoir:
            isPouvoir = True
            match = True

        if msg[i].lower() in faire:
            isFaire = True
            match = True

        if msg[i].lower() in banword:
            await message.channel.send(f"Ce mot est interdit {message.author.mention}")
            await system.send(f"{current_user} a envoyé : {message.content}. Son message a été supprimé !")
            await message.delete()
            already_answer = True
            match = True

        if msg[i].lower() in question:
            isQuestion = True
            match = True

        if msg[i].lower() in supprime:
            isSupprime = True
            match = True

        if msg[i].isdigit() == True:
            isDigit = True
            match = True
            nb_deleting_msg = int(msg[i]) + 1

        if msg[i].lower() in message_list:
            isMessage = True
            match = True

        if msg[i].lower() in channel_list:
            isChannel = True
            match = True

        if msg[i].lower() in aneantisssement:
            isAneantissement = True
            match = True

        if msg[i].lower() in apprendre:
            isApprendre = True
            match = True

        if msg[i].lower() in vocabulaire:
            isVocabulaire = True
            match = True

    addBanwords = False
    voirBanwords = False
    help = False
    delete_message = False
    delete_message_channel = False
    Vocalearn = False

    if cmd and isAjouter and isBanwords:
        addBanwords = True

    elif cmd and isAjouter and isInterdit and isMot:
        addBanwords = True

    elif cmd and isVoir and isBanwords and admin:
        voirBanwords = True

    elif cmd and isVoir and isMot and isInterdit and admin:
        voirBanwords = True

    elif cmd and isMontrer and isBanwords and admin:
        voirBanwords = True

    elif cmd and isMontrer and isMot and isInterdit and admin:
        voirBanwords = True

    elif cmd and isMontrer and isFaire:
        help = True

    elif cmd and isQuestion and isFaire:
        help = True

    elif cmd and isSupprime and isDigit and isMessage and admin:
        delete_message = True

    elif cmd and isSupprime and isChannel and admin:
        delete_message_channel = True

    elif cmd and isAneantissement and isChannel and admin:
        delete_message_channel = True

    elif cmd and isApprendre and isVocabulaire and not vocaChannel:
        Voca1 = client.get_channel(963787951320494094)
        Voca2 = client.get_channel(968891072220626964)
        await message.channel.send(f"Désolé, mais si tu apprends du vocabulaire ici on va déranger du monde, "
                                   f"rends toi plutôt dans ces salons : {Voca1.mention} et {Voca2.mention}")

    elif cmd and isApprendre and isVocabulaire and vocaChannel:
        Vocalearn = True

    if addBanwords:
        file = open(f"{chemin}/user/{current_id}.txt", "r")
        informations = file.readlines()
        file.close()
        informations[3] = "R.1.0"
        file = open(f"{chemin}/user/{current_id}.txt", "w")
        for i in range(len(informations)):
            file.write(informations[i])
        file.close()
        await message.channel.send("Ok, vas-y envoie, je note !")

    elif voirBanwords:
        await system.send(f"{message.author.mention}")
        await system.send(file=discord.File(f'{chemin}/liste/banwords.txt'))

    elif help:
        await message.channel.send("Je peux faire différentes choses, sur demande : \n - (pour les admins) "
                                   "Ajouter des "
                                   "banwords \n - (pour les admins) Voir les banwords\n - Gestion auto de salon "
                                   "vocal "
                                   "\n Je suis aussi actif sur vos messages :\n - Détection de mots interdit\n - "
                                   "C'est moi aussi qui ajoute les rôles à vos arrivées !")

    elif delete_message:
        dead_messages = await message.channel.history(limit=nb_deleting_msg).flatten()
        for i in range(nb_deleting_msg):
            await dead_messages[i].delete()
        await system.send(f"{nb_deleting_msg} ont bien été supprimé dans le salon {message.channel.mention}")

    elif delete_message_channel:
        await delete_msg_channel(message, system)

    elif Vocalearn:
        await vocalearn(current_id, message)

    elif already_answer:
        await message.channel.send("Je ne comprends pas ton message, essaye de réécrire ton message, si le"
                                   "problème persiste n'hésite pas à contacter Firekiking#3537")


async def delete_msg_channel(message, system):
    while message.channel.last_message is not None:
        dead_messages = await message.channel.history(limit=None).flatten()
        for i in range(len(dead_messages)):
            await dead_messages[i].delete()
    await system.send(f"Le salon {message.channel.mention} a totalement été nettoyé !")


async def maj_information_user(informations, current_id):
    file = open(f"{chemin}/user/{current_id}.txt", 'w')
    for i in range(len(informations)):
        file.write(f"{informations[i]}")
    file.close()
    if os.path.exists(f"{chemin}/user/{current_id}.txt"):
        file = open(f"{chemin}/user/{current_id}.txt", 'r')
        informations = file.readlines()
        file.close()
        return informations
    else:
        await message.channel.send("Error : Votre ID s'est perdu en chemin")
