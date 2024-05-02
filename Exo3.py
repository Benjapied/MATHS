import matplotlib.pyplot as plt

#On considère un sous marin avec une forme de capsule d'une longueur de 12m de long et 2 de haut
#
#    _______  ^ 2m
#   (_______) v
#   <------->
#       10m
#
#On estime sa masse à 200 tonnes
#Plusieures forces externes s'appliquent à ce sous marin:
#  - Le poid équivalent à 1,96x10**6 Newtons avec l'eau dans les doubles murs
#  - La poussée d'achimède équivalent à 997kg/m3 (masse volumique eau) * 104m3 (volume sous-marin) * 9.8 N/kg (g)
#  - Une poussé vers l'arrière simulant les frottements de l'eau 
#  - La poussée des moteurs vers l'avants



class SousMarin() :
    '''Contient toutes les infos du sous-marin'''
    def __init__(self):

        self.x = 0
        self.y = 0

        self.volume = 104 #en m3
        self.poids = 1960000
        self.pousseeDarchimede = 1020000
        self.forceMoteur = 100
        self.damping = 25
        self.airRelease = 0

        self.speed = 1

    def StabiliseNautilus(self):
        '''Calcule la quantité d'eau à relacher pour stabiliser le sous-marin sur y'''
        counterM3 = 0

        p = self.poids
        archi = self.pousseeDarchimede

        while p > archi:

            self.RelacherEau()

        self.poids = p
        self.volume = self.volume - counterM3

        return counterM3 

    def VecteurVertical(self):
        '''return la force verticale appliquée au sous-marin'''
        return (997 * 9.8 * self.volume) - self.poids
    
    def VecteurHorizontal(self):
        '''return la force horizontale appliquée au sous-marin'''
        return self.forceMoteur * self.speed - self.damping * self.speed

    def RelacherEau(self):
        '''On relache 1m3 d'eau'''
        self.airRelease += 1
        self.pousseeDarchimede = 997 * 9.8 * 104 + self.airRelease
        self.poids =- 9806 #on ne prend pas la différence entre eau et air car négligeable

    def Accelere(self):
        '''On accélère et on monte les moteurs'''
        self.forceMoteur += 15

    def Descélère(self):
        '''On baisse les moteurs et la speed baisse'''
        self.forceMoteur -= 15

    def UpdateSpeed(self):
        '''On update la speed'''
        self.speed = self.forceMoteur - self.damping

def TrajNautilus(nb, nautilus):
    x = []
    y = []

    #au départ le sous-marin veut déscendre, donc il va se laisser couler, puis lorsqu'il atteindra une hauteur d'environ -50m
    #il va lacher de l'air 

    for i in range(nb):        
        x.append(nautilus.x)
        y.append(nautilus.y)

        nautilus.Accelere()
        nautilus.UpdateSpeed()

        #if nautilus.poids > nautilus.pousseeDarchimede:
        #    nautilus.RelacherEau()

        nautilus.x = nautilus.x + nautilus.VecteurHorizontal() 
        nautilus.y = nautilus.y + nautilus.VecteurVertical()

    return x,y
    
nautilus = SousMarin()

listx, listY = TrajNautilus(10, nautilus)

plt.plot(listx,listY)
plt.scatter(listx,listY)
plt.show()

