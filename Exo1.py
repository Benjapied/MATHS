import matplotlib.pyplot as plt
import math 

def Fi1(teta):
    return (teta - 1)**2 * (2*teta +1)

def Fi2(teta):
    return (teta**2) * (-2*teta + 3)

def Fi3(teta):
    return (teta - 1) ** 2 * teta

def Fi4(teta):
    return teta**2 * (teta - 1)

def Hermite(xi, xi1, yi, yi1, zi, zi1, x):
    '''Xi, yi et zi sont respectivement xi, f(xi), f'(xi), de même pour xi1 = xi+1 '''
    oue = yi * Fi1(x - xi / xi1 - xi) + yi1 * Fi2(x - xi / xi1 - xi) + (xi1 - xi) * zi * Fi3(x - xi / xi1 - xi) + (xi1 - xi) * zi1 * Fi4(x - xi / xi1 - xi)
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

    for i in range(len(listX) - 1):
        #On fait ici le processus entre deux points 

        point1 = listX[i] 
        point2 = listX[i+1] 

        if point1 > point2:
            point2 = listX[i]
            point1 = listX[i+1]

        listeEntreDeuxPoints = MakeList(point1, point2, precision) #list qui contient les points entre xi et xi+1
        listTemp = [] #list qui va contenir les ordonnées après le passage de Hermite

        for j in range(len(listeEntreDeuxPoints)):
            
            ordonnee = Hermite(point1, point2, listY[i], listY[i + 1], listZ[i], listZ[i + 1], listeEntreDeuxPoints[j]) #pour chaque points entre xi et xi+1 on applique Hermite
            listTemp.append(ordonnee)

        if listX[i] > listX[i+1]:
            listTemp.reverse()

        #On concatene la liste trouvée dans la liste générale 
        newListX += listeEntreDeuxPoints
        newListY += listTemp

    return newListX, newListY


hermiteListX = [9,30,18,43,37,47,48,29,30,10,9]
hermiteListY = [30,35,48,42,30,27,20,13,9,15,30]
hermiteListZ = [0,0,0,0,0,0,0,0,0,0,0]

list1, list2 = MakeHermite(hermiteListX,hermiteListY,hermiteListZ, 10)

#plt.axis((0, 50, 0, 50))
plt.plot(list1,list2)
plt.show()