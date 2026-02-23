from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_connection():
    conn = sqlite3.connect("payroll.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    payslip = None
    if request.method == "POST":
        emp_id = request.form["empid"]
        pay_date = request.form["paydate"]
        conn = get_connection()
        c = conn.cursor()
        c.execute("""SELECT e.emp_id, e.emp_name, e.designation, d.dept_name,
                            p.basic_salary, p.deductions, p.bonus, p.net_salary, p.pay_date
                     FROM Employee e
                     JOIN Department d ON e.dept_id = d.dept_id
                     JOIN Payroll p ON e.emp_id = p.emp_id
                     WHERE e.emp_id=? AND p.pay_date=?""",
                  (emp_id, pay_date))
        payslip = c.fetchone()
        conn.close()
    return render_template("index.html", payslip=payslip)

@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM Department")
    depts = c.fetchall()
    if request.method == "POST":
        emp_name = request.form["name"]
        designation = request.form["designation"]
        dept_id = request.form["dept_id"]
        c.execute("INSERT INTO Employee(emp_name, designation, dept_id) VALUES (?,?,?)",
                  (emp_name, designation, dept_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    conn.close()
    return render_template("add_employee.html", depts=depts)

@app.route("/add_payroll", methods=["GET", "POST"])
def add_payroll():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM Employee")
    emps = c.fetchall()
    if request.method == "POST":
        emp_id = request.form["emp_id"]
        basic = float(request.form["basic"])
        deductions = float(request.form["deductions"])
        bonus = float(request.form["bonus"])
        pay_date = request.form["pay_date"]
        net_salary = basic - deductions + bonus
        c.execute("""INSERT INTO Payroll(emp_id, basic_salary, deductions, bonus, net_salary, pay_date)
                     VALUES (?,?,?,?,?,?)""",
                  (emp_id, basic, deductions, bonus, net_salary, pay_date))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    conn.close()
    return render_template("add_payroll.html", emps=emps)
@app.route("/show_all")
def show_all():
    conn = get_connection()
    c = conn.cursor()

    # Get all employees
    c.execute("SELECT * FROM Employee")
    employees = c.fetchall()

    # Get all payrolls (joined with employee and department for readability)
    c.execute("""SELECT e.emp_id, e.emp_name, e.designation, d.dept_name,
                        p.basic_salary, p.deductions, p.bonus, p.net_salary, p.pay_date
                 FROM Employee e
                 JOIN Department d ON e.dept_id = d.dept_id
                 JOIN Payroll p ON e.emp_id = p.emp_id
                 ORDER BY p.pay_date DESC""")
    payrolls = c.fetchall()

    conn.close()
    return render_template("show_all.html", employees=employees, payrolls=payrolls)

if __name__ == "__main__":
    app.run(debug=True)
