# Attendance Record Project

This project is designed for managing attendance records using Django. Follow the steps below to set up and run the project. Even if you're not tech-savvy, these instructions should help you get started.

## Prerequisites

Before starting, make sure you have the following installed:

- [Python](https://www.python.org/downloads/) (version 3.8 or above)
- [Git](https://git-scm.com/) for cloning the project
- A terminal or command prompt to run the commands

## Step-by-Step Setup

### 1. Install Git

If you don’t have Git installed, download it from [here](https://git-scm.com/downloads) and install it. This will help you clone the project.

### 2. Clone the Project

To download the project code to your computer, open a terminal (or command prompt on Windows) and run:

```bash

# Clone the Project
git clone https://github.com/junaidanwar080/attendance-record.git

# Navigate to the Project Directory
cd attendance-record

# Set Up a Virtual Environment

# For Windows:
python -m venv env
.\env\Scripts\activate

# For macOS/Linux:
python3 -m venv env
source env/bin/activate

# Install Required Dependencies
pip install -r requirements.txt

# Set Up the Database
python manage.py makemigrations
python manage.py migrate

# Create a Superuser
python manage.py createsuperuser
# When prompted, enter:
# Username: admin
# Email: admin@gmail.com
# Password: admin
# Confirm password by pressing (y) and Enter

# Run the Development Server
python manage.py runserver

# Open your browser and go to http://127.0.0.1:8000/ to view the project running locally
