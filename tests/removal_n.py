energy_list = []
index_list = [*range(0, 10, 1)]
removal_n = 10 

for i in range(pop_size):
    energy_list.append(float(format(pop_list[i].energy())))
    
zip_energy = zip(index_list, energy_list)

energy_dict = dict(zip_energy)
sorted_values = sorted(energy_dict.values()) # Sort the values
sorted_dict = {}

for i in sorted_values:
    for k in energy_dict.keys():
        if energy_dict[k] == i:
            sorted_dict[k] = energy_dict[k]
            break
            
for i in range(int(pop_size*(removal_n/100))):
    e_dict = sorted_dict.popitem()

print(sorted_dict)
