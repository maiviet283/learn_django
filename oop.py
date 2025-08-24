from abc import ABC, abstractmethod

class Animal(ABC):
    count = 0
    def __init__(self, name:str, age:int):
        self.__name = name
        self.__age = age
        Animal.countNumber()

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if len(value) > 0:
            self.__name = value
        else: 
            raise "len name > 0"
        
    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, value):
        if value > 0:
            self.__age = value
        else:
            raise "age > 0"


    @staticmethod
    def infomation():
        print("day la static method lop animal")

    @abstractmethod
    def speak(self):
        pass

    @classmethod
    def countNumber(cls):
        cls.count += 1
        return cls.count
    
    def __str__(self):
        return f"Animal {self.__name} : ({self.__age} years old)"
    

class Dog(Animal):
    def __init__(self, name, age, height):
        super().__init__(name, age)
        self.__height = height

    @property
    def height(self):
        return self.__height
    
    @height.setter
    def height(self, value):
        if value > 0:
            self.__height = value
        else:
            raise "height > 0"
        
    def speak(self):
        return "go go"
    
    def __str__(self):
        return f"Dog - " + super().__str__()
    

class Cat(Animal):
    def __init__(self, name, age, height):
        super().__init__(name, age)
        self.__height = height

    @property
    def height(self):
        return self.__height
    
    @height.setter
    def height(self, value):
        if value > 0:
            self.__height = value
        else:
            raise "height > 0"
        
    def speak(self):
        return "Meo Meo"
    

class Manager:
    def __init__(self):
        self.ds = []

    def addAnimal(self, animal: Animal):
        self.ds.append(animal)

    def allAnimalSpeak(self):
        for animal in self.ds:
            print(animal.speak())



dog1 = Dog("name dog 1", 3, 23)
dog2 = Dog("name dog 2", 5, 23)
dog3 = Dog("name dog 3", 2, 23)

cat1 = Cat("name cat 1", 3, 23)
cat2 = Cat("name cat 2", 3, 23)
cat3 = Cat("name cat 3", 3, 23)


manager = Manager()
manager.addAnimal(dog1)
manager.addAnimal(cat2)
manager.addAnimal(cat3)

manager.allAnimalSpeak()


print("So luong Animal (Dog + Cat) da duoc tao:", Animal.count)