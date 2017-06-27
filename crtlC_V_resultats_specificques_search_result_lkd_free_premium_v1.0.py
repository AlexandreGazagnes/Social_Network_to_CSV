def traitement_crtlC_V_resultats_specificques_search_result_lkd_free_premium(chaine):
  """input : les la chaine concaténée avec des "*****" ou pas des résultats d'une search linkedin free ou premium
    ndlr, que les resultats copiez collez à la mano, pas de crtlA de l'ensemble de la page
    ndlr pas dans un projet, mais juste la pages de résultats
    output : une chaine en format csv"""

  import time
  import sys
    
  taille_obj = sys.getsizeof(chaine)
  start = time.time()
  count=0


  def donner_numero_manipulation(count, fonction):
    count+=1
    nb = 2 if count<10 else 1 
    print("Manip n*{}{}: {}".format(count, nb * " ", 
      str(fonction.__name__).replace("_", " ")))
    return count


  def formatage_taille(nb):
    for i,j in ((1_000_000_000,"Go"), (1_000_000,"Mo"), (1_000, "Ko"), (1,"o")) : 
      if nb>i : return i,j

  
  def creer_stop(chaine): # OK
    return chaine.replace("Se connecter", "STOP").replace("Envoyer un InMail", "STOP").replace( "Message", "STOP")
  
  
  def creer_une_liste(chaine) : # OK
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
    for i,j in enumerate(liste):
      if "relation" in liste[i][0]: 
        liste[i][0] = (liste[i][0][:liste[i][0].find("relation")]).strip()
     
    """# accessoireremnt il faut dissocier et  améliorer "Prenom", "NOM" et "Prénom NOM" OK
    for i,j in enumerate(liste2):
       
      if " " in liste2[i][0]: 
        elem = liste2[i][0][liste2[i][0].find(" "):]
        liste2[i].insert(1,elem.strip().title())
        liste2[i][0] = liste2[i][0][:liste2[i][0].find(" ")].strip().title()
      else : 
        liste2[i].insert(1,"")"""
    
    return liste
  
  
  def rajouter_id(liste) : # OK 
    for i,j in enumerate(liste):
      liste[i].insert(0,str(i+1))
    return liste

  
  def spliter_poste_entreprise(liste) :# spliter le poste et l'entreprise (s'il y a un chez) OK
    
    liste_separateurs = [" chez "] # on peut eventuellement rajouter @ ou "at" en sep
    is_sep = False
    
    for sep in liste_separateurs : 
      for i,j in enumerate(liste):
        if sep in liste[i][3]:
          elem = liste[i][3][liste[i][3].find(sep):]
          elem = elem.replace(sep, "")
          liste[i].insert(4,elem.strip().title())
          liste[i][3] = liste[i][3][:liste[i][3].find(sep)].strip().title()
          is_sep = True
          break
    
    if not is_sep : 
      for i,_ in enumerate(liste) : 
        liste[i].insert(4,"-")

    # si pas entreprise on peut regarder si chez" dans le COMMENTAIRE dans le job, ou si chez "dans le commentaire"
    for i, j in enumerate(liste): 
      if liste[i][4] == "-" and len(liste[i]) >7 : 
        if "chez" in liste2[i][7] : 
          elem = liste[i][7][liste[i][3].find("chez"):]
          elem = elem.replace("chez ", "")
          liste[i][4] = elem.strip().title()
    
    return liste
        

  def stripper_le_reste(liste):   # tout le reste "hors région" part en commentaire, groupés par un ";"
    for i,j in enumerate(liste):
      if len(liste[i])>7:
        liste[i][6] = " / ".join(liste[i][6:])
        liste[i][7:] = []
    return liste
        

  # engfin il faut aller requeter sur  google pour chopper de l'info
  
  def rajouter_noms_des_colones(liste): # OK 
    liste.insert(0, ["ID", "Prénom NOM","Poste", "Entreprise", "Région", "Pays","com1","com2","com3"])
    return liste
  
  def exporter_en_csv(liste) :# ok
    liste = [",".join(i) for i in liste]
    chaine = "\n".join(liste)
    return chaine
    
  element = chaine 
  del chaine
  
  for fonction in [creer_stop, 
    creer_une_liste, enlever_doublons_noms,
    creer_liste_de_liste,dissocier_nom_prenom_relation, 
    rajouter_id, spliter_poste_entreprise,
    stripper_le_reste, rajouter_noms_des_colones,
    exporter_en_csv]: 
      element = fonction(element)
      count = donner_numero_manipulation(count,fonction)

  stop = time.time()
    
  coef, appel = formatage_taille(taille_obj)
    
  print("vitesse = {}, soit {} {} par secondes".format(
    round(stop-start,4), round((taille_obj/coef)/(stop-start)),appel))
  

  return element
    
