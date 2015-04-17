
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
    def compare_pos(self,b1,b2):
        if b1._x<b2._x:
            return (b1,b2)
        elif b1._x>b2._x:
            return (b2,b1)
        elif b1._x==b2._x:
            if b1._y<b2._y:
                return (b1,b2)
        elif b1._y>b2._y:
            return (b2,b1)

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
    points=[]

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
        assigne 'new' à un quadrant
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
        
    def fils_unique(self,boat):
        parent=boat._parent
        parent_plan=[parent._NO,parent._NE,parent._SO,parent._SE]
        for i in parent_plan:
            if isinstance(i,bateau) and i!=boat:
                return False
            elif isinstance(i,QuadTree):
                return False
            else:
                return True
        
        
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
        boat=bateau(x,y)
        g=self.divide() #divise la grille du présent quadrant
        niveau+=1
        for i in range(4):
            if g[i].contains(boat):
                position=self.quad(i) #quadrant qui contient les coordones du bateau
                break
            
        if isinstance(position,QuadTree):
            position=position.trouve(x,y,niveau)
            return position
        else:

            return (position,self,i,g[i],niveau)
            
            

        
        

    def inserer(self,boat):
        position,parent,ind,g,niveau=self.trouve(boat._x,boat._y)
        if position==None: #si le quadrant et vide on y place le bateau
            parent.setQuad(ind,boat)
            self.points.append(boat)
            
        elif isinstance(position,bateau): #si le quadrant est un bateau on transforme
                                      #le quadrant dans une QuadTree pour mets le
                                      #son vieux bateau dans le prémier quadrant
                                      #et fait un appeal recursive pour inserer 'boat'
            temp_bateau = position
            parent.setQuad(ind,QuadTree(g))
            self.inserer(temp_bateau)
            self.inserer(boat)


    def enlever(self,x,y):
        existe=False
        for i in self.points:
            if i.is_equal(x,y):
                boat=i
                parent=boat._parent
                existe =True
                break
        if existe==False:
            return "bateau n'existe pas"
        else:
            plan=[parent._NO,parent._NE,parent._SO,parent._SE]
            print(parent.frontiere())
            for i in range(4):
                if plan[i]==boat:
                    ind=i
            if self.fils_unique(boat)==False:
                self.points.remove(boat)
                parent.setQuad(ind,None)
            else:
                self.points.remove(boat)
                parent.setQuad(ind,boat)
                if self.fils_unique(parent):
                    self.enlever(parent)
                               
        

def PrintT(tree,niveau,init=0,carte=None):
    if carte==None:
        carte=[]
    if(tree==None):
        carte.append("None")
    elif(init==niveau):
        if isinstance(tree,bateau):
            carte.append(tree.coord())
        else:
            carte.append(tree.frontiere())
        if niveau==0:
            print(' '.join('{}'.format(i) for i in carte))
    else:
        if isinstance(tree,bateau):
            carte.append(tree.coord())
        else:
            PrintT(tree._NO,niveau,init+1,carte)
            PrintT(tree._NE,niveau,init+1,carte)
            PrintT(tree._SO,niveau,init+1,carte)
            PrintT(tree._SE,niveau,init+1,carte)
            if init==niveau-1:
                print(' '.join('{}'.format(i) for i in carte))
    



##test = QuadTree()
##test.inserer(bateau(6000,60))
##PrintT(test,0)
##PrintT(test,1)
##test.inserer(bateau(100,1000))
##PrintT(test,0)
##PrintT(test,1)
##test.inserer(bateau(100,6000))
##PrintT(test,0)
##PrintT(test,1)
##test.inserer(bateau(6000,6000))
##PrintT(test,0)
##PrintT(test,1)
##test.inserer(bateau(7000,7000))
##PrintT(test,0)
##PrintT(test,1)
##PrintT(test,3)

test = QuadTree()
test.inserer(bateau(6000,60))
PrintT(test,0)
test.inserer(bateau(1000,1000))
PrintT(test,1)
test.inserer(bateau(2,3))
print("niveau 4")
PrintT(test,4)
test.inserer(bateau(18,14))
PrintT(test,4)
PrintT(test,10)
test.inserer(bateau(15,16))
PrintT(test,4)
PrintT(test,10)
PrintT(test,11)


##PrintT(test,2)
##test.inserer(bateau(13,12))
##print('siiii')
##PrintT(test,0)
##PrintT(test,1)
##PrintT(test,2)
##print('4')
##PrintT(test,4)
##PrintT(test,5)
##print('10')
##PrintT(test,10)
##PrintT(test,11)
##PrintT(test,12)
##print(test.trouve(1000,1000))
##test.enlever(13,12)
##
##PrintT(test,3)
##PrintT(test,2)
##test.enlever(100,1000)
##PrintT(test,3)
##PrintT(test,2)




##test.inserer(bateau(2,3))
##test.inserer(bateau(100,1000))
##test.inserer(bateau(18,14))


