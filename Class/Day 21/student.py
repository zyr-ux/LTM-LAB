class Student:
    def __init__(self,id:int,name:str,age:int):
        self.id = id
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.id} : {self.name} {self.age}"

if __name__ == '__main__':
    sid = Student(1,'Sid',23)
    print(sid)
