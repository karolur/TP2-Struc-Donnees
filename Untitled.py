

class bateau:
    def __init__(self,x,y):
        self._x=x
        self._y=y

class QuadTree:

##    class _Node: ##private class to keep all the 4 children
##        def __init__(self, racine=None, NO=None, NE=None, SO=None,SE=None):
##            self._parent=parent
##            self._NO=NO
##            self._NE=NE
##            self._SO=SO
##            self._SE=SE

    class grille:

        def __init__(self, x1=0,y1=0,x2=10315,y2=10315):
            self._x1=x1
            self._y1=y1
            self._x2=x2
            self._y2=y2
            self._grille=[self._x1,self._y1,self._x2,self._y2]

        def contains(self,bateau):
            if self._x1<bateau._x and self._x2>bateau._x:
                if self._y1<bateau._y and self._y2>bateau._y:
                    return True
            else:
                return False
    

    #constructor
    def __init__(self,grille=grille(), parent=None, NO=None, NE=None, SO=None,SE=None):
   
        self._parent=parent
        self._NO=NO
        self._NE=NE
        self._SO=SO
        self._SE=SE
        self._plan=[self._NO,self._NE,self._SO,self._SE]
        self._grille=grille._grille
        print(self._grille)

    ##plan of each node
    def frontiere(self):
        plan=[]
        for i in self._plan:
            if i ==None:
                plan.append("0")
            elif isinstance(i,QuadTree):
                plan.append("1")
            else:
                plan.append("f")
        return "<"+str(' '.join('{}'.format(i) for i in plan))+">"

    #--------methods

    def divide(self):
        gNO=self.grille(self._grille[0],self._grille[1],(self._grille[2])/2,(self._grille[3])/2)
        gNE=self.grille((self.grille()._x2)/2,self.grille()._y1,self.grille()._x2,(self.grille()._y2)/2)
        gSO=self.grille(self.grille()._x2,(self.grille()._y2)/2,(self.grille()._x2)/2,self.grille()._y2)
        gSE=self.grille((self.grille()._x2)/2,(self.grille()._y2)/2,self.grille()._x2,self.grille()._y2)
        
        return [gNO,gNE,gSO,gSE]

    def inserer(self,boat):
        grilles=self.divide()
        for i in range(3):
            if grilles[i].contains(boat):
                ind=i
                break
        if self._plan[ind] == None:
            self._plan[ind]=boat
        elif isinstance(self._plan[ind],bateau):
            temp_bateau = self._plan[ind]
            self._plan[ind]=QuadTree(grilles[ind])
            print(type(self._NO))
            print(type(self._plan[ind]))
            self._plan[ind]._parent=self
            self._plan[ind]._NO=temp_bateau

            

        self.frontiere()

                
                
        

def PrintT(tree,niveau,init=0):
    if(tree==None):
        return "nada"
    elif(init==niveau):
        print(tree.frontiere())
    else:
        PrintT(tree._NO,niveau,init+1)
        PrintT(tree._NE,niveau,init+1)
        PrintT(tree._SO,niveau,init+1)
        PrintT(tree._SE,niveau,init+1)

test = QuadTree()
PrintT(test,0)
p=bateau(5,60)
test.grille().contains(p)
test.inserer(p)
PrintT(test,0)
test.inserer(bateau(2,3))
##test.inserer(bateau(100,1000))
##test.inserer(bateau(18,14))
PrintT(test,0)
PrintT(test,1)


