import numpy as np
import scipy
import pandas as pd
from tqdm import tqdm
from scipy.sparse import linalg
from scipy import interpolate
from sklearn.utils import extmath


def STLS_SINDy(Theta, Fine, lmbda, n=None,m=100):
  Xi = scipy.sparse.linalg.spsolve(Theta, Fine)
  if n is None:
    n = Xi.shape[1]
  for i in range(m):
    smallmask = np.abs(Xi)<lmbda
    Xi[smallmask] = 0
    for j in range(n):
      largemask = ~smallmask[:,j]
      Xi[largemask, j] = scipy.sparse.linalg.spsolve(Theta[:, largemask], Fine[:,j])
  return Xi

def FREDE(l, A, svd = scipy.linalg.svd): #sklearn.utils.extmath.randomized_svd is a good alternative to our r3svd, by the way
  B = np.zeros([l, A.shape[1]])
  for i in range(A.shape[0]):
    B[l,:] = A[i,:]
    u,s,v = svd(B)
    delta = s[l]^2
    B = scipy.linalg.sqrtm(np.diag(s)@np.diag(s)-delta*np.eye(l))@v
  return B
#frede is inserted here for completeness; it is only used in offline computations of datapoints


def r3svd(A,t,p,q,maxit,tau):
  Omega = np.random.normal(size = (A.shape[1], t+p))
  G = Omega
  Vl = None
  Sl = None
  Ul = None
  kpr = 0
  for i in range(maxit):
    Y = A@G
    Q,_ = np.linalg.qr(Y) #0 in alg is matlab shorthand for reduced qr
    for j in range(q):
      Y = A.T@Q
      Y = Y - Vl@(Vl.T@Y) if Vl is not None else Y
      Q,_ = np.linalg.qr(Y)
      Y = A@Q
      Y = Y - Vl@(Vl.T@Y) if Vl is not None else Y
      Q,_ = np.linalg.qr(Y)
    B = (A.T@Q).T
    Ub, Sb, Vb = scipy.linalg.svd(B, full_matrices = False)
    Vb = Vb.T
    Ub = Q@Ub
    aux = Vb if Vl is None else Vb-Vl@(Vl.T@Vb)
    Vb, _ = np.linalg.qr(aux)
    Ul = Ub[:t] if Ul is None else np.hstack([Ul, Ub[:t]])
    '''Sl = np.diag(Sb)[:t,:t] if Sl is None else np.block([
                                                         [Sl, np.zeros([Sl.shape[0], np.diag(Sb)[:t,:t].shape[1]])],
                                                         [np.zeros([np.diag(Sb)[:t,:t].shape[0], Sl.shape[1]]), np.diag(Sb)[:t,:t]]
    ])'''
    Sl = Sb[:t].reshape(-1,1) if Sl is None else np.vstack([Sl, Sb[:t].reshape(-1,1)])
    Vl = Vb[:t] if Vl is None else np.hstack([Vl, Vb[:t]])
    for j in range(t):
      kpr = i*t+j
      phipr = ((Sl)**2)[:kpr].sum()/(np.linalg.norm(A, ord = 'fro')**2)
      if phipr>tau:
        sorter = Sl.reshape(-1).argsort()
        print(sorter)
        print(Vl.shape)
        return Ul[sorter], Sl[sorter], Vl[sorter[::-1]].T
  print(phipr)
  sorter = Sl.argsort()
  return Ul[sorter], Sl[sorter], Vl[sorter[::-1]].T
      