import numpy as np
from scipy.signal import *
import matplotlib.pyplot as plt


j=complex(0,1)    

#la fonction synthétise un filtre dérivateur RIF à partir de la methode de la fenetre en utilisant une fenetre
#de hamming. On prend les 2M-1 premiers coefficents de la réponse impulsionnelle du filtre de réponse
#en fréquence 2*j*np.pi*f puis on multiplie par une fenetre de hamming.
#paramètre: M:taille de la fenetre, b: effet passe bas
#retour: filtre dérivateur 

def filtre_derivateur(M,b): #valeur usuel: fenetre de taille 2M-1=19, effet passe bas b=0.2
     n=np.arange(-M+1,M)
     n[M-1]=1 #On evite la division par 0 (n[m-1]=0 normalement)
     n[M-1]=1
     h=(-2*np.pi)*((np.sin(np.pi*n*b*2)/2)-np.pi*b*n*np.cos(np.pi*n*b*2))/((np.pi**2)*n**2) #reponse impulsionnel derivateur idéal
     h[M-1]=0 #(h0=0)
     h[M-1]=0
      
     return h*hamming(2*M-1) #methode de la fenetre

#effectue la dérivation d'un signal et conserve seulement les pics positifs. renvoie la dérivée seuillé en 0 et 
#la nouvelle echelle de temps calibrée pour l'affichage.
#paramètre:(sig=signal,M=taille de la fenetre du filtre rif,b=effet passe bas)
#retour: dérivée de sig

def derivateur(sig,M,b): #renvoie les pics 
    dtnf =lfilter(filtre_derivateur(M,b), 1,sig) 
    dtnf_ind = np.nonzero(dtnf>0) #on fixe le seuil de detection de pic a 0
    dtnf_ind=np.array(dtnf_ind) #on repasse en np.array
    dtnf=dtnf[dtnf_ind][0] 
    return dtnf
    
#renvoie la liste des pics positif de la dérivée, leur position, et la nouvelle echelle de temps calibrée 
#pour l'affichage. 
#paramètre: sig=signal
#retour: ind=renvoie la position en échantillons

def find_pic(sig): #liste des pics positifs de la dérivée
    dtnf=derivateur(sig,10,0.2) #M=10 et b=0.2 par defaut
    den = lfilter([+1,-1], 1, dtnf) 
    den = lfilter([+1,-1], 1, dtnf)
    den = np.sign(den)
    dden = lfilter([+1,-1], 1, den)
    ind = np.nonzero(dden==-2) #recherche des maximas
    ind = np.array(ind) -1 #on repasse en np.array
    pics=dtnf[ind][0] #listes des amplitudes des pics
    ind=ind[0] #liste des positions
    ind = np.array(ind) -1
    pics=dtnf[ind][0]
    ind=ind[0]
    return pics,ind #liste de pics et leur position ainsi que l'horloge calibré pour affichage