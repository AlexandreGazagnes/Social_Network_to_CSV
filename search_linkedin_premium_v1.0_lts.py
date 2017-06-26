def traitement_linkedin_premium_search_juin_2017(chaine):
  count=0

  # 1/ on enleve les blancs et les ***** - OK
  chaine = chaine.replace("*****", "").replace("****", "")
  
  count+=1; print("Manip n* {}".format(count))
  # --------------------------------------------

  # 2/ on en fait une liste  en supprimant les lignes vides et en rajoutant une ligne - OK
  li = chaine.split("\n"); li.insert(1,"NFA"); liste =  [i.strip() for i in li if i]

  count+=1; print("Manip n* {}".format(count))
  # --------------------------------------------
   
  # 3/ on en fait une liste de liste - OK 
  liste2, sous_liste = list(), list()

  for j in liste:
    if j[:12] == 'Sélectionner': 
      liste2.append(list(sous_liste))
      sous_liste = list()
    else : 
      sous_liste.append(j)
      
  count+=1; print("Manip n* {}".format(count))
  # --------------------------------------------

  # 4/ suppression 1ere valeur et creation d'un ID - OK
  for i,j in enumerate(liste2):
    liste2[i][0] = str(i) # --> forcément besoin de str et pas de int ???

  count+=1; print("Manip n* {}".format(count))
  # --------------------------------------------
  
  # 5/ separation nom n* réseau / On part la dessus mais on a un Gros PB ! Qui de si la personne n'est pas en réseau 1 / 2 / 3 ???? - OK MAIS à REVOIR
  for i,_ in enumerate (liste2): 
    if "\t" in liste2[i][1]: liste2[i][1] = liste2[i][1][:liste2[i][1].find("\t")].strip()

  count+=1; print("Manip n* {}".format(count))
  # --------------------------------------------  

  # 6/ suppression Titre uselless - OK
  for i,j in enumerate(liste2) : liste2[i].pop(2)
  
  count+=1; print("Manip n* {}".format(count))
  # -------------------------------------------- 
  
  # 7/ suppression pays - secteur - OK
  for i,j in enumerate(liste2) : liste2[i].pop(3)

  count+=1; print("Manip n* {}".format(count))
  # --------------------------------------------
  
  # 8/ Séparation métier / ssté / ancienneté - OK
  char = "chez" # sachant que char peut aussi valoir @ ou at
  for i, j in enumerate(liste2): # separation poste ssté
    if char in  liste2[i][3] : 
      elem = liste2[i][3][liste2[i][3].find(char):]
      liste2[i].insert(4, elem) 
      liste2[i][3] = liste2[i][3][:liste2[i][3].find(char)]
    else: 
      liste2[i].insert(4, "?") 
      
  for i, j in enumerate(liste2): # on enleve le char
    if char in  liste2[i][4] : liste2[i][4] = liste2[i][4].replace(char, "")
      
  for i, j in enumerate(liste2): # spéaration de la date
    nb =-1
    for k in liste2[i][4] : 
      if k.isdigit():
        nb = liste2[i][4].find(k)
        break
    if nb >0 : 
      elem = liste2[i][4][nb:]
      liste2[i].insert(5, elem)
      liste2[i][4] = liste2[i][4][:nb]
    else : 
      liste2[i].insert(5, "?") # ---> WTF
            
   # EST-CE QU'il FAUT AUSSI PRENDRE EN COMPTE LE "AT" OU LE "@"???
   
  for i,j in enumerate(liste2):
    liste2[i][5] = liste2[i][5][:4] if liste2[i][5] != "?" else "?"
   
  count+=1; print("Manip n* {}".format(count))
  # --------------------------------------------
  
  # 9/ Enlever le "France • Construction "
  char = ","
  for i, j in enumerate(liste2): #
    if char in  liste2[i][2] : 
      liste2[i][2] = liste2[i][2][:liste2[i][2].find(char)]

  count+=1; print("Manip n* {}".format(count))
  # --------------------------------------------


 # 10/ séparer formation abnnée de diplome
  for i, j in enumerate(liste2):
    for k,l in enumerate(liste2[i]):
      if l == "Formation" : 
        elem = liste2[i][k+1]
        liste2[i].insert(6,elem[:-11])
        liste2[i].insert(7,elem[-4:])

        break
      
    if "Formation" not in j:
      liste2[i].insert(6,"?")
      liste2[i].insert(7,"?")


  count+=1; print("Manip n* {}".format(count))
  # --------------------------------------------
  
  
  # 11 /  supprimer "relation en commun" et "Enregistrer dans projet"
  
  nb = -1
  for i, j in enumerate(liste2): 
    for k,l in enumerate(liste2[i]):
      if ("relations en commun" or "relation en commun" ) in l :
        nb = k
  if nb>0 : liste2[i].pop(nb)
        
  nb = -1      
  for i, j in enumerate(liste2): 
    for k,l in enumerate(liste2[i]):
      if "Enregistrer dans" in l :
        nb = k
  if nb>0 : liste2[i].pop(nb)
  
  nb = -1      
  for i, j in enumerate(liste2): 
    for k,l in enumerate(liste2[i]):
      if "Plus" == l :
        nb = k
  if nb>0 : liste2[i].pop(nb)


  # 11 / On strip le reste 
  for i, j in enumerate(liste2):
    lon = len(j)  
    liste2[i][8] = "; ".join(liste2[i][8: ])
    liste2[i][9:] = []
 
  count+=1; print("Manip n* {}".format(count))  
  # --------------------------------------------
  

  # CONTROLES 
  liste_len = list()
  for i,j in enumerate(liste2):
    liste_len.append((len(j),i))
    

  # PAS DE VIGULES DANS UN CSV 
  for i,j in enumerate(liste2):
    for k,l in enumerate(liste2[i]):
      liste2[i][k] = liste2[i][k].replace(",", " - ") 


  # COMPILE EN CSV
  retour = str()
  for i in liste2:     
    retour += ", ".join(i)
    retour+="\n"
  
  return retour
