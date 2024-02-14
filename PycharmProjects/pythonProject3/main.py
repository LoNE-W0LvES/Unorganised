# class Farmer:
#     def __init__(self, n=""):
#         self.n = n
#         self.c = []
#         self.f = []
#
#     def addCrops(self, *c):
#         if len(c) > 0:
#             self.c.extend(c)
#             print(len(c), "crop(s) added.")
#         else:
#             print("No crop(s) added.")
#
#     def addFishes(self, *f):
#         if len(f) > 0:
#             self.f.extend(f)
#             print(len(f), "fish(s) added.")
#         else:
#             print("No fish added.")
#
#     def showGoods(self):
#         print(f"Welcome to your farm, {self.n}!"if self.n != "" else "Welcome to your farm!")
#         print("-------------------")
#         print("You don't have any crop(s)." if len(self.c) > 0 else f"You have{len(self.c)} crop(s):\n{','.join(self.c)}")
#         print("You don't have any fish(s)." if len(self.f) > 0 else f"You have{len(self.f)} fish(s):\n{','.join(self.f)}")
#         print("-------------------")
#
#
# f1 = Farmer()
# print("-------------------")
# f1.addCrops('Rice', 'Jute', 'Cinnamon')
# print("-------------------")
# f1.addFishes()
# print("-------------------")
# f1.addCrops('Mustard')
# print("-------------------")
# f1.showGoods()
# print("-------------------")
# f2 = Farmer("Korim Mia")
# print("-------------------")
# f2.addFishes('Pangash', 'Magur')
# print("-------------------")
# f2.addCrops("Wheat", "Potato")
# print("-------------------")
# f2.addFishes("Koi", "Tuna", "Sardine")
# print("-------------------")
# f2.showGoods()
# print("-------------------")
# f3 = Farmer(2865127000)
# print("-------------------")
# f3.addCrops()
# print("-------------------")
# f3.addFishes("Katla")
# print("-------------------")
# f3.showGoods()
# print("-------------------")


# class UniversalStudiosUser:
#     def __init__(self, n, a, c):
#         print("Welcome to Universal Studios.")
#         self.n = n
#         self.a = a
#         self.c = c
#         self.srl = []
#
#     def selected_rides(self, *rides):
#         for r in rides:
#             self.srl.append({'ride': (r.split('-')[0].strip()), 'amount': int(r.split('-')[1])})
#         print("Added ride(s) successfully.")
#
#     def show_details(self):
#         print(f"Your information:\nName: {self.n}, Age: {self.a}, Category: {self.c}\nSelected rides:")
#         for ride in self.srl:
#             print(f"Ride: {ride['ride']}, Amount: {ride['amount']} dollar(s)")
#         ta = sum(ride['amount'] for ride in self.srl)
#         if self.c == "Special" and len(self.srl) > 3:
#             d = ta * 0.2
#             ta -= d
#             print("Congratulations!!! You've got a 20% discount.")
#         else:
#             d = 0
#         print(f"Please pay {float(ta)} dollar(s).")
#
#
# customer_1 = UniversalStudiosUser("Alice", 21, "Special")
# print("--------- 1 ---------")
# customer_1.selected_rides("Waterworld-100", "Accelerator-200", "DinoSoarin-50")
# print("--------- 2 ---------")
# customer_1.show_details()
#
# print("=================")
#
# customer_2 = UniversalStudiosUser("Bob", 20, "Normal")
# print("--------- 3 ---------")
# customer_2.selected_rides("Enchanted Airways-300", "Jurassic Park-500", "Accelerator-200", "DinoSoarin-50")
# print("--------- 4 ---------")
# customer_2.show_details()
#
# print("=================")
#
# customer_3 = UniversalStudiosUser("Mark", 15, "Special")
# print("--------- 5 ---------")
# customer_3.selected_rides("Transformers-450", "Jurassic Park-500", "Waterworld-100", "DinoSoarin-50")
# print("--------- 6 ---------")
# customer_3.show_details()


# class Department:
#     def __init__(self, n="ChE Department", s=5):
#         self.name = n
#         self.s = s
#         self.st = []
#
#     def add_students(self, *s):
#         self.st.extend(s)
#
#     def calculate_average_students(self):
#         if len(self.st) == self.s:
#             average_students = sum(self.st) / self.s
#             return average_students
#         else:
#             return None
#
#     def merge_Department(self, *dept):
#         m_d = []
#         for d in dept:
#             if len(d.st) == d.s:
#                 m_d.append(d)
#                 self.s += d.s
#                 self.st.extend(d.st)
#
#         if len(m_d) > 0:
#             m_d_r = ', '.join(dept.name for dept in m_d)
#             return f"{m_d_r} is merged to {self.name}.\nNow the {self.name} has an average of {self.calculate_average_students()} students in each section."
#         else:
#             return f"No departments merged to {self.name}."
#
#
# # Driver Code
# d1 = Department()
# print('1-----------------------------------')
# d2 = Department('MME Department')
# print('2-----------------------------------')
# d3 = Department('NCE Department', 8)
# print('3-----------------------------------')
# d1.add_students(12, 23, 12, 34, 21)
# print('4-----------------------------------')
# d2.add_students(40, 30, 21)
# print('5-----------------------------------')
# d3.add_students(12, 34, 41, 17, 30, 22, 32, 51)
# print('6-----------------------------------')
# mega = Department('Engineering Department', 10)
# print('7-----------------------------------')
# mega.add_students(21, 30, 40, 36, 10, 32, 27, 51, 45, 15)
# print('8-----------------------------------')
# print(mega.merge_Department(d1, d2))
# print('9-----------------------------------')
# print(mega.merge_Department(d3))

#
# class Department:
#     def __init__(self, n="ChE Department", s=5):
#         self.n = n
#         self.s = s
#         self.a = 0
#         self.st_l = []
#         print(f"The {self.n} has {self.s} sections.")
#
#     def add_students(self, *st):
#         if self.s == len(st):
#             self.st_l.extend(st)
#             self.a = sum(st) / self.s
#             print(f"The {self.n} has an average of {round(self.a, 2)} students in each section.")
#         else:
#             print(f"The {self.n} doesn't have {len(st)} sections.")
#
#     def merge_Department(self, *dept):
#         st_l = self.st_l
#         m = self.s
#         for d in dept:
#             st_l.extend(d.st_l)
#         self.a = sum(st_l) / m
#         for d in dept:
#             print(f"{d.n} is merged to {self.n}.")
#         return f"Now the {self.n} has an average of {self.a} students in each section."
#
#
# d1 = Department()
# print('1-----------------------------------')
# d2 = Department('MME Department')
# print('2-----------------------------------')
# d3 = Department('NCE Department', 8)
# print('3-----------------------------------')
# d1.add_students(12, 23, 12, 34, 21)
# print('4-----------------------------------')
# d2.add_students(40, 30, 21)
# print('5-----------------------------------')
# d3.add_students(12, 34, 41, 17, 30, 22, 32, 51)
# print('6-----------------------------------')
# mega = Department('Engineering Department', 10)
# print('7-----------------------------------')
# mega.add_students(21, 30, 40, 36, 10, 32, 27, 51, 45, 15)
# print('8-----------------------------------')
# print(mega.merge_Department(d1, d2))
# print('9-----------------------------------')
# print(mega.merge_Department(d3))


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
#


# class msgClass:
#     def __init__(self):
#         self.content = 0
# class Q5:
#     def __init__(self):
#         self.sum = 1
#         self.x = 2
#         self.y = 3
#     def methodA(self):
#         x, y = 1, 1
#         msg = []
#         myMsg = msgClass()
#         myMsg.content = self.x
#         msg.append(myMsg)
#         msg[0].content = self.y + myMsg.content
#         self.y = self.y + self.methodB(msg[0])
#         y = self.methodB(msg[0]) + self.y
#         x = y + self.methodB(msg[0], msg)
#         self.sum = x + y + msg[0].content
#         print(x," ", y," ", self.sum)
#
#     def methodB(self, mg1, mg2 = None):
#         if mg2 == None:
#             x, y = 5, 6
#             y = self.sum + mg1.content
#             self.y = y + mg1.content
#             x = self.x + 7 +mg1.content
#             self.sum = self.sum + x + y
#             self.x = mg1.content + x +8
#             # print(x, " ", y," ", self.sum)
#             return y
#         else:
#             x = 1
#             self.y += mg2[0].content
#             mg2[0].content = self.y + mg1.content
#             x = x + 4 + mg1.content
#             self.sum += x + self.y
#             mg1.content = self.sum - mg2[0].content
#             # print(self.x, " ",self.y," ", self.sum)
#             return self.sum
#
#
# q = Q5()
# q.methodA()

#
# class Test4:
#     def __init__(self):
#         self.sum, self.y = 0, 0
#     def methodA(self):
#         x, y = 0, 0
#         msg = [0]
#         msg[0] = 5
#         y = y + self.methodB(msg[0])
#         x = y + self.methodB(msg, msg[0])
#         self.sum = x + y + msg[0]
#         print(x, y, self.sum)
#     def methodB(self, *args):
#         if len(args) == 1:
#             mg1 = args[0]
#             x, y = 0, 0
#             y = y + mg1
#             x = x + 33 + mg1
#             self.sum = self.sum + x + y
#             self.y = mg1 + x + 2
#             # print(x, y, self.sum)
#             return y
#         else:
#             mg2, mg1 = args
#             x = 0
#             self.y = self.y + mg2[0]
#             x = x + 33 + mg1
#             self.sum = self.sum + x + self.y
#             mg2[0] = self.y + mg1
#             mg1 = mg1 + x + 2
#             # print(x, self.y, self.sum)
#             return self.sum
#
#
# t3 = Test4()
# t3.methodA()
# t3.methodA()
# t3.methodA()
# t3.methodA()



