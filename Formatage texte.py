import os
from Listes import chemin

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z", ' ', "'", "é", "ê", ",", "ä", "ü", "/", "â"]

file = open(f"{chemin}/Listes Vocalearn/Gleichberechtigung - ein langer Weg.txt", 'r')
informations = file.readlines()
file.close()
for i in range(len(informations)):
    information = informations[i].strip()
    for y in range(len(information)):
        if information[y].lower() not in alphabet:
            print(information[y])
            informations[i] = str(input(f"Correction de {informations[i].strip()} : "))
            file = open(f"{chemin}/Listes Vocalearn/Gleichberechtigung - ein langer Weg.txt", 'w')
            for x in range(len(informations)):
                file.write(f"{informations[i]}")
            file.close()
            break
        else:
            print("Correct")