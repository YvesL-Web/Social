chaine_de_characteres = "le langage de programation python est le meilleur langage"

def trouver_index_occurence(chaine_de_charactere, occurence):
    # trouver si l'occurence se trouve dans la chaine de charactere
    if occurence  in chaine_de_charactere:
        #trouver le premier charactere de l'occurence
        premier_charactere_occurence = occurence[0]
        # trouver longueur de  l'occurence
        longueur_occurence =  len(occurence)
        index=0
        # trouver l'index du premier charactère
        for character in chaine_de_charactere:   
            if  chaine_de_charactere[index:longueur_occurence + index] != occurence:
                # print(chaine_de_charactere[index:longueur_occurence+index])
                index +=1
            else :
                print(f"occurence: {chaine_de_charactere[index:longueur_occurence+index]}")
                break

        print(f"index: {index}")
        
    else:
        print(-1)


for mot in chaine_de_characteres:
    
    for index in range(len(chaine_de_characteres)):
        print(mot)



chaine = "le retourzehhdiud fut juste magique"

def mot_le_plus_long(chaine_de_caracteres):
 #recupérer les mots contenus dans chaine de caractères sous form de liste
    liste_de_mots = chaine_de_caracteres.split()
    long_mot = ""
    #trouver le plus long mot
    for mot in liste_de_mots:
        if (len(mot) >= len(long_mot)):
            long_mot = mot
    return long_mot


print(mot_le_plus_long(chaine))
