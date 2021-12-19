import click
from clusters import initialize
from clusters import management
from clusters import selection
from tests import test_sphere
import numpy as np


# Command Line Interface using Click
@click.group()
def cli():
    pass


@cli.command()
@click.option("--particles", '-p', type=click.IntRange(1), required=True, help="The cluster particle count")
@click.option("--energy", '-e', type=float, required=True, help="The empirical global minimum energy for the cluster")
@click.option("--output", '-o', default="pos", help="Name of output file containing final positions")
# starts genetic algorithm loop given the target energy and number of particles per cluster
def run(particles, energy, output):
    click.echo("Generating new population", nl=False)
    # initial population
    target_energy = energy
    n = particles
    pop_size = 40
    gen = 0
    mins = pop_size

    pop = initialize.make_population(pop_size, n)
    operators = [management.AngularOperator(0.3), management.TwistOperator(0.4), management.ImmigrateOperator(0.3)]

    # loop
    while not selection.converged(pop, target_energy):

        pop = selection.remove_top_percent(pop, 25)

        prev_energy = management.mean_energy(pop)

        size = pop_size - len(pop)

        for i, op in enumerate(operators):
            created = op.apply(pop, size)
            mins += len(created)
            rate = management.new_rate(prev_energy, created, op.rate)
            operators[i].rate = rate
            pop = np.concatenate((created, pop))

        management.normalize(operators)
        gen += 1
        click.echo("Generation: {}, {}".format(gen, min(pop)))

    click.echo("Global minimum reached after {} local minimizations, writing file...".format(mins))
    result = pop[np.argmin(pop)]
    filename = str(output) + ".xyz"
    with open(filename, 'w') as f:
        f.write('{}\n'.format(n))
        f.write('Energy: {}\n'.format(result.energy()))
        for j in range(n):
            f.write('LJ {:12.6g} {:12.6g} {:12.6g} \n'.format(*result.pos[j]))


@cli.command()
@click.option('--operator', '-op', required=True,
              type=click.Choice(['Twist', 'Angular', 'Immigrate'], case_sensitive=False),
              help="View the effects of an operator")
@click.option('--particles', '-p', default=10, type=click.IntRange(1))
# view the effects of operators
def view(operator, particles):
    print(operator)
    if operator == 'Twist':
        op = management.TwistOperator(1)
    elif operator == 'Angular':
        op = management.AngularOperator(1)
    else:
        op = management.ImmigrateOperator(1)

    test_sphere.test_operator(op, particles)
