# BBH-population-kicks
The final project for Astr8020 for Kyle and Levi

Link to paper draft: https://www.overleaf.com/read/qdtkhqfzjdmx

# Research question

Given that we know black hole mergers can often lead to a velocity 'kick' after the merger, we want to know how important this effect is when it comes 
to a heirarchy of mergers. Specifically we want to know what happens to the population of black holes after subsequent mergers inside a globular 
cluster, a common place for black holes to form and grow.


## Research plan

To do this, we plan to interact populations of black holes with each other in subsequent mergers. Using a distribution of Masses, spins, and 
velocities, we will be able to semi-randomly interact black holes with each other using the SurfinBH python package, which will give us information 
about the resulting kick velocities, masses, and spins. Mass ratio information could also be recorded to verify our simulations are consistent with observational rates. The resulting population will be our second generation of black holes. Any black holes that leave the globular 
cluster will be recorded, but not interacted again. Each new generation will need to time evolve, using dynamical friction to slow velocities, we will 
re-interact these second generation black holes to make a third generation. Repeating this until we have some resulting population of intermediate mass 
black holes (i.e. 500 M_sun). This could also allow for inferences about the expected mass ratios for IMBH mergers.


Once we have many generations of black holes, we can bring the population densities together to get a total BBH population. 


To tie this back to LIGO, we can use the rates of BBH mergers as a way to change our percentage densities into physical densities.

Talk with Karan in last class
compare to carnegie melon group, using GC, internal ZAMS to BH mass as a function of redshift, generic enough - looking at metallicity and hierarchical mergers, agnostic models. modular and modifiable. releasing a package - inviting future development. visual component for merger tree. Show 1-2 examples - on github. not delving into any major science statement. Every concept and everything you want to say for class paper for dump of ideas then can edit for ApJ later. Looking at max mass BH happening. relative heights in posterior. function to go through all the trees to make a list of mergers- merger rates. no time currently (relative merger rate for a single globular cluster over whole timespan of a cluster) - paper with gerosa and berti - inculded hierarchical mergers - if spins > .2 then no imbh - way to skip time argument?? subtle... apj is 3 pages - one tree look at high masses, spin info.... --- future = feed in spin PDF for priors. Prior implementation
scope: key is hierarchical merger - user input to represent many different environments that hierarchical mergers can take place in not just GCs. 
not as agnostic as we would like. 
get used to holding an iphone first. see how community uses it first - see what community wants... if next year a group wants to take it on - what would they work on? mentorship update of package. 



### Some papers

- [Gravitational Wave Recoil and the Retention of Intermediate-Mass Black Holes](https://iopscience.iop.org/article/10.1086/591218)
This does almost everything we plan to do, though much more analytical/mathematical than what we intend to do.

- [surfinBH: Surrogate final black hole properties for mergers of binary black holes](https://ui.adsabs.harvard.edu/abs/2018ascl.soft09007V/abstract) The Handy python package for mergers!

- [Remnant mass, spin, and recoil from spin aligned black-hole binaries](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.90.104004) Black hole kick formula!

- [Properties and Astrophysical Implications of the 150 M⊙ Binary Black Hole Merger GW190521](https://iopscience.iop.org/article/10.3847/2041-8213/aba493&lang=en) Could be useful when relating our results

- [SPIN-PRECESSION: BREAKING THE BLACK HOLE–NEUTRON STAR DEGENERACY](https://iopscience.iop.org/article/10.1088/2041-8205/798/1/L17)
- [Cosmological Black Hole Spin Evolution by Mergers and Accretion](https://iopscience.iop.org/article/10.1086/590379/meta)
These two might be helpful when deriving initial spin parameter distributions

- [Global Stellar Budget for LIGO Black Holes](https://ui.adsabs.harvard.edu/abs/2020ApJ...889L..35J/abstract)
Helpful for black hole formation and merger rates

- [Large Merger Recoils and Spin Flips from Generic Black Hole Binaries](https://iopscience.iop.org/article/10.1086/516712/pdf)
Explores mass ratio 2 and highly misaligned spin mergers and resulting recoil

- [Binary black hole mergers from globular clusters: Masses, merger rates, and the impact of stellar evolution](https://journals.aps.org/prd/pdf/10.1103/PhysRevD.93.084029)
Similar study to ours but more extensive globular cluster modeling from 2016 using very few GW events.

- [Very massive stars, pair-instability supernovae and intermediate-mass black holes with the SEVN code](https://academic.oup.com/mnras/article/470/4/4739/3883764#93923623)
