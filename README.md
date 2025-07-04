# pixies

Une fois l'image découpée en un fichier par carte détectée, soit 9 fichiers au maximum.
Notre programme doit retrouver les 3 caractéristiques de chaque cartes. Il s'agit du numéro de la carte, 
de la saison ainsi que du  nombre de bonus/malus qu'elle offre.

Pour reconnaitre les cartes, le programme compare des cartes 'modèles' dans le dossier du même nom aux cartes du joueur grâce aux fonctions match_image_features() et compute_feature_distance(). 
La première fonction calcule pour deux images des "keypoints", qui correspondent à des points d'intérêts de l'image (changement de texture brutal, de couleur etc...) et des "descriptors", qui sont des vecteurs contentant des informations sur l'aspect de la carte autour de ces "keypoints". 
Ensuite, elle cherche à retrouver les mêmes descriptors sur les différentes cartes, et effectue des matchs entre les différents descriptors des deux cartes. Plus les images sont proches, plus il y aura de match et meilleurs ceux-ci seront. La deuxième fonction permet donc de calculer une "distance" entre deux images. Ples images sont différentes, plus cette distance sera grande. L'avantage de cette méthode est qu'elle permet de retrouver deux cartes identiques malgré de grandes différences d'orientation.
En revanche, des reflets ou des contrastes peu élevés peut rendre les matches très mauvais. Cela constitue la principale faille de ce programme, car il se peut que les matches se fassent mal à cause d'une photo avec des couleurs altérées ou la présence d'un reflet. Pour améliorer les résultats, il faudrait que les cartes modèles que l'on utilise soit de très bonne qualité, ce qui n'est pas le cas ici. Certains modèles, sont légèrement flous, ont un fond, etc.

La fonction find_card() permet donc de calculer la distance entre la carte du joueur et toutes les cartes du jeu du même nuémro, et associe cette carte à celle où la distance calculée est la plus faible. 
Nous connaissons les caractéristiques de chaque carte scannée, et cette information est transcrite dans le nom du fichier de la carte modèle selon la nomenclature suivante : "NuméroCouleurValeurbonus.jpg".
Ainsi, l'image du 3 de la saison rouge ayant 3 spirales est nommée '3r3.jpg', et le 7 vert avec 2 croix '7v-2.jpg'. Pour les multicouleurs, on note 'all' à la place de la couleur et pour les bonus spéciaux dépendant des autres cartes, on remplace le montant par la lettre 's'.

Ces informations contenues dans les noms des fichiers sont ensuite utilisée dans le programme via une classe PixiesCard, dont les attributs sont 'num', 'season', et 'score'.

Une fois toutes les cartes retrouvées, il ne reste qu'à rassembler les informations pour calculer les points.
D'abord, on additionne les 'num' des cartes validées.
Puis, on calcule les points des bonus/malus. Pour les cartes spéciales, la fonction season_occurences() permet de connaître le nombre de carte de chaque saison, qu'elle renvoie dans un dictionnaire. 
Cette fonction renvoie également une grille 3x3 (sous forme de liste de liste) contenant les saisons de chaque carte.
Enfin, on trouve la plus grande zone contigüe d'une même saison grâce à la fonction find_largest_zone().
Celle-ci renvoie la taille de la plus grande zone contigüe d'une même saison en comparant les tailles des plus grandes zones contigües pour chaque saison, qui est déterminée grâce à la fonction largest_zone_season().
Cette dernière fonction fonctionne en deux étapes : 
-  elle trouve d'abord tous les numéros des cartes de la saison demandée.
-  elle les rapartit par zone contigüe. La grille étant de taille 3x3, il ne peut y avoir que deux au maximum. A l'aide de la fonction is_adj(), qui détermine si deux numéros sont adjacents dans la grille, elle les répartie dans la zone_1 ou la zone_2. Enfin, elle renvoie la taille de la plus grande zone. 

