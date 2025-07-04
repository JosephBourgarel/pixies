# pixies
La première composante du système constitue le module de reconnaissance et d'indexation des cartes individuelles, développé avec des techniques de vision par ordinateur utilisant la librairie OpenCV. Cette partie du code prend en entrée un chemin vers une photo d'une grille de carte en fin de partie et redonne en sortie autant de fichiers que de cartes dans la grille, ainsi qu'une liste de booléens qui dit si les cartes sont validées (1) ou non (0). 
Dans un premier temps, on charge l'image et on la met en niveau de gris et on la floute légèrement pour réduire le bruit. Ensuite on commence la détection des contours à l'aide de la fonction cv2.findContours. Afin de réduire le nombre de côtés du polygone obtenu, on ne garde que les coins ayant un angle important (loin de 180 degrés) afin de s'approcher le plus possible d'un rectangle. Aussi, on impose une aire minimale pour ne pas détourer les motifs du fond et des cartes, car seule la forme des cartes nous intéresse ici : on ne souhaite pas encore repérer les détails sur les cartes. 
L'étape suivante consiste à rogner la photo : en effet seulement la partie qui représente les cartes nous intéresse. On coupe donc au niveau des abscisses et ordonnées maximales et minimales de ces contours de cartes, auxquelles on ajoute quelques pixels par sécurité.
Toutes les étapes qui suivent seront donc effectuée sur la photo coupée, ne contenant que la grille de cartes, et en niveau de gris.
On utilise ensuite la fonction cards, qui va permettre de détecter les contours de chaque carte et former une liste de liste, chaque sous-liste contentant elle même la liste des coordonnées des sommets des cartes. Cette liste est stockée dans la variable cards_hikes
On s'intéresse ensuite à déterminer les coordonnées du centre des cartes, ce qui nous sera utile pour remettre les cartes dans l'ordre de la grille, car la fonction de détection des contours ne fonctionne pas forcément dans cet ordre (en général, elle fonctionne en spirale). Enfin, la fonction ordre est juste une fonction qui trie les sommets de cards_hikes dans l'ordre qui nous intéresse à savoir celui de la grille.
Maintenant que l'on sait précisément quelle carte est placée où dans la grille, on peut créer un fichier par carte contenant l'image rognée avec uniquement cette carte avec la fonction cv2.imwrite de la librairie cv2. On crée de plus une liste noms qui est composée de chaînes de caractères des noms des fichiers ainsi créés. Si il n'y a pas de carte dans un certain emplacement de la liste, on met "None".
Enfin, la dernière étape consiste à vérifier si les cartes sont validées ou non. Pour cela, on se base sur le nombre de sommets du contour repéré pour une carte donnée. S'il y en a plus de 5, c'est que le contour détecte en réalité deux cartes superposées : la carte est validée. Sinon, c'est que la carte est seule, elle n'est alors pas validée.

Une fois l'image découpée en un fichier par carte détectée, soit 9 fichiers au maximum.
Notre programme doit retrouver les 3 caractéristiques de chaque cartes. Il s'agit du numéro de la carte, 
de la saison ainsi que du  nombre de bonus/malus qu'elle offre.

Pour reconnaitre les cartes, le programme compare des cartes 'modèles' dans le dossier du même nom aux cartes du joueur grâce aux fonctions match_image_features() et compute_feature_distance(). 
La première fonction calcule pour deux images des "keypoints", qui correspondent à des points d'intérêts de l'image (changement de texture brutal, de couleur etc...) et des "descriptors", qui sont des vecteurs contentant des informations sur l'aspect de la carte autour de ces "keypoints". 
Ensuite, elle cherche à retrouver les mêmes descriptors sur les différentes cartes, et effectue des matchs entre les différents descriptors des deux cartes. Plus les images sont proches, plus il y aura de match et meilleurs ceux-ci seront. La deuxième fonction permet donc de calculer une "distance" entre deux images. Plus images sont différentes, plus cette distance sera grande. L'avantage de cette méthode est qu'elle permet de retrouver deux cartes identiques malgré de grandes différences d'orientation.
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
-  elle les répartit par zone contigüe. La grille étant de taille 3x3, il ne peut y avoir que deux au maximum. A l'aide de la fonction is_adj(), qui détermine si deux numéros sont adjacents dans la grille, elle les répartie dans la zone_1 ou la zone_2. Enfin, elle renvoie la taille de la plus grande zone. 

