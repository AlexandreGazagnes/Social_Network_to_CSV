def traitement_search_result_lkd_recruiter(chaine):

    import time
    import sys
    
    taille_obj = sys.getsizeof(chaine)
    
    start = time.time()

    count=0


    def donner_numero_manipulation(count, fonction):
        count+=1
        print("Manip n* {} : {}".format(count, 
              str(fonction.__name__).replace("_", " ")))
        return count


    def supprimer_les_etoiles(chaine): # On enleve les ***** - OK
        chaine = chaine.replace("*****", "").replace("****", "")
        return chaine


    def rajouter_1er_ligne_et_supprimer_blanck(chaine) :# OK
        liste = chaine.split("\n"); 
        liste.insert(1,"NFA"); 
        liste =  [i.strip() for i in liste if i]
        return liste

     
    def creer_liste_de_liste(liste): # OK 
        liste2, sous_liste = list(), list()

        for j in liste:
            if j[:12] == 'Sélectionner': 
                liste2.append(list(sous_liste))
                sous_liste = list()
            else : 
                sous_liste.append(j)
        return liste2


    def creation_ID(liste): # OK
        for i,j in enumerate(liste):
            liste[i][0] = str(i) # --> forcément besoin de str et pas de int ???
        return liste


    def separer_nom_num_reseau(liste): # OK +/-
        #On part la dessus mais on a un Gros PB ! Qui de si la personne n'est pas en réseau 1 / 2 / 3 ???? - OK MAIS à REVOIR
        for i,j in enumerate(liste): 
            char_list = ["1er","2e","3e"]
            for char in char_list : 
                if char in liste[i][1]: 
                    liste[i][1] = liste[i][1][:liste[i][1].find(char)].strip()  
        return liste


    def suppression_titre_sous_nom_useless(liste): # OK
        for i,j in enumerate(liste) : 
            liste[i].pop(2)
        return liste

    
    def supprimer_actruellement(liste): # OK
        for i,j in enumerate(liste) : 
            liste[i].pop(3)
        return liste

    
    def separer_metier_sste_anciennete(liste): # OK
        
        char = "chez" # sachant que char peut aussi valoir @ ou at
        
        for i, j in enumerate(liste): # separation poste ssté
            if char in  liste[i][3] : 
                elem = liste[i][3][liste[i][3].find(char):]
                liste[i].insert(4, elem) 
                liste[i][3] = liste[i][3][:liste[i][3].find(char)]
            else: 
                liste[i].insert(4, "?") 
                
        for i, j in enumerate(liste): # on enleve le char
            if char in  liste[i][4] : liste[i][4] = liste[i][4].replace(char, "")
                
        for i, j in enumerate(liste): # spéaration de la date
            nb =-1
            for k in liste[i][4] : 
                if k.isdigit():
                    nb = liste[i][4].find(k)
                    break
            if nb >0 : 
                elem = liste[i][4][nb:] # on sépare toute la date : 2014 -aujourd'hui
                liste[i].insert(5, elem)
                liste[i][4] = liste[i][4][:nb]
            else : 
                liste[i].insert(5, "?") # ---> WTF        
             # EST-CE QU'il FAUT AUSSI PRENDRE EN COMPTE LE "AT" OU LE "@"???
        
        for i,j in enumerate(liste): # on ne garde que les 4 1ers chiffres, date début
            liste[i][5] = liste[i][5][:4] if liste[i][5] != "?" else "?"
        
        return liste


    def supprimer_pays_secteur(liste): # OK
        char = ","
        for i, j in enumerate(liste): #
            if char in  liste[i][2] : 
                liste[i][2] = liste[i][2][:liste[i][2].find(char)]
        return liste


    def separer_formation_annee_diplome(liste): # OK
        for i, j in enumerate(liste):
            for k,l in enumerate(liste[i]):
                if l == "Formation" : 
                    elem = liste[i][k+1]
                    liste[i].insert(6,elem[:-11])
                    liste[i].insert(7,elem[-4:])
                    break              
            if "Formation" not in j:
                liste[i].insert(6,"?")
                liste[i].insert(7,"?")
        return liste

    
    def supprimer_champs_inutiles(liste): # EN COURS   
        for chaine in ['relations en', 'relation en', 'Enregistrer dans']:
            
            for i, j in enumerate(liste): 
                nb = list()
                for k,l in enumerate(liste[i]):
                    if chaine in l :
                        nb.append(k)
                if nb : 
                    for k in nb : 
                        liste[i].pop(k)
                        
        for i, j in enumerate(liste): 
            nb = list()
            for k,l in enumerate(liste[i]):
                if "Plus" == l :
                    nb.append(k)
                
            """if nb :
                for k in nb : ------------->>>>>>>>>>>>>> WTF ?????
                    liste[i].pop(k)"""  

        return liste


    def stripper_le_reste_des_champs(liste):
        for i, j in enumerate(liste):
            lon = len(j)
            liste[i][8] = "; ".join(liste[i][8: ])
            liste[i][9:] = []
        return liste
        
        
    def rajouter_source(liste, source="lkd"):
        for i,j in enumerate(liste):
            liste[i].insert(2,str(source))
        return liste
        

    def rajouter_champs_titres(liste):
        titres = ["ID", "Prenom NOM", "source", "Localisation", "Poste", "Ssté", "Date ssté", "formation", "date fomration", "commentaires"]
        liste.insert(0, titres)
        return liste

 
    def formatage_csv(liste):
        for i,j in enumerate(liste):     # PAS DE VIGULES DANS UN CSV 
            for k,l in enumerate(liste[i]):
                liste[i][k] = liste[i][k].replace(",", "-").replace(", ", "-") 

        chaine = str()     # COMPILE EN CSV
        for i in liste:     
            chaine += ", ".join(i) +"\n"
        
        return chaine

    
    ########################################################################


    element = chaine
    del chaine


    for fonction in [
        supprimer_les_etoiles, 
        rajouter_1er_ligne_et_supprimer_blanck, 
        creer_liste_de_liste, creation_ID, separer_nom_num_reseau, 
        suppression_titre_sous_nom_useless, 
        supprimer_actruellement, 
        separer_metier_sste_anciennete,
        supprimer_pays_secteur,
        separer_formation_annee_diplome, 
        supprimer_champs_inutiles, 
        stripper_le_reste_des_champs,
        rajouter_source,
        rajouter_champs_titres,
        formatage_csv] : 
            element = fonction(element)
            count = donner_numero_manipulation(count, fonction)
            
    stop = time.time()
    print("vitesse = {}, soit {} char par secondes".format(
    round(stop-start,3), round(taille_obj/(stop-start),3)))
    return element
