import numpy as np
import sympy
import surfinBH
from copy import deepcopy
import time

from .GlobularCluster import GlobularCluster 
from .BlackHole import BlackHole


class Simulator:


    def __init__(self,params=None,print_missing=True,rand_seed=None):
        '''Params is a dictionary of values for the Globular Cluster Simulation.
        
        Params needs the following parameters, if any are left as none, defaults are provided
        
        cluster_mass - The total mass of the globular cluster in solar masses [1e6]
        cluster_radius - The total radius of the cluster in (parsecs?) []
        imf_alpha - The alpha value for the imf dn/dm = m**(-alpha) [2.35] 
        min_bh_star - Minimum mass of a star that forms a black hole in solar masses [10]
        bh_mass_frac - The fraction of the star mass that remains in the black hole [0.5]
        min_star - The smallest star mass in the cluster in solar masses [0.8]
        max_star - The largest star mass in the cluster in solar masses [100]
        
        sbh_fitter - The fitter for surfinBH to use ['NRSur7dq4Remnant']
        
        vel_thresh - Threshold velocity to allow a collision of black holes
        '''
        if params==None:
            params = dict()
        pars = deepcopy(params)
        
        if 'cluster_mass' not in params.keys():
            pars.update({'cluster_mass':1e6})
            if print_missing:
                print(f"'cluster_mass' not set, defaulting to {pars['cluster_mass']}")
        if 'cluster_radius' not in params.keys():
            pars.update({'cluster_radius':1e6})
            if print_missing:
                print(f"'cluster_radius' not set, defaulting to {pars['cluster_radius']}")
        if 'imf_alpha' not in params.keys():
            pars.update({'imf_alpha':2.25})
            if print_missing:
                print(f"'imf_alpha' not set, defaulting to {pars['imf_alpha']}")
        if 'min_bh_star' not in params.keys():
            pars.update({'min_bh_star':10})
            if print_missing:
                print(f"'min_bh_star' not set, defaulting to {pars['min_bh_star']}")
        if 'bh_mass_frac' not in params.keys():
            pars.update({'bh_mass_frac':0.5})
            if print_missing:
                print(f"'bh_mass_frac' not set, defaulting to {pars['bh_mass_frac']}")
        if 'min_star' not in params.keys():
            pars.update({'min_star':0.8})
            if print_missing:
                print(f"'min_star' not set, defaulting to {pars['min_star']}")
        if 'max_star' not in params.keys():
            pars.update({'max_star':100})
            if print_missing:
                print(f"'max_star' not set, defaulting to {pars['max_star']}")
            
        if 'sbh_fitter' not in params.keys():
            pars.update({'sbh_fitter':'NRSur7dq4Remnant'})
            if print_missing:
                print(f"'sbh_fitter' not set, defaulting to {pars['sbh_fitter']}")
        if 'vel_thresh' not in params.keys():
            pars.update({'vel_thresh':1})
            if print_missing:
                print(f"'vel_thresh' not set, defaulting to {pars['vel_thresh']}")
            
            
        if rand_seed==None:
            self.seed = np.random.randint(0,1_000_000_000)
        else:
            self.seed = int(rand_seed)
        
        self.rng = np.random.default_rng(self.seed)
        
        
        self.GC = GlobularCluster(pars['cluster_mass'],pars['cluster_radius'],pars['imf_alpha'],
                                  pars['min_bh_star'],pars['bh_mass_frac'],
                                  pars['min_star'],pars['max_star']
                                 )
        
        self._set_mass_transform(pars['imf_alpha'],pars['min_bh_star'],
                                 pars['bh_mass_frac'],pars['max_star'])
        
        
        self.fit = surfinBH.LoadFits(pars['sbh_fitter'])
        
        self.v_thresh = pars['vel_thresh']
        
        for i in range(self.GC.Nbh):
            self.add_random_BH()
            
        print(f'Setup complete, Globular Cluster now has {len(self.GC.BHs)} black holes.')
         
    
    def begin_sim(self,stopTime=None,progress=1000):
        '''If stopTime==None, Run until one BH left'''
        cputime_s = time.time()
        
        if stopTime==None:
            stopTime=float(np.inf)
            print('No stop time specified, Running until 1 or 0 black holes remain')
        
        col_count = 0
        init_BH = len(self.GC.BHs)
        while(len(self.GC.BHs)>1):
            if col_count==progress:
                print(f'{len(self.GC.BHs)}/{init_BH} remaining')
                col_count=0
            
            if self.GC.BHs[0].t < stopTime:
                #sort the list!
                self.sort_by_time()
            
                #Take first two black holes
                bh1 = self.GC.remove_BH(0)
                bh2 = self.GC.remove_BH(0)
            
                #Collide them together
                mf,sf,vf,t = self.collideBH(bh1,bh2)
            
                #GC will check for ejected black holes,
                BHf, ejected = self.GC.add_BH(mf,sf,vf,t,bh1=bh1,bh2=bh2,ret=True)
            
                if not ejected:
                    #Time evolve the final BH to threshold velocity
                    self.time_evolve(BHf)
                col_count+=1
                
        print(f'Finished. Total Simulation time: {t}\nTotal CPU time: {time.time()-cputime_s}')

   
    def time_evolve(self,bh):
        #TODO: Include dynamical friction here
        #For now, just decrease velocity linearly
        a = -0.01
        totV = np.sum(np.square(bh.v)) #Get velocity magnitude
        
        t = (totV - self.v_thresh)/a
        bh.t+=t
        bh.v = self.v_thresh 
       
        
    def collideBH(self,bh1,bh2):
        #Second BH always has the longer time, (sorted by time)
        t = bh2.t
        bh1.t = t #Collision happened at the same time!
        
        mtot = bh1.m+bh2.m
        
        if bh1.m>=bh2.m:
            q = bh1.m/bh2.m
            s1 = bh1.s
            s2 = bh2.s
        else:
            q = bh2.m/bh1.m
            s1 = bh2.s
            s2 = bh1.s
            
        #TODO: Use surfinBH here
        #For now, just add masses, and make velocity a random number
        return mtot,s1,self.rng.random()*100,t
    
    
    def sort_by_time(self):
        '''Sort the Black holes by the time'''
        self.GC.BHs.sort(key=lambda b: b.t)
    
    
    def add_random_BH(self):
        '''Make a random BH to add to the GC. Starts at time 0 with 0 velocity'''
        m = self.random_mass()
        s = self.random_spin()
        v = 0
        t = 0
        
        return self.GC.add_BH(m,s,v,t,bh1=None,bh2=None)
        
    
    def random_mass(self):
        return self._mass_transform(self.rng.random())
      
        
    def random_spin(self,rand_type='uniform'):
        '''SurfinBH works best with spin [0,0.8) but works 'well' up to 1'''
        return self.rng.random()*(0.9-0) * self._random_uniform_sphere()
    
    
    def _set_mass_transform(self,imf,min_bh_star,bh_mass_frac,max_star):
        '''sets up the random mass generator. Uses inverse transform sampling'''
        print('Setting up analytic mass distribution. '+ 
              'This may take a while depending on your imf alpha')
        
        m = sympy.Symbol('m',real=True)
        p = sympy.Symbol('p',real=True)
        func = m**(-(imf-1))
        
        min_bh_mass = bh_mass_frac*min_bh_star
        max_bh_mass = bh_mass_frac*max_star

        norm = sympy.integrate(func, (m, min_bh_mass, max_bh_mass))
        
        pdf = (1/norm)*m**(-(imf-1))
        cdf = sympy.integrate(pdf,(m,5,m))
        
        quantile = sympy.solvers.solve(cdf-p,m)
        
        try:
            quantile = sympy.lambdify(p,quantile[0])
        except:
            quantile = sympy.lambdify(p,quantile)
        
        self._mass_transform = quantile
        print('Done')
        
    
    def _random_uniform_sphere(self):
        '''Returns a random vector of a unit sphere in cartesian'''
        phi = self.rng.random()*2*np.pi
        theta = np.arcsin(self.rng.random())
        xyz = np.array([np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)])
        return xyz
    
    
        
        