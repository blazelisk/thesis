import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
from tqdm import tqdm

#LaTeX Font
rc('text', usetex=True)
rc('font', family='serif')

#Define Function
def metzlerian(k, U, Ulag, Clag, Ibar):
    return U + k * U - (1 + k) * Ulag + Clag + Ibar
#Solves for steady state income
def ssincome(b, Ibar):
    return ( 1/(1-b) ) * Ibar
#Solves for steady state consumption
def ssconsumption(b, Ybar):
    return b * Ybar 
#Solves for U, goods produced for sale
def saledist(c, f, d, Cbar, Clag):
    Uextrapolate = Clag + c * (Clag - Cbar)
    Uregression = Clag + f * (Cbar - Clag)
    w = 1 / (1 + d * (Cbar - Clag)**2)
    return w * Uextrapolate + (1 - w)*Uregression
#Solves for consumption
def consumption(b, Ylag):
    return b * Ylag
#Solves for S, goods produced for stock
def stock(k, Ulag, Clag, U):
    qhatlag = k * Ulag
    Qlag = Qhatlag - (Clag - Ulag)
    Qhat = k * U
#Plots cobweb plot
def cobweb(b, c, d, f, k, Y0, U0, Ibar, iterations):
    Ybar = ssincome(b, Ibar)
    Cbar = ssconsumption(b, Ybar)
    Income = np.array([Y0,]*iterations)
    Sale = np.array([U0,]*iterations)
    Consumption = np.ones(iterations)
    Stock = np.ones(iterations)
    for i in tqdm(range(1, iterations)):
        Consumption[i-1] = consumption(b, Income[i-1])
        Sale[i] = saledist(c, f, d, Cbar, Consumption[i-1])
        Income[i] = metzlerian(k, Sale[i], Sale[i-1], Consumption[i-1], Ibar)
    px = []
    py = []
    for i in range(iterations-1):
        px = np.append(px, Consumption[i])
        py = np.append(py, Consumption[i+1])
    print(px)
    print(py)

    fig = plt.figure(dpi=1000)
    ax = fig.add_subplot(111)
    ax.plot(px, py, c='blue', alpha=0.25)
    plt.show()
    
cobweb(0.75, 0.3, 1.0, 0.1, 0.1, 40.6, 30.3, 10, 50)