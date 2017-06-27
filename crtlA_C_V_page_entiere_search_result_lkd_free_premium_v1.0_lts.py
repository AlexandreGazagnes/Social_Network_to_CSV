def traitement_crtlA_C_V_page_entiere_search_result_lkd_free_premium(chaine):
  """
  input Le CrtlA_C_V de l'ensemble d'une page de résultat linkedin free ou premium, search et pas projet attention :) 
  output : une chaine avec uniquement les réusltats expolitatbles de la search : la chaine de caracteres nom prenom poste etc etc
  """

  fin_debut = "résultats affichés" 
  if fin_debut in chaine :  # on enleve tout le debut useless
    nb = chaine.find(fin_debut) + len(fin_debut)
    chaine = chaine[nb : ]
    
  fin_fin = ["Suivant", "Filtrer les personnes par"]
  for char in fin_fin: # on enleve toute la fin  useless
    if char in chaine :
      nb = chaine.find("char")
      chaine = chaine[: nb ]
      break
   
  for k in range(100): # on supprime le n* des pages restantes
    char = chaine[-1]
    if (char.isdigit()) or (char == "\n") : # equivalent à not char.isalpha()
      chaine = chaine[:-1]
    else:
      break
  
  return chaine
