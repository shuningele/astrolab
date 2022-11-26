import numpy as np
from matplotlib import pyplot as plt
#from scipy import integrate
#from scipy.stats import multivariate_normal

def std_2d_gauss(x, y, sigma):
    return np.exp(-(x**2+y**2)/(2.*sigma**2))/((2*np.pi)*sigma)

#the domain is a circle or annulus with inner radius r1, outer radius r2, centred at (x,y) = (sigma, 0)
def domain(x, y, r1, r2):
    xc = 2
    return (x-xc)**2+y**2 >= r1**2 and (x-xc)**2+y**2 <= r2**2
    
def mc_integrate(func, r0, func_dom, n = 100000):
    # Monte Carlo integration of given function over domain specified by func_dom
    # sample domain points
    sigma = 1.1*r0/2.33
    r1 = 3.5
    r2 = 6.
    supernova_x = np.random.uniform(2-r0, 2+r0, n)
    supernova_y = np.random.uniform(-r0, r0, n)
    x_list = np.random.uniform(2-r2, 2+r2, n)
    y_list = np.random.uniform(-r2, r2, n)
    # determine whether sampled x is in or outside of domain, and calculate its volume
    in_sn = np.array([func_dom(x, y, 0, r0) for x, y in zip(supernova_x, supernova_y)])
    inside_domain = np.array([func_dom(x, y, r1, r2) for x, y in zip(x_list, y_list)])
#    print(inside_domain)
    frac_in_sn = sum(in_sn)/len(in_sn)
    sn_dom = (2.*r0)**2 * frac_in_sn
    frac_in_domain = sum(inside_domain)/len(inside_domain)
    domain = (2.*r2)**2 * frac_in_domain
    
    # calculate expected value of func inside background domain
    bg = np.array([func(x, y, sigma) for x, y in zip(x_list, y_list)])
    bg_mean = bg[inside_domain].sum()/len(bg[inside_domain])
    
    sn = np.array([func(x, y, sigma) for x, y in zip(supernova_x, supernova_y)])
    sn_mean = sn[inside_domain].sum()/len(bg[inside_domain])

    # estimated integration
    sn_integ = sn_dom * sn_mean
    subtracted = sn_integ - bg_mean*sn_dom
    print("For r0={}, The galaxy background in the supernova aperture is {};\n subtracting galaxy light  from the supernova aperture leaves counts in the supernova aperture to be {}".format(r0, sn_integ, subtracted))
    return sn_integ, subtracted


rs = np.linspace(0.75, 1.25, 20)
back_inc, back_sub = [], []
for r in rs:
    inc, sub = mc_integrate(std_2d_gauss, r, domain)
    back_inc.append(inc)
    back_sub.append(sub)

fig, ax = plt.subplots()
ax.scatter(rs, back_inc, marker = "+", color = "skyblue", label = "galaxy background included")
#ax2 = ax.twinx()
ax.scatter(rs, back_sub, marker = "x", color = "green", label = "galaxy background subtracted")
plt.legend()
ax.set_xlabel("Supernova Aperture Size (1 = average PSF FWHM)")
ax.set_ylabel("Fraction of Galaxy Light in S.A.")
plt.show()
