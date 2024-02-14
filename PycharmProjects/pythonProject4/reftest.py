class Program:
    def __init__(self, name, credit):
        self.name = name
        self.credit = credit
        self.students = []

    def __str__(self):
        s = "Program: " + self.name + ", Credit hours: " + str(self.credit) + "\n"
        s += "Total student(s): " + str(len(self.students)) + "\n"
        for student in self.students:
            s += str(student) + "\n"
        return s

    def addStudentWithCreditsCompleted(self, *args):
        for i in range(0, len(args), 2):
            self.students.append(Student(args[i], self.credit - args[i + 1], completed=False))

    def addStudentWithCreditsRemaining(self, *args):
        for i in range(0, len(args), 2):
            self.students.append(Student(args[i], self.credit - args[i + 1], completed=True))


class Student:
    def __init__(self, name, credits, completed=True):
        self.name = name
        self.credits = credits
        self.completed = completed

    def __str__(self):
        return "Name: " + self.name + (", Credits completed: " if self.completed else ", Credits remaining: ") + str(self.credits)


p1 = Program("CSE", 136)
print("1===================")
p1.addStudentWithCreditsCompleted("Bob", 12, "Carol", 18, "Mike", 18)
print("2===================")

print(p1)
print("3===================")
p1.addStudentWithCreditsRemaining("David", 12, "Simon", 18)
print("4===================")
print(p1)
