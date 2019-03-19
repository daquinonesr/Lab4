# Code to implement a B-tree 
# Programmed by Diego Quinones
# Last modified March 18, 2019

class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=3):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
        
def height(T):
    #Compute the height of the tree
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])
        
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)
        
def SortedList(T,L):
    #Extract the items in the B-tree into a sorted list.
    #checks if its at the bottom
    if T.isLeaf:
        for t in T.item:
            #adds value to the list
            L.append(t)
    else:
        for i in range(len(T.item)):
            #recursive call for when the values is not a leaf
            SortedList(T.child[i],L)
            L.append(T.item[i])
        SortedList(T.child[len(T.item)],L)
        
def MinAt(T,k):
    #Return the minimum element in the tree at a given depth d
    if k is 0:
        # it got to the desired depth
        return T.item[0]
    if T.isLeaf:
        #if it got to the bottom without being at depth k
        return -1
    #it is called again but with depth being reduced as it gets closer
    return MinAt(T.child[0],k-1)

def MaxAt(T,k):
    #Return the maximum element in the tree at a given depth d.
    if k is 0:
        # it got to the desired depth
        return T.item[-1]
    if T.isLeaf:
        #if it got to the bottom without being at depth k
        return -1
    #it is called again but with depth being reduced as it gets closer
    return MaxAt(T.child[-1],k-1)

def PrintAtDepth(T,k):
    # Prints items in tree in ascending order
    if k==0:
        for i in range(len(T.item)):
            print(T.item[i],end=' ')
    if T.isLeaf:
        return
    else:
        for i in range(len(T.item)):
            PrintAtDepth(T.child[i],k-1)
        PrintAtDepth(T.child[len(T.item)],k-1)  
        
def CountAtDepth(T,k):
    # Prints items in tree in ascending order
    a=0
    if k==0:
        #counts full leafes
        for i in range(len(T.item)):
            a=a+1
        return a
    else:
        for i in range(len(T.child)):
          #adds up every full leaf
           a=a+CountAtDepth(T.child[i],k-1)
    return a 


def SearchDepth(T,k):
    # Given a key k, return the depth at which it is found in the tree, of -1 if k is not in the tree.
    if k in T.item:
        return 0
    if T.isLeaf:
        return -1
    if k>T.item[-1]:
        return 1+SearchDepth(T.child[-1],k)
    else:
        return 1+SearchDepth(T.child[0],k)

def PrintLeafesFull(T):
    #Return the number of leaves in the tree that are full
    # counting value
    a=0
    if T.isLeaf:
        #counts full leafes
        if len(T.item) is T.max_items:
            return 1
    else:
        for i in range(len(T.child)):
          #adds up every full leaf
           a=a+PrintLeafesFull(T.child[i])
    return a
        
def PrintNodesFull(T):
    # Return the number of nodes in the tree that are full.
    #counting value
    a=0
    if T is None:
        return
    if not T.isLeaf:
        for i in range(len(T.child)):
            a=a+PrintNodesFull(T.child[i])
    if len(T.item)==T.max_items:
        #counts full nodes
        a=a+1
    return a


    
L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6]
T = BTree()    
for i in L:
    Insert(T,i)
Print(T)
PrintD(T,' ')
print()
print('1- Height:')
print('  ',height(T))
L1=[]
print('2- Sorted List',end=' ')
print()
SortedList(T,L1)
for i in L1:
    print(i,end=' ')
   
print()
print('3- Min At:')
print('  ',MinAt(T,1))
print('4- Max At:')
print('  ',MaxAt(T,1))
print('5- Count At Depth:')
print(CountAtDepth(T,2))
print('6- Print at Depth:')
PrintAtDepth(T,0)
print()
print('7- Full Nodes:')
print('  ',PrintNodesFull(T))
print('8- Full Leafes:')
print('  ',PrintLeafesFull(T))
print('9- Search Depth:')
print('  ',SearchDepth(T,200))

