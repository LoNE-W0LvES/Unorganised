# class StudentRoutineGenerator:
#     def __init__(self, n, mc):
#         self.n = n
#         self.mc = mc
#         self.c_c = 0
#         self.r = {'Sat/Thurs': {}, 'Sun/Tue': {}, 'Mon/Wed': {}}
#         print(f"Name: {self.n}\nMaximum Number of Courses: {self.mc}\nInitial Routine: {self.r}")
#
#     def addCourses(self, *courses):
#         for c in courses:
#             ff = 0
#             gg = 0
#             ci = c.split('-')
#             cc = ci[0].strip()
#             ct = ci[1].strip() + "-" + ci[2].strip()
#             ct_d = ct.split('-')[0]
#             ct_t = ct.split('-')[1]
#             if self.c_c < self.mc:
#                 for x in self.r.values():
#                     for y in x.values():
#                         if cc in y:
#                             ff = 1
#                 for x in self.r[ct_d]:
#                     if ct_t in x:
#                         gg = 1
#                 if ff == 0 and gg == 0:
#                     self.r[ct_d][ct_t] = cc
#                     self.c_c = self.c_c + 1
#                     print("Successfully added", cc + "!")
#                 else:
#                     if gg == 0:
#                         print("You already have", cc, "in your routine")
#                     else:
#                         print(f"Can't take {cc}. It's clashing with your {self.r[ct_d][ct_t]}")
#             else:
#                 print("You can't take more than", self.mc, "courses")
#
#     def dropCourse(self, cc):
#         cd = False
#         for t in self.r:
#             if cc in self.r[t].values():
#                 ct = list(self.r[t].keys())[list(self.r[t].values()).index(cc)]
#                 del self.r[t][ct]
#                 cd = True
#                 print("Successfully dropped", cc)
#                 break
#         if not cd:
#             print("No such course in your routine")
#
#     def showRoutine(self):
#         print("Updated Routine:")
#         print(self.r)
#         print("Routine Details:")
#         for t in self.r:
#             if self.r[t]:
#                 print(t + ":")
#                 for time in self.r[t]:
#                     print(time + " -", self.r[t][time])
#
# # Driver Code
# print("########################################")
# st1 = StudentRoutineGenerator('Harry', 4)
# print('------------------------------')
# st1.addCourses('CSE110-Mon/Wed-12:30', 'MAT110-Mon/Wed-2:00')
# st1.addCourses('ENG101-Sun/Tue-12:30', 'CSE110-Mon/Wed-9:30')
# st1.addCourses('PHY111-Sun/Tue-12:30')
# print('------------------------------')
# st1.showRoutine()
# print('------------------------------')
# st1.dropCourse('CSE110')
# st1.dropCourse('PHY112')
# print('------------------------------')
# st1.showRoutine()
# print('########################################')
# st2 = StudentRoutineGenerator('John', 3)
# print('------------------------------')
# st2.addCourses('MAT110-Mon/Wed-8:00')
# st2.addCourses('ENG101-Sat/Thurs-12:30', 'CSE110-Sun/Tue-9:30')
# st2.addCourses('PHY111-Sun/Tue-12:30')
# print('------------------------------')
# st2.showRoutine()


# class QuizB:
#     def __init__(self):
#         self.x = 3
#         self.y = 6
#         self.sum = 4
#
#     def methodA(self, *r):
#         self.y = self.sum + self.x + r[len(r)//2]
#         self.sum = r[2] + self.y
#         d = QuizB()
#         d.sum = self.sum + self.methodB(d, r) + self.sum
#         self.x = r[1] + r[2] + d.sum
#         print(self.x, self.y, self.sum)
#
#     def methodB(self, t, z=0):
#         y = 3
#         t.x = self.x + self.sum
#         t.sum = t.x + t.y + y
#         self.sum = self.y + y
#         print(t.x, t.y, t.sum)
#         if z == 0:
#             return t.sum
#         else:
#             return z[2]
#
#
# a = QuizB()
# a.methodA(8, 2, 4)
# a.methodB(a)
#


# class Book:
#     def __init__(self, title, author, genre):
#         self.__title = title
#         self.__author = author
#         self.__genre = genre
#         self.__available = True
#         self.__borrower = None
#
#     def set_title(self, title):
#         self.__title = title
#
#     def get_title(self):
#         return self.__title
#
#     def set_author(self, author):
#         self.__author = author
#
#     def get_author(self):
#         return self.__author
#
#     def set_genre(self, genre):
#         self.__genre = genre
#
#     def get_genre(self):
#         return self.__genre
#
#     def set_availability(self, available):
#         self.__available = available
#
#     def get_availability(self):
#         return self.__available
#
#     def set_borrower(self, borrower):
#         self.__borrower = borrower
#
#     def get_borrower(self):
#         return self.__borrower
#
#     def display_info(self):
#         print(f"Title: {self.__title}")
#         print(f"Author: {self.__author}")
#         print(f"Genre: {self.__genre}")
#         print(f"Availability: {'Available' if self.__available else 'Not Available'}")
#         if self.__borrower:
#             print(f"Borrower: {self.__borrower.get_name()}")
#         else:
#             print("Borrower: None")
#
#
# class LibraryMember:
#     def __init__(self, member_id, name):
#         self.__member_id = member_id
#         self.__name = name
#         self.__borrowed_books = []
#
#     def set_member_id(self, member_id):
#         self.__member_id = member_id
#
#     def get_member_id(self):
#         return self.__member_id
#
#     def set_name(self, name):
#         self.__name = name
#
#     def get_name(self):
#         return self.__name
#
#     def borrow_book(self, book):
#         if book.get_availability():
#             book.set_availability(False)
#             book.set_borrower(self)
#             self.__borrowed_books.append(book)
#             print(f"{self.__name} has borrowed the book '{book.get_title()}'")
#         else:
#             print("Sorry, the book is not available for borrowing.")
#
#     def return_book(self, book):
#         if book in self.__borrowed_books:
#             book.set_availability(True)
#             book.set_borrower(None)
#             self.__borrowed_books.remove(book)
#             print(f"{self.__name} has returned the book '{book.get_title()}'")
#         else:
#             print("You haven't borrowed this book.")
#
#     def display_borrowed_books(self):
#         if self.__borrowed_books:
#             print(f"{self.__name} has borrowed the following books:")
#             for book in self.__borrowed_books:
#                 print(f" - {book.get_title()}")
#         else:
#             print(f"{self.__name} has not borrowed any books yet.")
#
#
# class Library:
#     def __init__(self):
#         self.__books_available = []
#         self.__library_members = []
#
#     def add_book(self, book):
#         self.__books_available.append(book)
#
#     def add_library_member(self, member):
#         self.__library_members.append(member)
#
#     def display_book_list(self):
#         if self.__books_available:
#             print("List of available books in the library:")
#             for book in self.__books_available:
#                 print(f" - {book.get_title()} by {book.get_author()} (Genre: {book.get_genre()})")
#         else:
#             print("No books available in the library.")
#
#     def display_library_members(self):
#         if self.__library_members:
#             print("List of library members:")
#             for member in self.__library_members:
#                 print(f" - {member.get_name()} (Member ID: {member.get_member_id()})")
#         else:
#             print("No library members registered yet.")
#
#
# # Demo driver code
# if __name__ == "__main__":
#     book1 = Book("Harry Potter and the Chamber of Secrets", "J.K. Rowling", "Fiction")
#     book2 = Book("Nothing Lasts Forever", "Sidney Sheldon", "Fiction")
#     book3 = Book("Calculus", "Gilbert Strang", "Education")
#
#     # Create LibraryMember objects
#     member1 = LibraryMember("LM01", "Tom Cruise")
#     member2 = LibraryMember("LM02", "Brad Pitt")
#
#     # Create Library object
#     library = Library()
#
#     # Add books to the library
#     library.add_book(book1)
#     library.add_book(book2)
#     library.add_book(book3)
#
#     # Add library members
#     library.add_library_member(member1)
#     library.add_library_member(member2)
#
#     # Library members borrow books
#     member1.borrow_book(book1)
#     member1.borrow_book(book2)
#     member2.borrow_book(book3)
#
#     # Display all books in the library
#     library.display_book_list()
#     print("1======================================")
#
#     # Display library members and their borrowed books
#     member1.display_borrowed_books()
#     print("2======================================")
#     member2.display_borrowed_books()
#     print("3======================================")
#     # Returning book2 by member 1
#     member1.return_book(book2)
#     print("4======================================")
#     # Display library member1's borrowed books
#     member1.display_borrowed_books()
#     # Display all books in the library
#     library.display_book_list()



# class Book:
#     def __init__(self, title, author, genre):
#         self.title = title
#         self.author = author
#         self.genre = genre
#         self.available = True
#         self.borrower = None
#
#     def set_title(self, title):
#         self.title = title
#
#     def get_title(self):
#         return self.title
#
#     def set_author(self, author):
#         self.author = author
#
#     def get_author(self):
#         return self.author
#
#     def set_genre(self, genre):
#         self.genre = genre
#
#     def get_genre(self):
#         return self.genre
#
#     def set_availability(self, available):
#         self.available = available
#
#     def get_availability(self):
#         return self.available
#
#     def set_borrower(self, borrower):
#         self.borrower = borrower
#
#     def get_borrower(self):
#         return self.borrower
#
#     def display_info(self):
#         print(f"Title: {self.title}")
#         print(f"Author: {self.author}")
#         print(f"Genre: {self.genre}")
#         print(f"Available: {self.available}")
#         if self.borrower:
#             print(f"Borrowed by:{self.borrower.get_member_id()}")
#         else:
#             print("Borrowed by:None")
#         print("---------------")
#
#
# class LibraryMember:
#     def __init__(self, member_id, name):
#         self.member_id = member_id
#         self.name = name
#         self.borrowed_books = []
#
#     def set_member_id(self, member_id):
#         self.member_id = member_id
#
#     def get_member_id(self):
#         return self.member_id
#
#     def set_name(self, name):
#         self.name = name
#
#     def get_name(self):
#         return self.name
#
#     def borrow_book(self, book):
#         if book.get_availability():
#             book.set_availability(False)
#             book.set_borrower(self)
#             self.borrowed_books.append(book)
#
#     def return_book(self, book):
#         if book in self.borrowed_books:
#             book.set_availability(True)
#             book.set_borrower(None)
#             self.borrowed_books.remove(book)
#
#     def display_borrowed_books(self):
#         print(f"Books borrowed by {self.name}")
#         for book in self.borrowed_books:
#             print(f"Title: {book.get_title()}")
#             print(f"Author: {book.get_author()}")
#             print(f"Genre: {book.get_genre()}")
#             print(f"Available: {book.get_availability()}")
#             print("---------------")
#
#
# class Library:
#     def __init__(self):
#         self.books_available = []
#         self.library_members = []
#
#     def add_book(self, book):
#         self.books_available.append(book)
#
#     def add_library_member(self, member):
#         self.library_members.append(member)
#
#     def display_book_list(self):
#         print("All the books in library are:")
#         for book in self.books_available:
#             book.display_info()
#
#     def display_library_members(self):
#         print("Library Members:")
#         for member in self.library_members:
#             print(f"Member ID: {member.get_member_id()}, Name: {member.get_name()}")
#
#
# if __name__ == "__main__":
#     book1 = Book("Harry Potter and the Chamber of Secrets", "J.K. Rowling", "Fiction")
#     book2 = Book("Nothing Lasts Forever", "Sidney Sheldon", "Fiction")
#     book3 = Book("Calculus", "Gilbert Strang", "Education")
#
#     # Create LibraryMember objects
#     member1 = LibraryMember("LM01", "Tom Cruise")
#     member2 = LibraryMember("LM02", "Brad Pitt")
#
#     # Create Library object
#     library = Library()
#
#     # Add books to the library
#     library.add_book(book1)
#     library.add_book(book2)
#     library.add_book(book3)
#
#     # Add library members
#     library.add_library_member(member1)
#     library.add_library_member(member2)
#
#     # Library members borrow books
#     member1.borrow_book(book1)
#     member1.borrow_book(book2)
#     member2.borrow_book(book3)
#
#     # Display all books in the library
#     library.display_book_list()
#     print("1======================================")
#
#     # Display library members and their borrowed books
#     member1.display_borrowed_books()
#     print("2======================================")
#     member2.display_borrowed_books()
#     print("3======================================")
#     # Returning book2 by member 1
#     member1.return_book(book2)
#     print("4======================================")
#     # Display library member1's borrowed books
#     member1.display_borrowed_books()
#     # Display all books in the library
#     library.display_book_list()


# class Student:
#     def __init__(self, name, student_id, cgpa):
#         self.name = name
#         self.id = student_id
#         self.cgpa = cgpa
#
#     def getName(self):
#         return self.name
#
#     def getId(self):
#         return self.id
#
#     def getCgpa(self):
#         return self.cgpa
#
#     def setId(self, new_id):
#         self.id = new_id
#
#
# class Department:
#     def __init__(self, name):
#         self.name = name
#         self.students = []
#
#     def findStudent(self, student_id):
#         found = False
#         for student in self.students:
#             if student.getId() == student_id:
#                 print(f"Student info:\nStudent Name: {student.getName()}\nID: {student.getId()}\nCGPA:  {student.getCgpa()}")
#                 found = True
#                 break
#         if not found:
#             print("Student with this ID doesn't exist, Please give a valid ID")
#
#     def addStudent(self, *students):
#         for student in students:
#             id_exists = any(s.getId() == student.getId() for s in self.students)
#             if not id_exists:
#                 print(f"Welcome to {self.name} department, {student.getName()}")
#                 self.students.append(student)
#             else:
#                 print("Student with the same ID already exists, Please try with another ID")
#
#     def details(self):
#         print(f"Department Name: {self.name}\nNumber of student:{len(self.students)}\nDetails of the students: ")
#         for student in self.students:
#             print(f"Student name: {student.getName()}, ID: {student.getId()}, cgpa: {student.getCgpa()}")
#
#
# # Driver Code
# s1 = Student("Akib", 22301010, 3.29)
# s2 = Student("Reza", 22101010, 3.45)
# s3 = Student("Ruhan", 23101934, 4.00)
#
# print("1=======================================")
# cse = Department("CSE")
# cse.findStudent(22112233)
#
# print("2=======================================")
# cse.addStudent(s1, s2, s3)
#
# print("3=======================================")
# cse.details()
#
# print("4=======================================")
# cse.findStudent(22301010)
#
# print("5=======================================")
# s4 = Student("Nakib", 22301010, 3.22)
# cse.addStudent(s4)
#
# print("6=======================================")
# s4.setId(21201220)
# cse.addStudent(s4)
#
# print("7=======================================")
# cse.details()
#
# print("8=======================================")
# s5 = Student("Sakib", 22201010, 2.29)
# cse.addStudent(s5)
#
# print("9=======================================")
# cse.details()


# class Cargo:
#     def __init__(self, name, weight):
#         self.name = name
#         self.weight = weight
#
#     def get_name(self):
#         return self.name
#
#     def get_weight(self):
#         return self.weight
#
#
# class Spaceship:
#     def __init__(self, name, capacity):
#         self.name = name
#         self.capacity = capacity
#         self.cargo = []
#
#     def load_cargo(self, cargo):
#         total_cargo_weight = sum(c.get_weight() for c in self.cargo)
#         if total_cargo_weight + cargo.get_weight() <= self.capacity:
#             self.cargo.append(cargo)
#         else:
#             print(f"Warning: Unable to load {cargo.get_name()} inside {self.name}. Exceeds capacity by {total_cargo_weight + cargo.get_weight() - self.capacity}.")
#
#     def display_details(self):
#         total_cargo_weight = sum(c.get_weight() for c in self.cargo)
#         cargo_names = [c.get_name() for c in self.cargo]
#         print(f"Spaceship Name: {self.name}\nCapacity: {self.capacity}\nCurrent Cargo Weight: {total_cargo_weight}\nCargo: {cargo_names}")
#
#
# # Driver Code
# falcon = Spaceship("Falcon", 50000)
# apollo = Spaceship("Apollo", 100000)
# enterprise = Spaceship("Enterprise", 220000)
# print("1.===================================")
#
# gold = Cargo("Gold", 20000)
# platinum = Cargo("Platinum", 25000)
# dilithium = Cargo("Dilithium", 50000)
# trilithium = Cargo("Trilithium", 70000)
# neutronium = Cargo("Neutronium", 80000)
# print("2.===================================")
#
# falcon.load_cargo(gold)
# falcon.load_cargo(platinum)
# falcon.display_details()
# print("3.===================================")
#
# apollo.load_cargo(gold)
# apollo.display_details()
# print("4.===================================")
#
# falcon.load_cargo(neutronium)
# print("5.===================================")
#
# enterprise.load_cargo(dilithium)
# enterprise.load_cargo(trilithium)
# enterprise.load_cargo(neutronium)
# enterprise.display_details()



