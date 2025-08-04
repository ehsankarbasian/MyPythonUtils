from dict_of_lists import DictOfLists, DictOfSets


my_dict = DictOfLists()

my_dict['a'].append(1)
my_dict['a'].append(2)
my_dict['a'].append(1)
my_dict['b'].append(3)

my_dict['c'] = 5
my_dict['d']

print(my_dict)


my_dict = DictOfSets()

my_dict['a'].add(1)
my_dict['a'].add(2)
my_dict['a'].add(1)
my_dict['b'].add(3)

my_dict['c'] = 5
my_dict['d']

print(my_dict)
