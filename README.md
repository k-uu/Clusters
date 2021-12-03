# clusters.py

### By: Oskar Blyt, Alina Ehrl, Selina Mather

Code is inspired by the methodology outlined in:
[A New Genetic Algorithm Approach Applied to
Atomic and Molecular Cluster Studies](https://doi.org/10.3389/fchem.2019.00707)


*cluster: an assembly of atoms that is an intermediate between a simple
molecule and a nanoparticle*

This program utilizes a genetic algorithm to approximate the structure of Lennard Jones (LJ) 
clusters given the number of particles. It produces an .xyz file containing the final positions of the particles

requirements for package installation:

- pip is installed

Run instructions:

- In a shell, locate the source code directory and do
 ```$ python3 -m venv env``` to create a new virtual
environment
- do ```$ . env/bin/activate``` on OS X and Linux or 
```$ env\scripts\activate``` on Windows to active the environment
- ```$ pip install --editable .``` to install the package
- the clusters script should now be available by doing ```$ clusters```
- Use ```$ deactivate``` to close the virtual environment

