import random
from datetime import date, timedelta
# pyrefly: ignore [missing-import]
from django.core.management.base import BaseCommand
# pyrefly: ignore [missing-import]
from django.contrib.auth.models import User
from workspace.models import Profile, Department, Employee, ActivityLog

class Command(BaseCommand):
    help = 'Seeds initial database records for AuraEMS'

    def handle(self, *args, **options):
        self.stdout.write("Seeding AuraEMS Employee Management database...")

        # 1. Create Demo Admin
        admin_user, created = User.objects.get_or_create(username='admin', email='admin@auraems.com')
        if created or not admin_user.has_usable_password():
            admin_user.set_password('admin123')
            admin_user.save()
            
        profile = admin_user.profile
        profile.name = 'Admin User'
        profile.role = 'HR Manager'
        profile.avatar = None # Can be blank to use default
        profile.bio = 'System Administrator for AuraEMS.'
        profile.save()

        # 2. Clear existing entries
        Employee.objects.all().delete()
        Department.objects.all().delete()
        ActivityLog.objects.all().delete()

        # 3. Create 5 Departments
        dept_names = ['IT', 'HR', 'Finance', 'Marketing', 'Operations']
        depts = []
        for name in dept_names:
            dept = Department.objects.create(
                name=name,
                description=f"Company division handling {name} functions."
            )
            depts.append(dept)

        # 4. Create 50 Employees (42 active, 8 inactive)
        # Ensure we have the 5 core employees first
        core_employees_data = [
            {"first_name": "John", "last_name": "Doe", "email": "john.doe@auraems.com", "phone": "555-0101", "department": depts[0], "designation": "Software Engineer", "date_joined": date(2024, 1, 1), "salary": 115000.00, "status": "active"},
            {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@auraems.com", "phone": "555-0102", "department": depts[1], "designation": "HR Manager", "date_joined": date(2024, 2, 15), "salary": 95000.00, "status": "active"},
            {"first_name": "Mike", "last_name": "Johnson", "email": "mike.johnson@auraems.com", "phone": "555-0103", "department": depts[2], "designation": "Accountant", "date_joined": date(2024, 3, 10), "salary": 88000.00, "status": "inactive"},
            {"first_name": "Sarah", "last_name": "Wilson", "email": "sarah.wilson@auraems.com", "phone": "555-0104", "department": depts[3], "designation": "Marketing Executive", "date_joined": date(2024, 4, 5), "salary": 78000.00, "status": "active"},
            {"first_name": "David", "last_name": "Brown", "email": "david.brown@auraems.com", "phone": "555-0105", "department": depts[4], "designation": "Operations Manager", "date_joined": date(2024, 4, 20), "salary": 105000.00, "status": "active"}
        ]

        core_employees = []
        for emp_data in core_employees_data:
            emp = Employee.objects.create(
                first_name=emp_data["first_name"],
                last_name=emp_data["last_name"],
                email=emp_data["email"],
                phone=emp_data["phone"],
                department=emp_data["department"],
                designation=emp_data["designation"],
                joining_date=emp_data["date_joined"],
                salary=emp_data["salary"],
                status=emp_data["status"],
                gender="Male" if emp_data["first_name"] in ["John", "Mike", "David"] else "Female",
                date_of_birth=date(1990, 5, 12),
                address="123 Office Plaza",
                city="Chicago",
                state="IL",
                country="USA",
                zip_code="60601",
                notes="Core seed employee.",
                created_by=admin_user
            )
            core_employees.append(emp)

        # Allocate statuses for remaining 45: 38 active, 7 inactive
        status_list = ["active"] * 38 + ["inactive"] * 7
        random.seed(42)
        random.shuffle(status_list)

        first_names = [
            "Robert", "Emily", "Michael", "William", "Olivia", "James", "Sophia", "Charles", "Isabella", 
            "Thomas", "Mia", "Daniel", "Charlotte", "Matthew", "Amelia", "Anthony", "Harper", "Mark", 
            "Evelyn", "Donald", "Abigail", "Steven", "Paul", "Elizabeth", "Andrew", "Sofia", 
            "Kenneth", "Avery", "Joshua", "Ella", "Kevin", "Madison", "Brian", "Scarlett", "George"
        ]
        last_names = [
            "Brown", "Davis", "Wilson", "Jones", "Miller", "Garcia", "Martinez", "Rodriguez", "Hernandez", 
            "Lopez", "Gonzalez", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", 
            "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
        ]

        dept_allocations = [
            depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], depts[0], # IT: 17
            depts[1], depts[1], depts[1], depts[1], depts[1], depts[1], depts[1], depts[1], depts[1], # HR: 9
            depts[2], depts[2], depts[2], depts[2], depts[2], depts[2], depts[2], # Finance: 7
            depts[3], depts[3], depts[3], depts[3], depts[3], depts[3], depts[3], depts[3], # Marketing: 8
            depts[4], depts[4], depts[4], depts[4] # Operations: 4
        ]

        for idx, dept in enumerate(dept_allocations):
            first = random.choice(first_names)
            last = random.choice(last_names)
            email = f"{first.lower()}.{last.lower()}.{idx+6}@auraems.com"
            phone = f"555-01{idx+6:02d}"

            # Avoid duplicates
            while Employee.objects.filter(email=email).exists():
                first = random.choice(first_names)
                last = random.choice(last_names)
                email = f"{first.lower()}.{last.lower()}.{idx+6}@auraems.com"

            designations = {
                "IT": ["Systems Analyst", "Frontend Developer", "Backend Engineer", "QA Specialist", "DevOps Admin"],
                "HR": ["HR Coordinator", "Recruitment Lead", "Training Facilitator", "Benefits Specialist"],
                "Finance": ["Billing Analyst", "Auditor", "Payroll Clerk", "Financial Consultant"],
                "Marketing": ["Content Creator", "SEO Analyst", "Media Buyer", "Brand Manager"],
                "Operations": ["Office Assistant", "Logistics Specialist", "Facilities Manager"]
            }

            Employee.objects.create(
                first_name=first,
                last_name=last,
                email=email,
                phone=phone,
                department=dept,
                designation=random.choice(designations[dept.name]),
                joining_date=date.today() - timedelta(days=random.randint(30, 700)),
                salary=random.randint(60000, 130000),
                status=status_list[idx],
                gender=random.choice(["Male", "Female"]),
                date_of_birth=date(1992, 10, 8),
                address="Generated address.",
                city="Chicago",
                state="IL",
                country="USA",
                zip_code="60601",
                notes="System generated employee.",
                created_by=admin_user
            )

        # 5. Create System Activities
        ActivityLog.objects.create(user=admin_user, employee=core_employees[0], action="joined in IT department", created_at=date.today() - timedelta(minutes=2))
        ActivityLog.objects.create(user=admin_user, employee=core_employees[1], action="updated their profile", created_at=date.today() - timedelta(minutes=15))
        ActivityLog.objects.create(user=admin_user, action="New department Marketing added", created_at=date.today() - timedelta(hours=1))
        ActivityLog.objects.create(user=admin_user, employee=core_employees[2], action="deactivated", created_at=date.today() - timedelta(hours=2))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
