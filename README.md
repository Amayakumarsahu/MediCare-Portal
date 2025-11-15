# MediCare Portal — 
Patient & Doctor Signup, Login, and Dashboard Redirect using Django
This project is a Django-based authentication system designed for two types of users: Patients and Doctors.
It allows users to sign up, log in, and get redirected to their respective dashboards.
All user details (including profile picture) are stored in a SQLite database.

## Project Features

## User Signup

### Users provide:
First Name
Last Name
Profile Picture
Username
Email
Password & Confirm Password
Address (Line 1, City, State, Pincode)
User Type: Patient or Doctor
### Includes:
Password confirmation check
Username and email uniqueness validation
Image upload support

### User Login

Login using username + password
Backend validates user credentials
Redirects based on user type:
Patient → Patient Dashboard
Doctor → Doctor Dashboard

### User Dashboards

Each dashboard displays:
Name
Email
Username
Address
Profile picture
Dashboards are cleanly styled with inline CSS.

### Technologies Used
Python 3
Django 5.2.8
SQLite (default DB)
HTML + Inline CSS
