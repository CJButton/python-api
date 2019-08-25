WealthPark RESTful API Demo
------------------------------------------

Basic demo created using:
Python 3
Flask, flask_sqlalchemy, and flask_marshmallow

To try it out, clone the branch and cd into the folder.

You'll need to create a database first called 'wealthpark'. 

Run 'pip install' in your console.

In the console of your choice, enter python3 and hit enter.

Then type 'from app import db', hit enter and then type 'db.createall()' and hit enter once more.

You're basic database has been setup!

Next, exit out of python by entering 'exit()'

Now let's run our server. In the console, enter 'python3 app.py'. If you get no errors, we are up and running!

Our schema looks like this:
```
"employee_id": Integer (Primary Key),
"given_name": String,
"family_name": String,
"birthday": Date,
"address": String,
"boss": Integer, (ForeignKey is employee_id)
"salary": Integer
```

Here's our list of endpoints:

POST /add_employee
The body should look something like this:
```
{
  "given_name": "Musashi",
  "family_name": "Miyamoto",
  "birthday": "1584-03-01",
  "address": "Harima",
  "boss": None,
  "salary": "1000"
}
```


Returns the added employee if successful.

GET /employees
No params

Returns an array of JSON objects of all employees in the db.
 
GET /employee/employee_id

Returns a JSON object of the employee.

PUT employee/employee_id

Updates a record of the selected employee. Body is same as that of /add_employee

Returns a JSON object of the employee with all updated values.

DELETE employee/employee_id

Removes record of said employee.

All subordinates of this employee (if any) will have their boss field set to None.

GET /employees_paginate/<int:page>/<int:per_page>

Returns an array of employees

GET /employee_subordinates/employee_id

Returns an array of all employees of the entered id

GET /employee_salary_filter/<int:amount>

Returns a list of employees who have a salary equal to or greater than the amount.

Things that need improvement:
-----------------------------
- We should consider using an archive flag instead of deleting employees. Easier to check records in the future if HR needs them.

- The salary field is using Integer. But it looks like this can create issues if a field is entered with decimals. This could lead to strange ronding issues in the future.