import numpy as np
import time as time
from collections import deque


def ListeVoisins(D:dict,M:list,sommet:str)->list:
    """Renvoie la liste des voisins de sommet dans le graphe"""
    return [voisin for voisin in D if M[D[sommet]][D[voisin]] > 0]

def SommetNonTraitéPlusProche(Dis:dict,T:list)->str:
    """Renvoie un sommet non traité (qui n’est pas dans T) dont la valeur dans Dis est minimale
    Remarque: plus tard, T sera un dictionnaire pour gagner du temps"""
    m = np.inf
    for sommet in Dis:
        if sommet not in T and Dis[sommet] <= m:
            m = Dis[sommet]
            smin = sommet
    return smin

def Dijkstra(D:dict,M:list,source:str)->list:
    """Algorithme de Dijkstra: trouve le plus court chemin de source à n’importe quel sommet"""
    T = []#liste des sommets traités
    Dis = {sommet:np.inf for sommet in D}
    Dis[source] = 0
    P = {source:source}
    while len(T) < len(Dis):
        smin = SommetNonTraitéPlusProche(Dis,T)
        T.append(smin)
        for voisin in ListeVoisins(D,M,smin):
            d = Dis[smin] + M[D[smin]][D[voisin]]#distance entre source et voisin si on passe smin
            if Dis[voisin] > d:
                Dis[voisin] = d
                P[voisin] = smin
    return Dis,P

def Dijkstra2(D:dict,M:list,source:str)->list:
    """Algorithme de Dijkstra: trouve le plus court chemin de source à n’importe quel sommet
    méthode plus rapide car T est maintenant un dictionnaire et vérifier si un élément est une clé dans un dictionnaire
    et plus rapide"""
    T = {}#dictionnaire dont les clés sont les sommets traités
    Dis = {sommet:np.inf for sommet in D}
    Dis[source] = 0
    P = {source:source}
    while len(T) < len(Dis):
        smin=SommetNonTraitéPlusProche(Dis,T)
        T[smin] = smin
        for voisin in ListeVoisins(D,M,smin):
            d = Dis[smin] + M[D[smin]][D[voisin]]#distance entre source et voisin si on passe smin
            if Dis[voisin] > d:
                Dis[voisin] = d
                P[voisin] = smin
    return Dis,P

def Itineraire(D:dict,M:list,source:str,but:str)->list:
    """Renvoie l'itinéraire dans le graphe du plus court chemin entre source et but"""
    Dis,P = Dijkstra2(D,M,source)#On prend la version la plus rapide
    Chemin = [but]#Liste des sommets à parcourir
    d = Dis[but]
    while but != source:
        but = P[but]
        Chemin.append(but)
    Itt = []#Chemin est à l'envers, L va contenir les éléments de Chemin en sens inverse
    for i in range(len(Chemin)):
        Itt.append(Chemin[len(Chemin)-1-i])
    return Itt,d#On renvoie le chemin et le temps de parcours

def StationsPlusEloignees2()->tuple:
    """Renvoie les deux stations les plus éloignés du métro parisien, utilise la fonction Djikstra2
    (dico pour T au lieu de Liste)"""
    Max = 0
    for source in D:
        Dis,P = Dijkstra2(D,M,source)
        for but in D:
            if Dis[but] > Max:
                Max,dep,arr = Dis[but],source,but             
    return Itineraire(D,M,dep,arr)

def StationsPlusEloignees3(fonc:callable)->tuple:
    """Renvoie les deux stations les plus éloignés du métro parisien, f est la fonction utilisée (Djikstra ou Dijkstra2)"""
    Max = 0
    for source in D:
        Dis,P = fonc(D,M,source)
        for but in D:
            if Dis[but] > Max and Dis[but]<np.inf:
                Max,dep,arr = Dis[but],source,but             
    return Itineraire(D,M,dep,arr)

def main():
    D = np.load('GrapheDictionnaire.npy',allow_pickle='True').tolist()#Dictionnaire Métro dans Paris
    M = np.load('GrapheMatrice.npy')#Matrice des distances entre deux stations de métro voisines

    DicoOptimal={}
    for source in D:
        P={}
        for voisin in ListeVoisins(D,M,source):
            P[voisin]=M[D[source]][D[voisin]]
        DicoOptimal[source]=P
    np.save('DicoOptimal.npy', DicoOptimal)

if __name__=="__main__":
    main()
