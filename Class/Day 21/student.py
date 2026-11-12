import random

class AgeException(Exception):
    def __init__(self,*args):
        super().__init__("Age should be positive",*args)

class Student:
    def __init__(self,id:int,name:str,age:int):
        self.id = id
        self.name = name
        if age < 0:
            raise AgeException()
        self.age = age
        self.__password = random.randint(1,1000)*5253

    def get_password(self):
        return self.__password

    def __str__(self):
        return f"{self.id} : {self.name} {self.age}"

if __name__ == '__main__':
    sid = Student(1,'Sid',23)
    print(sid.get_password())
