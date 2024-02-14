import datetime


class Employee:
    employee_count = {}

    def __init__(self, name, joining_date, work_experience, weekly_work_hour=-1):
        self.name = name
        self.joining_date = joining_date
        self.work_experience = work_experience
        self.weekly_work_hour = 40 if weekly_work_hour > 60 else weekly_work_hour
        ymd = self.joining_date.split('-')
        self.s_j_date = f"{ymd[2]}-{ymd[1]}-{ymd[0]}"

        if type(self) != InternProgrammer:
            self.__class__.employee_count[type(self).__name__] = self.__class__.employee_count.get(type(self).__name__, 0) + 1

    @classmethod
    def showDetails(cls):
        total_employee_count = sum(cls.employee_count.values())
        print("Company workforce:")
        print(f"Total Employee/s: {total_employee_count}")
        for emp_type, emp_count in cls.employee_count.items():
            print(f"Total {emp_type} Employee/s: {emp_count}")


class Programmer(Employee):
    designation_list = ['Junior Software Engineer', 'Software Engineer', 'Senior Software Engineer', 'Technical Lead']
    base_salaries = {'Junior Software Engineer': 30000, 'Software Engineer': 45000, 'Senior Software Engineer': 70000, 'Technical Lead': 120000}

    def __init__(self, name, joining_date, work_experience, weekly_work_hour=-1):
        super().__init__(name, joining_date, work_experience, weekly_work_hour)
        self.overtime = 0
        self.id = self.createProgrammerID()
        self.designation = self.designation_list[min(self.work_experience // 3, 3)]
        if self.weekly_work_hour < 40 and self.weekly_work_hour != -1:
            print(f'{self.name} can not work for {self.weekly_work_hour} hours.')

    def createProgrammerID(self):
        emp_count = Employee.employee_count.get('Programmer', 0) + Employee.employee_count.get('HR', 0)
        ymd = self.joining_date.split('-')
        j_y = ymd[0][-2:]
        emp_id = f'P-{j_y}{ymd[1]}{ymd[2]}-{emp_count}'
        return emp_id

    def calculateSalary(self):
        base_salary = self.base_salaries[self.designation]
        salary = (base_salary * (1.15 ** (2023 - int(self.joining_date.split('-')[0])))) + self.overtime
        gg = (str(salary).split('.')[1])
        gx = []
        sw = 0
        for i in gg:
            gx.append(i)

        for i in range(len(gx)):
            if gx[i] == '9':
                sw = 1
                gx[i - 1] = str(int(gx[i - 1]) + 1)
                gf = gx[0:i]
                k = ''
                for j in gf:
                    k = k+j
                sal = str(salary).split('.')[0] + '.' + k
                return sal
        if sw == 0:
            if str(salary).split('.')[1] == '0':
                salary = int(salary)
            return salary

    def calculateOvertime(self):
        if self.weekly_work_hour > 40:
            overtime_hours = (self.weekly_work_hour - 40) * 4
            overtime_amount = overtime_hours * 500
            print(f'{self.name} will get BDT {overtime_amount} overtime.')
            self.overtime = overtime_amount
            return overtime_amount
        if self.weekly_work_hour < 40:
            print(f'{self.name} will not get overtime.')
            return 0

    def showProgrammerDetails(self):
        salary = self.calculateSalary()
        print("Programmer Employee:")
        print(f"Name: {self.name}")
        print(f"ID: {self.id}")
        print(f"Joining Date: {self.s_j_date}")
        print(f"Designation: {self.designation}")
        print(f"Salary: BDT {salary}")


class HR(Employee):
    def __init__(self, name, joining_date, work_experience, weekly_work_hour=-1):
        super().__init__(name, joining_date, work_experience, weekly_work_hour)
        self.id = self.createHREmployeeID()
        if self.weekly_work_hour < 40 and self.weekly_work_hour != -1:
            print(f'{self.name} can not work for {self.weekly_work_hour} hours.')

    def createHREmployeeID(self):
        emp_count = Employee.employee_count.get('Programmer', 0) + Employee.employee_count.get('HR', 0)
        ymd = self.joining_date.split('-')
        j_y = ymd[0][-2:]
        emp_id = f'HR-{j_y}{ymd[1]}{ymd[2]}-{emp_count}'
        return emp_id

    def showHREmployeeDetails(self):
        print("HR Employee:")
        print(f"Name: {self.name}")
        print(f"ID: {self.id}")
        print(f"Joining Date: {self.s_j_date}")


class InternProgrammer(Employee):
    intern_count = 0

    def __init__(self, name, joining_date, intern_type='Unpaid'):
        super().__init__(name, joining_date, 0, 40)
        self.temp_id = f"Temp_{self.__class__.intern_count + 1}"
        self.intern_type = intern_type
        self.status = "Eligible for promotion" if self.check_promotion_eligibility() else "Not Eligible for promotion"
        self.__class__.intern_count += 1

    def check_promotion_eligibility(self):
        # Assuming an intern can be promoted if they've worked for at least 4 months (120 days)
        return ('2023-04-30' >= self.joining_date >= '2023-01-01') or \
               ('2023-10-31' >= self.joining_date >= '2023-07-01')

    def showInternDetails(self):
        print("Intern (Programmer):")
        print(f"Name: {self.name}")
        print(f"ID: {self.temp_id}")
        print(f"Joining Date: {self.joining_date}")
        print(f"Type: {self.intern_type}")
        print(f"Status: {self.status}")

    def promoteToProgrammer(self):
        if self.status == "Eligible for promotion":
            new_programmer = Programmer(self.name, str(datetime.date.today()), 0)
            print(f"{self.name} is promoted!")
            return new_programmer
        else:
            print(f"{self.name} can not be promoted.")
            return self


if __name__ == "__main__":
    Employee.showDetails()
    print("=========1=========")
    richard = Programmer("Richard Hendricks", "2021-06-08", 4, 48)
    richard.calculateSalary()
    print("=========2=========")
    richard.showProgrammerDetails()
    print("=========3=========")
    richard.calculateOvertime()
    print("=========4=========")
    richard.showProgrammerDetails()
    print("=========5=========")
    monica = HR("Monica Hall", "2022-07-06", 2, 40)
    print("=========6=========")
    monica.showHREmployeeDetails()
    print("=========7=========")
    Employee.showDetails()
    print("=========8=========")
    gilfoyle = Programmer("Bertram Gilfoyle", "2020-03-02", 6, 35)
    gilfoyle.calculateSalary()
    print("=========9=========")
    gilfoyle.calculateOvertime()
    print("=========10=========")
    gilfoyle.showProgrammerDetails()
    print("=========11=========")
    gavin = Programmer("Gavin Belson", "2016-12-20", 9)
    gavin.calculateSalary()
    gavin.calculateOvertime()
    gavin.showProgrammerDetails()
    print("=========12=========")
    yang = InternProgrammer("Jian Yang", "2023-01-01")
    yang.showInternDetails()
    print("=========13=========")
    jared = InternProgrammer("Jared Dunn", "2023-06-05", "Paid")
    jared.showInternDetails()
    print("=========14=========")
    jared = jared.promoteToProgrammer()
    print("=========15=========")
    Employee.showDetails()
    print("=========16=========")
    yang = yang.promoteToProgrammer()
    yang.calculateSalary()
    yang.showProgrammerDetails()
    print("=========17=========")
    Employee.showDetails()
