from clusters import selection
from clusters import initialize


init_pop = initialize.make_population(10, 20)

init_pop.sort()
print(init_pop)

percent = 20

final_pop = selection.remove_top_percent(init_pop, percent)
print("after")
print(final_pop)
