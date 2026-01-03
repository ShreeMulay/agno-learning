
class Animal:
    """Base class for animals."""
    def __init__(self, name: str):
        self.name = name
    
    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    """A dog that can bark."""
    def __init__(self, name: str, breed: str):
        super().__init__(name)
        self.breed = breed
    
    def speak(self) -> str:
        return "Woof!"
    
    def fetch(self, item: str) -> str:
        return f"{self.name} fetched the {item}"

class Cat(Animal):
    """A cat that can meow."""
    def __init__(self, name: str, color: str):
        super().__init__(name)
        self.color = color
    
    def speak(self) -> str:
        return "Meow!"
    
    def scratch(self) -> str:
        return f"{self.name} scratches furniture"

class Pet:
    """A pet with an owner."""
    def __init__(self, animal: Animal, owner: str):
        self.animal = animal
        self.owner = owner
    
    def introduce(self) -> str:
        return f"{self.owner}\'s pet {self.animal.name} says {self.animal.speak()}"
