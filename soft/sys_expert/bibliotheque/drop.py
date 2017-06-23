#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 13:49:58 2017

@author: Jane
"""
import numpy as np
from scipy.signal import *


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

def detect_env(signal, T) :
    a=exp(-3/(44100*ln(a)))
    hn=np.array([a**n for n in range (len(T*44100))])
    return lfilter(hn, 1, signal**2)

#paramètres: signal à échantillonner, frequence d'échantillonnage de ce signal, facteur d'échantillonnage
#sorties : le signal sous-echantillonné, le temps sous-échantilonné, la nouvelle frequence d'echantillonnage
#Si on veut sous-échantillonner un signal par k, on prend 1 élément de la liste chaque k
#la fonction ci-dessous sous-échantillonne le signal, l'array de temps associé,
#et renvoie la nouvelle valeur de la fréquence d'échantillonnage,
#celle-ci devient plus petite, elle est divisée par k

def sous_ech(signal, time, fe, ech) :
    return signal[::ech], time[::ech], fe/ech

# entrées : signal,time, T, fe
#calcule les densités de pics sur chaqué échantillon du signal de T secondes, soit de longueur T*Fe 
def densite_pic(signal, time, T,fe ) :
    ech=T*fe
    pics_amplitude,pics_position = find_pics(signal, time)[0:1] #retourne les positions des pics
    densite = []
    liste=[0]**len(signal)
    liste[pics_position]=1
    densite = np.array([sum(liste[k*ech:(k+1)*ech]) for k in range (int( ])
    
    
#cette fonction sert par à priori finalement
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


def plot_spectrogram(signal,fe) :
    plt.specgram(signal, NFFT=2048,   Fs=fe, noverlap=3.0*2048/4)

