class Department:
    def __init__(self, name, required_credits):
        self.name = name
        self.required_credits = required_credits
        self.students = []
        print(f"{name} students need to complete {required_credits} credits")

    def addStudent(self, student):
        if student.major == self.name:
            self.students.append(student)
            print(f"{student.name} added! {self.name} department")
        else:
            print(f"{student.major} student can't be added to {self.name} department")

    def showAll(self):
        print(f"Total Students: {len(self.students)}")
        for student in self.students:
            print("------------------")
            print(f"Name: {student.name} ID: {student.id} CGPA: {student.cgpa}")


class Student:
    student_id = 0

    def __init__(self, name, major, cgpa):
        self.name = name
        self.major = major
        self.cgpa = cgpa
        self.id = f"{self.generateID() :03}"

    def generateID(self):
        Student.student_id += 1
        return Student.student_id

    def changeChoice(self, new_major):
        self.major = new_major

    @classmethod
    def createObject(cls, student_info):
        name, major, cgpa = student_info.split("-")
        return cls(name, major, float(cgpa))


# Simulation
d1 = Department("CSE", 136)
print("===================")
s1 = Student("Bob", "CSE", 3.8)

s2 = Student("Carol", "CSE", 3.9)

s3 = Student.createObject("Mike-CSE-3.5")

s4 = Student("Jake", "BBA", 3.7)
print("===================")
d1.addStudent(s1)
print("===================")
d1.addStudent(s2)
d1.addStudent(s3)
print("===================")
d1.addStudent(s4)
print("===================")
d1.showAll()
print("===================")
s4.changeChoice("CSE")
print("===================")
d1.addStudent(s4)
print("===================")
d1.showAll()
