"""
Date: 2015-04-19
Karol Andrea Ujueta Rojas

Ce programme implémante une structure de donnée, QuadTree, pour gérer le jeu battleship grandeur nature.
Ce programme peut lire une liste de bateaux dans un fichier texte, les insérer dans l'arbre et puis lire
une liste de bombes dans un fichier texte pour ensuite détruire les bateaux dans le rayon d'explosion pour chacune d'elle.
"""



import queue

"""
La classe bateau instancie des objets qui représentent les feuilles dans notre arbre.
Ces objets sont initialisés avec des coordonnées(x,y) et un pointeur sur son parent.
"""
class bateau:
	#CONSTRUCTEUR
	def __init__(self,x,y,parent=None):
		self._x=x
		self._y=y
		self.parent=parent
		
	#Retourne les coordonnées du bateau
	def coord(self):
		return "["+''.join('{} {}'.format(self._x,self._y))+"]"
		
	#Surcharge l'opérateur "="	
	def is_equal(self,x,y):
		if x==self._x and y==self._y:
			return True
		else:
			return False

"""
La classe QuadTree instancie des objets qui représentent les noeuds de l'arbre.
Ces objets sont initialisés avec des pointeurs sur enfant(s)/parent, la grille associée(l'endroit dans le plan) et
avec un ensembles contenant tous les bateaux(feuilles) de l'arbre.
"""			
class QuadTree:
	
	"""
	La classe grille instancie des objets qui indique "l'endroit" des noeuds de l'arbre.
	Ces objets sont initialisés avec des coordonnées qui déterminent les frontières du plan(grille).
	"""
	class grille:
		
		#CONSTRUCTEUR
		def __init__(self, x1=0,y1=0,x2=10315,y2=10315):
			self._x1=x1
			self._y1=y1
			self._x2=x2
			self._y2=y2
			self._grille=[self._x1,self._y1,self._x2,self._y2]
		
		#Méthode qui vérifie si le bateau est situé dans le plan représenté par la grille
		def contains(self,bateau):
			if self._x1 <= bateau._x and self._x2 >= bateau._x:
				if self._y1 <= bateau._y and self._y2 >= bateau._y:
					return True
				else:
					return False
			else:
				return False
	
	#CONSTRUCTEUR
	def __init__(self,grille=grille(), parent=None, NO=None, NE=None, SO=None,SE=None):
		self._NO = NO
		self._NE = NE
		self._SO = SO
		self._SE = SE
		self._parent = parent
		self._grille = grille._grille
		self._bateaux = set()

	#---------ACCESSEURS---------#
	
	#Méthode qui renvoit le noeuds associé au cadrant choisit
	def quad(self,ind):
		if ind == 0:
			return self._NO
		elif ind == 1:
			return self._NE
		elif ind == 2:
			return self._SO
		elif ind == 3:
			return self._SE
			
	
	#Méthode qui nous indique pour un QuadTree donné la position de ses enfants dans sont plan (NO,NE,SO,SE)
	#en attribuant 0 ou 1 
	def frontiere(self):
		nodes=[self._NO,self._NE,self._SO,self._SE]
		#Si c'est un bateau, il n'y a rien à faire.
		if isinstance(self,bateau):
			return True
		else:
			plan=[]
			for i in nodes:
				if i == None:
					plan.append("0")
				elif isinstance(i,QuadTree) or isinstance(i,bateau):
					plan.append("1")
			return "<"+str(' '.join('{}'.format(i) for i in plan))+">"

	#Méthode récursive qui renvoit la position dans l'arbre selon les coordonnées choisies.
	#Si un bateau est à cette endroit, elle retourne le bateau
	def trouve(self,x,y,niveau=0):
		boat=bateau(x,y)
		g=self.divide()
		niveau+=1
		#On trouve le cadrant dans lequel la bateau se situerai
		for i in range(4):
			if g[i].contains(boat):
				position = self.quad(i)
				break
		
		#Si à cet endroit, on a toujours un QuadTree, on continue de descendre dans l'arbre en redivisant la grille.
		if isinstance(position,QuadTree):
			position = position.trouve(x,y,niveau)
			return position
			
		#Retourne la position où le bateau devrait être, son parent 'self',
		#l'indice 'i' qui fait référence à un quadrant (voir setQuad()),
		#la grille du quadrant 'i' et la profondeur de la position
		return (position,self,i,g[i],niveau)
				
	#Méthode qui renvoit une liste des frères d'un noeud donné.
	def freres(self,noeud):
		parent = noeud._parent
		nomFrere=[]
		parent_plan=[parent._NO,parent._NE,parent._SO,parent._SE]
		for i in range(4):
			if parent_plan[i] != noeud and parent_plan[i] != None:
				nomFrere.append(parent_plan[i])
		return nomFrere

	#Méthode qui renvoit une liste d'indices représentant dans quel cadrant les frère bateaux du noeud choisit se trouvent
	def freres_bateaux(self,noeud):
		parent=noeud._parent
		numFrereBateau = []
		parent_plan=[parent._NO,parent._NE,parent._SO,parent._SE]
		#Si c'est un bateau et différent du noeud rentré, on ajoute sa position à la liste
		for i in range(4):
			if isinstance(parent_plan[i],bateau) and parent_plan[i] != noeud:
				numFrereBateau.append(i)
		return numFrereBateau

	#---------MODIFICATEURS---------#	
	
	
	#Méthode qui modifie un enfant d'un noeud donné
	def setQuad(self,i,new):
	
		#Si on veut enlever un enfant
		if new == None:
			if i == 0:
				self._NO = new
			if i == 1:
				self._NE = new
			if i == 2:
				self._SO = new
			if i == 3:
				self._SE = new
		
		#On vérifie le paramètre entré est bien un QuadTree/Bateau
		if isinstance(new,bateau) or isinstance(new,QuadTree):
			if i == 0:
				self._NO = new
				new._parent = self
				return self._NO
			elif i == 1:
				self._NE = new
				new._parent = self
				return self._NE
			elif i == 2:
				self._SO = new
				new._parent = self
				return self._SO
			elif i == 3:
				self._SE = new
				new._parent = self
				return self._SE
		
	#Méthode qui divise la grille en quadrants
	def divide(self):
		x1,y1,x2,y2=self._grille
		gNO=self.grille(x1,y1,x1+(x2-x1)/2,y1+(y2-y1)/2)
		gNE=self.grille((x2-x1)/2+x1,y1,x2,y1+(y2-y1)/2)
		gSO=self.grille(x1,y1+(y2-y1)/2,x1+(x2-x1)/2,y2)
		gSE=self.grille((x2-x1)/2+x1,y1+(y2-y1)/2,x2,y2)
		
		return [gNO,gNE,gSO,gSE]
				
	#Méthode qui insère une bateau avec coordonnées (x,y) dans l'arbre
	def inserer(self,x,y):
		b=bateau(x,y)
		self.inserer_bateau(b)
		
	#Méthode qui insère un bateau dans l'arbre
	def inserer_bateau(self,boat):
		#On trouve toutes les informations du noeud situé à l'endroit donné (coordonnées du bateau) 
		position,parent,ind,g,niveau=self.trouve(boat._x,boat._y)

		#S'il n'y a pas de bateau à cet endroit, on y insère le bateau
		if position == None:
			parent.setQuad(ind,boat)
			boat._parent = parent
			self._bateaux.add(boat)
			
		#S'il y a un bateau à cet endroit, on crée un nouveau noeud(divise la grille) et on réattribue un quadrant
		#à chaque bateau en rappellant la fonction. Elle sera rappellé jusqu'à temps qu'ils aient un quadrant chacun.
		elif isinstance(position,bateau):
			temp_bateau = position
			parent.setQuad(ind,QuadTree(g))
			parent.quad(ind)._parent = parent
			self.inserer_bateau(temp_bateau)
			self.inserer_bateau(boat)

	#Méthode qui réduit l'arbre. Elle est nécessaire lorsqu'on enlève un bateau ayant un unique bateau dans son "voisinage".
	#En d'autre termes, elle réduit la précision(c-à-d le nombre de fois qu'on divise une grille ou qu'on descent dans l'arbre) de 
	#l'emplacement d'un bateau si ce n'est plus nécessaire après la destruction d'un aure bateau "proche".
	def collapse(self,qnode,boat):
		if qnode != None:
			parent=qnode._parent
			nomFrere=self.freres(boat)
			if len(nomFrere) == 0 and parent != None:
				parent_plan = [parent._NO,parent._NE,parent._SO,parent._SE]
				for i in range(4):
					if parent_plan[i] == qnode:
						parent.setQuad(i,boat)
						parent.quad(i)._parent = parent
						self.collapse(parent,boat)

	#Méthode qui enlève un bateau de l'arbre avec les coordonnées (x,y)
	def enlever(self,x,y):
		b = bateau(x,y)
		self.enlever_bateau(b)
		
	#Méthode qui enlève un bateau de l'arbre
	def enlever_bateau(self,boat):
		#On trouve toutes les informations du noeud situé à l'endroit donné (coordonnées du bateau) 
		position,parent,ind,g,niveau=self.trouve(boat._x,boat._y)
		
		#Si la position trouvé n'a pas de bateau...Ne rien faire
		if position == None:
			return None

		#Sinon, s'il y a un bateau à cet endroit, on vérifie qu'ils aient les mêmes coordonnées
		elif position._x == boat._x and position._y == boat._y:
			#On accède à la liste des frères du bateau
			nomFrere=self.freres(position)
			numBateau = self.freres_bateaux(position)
			
			#S'il ne possède aucun frère, on enlève le bateau et on réduit l'arbre
			if len(nomFrere) == 0:
				self._bateaux.remove(position)
				grand_parent = parent._parent
				parent.setQuad(ind, None)
				self.collapse(grand_parent,parent)
				
			#Sinon, s'il possède un seul frère et que ce frère soit un bateau, on enlève le bateau et on 
			#collapse l'arbre avec l'unique frère
			elif len(nomFrere) == 1 and len(numBateau) == 1:
				seul=parent.quad(numBateau[0])
				self._bateaux.remove(position)
				parent.setQuad(ind,None)
				self.collapse(parent,seul)
			
			#Dans tout les autres cas, on a pas besoin de réduire l'arbre, on enlève simplement le bateau de l'arbre
			else:
				self._bateaux.remove(position)
				parent.setQuad(ind,None)
				
	#Méthode qui enlève tous les bateaux dans une zone donnée
	def zone_destruction(self,bombe):
		#On crée une copy de l'ensemble puisque la taille de cet ensemble
		#sera réduite pendant l'itération
		bateaux = set(self._bateaux)
		zone = self.grille(bombe[0],bombe[1],bombe[2],bombe[3])
		#On parcourt l'ensemble des bateaux
		for i in bateaux:
			if zone.contains(i):
				self.enlever_bateau(i)

	#Méthode qui affiche l'arbre, chaque ligne représente un niveau de l'arbre en commencant avec la racine.
	#Les noeuds internes sont représentés par <NO, NE, SO, SE> et les bateaux par [x y] où (x,y) sont les coordonnées
	#du bateau.
	def Afficher(self):
		q = queue.Queue()
		q.put(self)
		carte = []
		#Tout dépendant ce qu'on rencontre, soit Bateau/Noeud interne on affiche en conséquant.
		while q.empty() == False:
			tree = q.get()
			
			if isinstance(tree,bateau):
				carte.append(tree.coord())

			elif isinstance(tree,QuadTree):
				carte.append(tree.frontiere())
				q.put(";")
				q.put(tree._NO)
				q.put(tree._NE)
				q.put(tree._SO)
				q.put(tree._SE)
				
			else:
				carte.append(str(tree))
				
		coller = " ".join(carte)
		s = coller.split(";")
		print("\n".join(s)+"\n")

	#Méthode qui lit les coordonnées des bateaux dans un fichier texte et les insère dans l'arbre
	def lire_Bateaux(self):
		with open('positionsDesBateaux.txt') as f:
			for line in f:
				split=line.split()
				self.inserer(int(split[0]),int(split[1]))
	
	#Méthode qui, comme son nom l'indique si bien, lit les coordonnées des bombes dans un fichier texte
	#et les fait "exploser". On enlève les bateaux touchés de l'arbre.
	def faireToutSauter(self):
		with open('bombes.txt') as f:
			for line in f:
				split=line.split()
				bombes = [int(x) for x in split]
				self.zone_destruction(bombes)
	
	#Méthode qui lance le jeu.
	def jouer(self):
		self.lire_Bateaux()
		print("L'arbre avant la destruction : \n")
		self.Afficher()
		self.faireToutSauter()
		print("L'arbre après la destruction : \n")
		self.Afficher()

test = QuadTree()
test.jouer()



