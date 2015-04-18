import copy
import queue
class bateau:
    """bateau représenté par les coordonnées x et y"""
    def __init__(self,x,y,parent=None):
        self._x=x
        self._y=y
        self.parent=parent
    def coord(self):
        return "["+''.join('{} {}'.format(self._x,self._y))+"]"
    def is_equal(self,x,y):
        if x==self._x and y==self._y:
            return True
        else:
            return False

class QuadTree:
    

    class grille:
        """grille limite le territoire des QuadTrees
        la taille du QuadTree racine est 10315x10315
        """
        
        def __init__(self, x1=0,y1=0,x2=10315,y2=10315):
            self._x1=x1
            self._y1=y1
            self._x2=x2
            self._y2=y2
            self._grille=[self._x1,self._y1,self._x2,self._y2]

        def contains(self,bateau):
            """évalue si la grille contient les coordonnées du bateau
            """

            if self._x1<bateau._x and self._x2>bateau._x:
                if self._y1<bateau._y and self._y2>bateau._y:
                    return True
                else:
                    return False
            else:
                return False
    def list_bateaux(self):
        b=list(set(self.bateaux))
        self.bateaux=b
        return b
    bateaux=[]

    #constructor
    def __init__(self,grille=grille(), parent=None, NO=None, NE=None, SO=None,SE=None):
        self._NO=NO
        self._NE=NE
        self._SO=SO
        self._SE=SE
        self._parent=parent
        self._grille=grille._grille

    def frontiere(self):
        """contenu de chaque QuadTree dans leur grille
        NO, NE, SE et SO  prennent la	valeur 1 s’il existe un enfant
        associé	à ce pointeur ou la valeur 0 si ce pointeur est null. Un
        bateau est encodée aves ses coordonnées
        """
        
        nodes=[self._NO,self._NE,self._SO,self._SE]
        if isinstance(self,bateau):
            return True ## "["+str(' '.join('{},{}'.format(self._x,self._y))+"]"
        else:
            plan=[]
            for i in nodes:
                if i ==None:
                    plan.append("0")
                elif isinstance(i,QuadTree) or isinstance(i,bateau):
                    plan.append("1")
            return "<"+str(' '.join('{}'.format(i) for i in plan))+">"

    ##----- accesors
    def quad(self,ind):
        """
        quadrant (ou fils) du QuadTree d'après ind
        """
        if ind==0:
            return self._NO
        elif ind==1:
            return self._NE
        elif ind==2:
            return self._SO
        elif ind==3:
            return self._SE

    #--------methods
        
    def setQuad(self,i,new):
        """
        assigne 'new' à un quadrant selon indice 'i'
        """
        if i==0:
            self._NO=new
            if isinstance(new,bateau) or isinstance(new,QuadTree):
                new._parent=self
            return self._NO
        elif i==1:
            self._NE=new
            if isinstance(new,bateau) or isinstance(new,QuadTree):
                new._parent=self
            return self._NE
        elif i==2:
            self._SO=new
            if isinstance(new,bateau) or isinstance(new,QuadTree):
                new._parent=self
            return self._SO
        elif i==3:
            self._SE=new
            if isinstance(new,bateau) or isinstance(new,QuadTree):
                new._parent=self
            return self._SE
        
    def freres(self,boat):
        """
        compte les frères si 'boat' en a.
        """
        parent=boat._parent
        nomFrere=[]
        parent_plan=[parent._NO,parent._NE,parent._SO,parent._SE]
        for i in range(4):
            if isinstance(parent_plan[i],bateau) and parent_plan[i]!=boat:
                nomFrere.append(i)
        return nomFrere

        
        
    def divide(self):
        """
        divide en quatre la grille et assigne les parties à chaque quadrant
        """
        x1,y1,x2,y2=self._grille
        gNO=self.grille(x1,y1,x1+(x2-x1)/2,y1+(y2-y1)/2)
        gNE=self.grille((x2-x1)/2+x1,y1,x2,y1+(y2-y1)/2)
        gSO=self.grille(x1,y1+(y2-y1)/2,x1+(x2-x1)/2,y2)
        gSE=self.grille((x2-x1)/2+x1,y1+(y2-y1)/2,x2,y2)
        
        return [gNO,gNE,gSO,gSE]

    def trouve(self,x,y,niveau=0):
        """
        retourne la position d'un bateau de coordonées x et y où un place vide
        pour le mettre
        """
        boat=bateau(x,y)
        g=self.divide() #divise la grille du présent quadrant
        niveau+=1
        for i in range(4):
            if g[i].contains(boat):
                position=self.quad(i) #quadrant qui contient les coordones du bateau
                break
            
        if isinstance(position,QuadTree):# appeal recursive pour trouver le bateau
                                         #(où un place vide) dans un enfant QuadTree
            position=position.trouve(x,y,niveau)
            return position
        else:
            #retourne la position où le bateau devrait être, son parent 'self',
            #l'indice 'i' qui fait réferance à un quadrant (voir setQuad())
            #la grille du quadrant 'i' et le profondeur de la position
            return (position,self,i,g[i],niveau)
            
            
    def inserer(self,tup):
        b=bateau(tup[0],tup[1])
        self.inserer_bateau(b)
    def inserer_bateau(self,boat):
        """
        insertion d'un bateau 'boat' avec coordonees x,y
        """
        #position où bateau devrait être
        position,parent,ind,g,niveau=self.trouve(boat._x,boat._y)

        if position==None: #si la position et vide on y place le bateau
            parent.setQuad(ind,boat)               
            self.bateaux.append((boat._x,boat._y))
            
        elif isinstance(position,bateau): #si la position est un bateau on transforme
                                      #le quadrant(position) dans une QuadTree et
                                      #on fait un appeal recursive pour mettre les vieux
                                      #et nouveau bateau 'boat'
            temp_bateau = position
            parent.setQuad(ind,QuadTree(g))
            self.inserer_bateau(temp_bateau)
            self.inserer_bateau(boat)

    def collapse(self,qnode,boat=None):
        parent=qnode._parent
        if parent!=None:
            parent_plan=[parent._NO,parent._NE,parent._SO,parent._SE]
            for i in range(4):
                if parent_plan[i]==qnode:
                    ind=i
                    parent.setQuad(i,boat)
                    nomFrere=self.freres(boat)
                    if len(nomFrere)==0:
                        self.collapse(parent,boat)


    def enlever(self,tup):
        b=bateau(tup[0],tup[1])
        self.enlever_bateau(b)
    def enlever_bateau(self,boat):
        """
        deletion d'un bateau 'boat' avec coordonees x,y
        """
        #position où bateau devrait être
        position,parent,ind,g,niveau=self.trouve(boat._x,boat._y)
        
        if position==None:
            return None

        #evalue si la position a les mêmes coordonées du bateau
        elif position._x==boat._x and position._y==boat._y:
            nomFrere=self.freres(position)
            if len(nomFrere)<=1:
                if len(nomFrere)==1: #si le bateau a un seul frère, on fait un
                                     #copie de son frère et on collapse le
                                     #sous-arbre
                    seul=parent.quad(nomFrere[0])
                    parent.setQuad(ind,None)
                    
                    self.collapse(parent,seul)
                else: #position va prendre None comme valeur et on collapse
                    parent.setQuad(ind,None)
                    
                    self.collapse(parent,position)
            else: #si le bateau a plus qu'un frère on ne collapse pas le sous-
                  #arbre
                parent.setQuad(ind,None)

    def zone_destruction(self,bombe):
        it=list(set(self.bateaux))
        x1,y1,x2,y2=bombe
        zone=self.grille(x1,y1,x2,y2)
        detruits=[]
        for i in it:
            if zone.contains(i):
                detruit.append(i)
        return detruits
    
        
        
        

    def Afficher(self):
        """
        affichage de tous les noeuds de l'arbre par 'first depth search'
        """
        q=queue.Queue()
        q.put(copy.copy(self))
        carte=[]
        enf=0
        ind=0
        while q.empty()==False:
            tree=q.get()
            if tree==None:
                carte.append('n')
            elif isinstance(tree,bateau):
                carte.append(tree.coord())
                ind+=1
            else:
                if isinstance(tree,str):
                    carte.append(tree)
                elif isinstance(tree,QuadTree):
                    carte.append(tree.frontiere())
                    
                    if enf==ind:
                        q.put(";")
                        enf=0
                        ind=0
                    
                    ind+=1
                    for i in [tree._NO,tree._NE,tree._SO,tree._SE]:
                        if i!=None:
                            enf+=1
                    q.put(tree._NO)
                    q.put(tree._NE)
                    q.put(tree._SO)
                    q.put(tree._SE)
        coller = " ".join(carte)
        s=coller.split(";")
        print("\n".join(s))

content=[]
with open('positionDesBateaux.txt') as f:
    for line in f:
        split=line.split()
        pair = [ int(x) for x in split ]
        tup=tuple(pair)
        content.append(tup)
tree=QuadTree()
for i in content:
    tree.inserer(i)

tree.Afficher()
tree.list_bateaux()
print(tree.bateaux)
##test.enlever(15,16)
##test.enlever(2,3)
##test.enlever(18,14)
##test.enlever(1000,1000)
##test.enlever(6000,60)
##tree.Afficher()

##tree.zone_destruction((6,4,3,5))



##test = QuadTree()

##test.inserer(6000,60)
##test.inserer(1000,1000)f
##test.inserer(18,14)
##test.inserer(2,3)
##test.inserer(15,16)
####test.inserer(7000,100)
##test.Afficher()



##test.enlever(15,16)
##
##test.enlever(2,3)
##test.enlever(18,14)
##
##test.enlever(1000,1000)
##test.enlever(6000,60)



##print("0: ")
##PrintT(test,0)
##print("1: ")
##PrintT(test,1)
##print("2: ")
##PrintT(test,2)
##print("3: ")
##PrintT(test,3)
##print("4: ")
##PrintT(test,4)
##print("10: ")
##PrintT(test,10)
##print("11: ")
##PrintT(test,11)


