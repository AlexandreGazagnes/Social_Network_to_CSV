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



chaine = """


Guillaume Raulet	2e
Ingénieur chargé d'affaires chez Barbanel
Paris 12, Île-de-France, France • Construction
Actuellement
Ingénieur chargé d'affaires, Ingénieur CVCD chez Barbanel2014 – Actuel
Précédent
Ingénieur CVC / PLB chez S2T INGENIERIE2012 – 2014
Ingénieur stagiaire chez S2T INGENIERIE2012 – 2012
Formation
Polytech Nancy - ex ESSTIN2007 – 2012
DTU - Technical University of Denmark2010 – 2011
1 relation en commun
Enregistrer dans projetPlus d’actions
Sélectionner Guillaume Raulet
Fran&#231;ois Huneault

François Huneault	2e
Ingénieur CVC chez SYSTRA
Région de Paris, France • Architecture et urbanisme
Actuellement
Ingénieur CVC chez SYSTRA2016 – Actuel
Précédent
Ingénieur Génie Climatique chez AREP2009 – 2016
Stagiaire Génie Climatique chez Bouygues Construction2009 – 2009
Plus
Formation
Université de Nantes2006 – 2009
Lycée Ambroise Paré
12 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Fran&#231;ois Huneault

Eric MASSON
Eric MASSON	2e
Responsable Etudes CVCD-PLB-FLI
Région de Paris, France • Construction
Actuellement
Responsable études CVC chez AREP2015 – Actuel
Enseignement Thermique Industrielle et Hydraulique Industrielle chez ECAM-EPMI Ecole d'Ingénieurs2013 – Actuel
Précédent
Expert inscrit auprès de la cours d'appel de Versailles chez Expert de justice2012 – 2015
Directeur des opérations chez SAS PCVE - Groupe HGP2015 – 2015
Plus
Formation
INSA de Rouen2001 – 2005
INSA de Rouen2000 – 2001
Plus
11 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Eric MASSON
Lucie Lavall&#233;e
Lucie Lavallée	2e
Ingénieur
Région de Paris, France • Construction
Actuellement
Ingénieur projets chez Oteis2016 – Actuel
Précédent
Spécialiste CVCD chez COSEBA2016 – 2016
Chargée d'opérations réhabilitation chez Haute-Savoie HABITAT2009 – 2016
Plus
Formation
Polytech'Chambéry-Annecy2005 – 2006
EI.CESI - Ecole d'ingénieurs du CESI2002 – 2005
1 relation en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Lucie Lavall&#233;e
Bertrand Rofidal
Bertrand Rofidal	1er
Chef de projet CET spécialiste CVC-D-PLB chez CET Ingénierie
Région de Paris, France • Construction
Actuellement
Chef de projet CET spécialiste CVC-D-PLB chez CET Ingénierie2017 – Actuel
Précédent
Ingénieur chargé d'études CVC-D-PLB chez CET Ingénierie2016 – 2016
Ingénieur chargé d'études CVC-D chez CET ingenierie2016 – 2016
Plus
Formation
Université de Reims Champagne-Ardenne2003 – 2010
63 relations en commun1 message1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Bertrand Rofidal
Michel Ong
Michel Ong	1er
Ingénieur Chef de projet CVC/HVAC chez INEX
Région de Paris, France • Construction
Actuellement
Ingénieur Chef de projet CVC/HVAC chez INEX2016 – Actuel
Précédent
Ingénieur Chef de projet CVC/HVAC chez CET Ingenierie2012 – 2016
Ingénieur chargé d'affaires chez PAZIAUD SA2010 – 2012
Plus
Formation
Ecole centrale de Lyon2007 – 2010
Lycée Chaptal2004 – 2007
Plus
10 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Michel Ong
C&#233;dric TOILLIEZ
Cédric TOILLIEZ	2e
Gerant Nova THermie - HVAC/ PB/ THermique
Beauvais, Picardie, France • Construction
Actuellement
Gérant chez Nova THermie2015 – Actuel
Précédent
Responsable Travaux des lots Techniques CVC / PLO / GTC / Cuisine / Froid chez Bouygues Construction2005 – 2014
Thermicien chez BERIM2010 – 2010
Formation
EDHEC Business School2015 – 2016
Ecole des Mines de Douai2003 – 2005
18 relations en commun
Enregistrer dans projetPlus d’actions
Sélectionner C&#233;dric TOILLIEZ
William TEYSSIER
William TEYSSIER	1er
Chargé d'études Génie Climatique chez AREP
Région de Paris, France • Construction
Actuellement
Chargé d'études Génie Climatique chez AREP2016 – Actuel
Précédent
Chef de service CVC chez Groupe SLH2014 – 2016
Ingénieur CVC chez Groupe SLH2013 – 2016
Plus
Formation
Université Paul Sabatier (Toulouse III)2005 – 2008
Université de Bordeaux à Agen2004 – 2005
Plus
30 relations en communVues2 messages2 projets
Enregistrer dans projetPlus d’actions
Sélectionner William TEYSSIER
k&#233;vin SLOBADZIAN
kévin SLOBADZIAN	1er
Directeur Adjoint - ARTELIA
Région de Paris, France • Construction
Actuellement
Chef de service ingénierie Pôle CVCD/Fluides chez Artelia2017 – Actuel
Précédent
Adjoint au directeur de département Fluides et Energie chez INGEROP2012 – 2017
Chargé d'affaire fluides et énergétique chez INGEROP2007 – 2017
Plus
Formation
ISUPFERE2006 – 2008
Conservatoire National des Arts et Métiers / CNAM2002 – 2003
Plus
26 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner k&#233;vin SLOBADZIAN
Alexis Guillaume Biard
Alexis Guillaume Biard	2e
Thermicien et Ingénieur CVC / Plomberie chez CET ingenierie
Vincennes, Île-de-France, France • Environnement et énergies renouvelables
Actuellement
Ingénieur CVC / Plomberie et Thermicien chez CET ingenierie2016 – Actuel
Précédent
Apprenti ingénieur CVC / Plomberie chez CET ingenierie2013 – 2016
Stage chargé d'études technique chez Abac Ingénierie2013 – 2013
Plus
Formation
ECAM-EPMI2013 – 2016
Université Paris-Est Créteil (UPEC)2012 – 2013
Plus
5 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Alexis Guillaume Biard
Sacha Petrovic
Sacha Petrovic	2e
Gérant P2I
Villeparisis, Île-de-France, France • Formation professionnelle et coaching
Actuellement
Gérant chez P2-Ingenierie2016 – Actuel
Précédent
Professeur vacataire chez MINES ParisTech - Ecole des mines de Paris2009 – 2016
Chef de projets CVC chez Cap Ingelec2011 – 2016
Plus
Formation
Conservatoire National des Arts et Métiers2000 – 2005
Institut Français de Froid Industriel et du Génie Climatique1999 – 2000
Plus
24 relations en commun
Enregistrer dans projetPlus d’actions
Sélectionner Sacha Petrovic
Armel NGOMBI
Armel NGOMBI	2e
Responsable d'affaire cvc plomberie
Région de Paris, France • Construction
Actuellement
Responsable d'affaire cvc plomberie chez SYSTRA2016 – Actuel
Précédent
Chef de Projet Moe CVC PLOMBERIE chez SYSTRA2013 – 2016
Ingénieur Hvac plomberie chez SYSTRA2011 – 2013
Plus
Formation
Université Claude Bernard (Lyon I)2006 – 2007
Université de Cergy-Pontoise
3 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Armel NGOMBI
Babacar Ndiaye
Babacar Ndiaye	2e
Chargé de Projet chez Egis
Région de Paris, France • Construction
Actuellement
Chargé de Projet CVC chez Egis2014 – Actuel
Précédent
Responsable Technique chez Adoma, filiale du Groupe SNI (Caisse des Dépôts)2010 – 2014
Assistant conducteur de travaux chez GTM BATIMENT2008 – 2009
Formation
Université de Technologie de Compiègne (UTC)2007 – 2010
Université de Rouen Normandie2005 – 2007
20 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Babacar Ndiaye
Antoine Coipel
Antoine Coipel	2e
Contract Manager chez ENGIE Cofely France
Région de Paris, France • Environnement et énergies renouvelables
Actuellement
Contract Manager chez ENGIE Cofely France2016 – Actuel
Précédent
Ingénieur d'études/Chef de projet chez Cofely Services France2014 – 2016
Ingénieur Consultant chez agap22012 – 2014
Plus
Formation
Université Paul Sabatier (Toulouse III)2010 – 2012
Université d'Avignon et des Pays de Vaucluse2007 – 2009
2 relations en commun2 projets
Enregistrer dans projetPlus d’actions
Sélectionner Antoine Coipel
Arthur LEMOIGNE
Arthur LEMOIGNE	3e
Assistant Responsable d'Affaires CVC Tertiaire chez SPIE Ile-de-France Nord-Ouest
Paris 12, Île-de-France, France • Environnement et énergies renouvelables
Actuellement
Assistant Responsable d'Affaires chez SPIE ILE DE FRANCE NORD OUEST2017 – Actuel
Précédent
Chargé d'affaires / Conducteur de Travaux TCE chez Oteis2016 – 2017
Apprentis Chef de Projets CVC chez ACIE ING2013 – 2016
Plus
Formation
Ecole spéciale des Travaux publics, du Bâtiment et de l'Industrie2013 – 2016
Université Paris-Est Créteil (UPEC)2011 – 2013
1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Arthur LEMOIGNE
Alexandru Paun
Alexandru Paun	2e
Attaché commercial froid
Draveil, Île-de-France, France • Génie civil
Actuellement
Attaché commercial chez Dalkia2017 – Actuel
Précédent
Ingénieur d'études CVC (Prestataire) chez BERIM2017 – 2017
Chargé d'études CVC-PB (Intérim) chez VINCI Energies2016 – 2017
Plus
Formation
Université de La Rochelle2010 – 2012
Universitatea Tehnică de Construcții din București2007 – 2012
9 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Alexandru Paun
Pierre MASSE
Pierre MASSE	1er
Chef de projet CVC-Plomberie-Désenfumage chez Deerns
Pantin, Île-de-France, France • Construction
Actuellement
Chef de projet CVC-Plomberie-Désenfumage chez Deerns2015 – Actuel
Précédent
Chargé d’affaires lot Génie Climatique - Désenfumage chez SNC-Lavalin2008 – 2015
Chargé de Projet Tous Corps d'Etats chez SNC-Lavalin2007 – 2008
Plus
Formation
Université de Technologie de Compiègne2002 – 2007
Institut Français du Froid Industriel et du Génie Climatique2008 – 2009
22 relations en commun2 projets
Enregistrer dans projetPlus d’actions
Sélectionner Pierre MASSE
Jean-Benoit LAFOND
Jean-Benoit LAFOND	2e
Responsable du pôle Management de l'énergie
Région de Paris, France • Construction
Actuellement
Responsable du pôle Management de l'énergie chez Optimal Solutions2017 – Actuel
Chargé de projets en efficacité énergétique-CPE chez Optimal Solutions2016 – Actuel
Précédent
Consultant en efficacité énergétique chez Econoler2013 – 2015
Chargé de projet HQE chez OASIIS2011 – 2013
Plus
Formation
Université de La Rochelle2008 – 2009
Université Paul Sabatier (Toulouse III)2007 – 2008
Plus
1 relation en commun
Enregistrer dans projetPlus d’actions
Sélectionner Jean-Benoit LAFOND
Benoit QUIGNON
Benoit QUIGNON	2e
Chef de projet CVC Thermique chez S2T
Région de Paris, France • Études/recherche
Actuellement
Chef de projet CVC Thermique chez S2T2015 – Actuel
Précédent
Ingénieur thermicien chez CET ingéniérie2006 – 2015
Chargé d'affaires exploitation chez Oxygène2004 – 2006
Plus
Formation
Institut national des Sciences appliquées de Lyon1996 – 2001
IAE Lyon2001 – 2002
25 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Benoit QUIGNON
charlie BULLOU
charlie BULLOU	2e
Ingénieur Efficacité Energétique chez GrDF
Pantin, Île-de-France, France • Pétrole et énergie
Actuellement
Ingénieur Efficacité Energétique chez GrDF2014 – Actuel
Cogérant chez SCI LPB2014 – Actuel
Précédent
ingénieur d'études CVC chez Artelia2012 – 2014
ingénieur d'études thermique chez ELITHIS2011 – 2012
Formation
Institut Supérieure d'Etudes en Alternance du Management2010 – 2011
Université de Versailles Saint-Quentin-en-Yvelines2009 – 2010
Plus
16 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner charlie BULLOU
s&#233;bastien biout
sébastien biout	2e
chef de projet - Ingénieur coordinateur (AMO-MOD)
Région de Paris, France • Pétrole et énergie
Précédent
Chef de projet - Ingénieur coordinateur chez Artelia2016 – 2017
Chargé d'étude chez AREP2015 – 2016
Plus
Formation
Ecole supérieure de la conduite de travaux2013 – 2013
Ecole spéciale des Travaux publics, du Bâtiment et de l'Industrie2009 – 2009
Plus
3 relations en commun
Enregistrer dans projetPlus d’actions
Sélectionner s&#233;bastien biout
Romuald Pierrot
Romuald Pierrot	2e
Ingénieur Performance énergétique chez Bouygues Energies & Services
Puteaux, Île-de-France, France • Construction
Actuellement
Ingénieur Performance énergétique chez Bouygues Energies & Services2016 – Actuel
Précédent
Ingénieur Commissionnement chez Artelia2015 – 2016
AMO Energie et Exploitation chez Aveltys2015 – 2015
Plus
Formation
Arts et Métiers ParisTech - École Nationale Supérieure d'Arts et Métiers2013 – 2014
IUP Transferts Thermiques2003 – 2006
2 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Romuald Pierrot
Pierre-Hadrien Forestier
Pierre-Hadrien Forestier	2e
Coordinateur & B.I.M Manager d'Operation chez T.T.T
Châtenay-Malabry, Île-de-France, France • Construction
Actuellement
Coordinateur - BIM chez INGEROP2017 – Actuel
Précédent
Coordinateur - BIM chez Y-Ingenierie2017 – 2017
Coordinateur - BIM chez INGEROP2017 – 2017
Plus
Formation
REFSA2015 – 2015
Aricad2012 – 2012
Plus
1 relation en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Pierre-Hadrien Forestier
laurent LE DEVEHAT
laurent LE DEVEHAT	2e
Directeur du département CVC / fluides / Développement durable - INGEROP
Région de Paris, France • Construction
Actuellement
Directeur Departement cvc/ fluides chez INGEROP2010 – Actuel
Précédent
Ingénieur en chef cvc/fluides chez INGEROP2007 – 2010
Charge d'affaires CVC fluides chez Terrell Ltd2004 – 2007
Plus
Formation
INSA de Strasbourg1988 – 1991
60 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner laurent LE DEVEHAT
Cl&#233;mence Rondepierre
Clémence Rondepierre	2e
Responsable de projets - Montage & AMO chez Convergences - CVL
Région de Paris, France • Architecture et urbanisme
Actuellement
Responsable de projets - Pôle Montage & AMO chez Convergences-CVL2014 – Actuel
Précédent
Consultante expérimentée - Pôle Valorisation Immobilière et Territoires chez DTZ Consulting2011 – 2014
Chargée d'études HQE chez Cap Terre2010 – 2010
Plus
Formation
Institut d'Etudes politiques de Paris2010 – 2011
IAE de Caen2009 – 2010
Plus
8 relations en commun2 projets


*****


Mounir AKNAZZAY	2e
Chef de projet
Région de Paris, France • Ingénierie mécanique ou industrielle
Actuellement
Consultant senior chez JLL2016 – Actuel
Précédent
Chef de projet - spécialiste CVC / Project manager - HVAC designer chez Technip TPS2011 – 2016
Chef de projet chez WSP Flack + Kurtz2007 – 2011
Plus
Formation
Mines Douai1999 – 2001
Prépa ENSI
8 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Mounir AKNAZZAY
AURORE ROUCHON
AURORE ROUCHON	2e
expert en efficacité énergétique
Nantouillet, Île-de-France, France • Environnement et énergies renouvelables
Actuellement
technicienne en CVC chez BERIM2016 – Actuel
auto entrepreneur chez aerofluid2017 – Actuel
Précédent
Technicienne Fluides CDD chez ART'X BAT2016 – 2016
Ingénieur CVCD chez FERRO Ingenierie2016 – 2016
Plus
Formation
universite1998 – 2001
lycee maximilien perret1995 – 1998
Plus
53 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner AURORE ROUCHON
Jacqueline CASPER
Jacqueline CASPER	1er
Ingénieur Fluides - Génie Climatique chez WSP France
Région de Paris, France • Environnement et énergies renouvelables
Actuellement
Ingénieur Fluides - Génie Climatique chez WSP France2016 – Actuel
Précédent
Ingénieur thermicien chez Deerns2011 – 2016
Ingénieur spécialiste CVC chez Iosis Bâtiments2008 – 2011
Plus
Formation
Ecole Centrale de Marseille2003 – 2006
ESIM2003 – 2006
Plus
95 relations en commun
Enregistrer dans projetPlus d’actions
Sélectionner Jacqueline CASPER
Sophie TREHOUT
Sophie TREHOUT	2e
Chef de projet chez Colliers International France
Région de Paris, France • Immobilier
Actuellement
Chef de projet chez Colliers International France2013 – Actuel
Précédent
Ingénieur d'études CVC-plomberie-fluides spéciaux chez SNC-Lavalin2011 – 2013
Ingénieur d'études CVC-plomberie-fluides spéciaux chez Technip TPS2003 – 2010
Plus
Formation
Université Jean Monnet Saint-Etienne2001 – 2002
ENISE2000 – 2002
Plus
11 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Sophie TREHOUT
Simon Richard
Simon Richard	2e
Ingénieur performance énergétique chez Artelia
Maisons-Alfort, Île-de-France, France • Construction
Actuellement
Ingénieur performance énergétique chez Artelia2012 – Actuel
Précédent
Ingénieur CVC / fluides chez Egis2011 – 2012
Ingénieur R&D modélisation chez Air Liquide2009 – 2010
Plus
Formation
Ecole centrale de Nantes2006 – 2009
2 relations en commun2 projets
Enregistrer dans projetPlus d’actions
Sélectionner Simon Richard
S&#233;bastien Copitet
Sébastien Copitet	2e
Chargé de projet chez SNC-Lavalin
Champigny-sur-Marne, Île-de-France, France • Construction
Actuellement
Chargé de projet et spécialiste CVC chez SNC-Lavalin2009 – Actuel
Formation
Université de Rennes I2008 – 2009
Université Paris-Est Marne-la-Vallée2006 – 2008
1 relation en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner S&#233;bastien Copitet
Laila KHALFI
Laila KHALFI	2e
FAFCO SA
Montesson, Île-de-France, France • Environnement et énergies renouvelables
Actuellement
Responsable Commercial Export chez FAFCO SA2015 – Actuel
Précédent
Ingénieur commercial chez FAFCO SA2012 – 2015
Chef de Projets CVC chez CAP INGELEC2008 – 2010
Plus
Formation
ENSAIS (Ecole Nationale Supérieure des Arts et Industries de Strasbourg)1997 – 2002
IUT Belfort-Montbéliard1995 – 1997
1 relation en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Laila KHALFI
AbdelKRIM Muman
AbdelKRIM Muman	2e
PROJETEUR SENIOR BIM EN GENIE CLIMATIQUE - FLUIDES - PLOMBERIE
Ivry-sur-Seine, Île-de-France, France • Construction
Actuellement
RESPONSABLE ADJOINT TECHNIQUE chez Groupe NOX2017 – Actuel
Précédent
PROJETEUR CVC-PLOMBERIE-FLUIDES SPECIAUX chez Artelia2007 – 2017
Formation
A.F.P.A. Lardy1997 – 1998
Université Paris Sud (Paris XI)1995 – 1997
3 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner AbdelKRIM Muman
Jordi Escuyer
Jordi Escuyer	2e
Ingénieur transport chez Edeis
Région de Paris, France • Transports routiers et ferroviaires
Actuellement
Ingénieur transport chez Edeis2016 – Actuel
Précédent
Ingénieur transport - Stage de fin d'étude chez SNC-Lavalin2016 – 2016
Geopolymer research Internship chez King Mongkut's University of Technology of North Bangkok2015 – 2015
Plus
Formation
Ecole des Ingénieurs de la Ville de Paris2013 – 2016
上海大学2015 – 2016
Plus
2 relations en commun
Enregistrer dans projetPlus d’actions
Sélectionner Jordi Escuyer
Nicolas DUFILS
Nicolas DUFILS	2e
Responsable de missions - ARTELIA BI
Bezons, Île-de-France, France • Construction
Actuellement
Responsable de mission chez Artelia2016 – Actuel
Précédent
chef de projet - Directeur de travaux MOEX chez INGEROP2014 – 2016
Chargé d'affaires CVC / Fluides chez INGEROP2012 – 2014
Plus
Formation
Université Paris-Est Marne-la-Vallée2006 – 2007
Université Paris-Est Marne-la-Vallée2005 – 2006
Plus
15 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Nicolas DUFILS
Yann Krieger
Yann Krieger	2e
Mechanical Engineer
Paris 15, Île-de-France, France • Génie civil
Actuellement
Mechanical Engineer chez Deerns2017 – Actuel
Précédent
Ingénieur de projets CVC chez Egis2016 – 2017
Ingénieur de projets Data Center chez Cap Ingelec2012 – 2016
Plus
Formation
Polytech'Nantes2009 – 2012
13 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Yann Krieger
Thomas Valantin
Thomas Valantin	2e
Responsable Fluide chez COALLIA
Montreuil, Île-de-France, France • Construction
Actuellement
Responsable du pôle énergie, fluide en maîtrise d'ouvrage chez COALLIA2012 – Actuel
Précédent
Chef de projet projet maîtrise d'oeuvre - ingénierie du bâtiment chez SNC-Lavalin2008 – 2012
Cadre technique de chantier en maîtrise d'oeuvre (industrie pharmaceutique et hospitalière) chez ELCIMAI2007 – 2008
Plus
Formation
Universite de La Rochelle2004 – 2004
Université de La Rochelle2003 – 2004
Plus
9 relations en commun
Enregistrer dans projetPlus d’actions
Sélectionner Thomas Valantin
Jean-Mary SANTORIN
Jean-Mary SANTORIN	2e
Ingénieur CVC chez BERIM
Région de Paris, France • Études/recherche
Actuellement
Ingénieur CVC chez BERIM2006 – Actuel
Précédent
Ingénieur CVC-plomberie chez SAUNIER ET ASSOCIES (suite au plan de cession de GAUDRIOT SA)2005 – 2006
Ingénieur CVC-plomberie chez GAUDRIOT SA2003 – 2005
Formation
Polytech'Nantes1999 – 2002
7 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Jean-Mary SANTORIN
Simon Chocron
Simon Chocron	2e
Ingénieur de porjet CVC chez Cap Ingelec
Paris 12, Île-de-France, France • Ingénierie mécanique ou industrielle
Actuellement
Ingénieur de projets CVC chez CAP INGELEC / S.E.C.A.T.H2016 – Actuel
Précédent
Service civique, Application démarche EDD chez Les Francas2015 – 2016
Responsable de la démarche écologique / Responsable du service qualité des marchandises chez Boutique Plein Air Le Yeti2014 – 2015
Plus
Formation
Université Bordeaux I2012 – 2013
Université de Bretagne Sud, Lorient2011 – 2012
Plus
1 relation en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Simon Chocron
Antoine Pelard
Antoine Pelard	2e
Ingénieur d'études Fluides Médicaux
Rungis, Île-de-France, France • Construction
Actuellement
Ingénieur Fluides Médicaux chez Air Liquide Santé - TH Services2015 – Actuel
Précédent
Stagiaire ingénieur génie climatique chez Egis Bâtiments Centre-Ouest2014 – 2014
Stagiaire fluides chez Ethis2013 – 2013
Plus
Formation
Université de Bretagne-Sud2012 – 2014
Université de Bretagne-Sud2011 – 2012
Plus
1 relation en commun2 projets
Enregistrer dans projetPlus d’actions
Sélectionner Antoine Pelard
Nacera CHALLAL
Nacera CHALLAL	2e
Chargée d'Etudes TCE
Paris 16, Île-de-France, France • Construction
Actuellement
Dessinateur projeteur chez Cet ingenierie2015 – Actuel
Précédent
Architecture d'intérieur chez Studio des arts déco2015 – 2015
Décoratrice d'intérieur chez Lemaire et Fils2015 – 2015
Plus
Formation
Université du Littoral Côte d'Opale2010 – 2011
Université Mouloud Mammeri Tizi-Ouzou2005 – 2010
Plus
13 relations en commun2 projets
Enregistrer dans projetPlus d’actions
Sélectionner Nacera CHALLAL
Thibault COTTINEAU
Thibault COTTINEAU	2e
Ingénieur Commercial
Région de Paris, France • Environnement et énergies renouvelables
Actuellement
Ingénieur Commercial chez ENGIE Cofely2015 – Actuel
Précédent
Ingénieur Commercial chez ENGIE Réseaux, CPCU, Climespace2012 – 2015
Ingénieur Chef de projet chez COFELY GDF-SUEZ2012 – 2012
Plus
Formation
Université de La Rochelle2010 – 2012
Université de La Rochelle2009 – 2010
Plus
4 relations en communVues2 projets
Enregistrer dans projetPlus d’actions
Sélectionner Thibault COTTINEAU
Natacha Bou Ferraa
Natacha Bou Ferraa	2e
Ingénieur en Génie Climatique-Thermicien, Double formation Architecte/Ingénieur
Région de Paris, France • Construction
Précédent
Ingénieur Chargé d'affaires en génie climatique chez Technibat Sas2015 – 2015
Ingénieur chargé d’études en génie climatique chez EDF OPTIMAL SOLUTIONS2014 – 2015
Plus
Formation
Institut national des Sciences appliquées de Strasbourg2010 – 2012
Institut national des Sciences appliquées de Strasbourg2009 – 2010
Plus
32 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Natacha Bou Ferraa
Lucille PREVOST
Lucille PREVOST	3e
Ingénieure d'études - Expertise thermique chez E3C Conseil - Cabinet WOOG
Région de Paris, France • Construction
Actuellement
Ingénieure d'études - Expertise thermique chez E3C Conseil - Cabinet WOOG2014 – Actuel
Précédent
Stage Ingénieur CVC chez TPF INGENIERIE2013 – 2013
Formation
Ecole des Mines d'Albi-Carmaux2009 – 2013
Lycée Camille Guérin, Poitiers2008 – 2009
1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Lucille PREVOST
Franck Testud
Franck Testud	3e
Responsable de mission et coordinateur d'études chez ARTELIA BATIMENT & INDUSTRIE
Région de Paris, France • Ingénierie mécanique ou industrielle
Actuellement
Responsable de mission et coordinateur d'études chez ARTELIA Bâtiment & Industrie2014 – Actuel
Précédent
Chargé de missions et coordinateur des études chez ARTELIA Bâtiment & Industrie2011 – 2013
Responsable de missions chez COTEBA2009 – 2011
Plus
Formation
Centre d'Etudes supérieures industrielles2001 – 2004
Université Paris X Nanterre1998 – 2001
1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Franck Testud
Alexis Fontaine
Alexis Fontaine	2e
Data Center projet engineer at Cap Ingelec
Région de Paris, France • Ingénierie mécanique ou industrielle
Actuellement
Ingénieur de Projet Data Center chez CAP INGELEC2016 – Actuel
Précédent
Ingénieur CVC chez Barbanel2014 – 2016
Stage de fin d'études chez Airbus Defence and Space2014 – 2014
Plus
Formation
Grenoble INP-ENSE32011 – 2014
Grenoble INP-ENSE32011 – 2014
Plus
2 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Alexis Fontaine
Julien BAUGE
Julien BAUGE	2e
Responsable Projet CVCD chez Eiffage Energie Thermie
Région de Paris, France • Études/recherche
Actuellement
Responsable Projet CVCD chez Eiffage Energie Thermie2016 – Actuel
Ingenieur d'Etudes CVC chez Valentin - Vinci Energies2015 – Actuel
Précédent
Assistant Ingenieur d'affaires chez Lefort Francheteau - Vinci Energies2015 – 2015
Assistant Ingenieur Etudes de Prix CVC chez Lefort Francheteau - Vinci Energies2012 – 2015
Plus
Formation
ECAM-EPMI2012 – 2015
Université de Technologie de Troyes2010 – 2011
Plus
17 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Julien BAUGE
Hichem Boughrara
Hichem Boughrara	3e
Consultant études et travaux fluides
Région de Paris, France • Ingénierie mécanique ou industrielle
Actuellement
Consultant Chargé d'etudes MOE cvc ,plomberie et securité chez euro engineering France2014 – Actuel
Précédent
Consultant Chargé d'affaires travaux de maintenance en genie climatique chez euro engineering France2013 – 2014
Consultant chargé d'etudes génie climatique , fluides et désenfumage chez euro engineering France2011 – 2012
Plus
Formation
Université de Perpignan Via Domitia2005 – 2006
Université de tébessa1999 – 2003
1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Hichem Boughrara
Marouane Chalhi
Marouane Chalhi	2e
Ingénieur Froid CVC
Région de Paris, France • Ingénierie mécanique ou industrielle
Actuellement
Responssable de projet Froid chez Lidl France2016 – Actuel
Ingénieur Conception en Génie climatique chez SNC-Lavalin2013 – Actuel
Précédent
Ingénieur Graduate CVC Ferroviaire chez Interfleet2014 – 2015
Chargé d'étude Froid , CVC et Cuisine chez Groupe BALAS2012 – 2013
Plus
Formation
ECAM-EPMI2013 – 2015
Conservatoire National des Arts et Métiers / CNAM2012 – 2013
Plus
47 relations en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Marouane Chalhi
Giuseppe DE MAIO
Giuseppe DE MAIO	2e
Ingénieur chargé d'affaires CVC chez BIM Ingenierie
Région de Paris, France • Études/recherche
Actuellement
Ingénieur chargé d'affaires CVC chez BIM Ingenierie2016 – Actuel
Précédent
Ingénieur CVC chez CET Ingénierie2006 – 2016
Ingénieur CVC chez Studio DAI2005 – 2005
Formation
Università degli Studi di Napoli 'Federico II'1997 – 2004
5 relations en commun1 projet

*****


Edouard Sellé	2e
Ingénieur Energéticien chez Safran
Région de Paris, France • Environnement et énergies renouvelables
Actuellement
Responsable Travaux du site de Saint Quentin (facility manager) chez Safran2016 – Actuel
Précédent
Ingénieur Energéticien chez Safran Aircraft Engines2013 – 2016
Ingénieur d'étude CVC chez Terrell2011 – 2013
Plus
Formation
IAE Paris2012 – 2013
Arts et Métiers ParisTech - École Nationale Supérieure d'Arts et Métiers2009 – 2012
Plus
1 relation en commun1 projet
Enregistrer dans projetPlus d’actions
Sélectionner Edouard Sell&#233;
Rousset Stephanie
Rousset Stephanie	2e
Ingénieur CVC chez SNC-Lavalin
Région de Paris, France • Construction
Actuellement
Ingénieur CVC chez SNC-Lavalin2010 – Actuel
Précédent
Ingénieur CVC chez BARBANEL2008 – 2010
Ingénieur CVC chez SOCOTEC2006 – 2008
Formation
IUP GSI A GRENOBLE2002 – 2004
Institut national des Sciences appliquées de Lyon1999 – 2002
20 relations en commun1 message1 projet




"""

traitement_linkedin_premium_search_juin_2017(chaine)
