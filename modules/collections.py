from colorama import init, Fore

from collections import Counter
from collections import defaultdict
from collections import OrderedDict
from collections import namedtuple

# Colorama (run this in cmd.exe)
init()

# Counter
print(Fore.RED + "Counter: ")
sentence = 'How many many many times does does does each word word word word word show up in this sentence'
cntr = Counter(sentence.split())
print(cntr.most_common())
print()

# Defaultdict
print(Fore.MAGENTA + "DefaultDict: ")
default_dictionary = defaultdict(lambda: 'default')
default_dictionary['key']
print(default_dictionary.items())
print()

# OrderedDict (only equal if order is the same)
print(Fore.BLUE + "OrderedDict: ")
ordered_dictionary = OrderedDict()
ordered_dictionary['a'] = 1
ordered_dictionary['b'] = 2
ordered_dictionary['c'] = 3
ordered_dictionary['d'] = 4
ordered_dictionary['e'] = 5
for key,value in ordered_dictionary.items():
    print(f"{key} : {value}")
print()

# NamedTuple
print(Fore.CYAN + "Namedtuple: ")
Person = namedtuple('Person', 'firstname lastname age')
person1 = Person(firstname="Kenny", lastname="Blanckaert", age=22)
print(person1.firstname)
print(person1.lastname)
print(person1.age)

