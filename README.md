# Student_Management_System
A simple console-based Student Management System built using Python, designed to run in CLI and store student data in a remote MySQL database (such as FreeSQLDatabase.com).

This project demonstrates:

    Python + MySQL database connectivity
    
    CRUD operations (Create, Read, Update, Delete)
    
    File-free data storage using a cloud-hosted MySQL server
    
    Clean and easy-to-understand code for students and beginners

Features:

    ✔ Add Student
    
    Stores new student details (Roll, Name, Age, Course, Email).
    
    ✔ View Students
    
    Displays all student records stored in the MySQL database.
    
    ✔ Search Student
    
    Searches student by roll number.
    
    ✔ Update Student
    
    Updates existing student information.
    
    ✔ Delete Student
    
    Deletes a student based on roll number.
    
    ✔ Uses Cloud MySQL
    
    Works with FreeSQLDatabase, PlanetScale, or any remote MySQL server.

Implementation:

1.Install MySQL Connector by using the following command:

    pip install mysql-connector-python

2.Create an account in remote MySQl database (such as FreeSQLDatabase.com).

3.Replace the config variable fields with your database connection details.

4.Run the program by using the following command in CLI:

    python student_management_system.py

