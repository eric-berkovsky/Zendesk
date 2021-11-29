# Zendesk Ticket Viewer

Welcome to my ticket viewer! This browser-based program fetches all the tickets in your Zendesk account and allows you to page through them. You can also click the View Ticket button on any of the tickets to view more information about it. This program was built using the Django web framework which provides a convenient way to make API calls and dynamically generate information about tickets for the web page. 

# How to Use

First, make sure you have python3 and git installed on your computer. Then, clone this repository. Open your command line interpreter and then enter the following command:
```
git clone https://github.com/eric-berkovsky/Zendesk-Ticket-Viewer.git
```

Next, enter this new directory which contains the program then create a virtual environment for the program to run in. Enter this new virtual environment. 
```
cd Zendesk-Ticket-Viewer 
python3 -m venv venv
source venv/bin/activate
```

Now, you will need to download the project dependencies. You can first run an ls command to ensure that requirements.txt is present in your current directory. 
```
pip install -r requirements.txt
```

Up next, you will need to configure the program to use your Zendesk credentials. Open the file config.py (inside the 'zendesk' directory) in a text editor or IDE. 
First, you will need to generate a Django secret key. Open the Python interpreter by typing in python3 on your command line and entering. Once it loads, type in:
```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
Copy the output from the print statement then type CTRL + D to close the Python interpreter. Paste this secret key into config.py where it says 'enter_your_django_secret_key'.
Then, enter your Zendesk subdomain where it says 'enter_your_subdomain'. Enter your email address and API key in the designated spaces as well. If you do not have an API key you can generate one from your Admin page. 

Go back to your command line and navigate to the main directory where manage.py is located. 

Type in the following two commands:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Finally, it's time to run the program. Type in the following command:
```
python3 manage.py runserver
```
Then, go to your browser and enter http://127.0.0.1:8000/. The program should now appear. 
One important note: your program is running with Debug Mode on. This is so that Django will handle static files like css for you. If you want to use this program in production you will need to set Debug Mode to False (this can be done in settings.py) and configure a web server such as nginx to handle static files for you. 

When you are done, you can quit the server by pressing CTRL + C. Then, enter 'deactivate' to exit your virtual environment. 

Feel free to contact me if you have any questions!

# Sample Ticket Viewer Home Page

<img width="662" alt="Screen Shot 2021-11-29 at 12 54 08 AM" src="https://user-images.githubusercontent.com/52947849/143836931-c2756e96-ffa1-4fcd-a131-f81c2ac5e94e.png">

# Sample Ticket Page

<img width="1138" alt="Screen Shot 2021-11-29 at 12 54 47 AM" src="https://user-images.githubusercontent.com/52947849/143837029-9a8f6b40-b0c3-45d2-9e69-7919fe799964.png">

# Testing

This program was tested using Python's unittest framework and its mock library. The testing file, tests.py, can be found in the ZendeskCodingChallenge folder. Every function in functions.py, which is the file that handles calls to Zendesk's API, is tested with mock API calls. To run all the tests, enter:
```
python3 manage.py test
```


