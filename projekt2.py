import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sys


#Przyznaję, że nie napisałem sam kawałka poniżej, tylko go znalazłem na StackExchange.
#Ale jest bardzo zwięzły, więc postanowiłem go zostawić
def conv2d(a, f):
    #to tworzy 4-wymiarową n-tkę. Dwie pierwsze liczby to wymiary f, dwie kolejne to 
    #liczba podmacierzy wymiaru f.shape w macierzy a. Np jak a to macierz 5x5, a f 3x3, to dostajemy
    # (3,3,3,3), bo w macierzy a mozemy utworzyc po 3 podmacierze wymiarow 3x3 w kazdym wierszu i kolumnie
    s = f.shape + tuple(np.subtract(a.shape, f.shape) + 1)   
    #nazwanie funkcji inaczej
    strd = np.lib.stride_tricks.as_strided
    ##
    subM = strd(a, shape = s, strides = a.strides * 2)
    ##To jest convolution macierzy subM z macierzą f.
    # W naszym przypadku to aplikuje operator Sobela do kazdego pixela razem z ośmioma pixelami 
    #przylegającymi dla f=sobelx, a=a. Potem zwraca macierz 
    return np.einsum('ij,ijkl->kl', f, subM)
#wykrywanie krawedzi metodą operatorów Sobela
#Dzialamy na kazdy pixel operatorem Sobela, bierzemy pierwiastek z kwadratów skladowych
#Krawedz to pixele o wartosci > threshold    
def krawedzie(img):
    pionowe = conv2d(img, sobely)
    poziome = conv2d(img, sobelx)
    krawedzie = np.sqrt(np.square(poziome)+np.square(pionowe))
    krawedzie = np.where(krawedzie< threshold, 0, 255)    
    return krawedzie
#funkcja zwracajaca kąt gradientu kazdego pixela, a dokladniej cala macierz katow
def katy(img):
    krawedz = krawedzie(img)
    pionowe = conv2d(img, sobely)
    poziome = conv2d(img, sobelx)
    
    listapionowe = pionowe[krawedz !=0]
    listapoziome = poziome[krawedz !=0]
    #Gdy gradient w kierunku x nie jest równy zero, mozemy podzielic i policzyc kat
    #z arctan
    poziomeniezero = listapoziome[listapoziome != 0]
    pionoweniezero = listapionowe[listapoziome !=0]
    rozklad1 = np.arctan(np.divide(pionoweniezero, poziomeniezero))
    
    #tutaj gradient w kierunku x=0, wiec nie mozemy podzielic elementów przez siebie
    znakipionowe = np.sign(listapionowe[listapoziome == 0])
    znakipionowe = np.pi*znakipionowe
    rozklad = np.concatenate((rozklad1,znakipionowe), axis=None)
    return rozklad
    

        


    
    #próg tolerancji. 70 działa całkiem dobrze.
threshold = 70
sobely = np.array(([1,2,1],[0,0,0],[-1,-2,-1]) )
sobelx = np.swapaxes(sobely,0,1)
try:
    nazwa = sys.argv[1]
except IndexError:
    nazwa = input('Podaj nazwe pliku \n')
except FileNotFoundError:
    nazwa = input('Brak takiego pliku. Spróbuj ponownie. \n')
        
image = Image.open(nazwa)    
image = image.convert('L')
image = np.array(image)

#operatory Sobela wykrywający krawędzie
gaussianblur = np.array(([1/16,1/8,1/16],[1/8,1/4,1/8],[1/16,1/8,1/16]))
zdjecie = krawedzie(image)
output = Image.fromarray(np.uint8(zdjecie)).convert('L')
output.show()


#wykresy
#Tam gdzie krawędź została wykryta mamy 'nachylenie' danego pixela, tam gdzie krawedzi
# nie ma, będzie wartosc 5, ktora nie bedzie wplywac na 
rozkladkatow = katy(image)
rozkladkatow = (180/(np.pi))*rozkladkatow
przedzial = np.linspace(-np.pi,np.pi,50)
przedzial = (180/(np.pi))*przedzial

plt.hist(rozkladkatow, przedzial)
plt.xlabel('Radiany')
plt.ylabel('Gęstość występowania')
plt.show()
