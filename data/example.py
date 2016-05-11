import numpy as np
data = np.loadtxt('Clusters_W1.dat')
data.shape
data[0:4, :]  # print first 4 clusters
redshift = data[:, 2]
sig = data[:, 3]
richness = data[:, 4]

# select a subset
here = (sig > 15) & (redshift < 0.5)
sig[here].shape
z = redshift[here]
n200 = richness[here]

import clusterlensing
c = clusterlensing.ClusterEnsemble(z)
c.n200 = n200
c.dataframe.head()

rbins = np.logspace(np.log10(0.1),
                    np.log10(10.0), num=20)
c.calc_nfw(rbins)

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import matplotlib
matplotlib.rcParams['axes.labelsize'] = 20
matplotlib.rcParams['legend.fontsize'] = 20

# strings for plots
raxis = '$R\ [\mathrm{Mpc}]$'
sgma = '$\Sigma(R)$'
sgmaoff = '$\Sigma^\mathrm{off}(R)$'
delta = '$\Delta$'
sgmaunits = ' $[M_{\odot} / \mathrm{pc}^2]$'

# order from high to low richness
order = c.n200.argsort()[::-1]

for s, n in zip(c.sigma_nfw[order], c.n200[order]):
    plt.plot(rbins, s, label=str(int(n)))
plt.xscale('log')
plt.legend(fontsize=10)
plt.ylabel(sgma+sgmaunits)
plt.xlabel(raxis)
plt.savefig('f1.eps')
plt.close()

sigma = c.sigma_nfw.mean(axis=0)
dsigma = c.deltasigma_nfw.mean(axis=0)

plt.plot(rbins, sigma, label=sgma)
plt.plot(rbins, dsigma, label=delta+sgma)
plt.legend()
plt.ylim([0., 1400.])
plt.xscale('log')
plt.xlabel(raxis)
plt.ylabel(sgmaunits)
plt.savefig('f2.eps')
plt.close()

offsets = np.ones(c.z.shape[0]) * 0.1
c.calc_nfw(rbins, offsets=offsets)
sigma_offset = c.sigma_nfw.mean(axis=0)
dsigma_offset = c.deltasigma_nfw.mean(axis=0)

plt.plot(rbins, sigma_offset, label=sgmaoff)
plt.plot(rbins, dsigma_offset, label=delta+sgmaoff)
plt.legend()
plt.ylim([0., 1400.])
plt.xscale('log')
plt.xlabel(raxis)
plt.ylabel(sgmaunits)
plt.savefig('f3.eps')
plt.close()
