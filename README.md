# Contacts-Display-Window
SQL programming project involves the creation of a database host application that interfaces with a backend MySQL database implementing a Contact List application.

Instructions to run the project:
1. Install Anaconda (Windows/Mac) latest version with python 3.7 or greater. Make sure you Anaconda’s PATH is registered in Environment’s PATH variable.
2. Unzip/Pull the repo in your desired location. From terminal/command prompt window, cd to the unzipped location.
3. Run the command 'conda env create --name django --file=environment.yml' to create the conda environment.
4. Activate the environment in terminal by running 'conda activate django' if Windows. Else, 'source activate django' if Mac.
5. Import the contact_details.sql file into local running MySQL server using MySQL Workbench or XAMPP.
6. Run 'python manage.py runserver' to start the Django server. And open the browser https://localhost:8000
