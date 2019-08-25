from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/wealthpark'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

class Employees(db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.Integer, primary_key=True)
    given_name = db.Column(db.String(50), nullable=False)
    family_name = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    boss = db.Column(db.Integer, db.ForeignKey("employees.employee_id"))
    salary = db.Column(db.Integer)
    isArchived = db.Column(db.Boolean)
    parent = db.relationship("Employees", remote_side=[employee_id])

    def __init__(self, given_name, family_name, birthday, address, boss, salary):
      self.given_name = given_name
      self.family_name = family_name
      self.birthday = birthday
      self.address = address
      self.boss = boss
      self.salary = salary

class EmployeesSchema(ma.Schema):
  class Meta:
    fields = ('employee_id', 'given_name', 'family_name', 'birthday', 'address', 'boss', 'salary')

employee_schema = EmployeesSchema()
employees_schema = EmployeesSchema(many=True)

# Create an Employee
@app.route('/add_employee', methods=['POST'])
def add_employee():
    given_name = request.json['given_name']
    family_name = request.json['family_name']
    birthday = request.json['birthday']
    address = request.json['address']
    boss = request.json['boss']
    salary = request.json['salary']

    new_employee = Employees(given_name, family_name, birthday, address, boss, salary)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)

# Get All Employees
@app.route('/employees', methods=['GET'])
def get_employees():
  all_employees = Employees.query.all()
  result = employees_schema.dump(all_employees)
  return jsonify(result)

# Get a single Employee
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
  employee = Employees.query.get(id)
  return employee_schema.jsonify(employee)

# Update an Employee record
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
  employee = Employees.query.get(id)

  given_name = request.json['given_name']
  family_name = request.json['family_name']
  birthday = request.json['birthday']
  address = request.json['address']
  boss = request.json['boss']
  salary = request.json['salary']

  employee.given_name = given_name
  employee.family_name = family_name
  employee.birthday = birthday
  employee.address = address
  employee.boss = boss
  employee.salary = salary

  db.session.commit()

  return employee_schema.jsonify(employee)

# Delete an Employee Record
# Strongly recommend we archive employees rather than permantenly deleting them
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
  employee = Employees.query.get(id)
  subordinates = fetch_subordinates(id)

  # Removing the links between items
  # Would throw an error if we don't do this
  for s in subordinates:
    s.boss = None
    db.session.add(s)

  db.session.delete(employee)
  db.session.commit()

  return employee_schema.jsonify(employee)

# Get a paginated list of Employees
@app.route('/employees_paginate/<int:page>/<int:per_page>', methods=['GET'])
def page(page, per_page):
    employees = Employees.query.paginate(page, per_page)
    return employees_schema.jsonify(employees.items)

# Get all subordinates of selected Employee (if any)
# filter for the list endpoint
@app.route('/employee_subordinates/<int:id>', methods=['GET'])
def find_subordinates(id):
    return employees_schema.jsonify(fetch_subordinates(id))

# Get all employees who have a salary equal to or greater than the paramter supplied
# one more filter for the list endpoint
@app.route('/employee_salary_filter/<int:amount>', methods=['GET'])
def filter_salaries(amount):
    matching_employees = Employees.query.filter(Employees.salary >= amount).all()
    return employees_schema.jsonify(matching_employees)

# helper function
def fetch_subordinates(id):
    return Employees.query.filter(Employees.boss == id).all()

# Run Server
if __name__ == '__main__':
  app.run(debug=True)