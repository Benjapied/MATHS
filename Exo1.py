import matplotlib.pyplot as plt

def Phi1(teta):
    return ((teta - 1)**2) * (2*teta +1)
    
def Phi2(teta):
    return (teta**2) * (-2*teta + 3)

def Phi3(teta):
    return ((teta - 1) ** 2) * teta

def Phi4(teta):
    return teta**2 * (teta - 1)

def Hermite(xi, xi1, yi, yi1, zi, zi1, x):
    '''Xi, yi et zi sont respectivement xi, f(xi), f'(xi), de même pour xi1 = xi+1 '''
    oue2 = x - xi / (xi1 - xi)
    oue = yi * Phi1((x - xi) / (xi1 - xi)) + yi1 * Phi2((x - xi) / (xi1 - xi)) + (xi1 - xi) * zi * Phi3((x - xi) / (xi1 - xi)) + (xi1 - xi) * zi1 * Phi4((x - xi) / (xi1 - xi))
    return oue

def MakeList(a, b, nb):
    '''Créer une liste avec le nombre de points précisé dans nb entre a et b'''
    list = []
    for i in range(nb + 1):
        list.append(a + (b-a)/nb * i)

    return list
def MakeHermite(listX, listY, listZ, precision):
    '''Paramètres: liste des points et leur ordonnée ainsi que leur dérivé, précision est le nombre de points entre deux points'''
    newListX = []
    newListY = []

    for i in range(len(listX)):
        #On fait ici le processus entre deux points 

        iplus1 = i + 1

        if iplus1 > len(listX) - 1:
            iplus1 = 0

        point1 = listX[i] 
        point2 = listX[iplus1] 


        listeEntreDeuxPoints = MakeList(point1, point2, precision) #list qui contient les points entre xi et xi+1
        listTemp = [] #list qui va contenir les ordonnées après le passage de Hermite

        for j in range(len(listeEntreDeuxPoints)):
            ordonnee = Hermite(point1, point2, listY[i], listY[iplus1], listZ[i], listZ[iplus1], listeEntreDeuxPoints[j]) #pour chaque points entre xi et xi+1 on applique Hermite
            listTemp.append(ordonnee)

        

        #On concatene la liste trouvée dans la liste générale 
        newListX += listeEntreDeuxPoints
        newListY += listTemp

    return newListX, newListY


# hermiteListX = [2,5.6,4,8.6,7.6,9.6,8,6,2.6]
# hermiteListY = [7,6.8,9.6,8,5,5,3.2,2,2]
# hermiteListZ = [1,0.1,0.1,-2,-3,-5,0,3,-0.5]

# list1, list2 = MakeHermite(hermiteListX,hermiteListY,hermiteListZ, 100)

# #plt.axis((0, 20, 0, 20))
# plt.plot(list1,list2)
# plt.scatter(hermiteListX,hermiteListY)
# plt.show()