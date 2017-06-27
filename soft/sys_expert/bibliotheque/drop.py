#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 13:49:58 2017

@author: Jane
"""
import numpy as np
from scipy.signal import *

from math import *
import matplotlib.pyplot as plt

import scipy.fftpack as scfft

from scipy.signal import *


#paramètres: signal à échantillonner, frequence d'échantillonnage de ce signal, facteur d'échantillonnage
#sorties : le signal sous-echantillonné, le temps sous-échantilonné, la nouvelle frequence d'echantillonnage
#Si on veut sous-échantillonner un signal par k, on prend 1 élément de la liste chaque k
#la fonction ci-dessous sous-échantillonne le signal, l'array de temps associé,
#et renvoie la nouvelle valeur de la fréquence d'échantillonnage,
#celle-ci devient plus petite, elle est divisée par k
def sous_ech(signal, time, fe, ech) :
    return signal[::ech], time[::ech], fe*1.0/ech


#paramètres : le signal à filter, T le temps de convergence du filtre voulue
#sortie: le signal filtré
#calculer l'énergie du signal revient à faire la convolution du signal au carré par hn
#hn est la suite des a puissance n pour n supérieur à zéro ou nul
#par défaut fe=44100
#on choisit a pour que le filtre converge vite en T
#il converge quand exp(n*ln(a))=exp(T*fe*ln(a)) est presque nul (0.01 par exemple)
#ceci converge après trois tho, où le temps caractéristique est ici -1/(fe*ln(a))
#il faut donc a tel que -3/(fe*ln(a))=T puis a =exp(-3/(fe*T))
#par exemple pour T=0.01s à fe=44100hz on a a=0.9932
#on utilise lfilter de scipy.signal qui convolue hn avec signal**2
def detect_env(signal, time,fe) :
    a=0.99995
    ech=len(signal)
    energie = np.zeros(ech)
    energie[0]= signal[0]
    n=0
    for n in range (1, ech):
        energie[n]=a*energie[n-1]+ (1.0-a)*(signal[n]**2)
    #energie=energie/max(energie)
    echantillonnage=100
    time, energie = time[::echantillonnage], energie[::echantillonnage]
    fe=fe*1.0/echantillonnage
    energie =lfilter(np.hanning(100),1,energie)
    return energie, time,fe

"""
def detect_env(signal, time, fe, T) :
    a=np.exp(-3.0/(fe*T))
    signal_carre =np.square(signal)
    energie = lfilter([1], [1,-a], signal_carre)
    #n=2000
    #energie = lfilter(np.ones(n)*1.0/n,1,signal_carre)
    energie = energie[::100]
    time=time[::100]
    #energie =lfilter(np.hanning(100),1,energie)
    return energie, time, fe
"""

#detection_creux trouve tous les creux dans le signal d'entrée, en applicant deux filtres successifs (dérivée seconde)
#après l'application de ces deux filtres, quand on trouve la valeur 2 on est en présence d'un creux 
#les résultats sont décalés d'un échantillons, donc on enlève 1 
def detection_creux(signal) :
    den = lfilter([+1,-1], 1, signal)
    den = np.sign(den)
    dden = lfilter([+1,-1], 1, den)
    ind = np.nonzero(dden==2)
    ind = np.array(ind) -1
    return ind[0]
            

#fonction de sélection des creux pouvant correspondre à un drop dans "signal"
#c'est une extension de selection_creux
#ceci doit fonctionner en temps réel donc on compare les creux à ceux d'avant
#on décide que si un creux et inférieur aux 5 pics d'avant, il est susceptible d'être un drop
#on ne vérifie donc que ceci pour les creux à partir du 6 ème creux

def selection_creux(signal, n) :
    den = lfilter([+1,-1], 1, signal)
    den = np.sign(den)
    dden = lfilter([+1,-1], 1, den)
    ind = np.nonzero(dden==2)
    ind= np.array(ind) -1
    ind=ind[0]
    creux = []
    for i in range (5, len(ind)) :
        compteur =0
        for k in range (1,6) :
            if (signal[ind[i]]<signal[ind[i-k]]):
                compteur=compteur+1
        if (compteur == 5) : 
            creux.append(ind[i])
    return creux


#fonction qui annonce qu'il pourrait y avoir un creux qui correspond à un drop dans le signal
#parce que notre système fonctionne en temps réel, il est mieux de répondre True ou False, plutôt qu'un indice
#qui correspond à un moment qui est déjà passé.
#cette fonction sera appelée sur des échantillons de 5 secondes chaque x ms
#elle fonctionne sur le même principe que la fonction précédente
#cependant, si on détecte au moins un creux susceptible d'être un drop,
#la fonction répond simplement True

def is_creux(signal, time, fe, n) :
    signal = detect_env(signal, time, fe)[0]
    den = lfilter([+1,-1], 1, signal)
    den = np.sign(den)
    dden = lfilter([+1,-1], 1, den)
    ind = np.nonzero(dden==2)
    ind= np.array(ind) -1
    ind=ind[0]
    creux = []
    for i in range (n, len(ind)) :
        compteur =0
        for k in range (1,n+1) :
            if (signal[ind[i]]<signal[ind[i-k]]):
                compteur=compteur+1
        if (compteur == n) : 
            creux.append(ind[i])
    if (len(creux)>0) :
        return True
    else :
        return False
    
    


 
#la fonction synthétise un filtre dérivateur RIF à partir de la methode de la fenetre en utilisant une fenetre
#de hamming. On prend les 2M-1 premiers coefficents de la réponse impulsionnelle du filtre de réponse
#en fréquence 2*j*np.pi*f puis on multiplie par une fenetre de hamming.
#paramètre: M:taille de la fenetre, b: effet passe bas
#retour: filtre dérivateur
j=complex(0,1)
def filtre_derivateur(M,b): #valeur usuel: fenetre de taille 2M-1=19, effet passe bas b=0.2
     n=np.arange(-M+1,M)
     n[M-1]=1
     h=(-2*np.pi)*((np.sin(np.pi*n*b*2)/2)-np.pi*b*n*np.cos(np.pi*n*b*2))/((np.pi**2)*n**2) #reponse impulsionnel derivateur idéal
     h[M-1]=0
     return h*hamming(2*M-1) #methode de la fenetre
 
    
    
#effectue la dérivation d'un signal et conserve seulement les pics positifs. renvoie la dérivée seuillé en 0 et 
#la nouvelle echelle de temps calibrée pour l'affichage.
#paramètre:(sig=signal,M=taille de la fenetre du filtre rif,b=effet passe bas)
#retour: dérivée de sig
def derivateur(sig,time, M,b): #renvoie les pics 
    dtnf =lfilter(filtre_derivateur(M,b), 1,sig) 
    dtnf_ind = np.nonzero(dtnf>0) #on fixe le seuil de detection de pic a 0
    dtnf_ind=np.array(dtnf_ind) #on repasse en np.array
    dtnf=dtnf[dtnf_ind][0]
    time = time[dtnf_ind][0]
    return dtnf, time
    

#renvoie la liste des pics positif de la dérivée, leur position, et la nouvelle echelle de temps calibrée 
#pour l'affichage. 
#paramètre: sig=signal
#retour: dtnf:dérivée du signal,pics:pics positifs de la dérivée,ind=renvoie la position en échantillons,time: horloge calibrée
#note: pour afficher faire: plt.plot(time,dtnf) puis plt.plot(time[ind],pics,'o')

def find_pic(sig,time): #liste des pics positifs de la dérivée
    dtnf,time=derivateur(sig, time,10,0.2) #M=10 et b=0.2 par defaut
    den = lfilter([+1,-1], 1, dtnf) 
    den = lfilter([+1,-1], 1, dtnf)
    den = np.sign(den)
    dden = lfilter([+1,-1], 1, den)
    ind = np.nonzero(dden==-2) #recherche des maximas
    ind = np.array(ind) -1 #on repasse en np.array
    pics=dtnf[ind][0] #listes des amplitudes des pics
    ind=ind[0] #liste des positions
    return dtnf,pics,ind,time #liste de pics et leur position ainsi que l'horloge calibré pour affichage


# entrées : signal,time, T, fe
#calcule les densités de pics sur chaqué échantillon du signal de T secondes, soit de longueur T*Fe
#On calcule le nombre de pics en utilisant find_pics.
#On crée une liste de même longueur que le signal, qui vaut 1 aux indices où il y a un pic, 0 autre part
#on somme ces 1 sur les intervalles de longueur int(T*fe) qui nous intérèssent
#on trouve ainsi le nombre de pics par intervalle de longueur int(T*fe)
#
def densite_pic_haut(signal, time, T,fe ) :
    b,a = iirfilter(N=2,Wn=[5000.0/fe*2],btype="highpass",ftype="butter")
    signal = lfilter(b,a,signal)
    ech=int(T*fe)
    derivee, pics_amplitude, pics_position, time= find_pic(signal, time) #retourne les positions des pics, leurs amplitudes
    densite = []
    liste=[0]*len(signal)
    for i in range (len(pics_position)) :
        liste[pics_position[i]]=1
    for k in range (int(len(signal)/ech)) :
        densite.append(sum(liste[k*ech:(k+1)*ech]))
    return densite


#trace le spectrogramme du signal
#fonctionne bien pour un signal échantillonné à 44100Hz
def plot_spectrogram(signal) :
    plt.specgram(signal, NFFT=2048,   Fs=fe, noverlap=3.0*2048/4)


#calcule la moyenne des basses de signal
#on applique un filtre de butterworth passe-bas de fréquence de coupure 100Hz
#on calcule l'énergie du signal filtré
#puis la moyenne de celle ci
def bass_medium(signal, time, fe) :
    b,a = iirfilter(N=2,Wn=[100.0/fe*2],btype="lowpass",ftype="butter")
    signal = lfilter(b,a,signal)
    env_bass = detect_env(signal, time,fe)[0]
    return sum(env_bass) /len(env_bass)


#fonction qui compare la moyenne de basse d'un signal à une valeur
#   
#freq de coupure fc/fe=0.1 si Wn= [0.1¨*2]
def no_bass(signal,m, time, fe) :
    b,a = iirfilter(N=2,Wn=[100.0/fe*2],btype="lowpass",ftype="butter")
    signal = lfilter(b,a,signal)
    env_bass = detect_env(signal, time,fe)[0]
    m2= sum(env_bass)/len(env_bass)
    if (0.33*m > m2) :
        return True
    else : 
        return False
    
    

##
    
    
    
    
    
    
    
    
    
    
"""
def densite_pic(signal, time, T,fe ) :
    ech=T*fe
    pics_amplitude,pics_position = find_pics(signal, time)[0:1] #retourne les positions des pics
    densite = []
    liste=[0]**len(signal)
    liste[pics_position]=1
    densite = np.array([sum(liste[k*ech:(k+1)*ech]) for k in range (int( ])
 
    
#cette fonction sert plus à priori finalement
#servait à compter le nombre de pics dans des intervalles avec un pic particulier
def densite_pic(indpics,ipic,n,T,f) :
    #ipic = indpics[ipic]
    ech=int(f*T*1.0/n)
    compte=[0]*n
    k=0

    while ( k<n ) :
        i=0
        while (indpics[i] <= ipic-k*ech) :
            if (ipic-(k+1)*ech<indpics[i]) :
                compte[k]=compte[k]+1
            i=i+1
        k=k+1
    return compte


"""

def moy_glissante(signal,N):
    b=np.ones(N)
    moy=lfilter(b,[N],signal)
    return moy

def detect_low_freq_event(signal,N,M,fe,seuil_old):
    time =np.arange(len(signal))*1.0/fe
    b,a = iirfilter(N=2,Wn=[100.0/fe*2],btype="lowpass",ftype="butter")
    signal = lfilter(b,a,signal)
    signal, time, fe = detect_env(signal, time, fe)
    derivee, pic_der, ind_der, time = find_pic(signal, time)
    seuil=moy_glissante(derivee,N)
    derivee=derivee-M*seuil
    compteur=0
    plt.figure()
    plt.plot(time,derivee)
    plt.plot(time,seuil)
    for i in range(1,(int)(len(derivee[ind_der])/4)):
        if derivee[ind_der][i]>seuil_old:
            compteur=1
    for i in range((int)(len(derivee[ind_der])/4),len(derivee[ind_der])):
        if derivee[ind_der][i]>seuil[ind_der][i]:
            compteur=1
   
    if compteur==1:
        return True,seuil[len(seuil)-1]
    else: 

        return False,seuil[len(seuil)-1]

    
    
def autocor(signal, time, fe) :
    signal3 , time3, fe = dr.detect_env(signal2, time2, fe)
    der, a_pics, ind_pics, time = dr.find_pic(signal3, time3)
    only_pics =  np.zeros(len(der))
    for i in range (len(ind_pics)):
        only_pics[ind_pics[i]]=a_pics[i] 
    only_pics = np.concatenate([only_pics, np.zeros(len(only_pics))])
    autocorr = np.correlate(der, der, mode='full')
    autocorr = autocorr[autocorr.size/2:]
    #plt.figure()
    #plt.plot(np.arange(len(autocorr)), autocorr)
    return autocorr
    


