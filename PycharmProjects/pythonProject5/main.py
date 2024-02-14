# Output:
# Disease Name: Dengue
# Symptoms: ['Fever', 'Cold']
# ======================
# Disease Name: Covid
# Symptoms: ['Sore throat', 'Cough', 'Headache']

# class Disease:
#     def __init__(self, name, *sy0):
#         self.d_name = name
#         self.d_symp = list(sy0)
#
#     def details(self):
#         return f'Disease Name: {self.d_name}\nSymptoms: {self.d_symp}'
#
#
# d1 = Disease("Dengue", "Fever", "Cold")
# print(d1.details())
#
# print("======================")
#
# d2 = Disease("Covid", "Sore throat", "Cough", "Headache")
# print(d2.details())


class MidA:
    def __init__(self):
        self.x = -1
        self.y = 2
        self.sum = 7

    def methodA(self, p):
        self.y = self.sum + self.x           # self.y = 7 - 1 = 6
        self.sum = p[1] * len(p)            # self.sum = 3 * 5 = 15
        f = MidA()
        f.sum = self.sum + self.methodB(f, list(p))
        self.x = p[0] + p[-1] + f.sum
        print(self.x, self.y, self.sum)
    def methodB(self, t, r= [1, 2]):
        y = 3
        t.x = self.x + self.sum
        t.sum = t.x + t.y + y
        print(t.x, t.y, t.sum)
        return r[1]

a = MidA()

a.methodA((7,3,2,4,8))
a.methodB(a)