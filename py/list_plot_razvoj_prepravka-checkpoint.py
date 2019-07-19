# Razvoj funkcije za plotovanje podataka koriscenjem
# matplotlib modula

from grf_master.epanet_fun import *
import matplotlib.pyplot as plt


def listplot(data, COLOR='', LINE=''):
    plt.plot(data,
             color='',   # primer: 'green'
             linestyle='l',  # primer: 'dashed'
             marker='o',       # primer: 'o'- kruzic
             markerfacecolor='blue',    # primer: 'green'
             markersize=8)         # primer:  12
    return plt.show()


f = openepafile("C:\\PROJEKTI\\Net3\\Net3.inp")
p0_5 = junctpressure(5)

setQH(f, 'kriva1', [[0, 80], [800, 45], [1000, 20]])

# f = openepafile("C:\\PROJEKTI\\Net3_newQH\\Net3_newQH.inp")
p1_5 = junctpressure(5)

plt.plot(p0, linestyle='--')
plt.plot(p1, linestyle=':')
plt.show()
