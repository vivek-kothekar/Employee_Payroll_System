import sqlite3

# Connect (creates payroll.db if not exists)
conn = sqlite3.connect("payroll.db")
c = conn.cursor()

# Drop tables if they already exist
c.execute("DROP TABLE IF EXISTS Payroll")
c.execute("DROP TABLE IF EXISTS Employee")
c.execute("DROP TABLE IF EXISTS Department")

# Create tables
c.execute("""CREATE TABLE Department (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT
)""")

c.execute("""CREATE TABLE Employee (
    emp_id INTEGER PRIMARY KEY,
    emp_name TEXT,
    designation TEXT,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
)""")

c.execute("""CREATE TABLE Payroll (
    payroll_id INTEGER PRIMARY KEY,
    emp_id INTEGER,
    basic_salary REAL,
    deductions REAL,
    bonus REAL,
    net_salary REAL,
    pay_date TEXT,
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id)
)""")

# Insert Departments
c.execute("INSERT INTO Department VALUES (1,'HR')")
c.execute("INSERT INTO Department VALUES (2,'IT')")
c.execute("INSERT INTO Department VALUES (3,'Finance')")

# Insert Employees
c.execute("INSERT INTO Employee VALUES (101,'Vivek Kothekar','Manager',1)")
c.execute("INSERT INTO Employee VALUES (102,'Roshan Hingnekar','Software Engineer',2)")
c.execute("INSERT INTO Employee VALUES (103,'Vansh Parate','Accountant',3)")

# Insert Payroll Records
c.execute("INSERT INTO Payroll VALUES (1,101,50000,2000,5000,53000,'2025-09-01')")
c.execute("INSERT INTO Payroll VALUES (2,102,40000,1500,2000,40500,'2025-09-01')")
c.execute("INSERT INTO Payroll VALUES (3,103,35000,1000,1000,35000,'2025-09-01')")

conn.commit()
conn.close()
print("Database setup completed! ✅")
