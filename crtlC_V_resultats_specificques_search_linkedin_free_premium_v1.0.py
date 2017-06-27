def traitement_crtlC_V_resultats_specificques_search_linkedin_free_premium(chaine):
  """
  EN COURS
  """
  
  def creer_stop(chaine): # OK
    return chaine.replace("Se connecter", "STOP").replace("Envoyer un InMail", "STOP").replace( "Message", "STOP")
  
  
  def creer_une_liste(chaine) : 
    return chaine.split("\n")
  
  
  def enlever_doublons_noms(liste): # on supprime les éléments commencant par " " qui sont des "erreur" propres à crtlC+V sous chrome
    return [i for i in liste if i[0] != " "]
  
  
  def creer_liste_de_liste(liste): # On va créer une liste de liste chaque elem de la liste sera une ligne, chaque elem d'une ligne sera une colonne
    liste2 = list()
    k = list()
    i=0
    for _ in range(len(liste)-2):
      try:
        while liste[i] != "STOP":
          k.append(liste[i])
          i+=1
        liste2.append(k)
        k = list()
        i+=1
      except:
        break
    
    return liste2

  
  def dissocier_nom_prenom_relation(liste):
    # il faut dissoicer prenom nom et "relation" OK 
    for i,j in enumerate(liste2):
      if "relation" in liste2[i][0]: 
        liste2[i][0] = (liste2[i][0][:liste2[i][0].find("relation")]).strip()
    return liste
        
      
  """# accessoireremnt il faut dissocier et  améliorer "Prenom", "NOM" et "Prénom NOM" OK
  for i,j in enumerate(liste2):
     
    if " " in liste2[i][0]: 
      elem = liste2[i][0][liste2[i][0].find(" "):]
      liste2[i].insert(1,elem.strip().title())
      liste2[i][0] = liste2[i][0][:liste2[i][0].find(" ")].strip().title()
    else : 
      liste2[i].insert(1,"")"""
  
  
  def rajouter_id(liste) : # OK 
    for i,j in enumerate(liste2):
      liste2[i].insert(0,str(i+1))
    return liste
  
  
  def spliter_poste_entreprise(liste) :# spliter le poste et l'entreprise (s'il y a un chez) OK
    for i,j in enumerate(liste2):
      if "chez" in liste2[i][3]:
        elem = liste2[i][3][liste2[i][3].find("chez"):]
        elem = elem.replace("chez ", "")
        liste2[i].insert(4,elem.strip().title())
        liste2[i][3] = liste2[i][3][:liste2[i][3].find("chez")].strip().title()
    else:
      liste2[i].insert(4,"-")
      
    liste_job = list()
    for i,j in enumerate(liste2): 
      if str(liste2[i][4]) != "-" :liste_job.append(True) 
      else :liste_job.append(False)
    
    # si pas entreprise on peut regarder si "at" dans le job, ou si chez "dans le commentaire"
    
    for i, j in enumerate(liste2): 
      if liste2[i][4] == "-": 
        if "at" in liste2[i][3] : 
          elem = liste2[i][3][liste2[i][3].find("at"):]
          elem = elem.replace("at ", "")
          liste2[i][4] = elem.strip().title()
          liste2[i][3] = liste2[i][3][:liste2[i][3].find("at")].strip().title()
    
    # si pas entreprise on peut regarder si "@" dans le job, ou si chez "dans le commentaire"
    
    for i, j in enumerate(liste2): 
      if liste2[i][4] == "-": 
        if "@" in liste2[i][3] : 
          elem = liste2[i][3][liste2[i][3].find("@"):]
          elem = elem.replace("@ ", "")
          liste2[i][4] = elem.strip().title()
          liste2[i][3] = liste2[i][3][:liste2[i][3].find("@")].strip().title()
  

    # si pas entreprise on peut regarder si chez" dans le COMMENTAIRE dans le job, ou si chez "dans le commentaire"
  
    for i, j in enumerate(liste2): 
      if liste2[i][4] == "-" and len(liste2[i]) >7 : 
        if "chez" in liste2[i][7] : 
          elem = liste2[i][7][liste2[i][3].find("chez"):]
          elem = elem.replace("chez ", "")
          liste2[i][4] = elem.strip().title()
    
    return liste
        

    def stripper_le_reste(liste):       
    # tout le reste "hors région" part en commentaire, groupés par un ";"
      for i,j in enumerate(liste2):
        if len(liste2[i])>7:
          liste2[i][6] = " / ".join(liste2[i][6:])
          liste2[i][7:] = []
      return liste
        
    # ???????????????????????????????????????????????????????????????????????
    """liste_job = list()
    for i,j in enumerate(liste2): 
      if str(liste2[i][4]) != "-" :liste_job.append(True) 
      else :liste_job.append(False)"""
      

  # engfin il faut aller requeter sur  google pour chopper de l'info
  
  
  def rajouter_noms_des_colones(liste): # OK 
    return liste.insert(0, ["ID", "Prénom","NOM","Poste", "Entreprise", "Région", "Pays","com1","com2","com3"])
  
  def exporter_en_csv(liste) :# ok
    liste3 = [",".join(i) for i in liste2]
    chaine2 = "\n".join(liste3)
    return chaine2
    
  element = chaine 
  del chaine
  
  for fonction in [creer_stop, 
    creer_une_liste, enlever_doublons_nom,
    creer_liste_de_liste,
    dissocier_nom_prenom_relation, 
    rajouter_id,
    spliter_poste_entreprise,
    stripper_le_reste,
    rajouter_noms_des_colones,
    exporter_en_csv]: 
      element = fonction(element)
      
  return element
