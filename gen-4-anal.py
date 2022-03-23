#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 03:44:44 2022

@author: user
"""
import numpy as np
#complete profile of cyl-32-16 with however many files I fit on the remote machine

dir_coarse = './coarse_cyl_32_16/'
dir_fine = './cylinder-files/'

def gram_schmidt_columns(X):
    Q, R = np.linalg.qr(X)
    return Q

def score(X,Y): #Y is true
    return np.max((np.linalg.norm(X-Y, ord = 1, axis = 0))/np.linalg.norm(Y, ord = 1, axis = 0))

def rectifier(alphas, betas, lmbda = .2):
    #r = np.zeros_like(betas)
    r = np.matmul(np.linalg.inv(np.matmul(betas.T, betas)+lmbda*np.eye((np.matmul(betas.T, betas)).shape[0], (np.matmul(betas.T, betas)).shape[1])),np.matmul(betas.T, alphas))
    '''for i in range(alphas.shape[1]):
        r[:,i] = np.linalg.inv(betas.T@betas+lmbda*np.eye((betas.T@betas).shape[0], (betas.T@betas).shape[1]))@betas.T@alphas
'''
    return r

a = None #fine array
b = None #coarse array
#I am pretty wasteful with RAM because I finally can NOT hoard it


bases = [5,10,15,25,50,75,100,125,148]
coarse_snap_amt = 101 #how many snapshots of coarse-interp
fine_snap_amt = 175


for i in range(coarse_snap_amt):
    print('Reading coarse at '+str(i))
    with open(dir_coarse+'coarse-cyl-32-001-01-visc-step'+str(i)+'.npz', 'rb') as f:
        c = np.load(f)
        b = c.reshape(-1,1) if b is None else np.concatenate([b,c.reshape(-1,1)], axis = 1)
for i in range(fine_snap_amt):    
    print('Reading fine at '+str(i))
    with open(dir_fine+'fine-cyl-32-001-01-visc-step'+str(i)+'.npz', 'rb') as f:
        c = np.load(f)
        a = c.reshape(-1,1) if a is None else np.concatenate([a,c.reshape(-1,1)], axis = 1)

print(a.shape)
print(b.shape)

aux = min(b.shape[1], a.shape[1])

lmbda = 10

scores = {'raw': 0}

for NS in bases:
    scores[NS] = {'NIRB': 0, 'NIRB-R':0}

scores['raw'] = score(b,a[:b.shape[0], :b.shape[1]])
print(scores['raw'])
for NS in bases:
    print('NS is '+str(NS))
    d = np.copy(a[:,:NS])
    print(d.shape)
    modes1 = gram_schmidt_columns(d)
    
    mx2p5 = 0
    for i in range(b.shape[1]):
        vec = np.copy(b[:,i])
        beta = []
        nirb = np.zeros_like(vec)
        for j in range(modes1.shape[1]):
            beta.append(np.dot(modes1[:,j],vec))
            nirb+=beta[j]*modes1[:,j]
        diff = nirb - a[:b.shape[0],i]
        diff = np.linalg.norm(diff, ord = 1)/np.linalg.norm(a[:b.shape[0],i], ord = 1)
        if mx2p5<diff:
            mx2p5 = diff
    scores[NS]['NIRB'] = mx2p5
    
    betas = []
    for i in range(b.shape[1]):
        vec = np.copy(b[:,i])
        beta = []
        nirb = np.zeros_like(vec)
        for j in range(modes1.shape[1]):
            beta.append(np.dot(modes1[:,j],vec))
        betas.append(beta)
    
    betas = np.array(betas)
    
    
    alphas = []
    for i in range(a.shape[1]):
        vec = np.copy(a[:,i])
        alpha = []
        nirb = np.zeros_like(vec)
        for j in range(modes1.shape[1]):
            alpha.append(np.dot(modes1[:,j],vec))
        alphas.append(alpha)
    
    alphas = np.array(alphas)
    
    
    R = rectifier(alphas[:NS],betas[:NS], lmbda)
    mx2p5 = 0
    for i in range(b.shape[1]):
        vec = np.copy(b[:,i])
        beta = []
        nirb = np.zeros_like(vec)
        for j in range(modes1.shape[1]):
            beta.append(np.dot(modes1[:,j],vec))
        beta = np.array(beta)
        betaR = np.matmul(R.T,beta)
        for j in range(modes1.shape[1]):
            nirb+=betaR[j]*modes1[:,j]
        diff = nirb - a[:b.shape[0],i]
        diff = np.linalg.norm(diff, ord = 1)/np.linalg.norm(a[:b.shape[0],i], ord = 1)
        if mx2p5<diff:
            mx2p5 = diff
    scores[NS]['NIRB-R'] = mx2p5
    print(scores[NS])

print(scores)