from abc import ABC, abstractmethod
from datetime import datetime
import statistics
import time

class Source(ABC):
    @abstractmethod
    def read(self):
        pass
    
class ActionObserver(ABC):
    @abstractmethod
    def update(self, collection):
        pass
    
class KeyboardSource(Source):
    def read(self):
        try:
            return int(input("Enter number (-1 to stop): "))
        except:
            print("Invalid input. Please enter a number.")
            return self.read()
        
class FileSource(Source):
    def __init__(self, filename) -> None:
        self.file = open(filename, 'r')
        
    def read(self):
        _input = self.file.readline().strip()
        return int(_input) if _input else -1
    
    def __del__(self):
        self.file.close()
        
class FileAction(ActionObserver):
    def __init__(self, filename) -> None:
        self.filename = filename
        
    def update(self, collection):
        with open(self.filename, 'w+') as f:
            timestamp = datetime.datetime.now()
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Collection: {collection}\n\n")
    
class SumAction(ActionObserver):
    def update(self, collection):
        print(f"Sum: {sum(collection)}")

class MeanAction(ActionObserver):
    def update(self, collection):
        print(f"Mean: {statistics.mean(collection)}")
        
class MedianAction(ActionObserver):
    def update(self, collection):
        print(f"Median: {statistics.median(collection)}")

class NumberSequence:
    def __init__(self, source: Source) -> None:
        self.source: Source = source
        self.collection = []
        self.action_observers: list[ActionObserver]= []
        
    def add_observers(self, *observers):
        self.action_observers.extend(observers)
        
    def update_observers(self):
        [observer.update(self.collection) for observer in self.action_observers]
        
    def start(self):
        while True:
            _input = self.source.read()
            if _input == -1:
                break
            self.collection.append(_input)
            time.sleep(1)
            self.update_observers()
    
def main():
    ns = NumberSequence(KeyboardSource())
    actions = [SumAction(), MeanAction(), MedianAction()]
    ns.add_observers(*actions)
    ns.start()

if __name__ == "__main__":
    main()
   
