# PESU-CAFETERIA-MENU-FEEDBACK-TRACKER-MINIPROJECT
PESU Cafeteria Menu & Feedback Tracker
A comprehensive Database Management System (DBMS) project designed to streamline cafeteria operations, manage menus, track orders, and collect student feedback. This desktop application features a modern GUI, Role-Based Access Control (RBAC), and advanced SQL implementations including Stored Procedures, Triggers, and ACID-compliant transactions.

Table of Contents
About the Project

Key Features

Tech Stack

Database Design

Installation & Setup

Usage Guide

Advanced SQL Implementations

Team Details

About the Project
This project addresses the need for a digitized system to manage the university cafeteria. It moves away from manual record-keeping to a centralized relational database system. The application ensures data integrity through 3NF Normalization and provides a secure interface distinguishing between Administrators (Staff) and Students.

Key Features
Security & Access Control
Secure Login System: Username/Password authentication.

Role-Based Access Control (RBAC):

Admins: Full access to all CRUD operations, Staff management, and DB Admin tools.

Students: Restricted access. Can view menus, place orders, and manage only their own reviews.

Backend Security: Uses MySQL GRANT statements to enforce privileges at the database level, not just the UI level.

Administrator Module
Staff & Menu Management: Add, update, or delete staff members and daily menus.

Order Tracking: View all placed orders and detailed item breakdowns.

User Management: Create new database users and assign roles (Admin/Student) directly from the GUI.

Reports Dashboard: Visualize data using Aggregate queries (e.g., Total Revenue) and Complex Joins (e.g., Item popularity).

Student Module
View Menus & Items: Browse available food items and daily specials.

Place Orders: A transaction-based system to order multiple items at once.

Reviews: Submit feedback and ratings for items. Students can update their own reviews but cannot delete them.

Technical Highlights
ACID Transactions: Order placement uses COMMIT and ROLLBACK to ensure data consistency.

Auto-Reconnect: The application automatically attempts to reconnect to the database if the connection drops.

Modern GUI: Built with ttkbootstrap for a clean, flat design.

Tech Stack
Language: Python 3.x

GUI Framework: tkinter with ttkbootstrap

Database: MySQL 8.0

Driver: mysql-connector-python

Editor: VS Code
