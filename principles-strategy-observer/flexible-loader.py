from abc import ABC, abstractmethod
from time import time


class Source(ABC):
    @abstractmethod
    def read():
        pass
    
class ActionObserver(ABC):
    @abstractmethod
    def update():
        pass

class NumberSequence:
    def __init__(self, source: Source) -> None:
        self.source: Source = source
        self.collection = []
        self.action_observers: list[ActionObserver]= []
        
    def add_observers(self, *observers):
        self.action_observers.extend(observers)
        
    def update_observers(self):
        [observer.update() for observer in self.action_observers]
        
    def start(self):
        while True:
            _input = self.source.read()
            if _input == -1:
                break
            time.sleep(1)
            self.update_observers()
    
def main():
    ns = NumberSequence("a")
    ns.add_observers("a", "b", "cccc")
    ns.start()

if __name__ == "__main__":
    main()
   
