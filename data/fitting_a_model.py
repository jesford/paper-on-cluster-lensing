import numpy as np
from clusterlensing import ClusterEnsemble

logm_true = 14
off_true = 0.3

nbins = 10
rbins = np.logspace(np.log10(0.1), np.log10(5), num=nbins)
redshift = [0.2]
cdata = ClusterEnsemble(redshift)
cdata.m200 = [10**logm_true]
cdata.calc_nfw(rbins=rbins, offsets=[off_true])
dsigma_true = cdata.deltasigma_nfw.mean(axis=0).value

# add scatter with a stddev of 20% of data
noise = np.random.normal(scale=dsigma_true*0.2, size=nbins)
y = dsigma_true + noise
yerr = np.abs(dsigma_true/3)  # 33% error bars

# ------------------------

# probability of the data given the model
def lnlike(theta, z, rbins, data, stddev):
    logm, offsets = theta

    # calculate the model
    c = ClusterEnsemble(z)
    c.m200 = [10 ** logm]
    c.calc_nfw(rbins=rbins, offsets=[offsets])
    model = c.deltasigma_nfw.mean(axis=0).value

    diff = data - model
    lnlikelihood = -0.5 * np.sum(diff**2 / stddev**2)
    return lnlikelihood

# uninformative prior
def lnprior(theta):
    logm, offset = theta
    if 10 < logm < 16 and 0.0 <= offset < 5.0:
        return 0.0
    else:
        return -np.inf

# posterior probability
def lnprob(theta, z, rbins, data, stddev):
    lp = lnprior(theta)
    if not np.isfinite(lp):
        return -np.inf
    else:
        return lp + lnlike(theta, z, rbins, data, stddev)

# ------------------------

import emcee

ndim = 2
nwalkers = 20
p0 = np.random.rand(ndim * nwalkers).reshape((nwalkers, ndim))
p0[:, 0] = p0[:, 0] + 13.5  # start somewhere close to true logm ~ 14

sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob,
                                args=(redshift, rbins, y, yerr), threads=8)

pos, prob, state = sampler.run_mcmc(p0, 500)

# ------------------------

import seaborn; seaborn.set()
import corner
import matplotlib
matplotlib.rcParams["axes.labelsize"] = 20

burn_in_step = 80
samples = sampler.chain[:, burn_in_step:, :].reshape((-1, ndim))
fig = corner.corner(samples,
                    labels=["$\mathrm{log}M_{200}$", "$\sigma_\mathrm{off}$"],
                    truths=[logm_true, off_true])
fig.savefig('f4.eps')  # output is Figure 4
