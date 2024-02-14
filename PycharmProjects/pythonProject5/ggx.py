class Employee:
    employee_count = {}

    def __init__(self, name, joining_date, work_experience, weekly_work_hour=40):
        self.name = name
        self.joining_date = joining_date
        self.work_experience = work_experience
        if 40 <= weekly_work_hour <= 60:
            self.weekly_work_hour = weekly_work_hour
        else:
            print("Invalid weekly work hour. Setting to default (40 hours)")
            self.weekly_work_hour = 40

        emp_type = self.__class__.__name__
        if emp_type != 'InternProgrammer':
            Employee.employee_count[emp_type] = Employee.employee_count.get(emp_type, 0) + 1

    @classmethod
    def showDetails(cls):
        print("Total Employee/s:", sum(cls.employee_count.values()))
        for emp_type, count in cls.employee_count.items():
            print(f"Total {emp_type} Employee/s:", count)


class Programmer(Employee):
    designation_list = [
        'Junior Software Engineer', 'Software Engineer', 'Senior Software Engineer', 'Technical Lead'
    ]

    def __init__(self, name, joining_date, work_experience, weekly_work_hour=40):
        super().__init__(name, joining_date, work_experience, weekly_work_hour)
        self.id = self.createProgrammerID()
        self.designation = self.get_designation()

    def createProgrammerID(self):
        emp_count = Employee.employee_count.get('Programmer', 0)
        joining_year = self.joining_date.split('-')[0][-2:]
        emp_id = f'P-{joining_year}{self.joining_date[5:7]}-{emp_count + 1:02d}'
        print(emp_id)
        return emp_id

    def get_designation(self):
        if 0 <= self.work_experience < 3:
            return Programmer.designation_list[0]
        elif 3 <= self.work_experience < 5:
            return Programmer.designation_list[1]
        elif 5 <= self.work_experience < 8:
            return Programmer.designation_list[2]
        else:
            return Programmer.designation_list[3]

    def calculateSalary(self):
        base_salary = self.get_base_salary()
        salary = base_salary * (1.15 ** self.work_experience)
        self.salary = salary

    def get_base_salary(self):
        designation_salary = {
            'Junior Software Engineer': 30000,
            'Software Engineer': 45000,
            'Senior Software Engineer': 70000,
            'Technical Lead': 120000
        }
        return designation_salary[self.designation]

    def calculateOvertime(self):
        overtime_hours = max(0, self.weekly_work_hour - 40)
        overtime_pay = overtime_hours * 500
        self.salary += overtime_pay
        print("Overtime pay:", overtime_pay)

    def showProgrammerDetails(self):
        print("Programmer Name:", self.name)
        print("ID:", self.id)
        print("Joining Date:", self.joining_date)
        print("Designation:", self.designation)
        print("Salary:", self.salary)


class HR(Employee):

    def __init__(self, name, joining_date, work_experience, weekly_work_hour=40):
        super().__init__(name, joining_date, work_experience, weekly_work_hour)
        self.id = self.createHREmployeeID()


    def createHREmployeeID(self):
        emp_count = Employee.employee_count.get('HR', 0)
        joining_year = self.joining_date.split('-')[0][-2:]
        emp_id = f'HR-{joining_year}{self.joining_date[5:7]}-{emp_count + 1:02d}'
        return emp_id

    def showHREmployeeDetails(self):
        print("HR Employee Name:", self.name)
        print("ID:", self.id)
        print("Joining Date:", self.joining_date)


class InternProgrammer(Employee):
    intern_count = 0

    def __init__(self, name, joining_date, intern_type='Unpaid'):
        super().__init__(name, joining_date, 0, 40)
        InternProgrammer.intern_count += 1
        self.temp_id = f"Temp_{InternProgrammer.intern_count}"
        self.intern_type = intern_type
        self.status = "Eligible" if self.is_eligible_for_promotion() else "Not Eligible"

    def is_eligible_for_promotion(self):
        # Assuming intern is recruited in January or July
        months_since_joining = (int(self.joining_date.split('-')[1]) - 1) % 6
        return months_since_joining >= 4

    def showInternDetails(self):
        print("Intern Name:", self.name)
        print("Temporary ID:", self.temp_id)
        print("Joining Date:", self.joining_date)
        print("Intern Type:", self.intern_type)
        print("Eligibility Status:", self.status)

    def promoteToProgrammer(self):
        if self.status == "Eligible":
            print("The intern is promoted!")
            return Programmer(self.name, self.get_current_date(), 0, 40)
        else:
            print("The intern cannot be promoted.")

    def get_current_date(self):
        import datetime
        return datetime.datetime.now().strftime('%Y-%m-%d')


# Driver Code
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
