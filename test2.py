

class bateau:
    def __init__(self,x,y):
        self._x=x
        self._y=y
    def coord(self):
        return "["+''.join('{} {}'.format(self._x,self._y))+"]"

class QuadTree:

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
        self._plan=[NO,NE,SO,SE]
        self._grille=grille._grille
        print(self._grille)

    ##plan of each node
    def frontiere(self):
        
        if isinstance(self,bateau):
            return True ## "["+str(' '.join('{},{}'.format(self._x,self._y))+"]"
        else:
            plan=[]
            for i in self._plan:
                if i ==None:
                    plan.append("0")
                elif isinstance(i,QuadTree) or isinstance(i,bateau):
                    plan.append("1")
            return "<"+str(' '.join('{}'.format(i) for i in plan))+">"

    ##----- accesors
##    def NO(self):
##        if isinstance(self._plan[0],QuadTree):
##            return self._plan[0].frontiere()
##        elif isinstance(self._plan[0],bateau):
##            return (self._plan[0]._x,self._plan[0]._y)
##        else:
##            return "None"
##    def NE(self):
##        if isinstance(self._plan[1],QuadTree):
##            return self._plan[1].frontiere()
##        elif isinstance(self._plan[1],bateau):
##            return (self._plan[1]._x,self._plan[1]._y)
##        else:
##            return "None"
##    def SO(self):
##        if isinstance(self._plan[2],QuadTree):
##            return self._plan[2].frontiere()
##        elif isinstance(self._plan[2],bateau):
##            return (self._plan[2]._x,self._plan[2]._y)
##        else:
##            return "None"
##    def SE(self):
##        if isinstance(self._plan[3],QuadTree):
##            return self._plan[3].frontiere()
##        elif isinstance(self._plan[3],bateau):
##            return (self._plan[3]._x,self._plan[3]._y)
##        else:
##            return "None"
##    def parent(self):
##        return self._parent    

    #--------methods

    def divide(self):
        gNO=self.grille(self._grille[0],self._grille[1],(self._grille[2])/2,(self._grille[3])/2)
        gNE=self.grille((self._grille[2])/2,self._grille[1],self._grille[2],(self._grille[3])/2)
        gSO=self.grille(self._grille[2],(self._grille[3])/2,(self._grille[2])/2,self._grille[3])
        gSE=self.grille((self._grille[2])/2,(self._grille[3])/2,self._grille[2],self._grille[3])
        
        return [gNO,gNE,gSO,gSE]

    def inserer(self,boat):
        grilles=self.divide()
        for i in range(4):
            if grilles[i].contains(boat):
                ind=i
                break
        if self._plan[ind] == None:
            self._plan[ind]=boat
        elif isinstance(self._plan[ind],bateau):
            temp_bateau = self._plan[ind]
            self._plan[ind]=QuadTree(grilles[ind])
            self._plan[ind]._parent=self
            self._plan[ind]._plan[0]=temp_bateau
            self.inserer(boat)
        elif isinstance(self._plan[i],QuadTree):
            nomBoat=0
            for j in range(1,4):
                if self._plan[i]._plan[j]==None:
                    self._plan[i]._plan[j]=boat
                    break
                nomBoat+=1
            if nomBoat==3:
                temp_bateau = self._plan[ind]
                self._plan[ind]._plan[0]=QuadTree(grilles[ind])
                self._plan[ind]._plan[0]._parent=self._plan[ind]
                self._plan[ind]._plan[0]._plan[0]=temp_bateau
                self._plan[ind].inserer(boat)
            

        self.frontiere()

                
                
        

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
            PrintT(tree._plan[0],niveau,init+1,carte)
            PrintT(tree._plan[1],niveau,init+1,carte)
            PrintT(tree._plan[2],niveau,init+1,carte)
            PrintT(tree._plan[3],niveau,init+1,carte)
            if init==niveau-1:
                print(' '.join('{}'.format(i) for i in carte))
    

test = QuadTree()
PrintT(test,0)
test.inserer(bateau(6000,60))
print("test.inserer(bateau(5,60))")
PrintT(test,0)
PrintT(test,1)
print("test.inserer(bateau(100,1000))")
test.inserer(bateau(100,1000))
test.inserer(bateau(2,3))
test.inserer(bateau(18,14))
test.inserer(bateau(15,16))
test.inserer(bateau(13,12))
PrintT(test,0)
PrintT(test,1)
PrintT(test,2)
PrintT(test,3)
PrintT(test,4)


##test.inserer(bateau(2,3))
##test.inserer(bateau(100,1000))
##test.inserer(bateau(18,14))


