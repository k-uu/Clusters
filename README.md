# clusters.py

### By: Oskar Blyt, Alina Ehrl, Selina Mather

Code is inspired by the methodology outlined in:
[A New Genetic Algorithm Approach Applied to
Atomic and Molecular Cluster Studies](https://doi.org/10.3389/fchem.2019.00707)


*cluster: an assembly of atoms that is an intermediate between a simple
molecule and a nanoparticle*

This program utilizes a genetic algorithm to approximate the structure of Lennard Jones (LJ) 
clusters given the number of particles. It produces an .xyz file containing the final positions of the particles


### TODO:

- Initialization Step: (Oct 24 - 28)
  - Stop condition
    - With the actual energies of LJ clusters known, convergence to local minima can be avoided
    - Check each individual of current population to see if the energy minimum has been achieved
- produce initial population by generating individuals made up of random points bounded by a sphere and 
  separated by a minimum distance -> initialize.py
  - given the number of particles and initial population size, generate a population 
  - of spheres containing random points (particle positions) -> function to generate spheres 
  - How to represent particle positions? -> numpy array 


*do while (!stop condition)*

- Selection Step: (Oct 29 - Nov 3)
  - determine the energy of each individual Remove the n% of highest
    energy individuals
- Management Step: (Nov 4 - 8)
  - Update the creation rate of operators based on the energies of individuals they created compared to the energy of the previous
  generation
  - Determine variation toward creation rate for each individual
  - Sum the variations for individuals created using the same operator to determine the operator's new creation rate
  - Normalize the creation rates for each operator to 1 and multiply each creation rate by the number of individuals
- Operator Step: (Nov 8 - 12)
- Create variation in genetic material (atom positions). This must be performed in
order to avoid population stagnation
- Select different operators: Crossover, Mutation
- Generate next population

*end do*

- Finalization: (Nov 12 - )
  - Convert coordinates of particles into a format for visualization (VMD?)
  - Test additional genetic variation mechanisms
  - Experiment with different particle sizes
  - Make final presentation and writeup
