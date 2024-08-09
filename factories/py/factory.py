import os
import importlib

def myfactory(module_name):
    mod = importlib.import_module('plugins.' + module_name)
    return getattr(mod, module_name)


def printGreeting(pet):
    print(f"{pet.name}: {pet.greet()}")


def printMenu(pet):
    print(f"{pet.name} voli {pet.menu()}")


def test():
    pets = []

    for mymodule in os.listdir('plugins'):
        moduleName, moduleExt = os.path.splitext(mymodule)

        if moduleExt == '.py':
            ljubimac = myfactory(moduleName)('Ljubimac ' + str(len(pets)))
            pets.append(ljubimac)

    for pet in pets:
        printGreeting(pet)
        printMenu(pet)

if __name__ == "__main__":
    test()