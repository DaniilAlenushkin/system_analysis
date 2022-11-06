import math
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')


def plotting(data, m):
    fig, ax = plt.subplots()
    ax.set_title(f'Costs of system operation from the number of service channels \n'
                 f'(µ= {m})')
    for index, value in enumerate(data):
        # value = list(map(lambda x: abs(x), value)) # ?
        print(f'µ = {m}, λ = {index+10}, min cost = {min(value)}$, '
              f'optimal number of service channels = {value.index(min(value))+1}')
        ax.plot(range(1, 10), value)

    ax.legend([f'λ = {i}' for i in range(10, 21)])
    ax.grid()
    ax.set_xlabel('Number of service channels')
    ax.set_ylabel('System operating costs ($)')
    plt.show()


Cef = 0.15/365  # $/year
C1 = 100000  # $
C2 = 50  # $/day
C3 = 30  # $/day
C4 = 60  # $/day pcs
C5 = 100  # $/day pcs
T = 6000/24  # day
lmbds = [i for i in range(10, 21)] # pcs/day
mus = [i for i in range(2, 8)] # pcs/day
for mu in mus:
    I_mu_const = []
    for lmbd in lmbds:
        I = []
        for s in range(1, 10):
            m = 10 - s
            ro = lmbd/mu
            summ_for_P0 = sum([(ro**k)/(math.factorial(k)) for k in range(0, s+1)])
            if ro/s != 1.0:
                P0 = (summ_for_P0+(((ro**(s+1))/(s*math.factorial(s)))*((1-((ro/s)**m))/(1-(ro/s)))))**(-1)
                M1 = ((ro**(s+1))/(s*math.factorial(s)))*((1-((ro/s)**m)*(m+1-m*(ro/s)))/((1-(ro/s))**2))*P0
            else:
                P0 = (summ_for_P0+(m*(ro**(s+1)))/(s*math.factorial(s)))**(-1)
                M1 = ((ro**(s+1))/(s*math.factorial(s)))*((m*(m+1))/2)*P0
            Psm = ((ro**(s+m))*P0)/((s**m)*math.factorial(s))
            M2 = sum([((s-k)*(ro**k)*P0)/math.factorial(k) for k in range(s)])
            I.append(Cef*C1*s + C2*(s-M2)*T + C3*M2*T + C5*T*lmbd*Psm + C4*M1*T)
        I_mu_const.append(I)
    plotting(I_mu_const, mu)
