# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 16:43:07 2018

@author: HITCSC-AI
"""

import math
import sys
import random

def print_usage():
    print("Usage: GA.py")

def singleReplace(string,p,c):
    new = []
    for s in string:
        new.append(s)
    new[p] = c
    return ''.join(new)

def multiReplace(string,p,c):
    new = []
    for s in string:
        new.append(s)
    for index,point in enumerate(p):
        new[point] = c[index]
    return ''.join(new)

def fitFun(x):
    temp = x * math.sin(10 * math.pi * x) + 2
    if temp > 0:
        return temp
    else:
        return 0

def getCodeParam(x, ran):
    num = (max(ran) - min(ran)) / x
    bitPower = int(-1)
    while(math.pow(2,bitPower) <= num):
        bitPower += 1
    xMax = max(ran)
    xMin = min(ran)
    e = (max(ran) - min(ran)) / math.pow(2,bitPower)
    diff = math.pow(2,bitPower) * e + xMin -xMax
    return e, bitPower,diff

def cross(first, second, Pc, bP):
    '''
    cross over with probability Pc, gene length is bP
    '''
    if random.random() < Pc:
        location = random.randint(0,bP-1)
        temp = first[location:]
        first = first[:location] + second[location:]
        second = second[:location] + temp
    return first, second


def mutate(first, second, Pm, bP):
    '''
    mutation with probability Pm, and the length is bP
    '''
    if random.random() < Pm:
        location = random.randint(int(bP / 2),bP-1)
        a = str(1-int(first[location]))
        first = singleReplace(first, location, a)
        a = str(1-int(second[location]))
        second= singleReplace(second, location, a)
    return first, second

def RWS(p):
    '''
    Roulette Wheel Selection
    '''
    m = 0.0
    r = random.random()
    for it in p:
        m += it
        if r <= m:
            return p.index(it)
    
def initSpecies(length,size):
    species = []
    for j in range(size):
        temp = ''
        for i in range(length):
            temp += str(random.randint(0,1))
        species.append(temp)
    return species

    
#print(getCodeParam(3/512,ran))    

if __name__ == "__main__":
    if True:
        eps = 1e-3
        error = 1
        G = -1
        Gmax = 1000
        ran = [-1,2]
        speSize = 100
        Pc = 0.6
        Pm = 0.8
        _, geneLength, _ = getCodeParam(eps,ran)
        spe = initSpecies(geneLength, speSize)
        maxFit = 0.
        maxX = 0.
        while G < Gmax:
            G += 1
            speNew = []
            speFF = []
            for it in spe:
                speFF.append(fitFun(int(it,2) / pow(2, geneLength) * 3 - 1))
            while len(speNew) < speSize:
                summer = sum(speFF)
                speFF = [it / summer for it in speFF ]
                playerReady1 = spe[RWS(speFF)]
                playerReady2 = spe[RWS(speFF)]
                playerReady1, playerReady2 = cross(playerReady1, playerReady2, Pc, geneLength)
                playerReady1, playerReady2 = mutate(playerReady1, playerReady2, Pm, geneLength)
                speNew.append(playerReady1)
                speNew.append(playerReady2)
                if len(speNew) == speSize:
                    spe = speNew
            if maxFit < fitFun(int(spe[speFF.index(max(speFF))],2) / pow(2, geneLength) * 3 - 1):
                maxFit = fitFun(int(spe[speFF.index(max(speFF))],2) / pow(2, geneLength) * 3 - 1)
                maxX = int(spe[speFF.index(max(speFF))],2) / pow(2, geneLength) * 3 - 1
            print(G,"iteration, solution is:", int(spe[speFF.index(max(speFF))],2) / pow(2, geneLength) * 3 - 1)
        print(maxFit,'at',maxX)
    else:
        if len(sys.argv) != 3:
            print_usage()
        a = '11111111'
        b = '00000000'
        print(initSpecies(5,10))
        a = initSpecies(5,10)
        
        print(RWS([0.1,0.2,0.3,0.4]))
        print(cross(a,b,0.9,3))
        print(mutate(a,b,0.9,3))
        a = 1.1
        b = (a + 1) / 3 * 512
        print(b,bin(int(b)))
        c = format(int(b), 'b')        
    
        