<p align="center">
 <img alt="logo" src="https://github.com/LeChat76/Projet9OC/assets/119883313/93b79d39-0b2f-4a2b-aeb4-e1641983a0bc">
</p>

# Projet9OC
The aim of this project is to create a site enabling a community of users to consult or request a book review on demand.  
This website was created with the __Django framework__.

--------------------------------------------------------------------------------------------------------------------------------------------------

## Installation
```sh
"git clone https://github.com/LeChat76/Projet9OC.git"
"cd Projet9OC"
Create virtual environment :
* "python -m venv .venv"
* activate environment :
    * for Linux "source .venv/bin/activate"
    * for Windows ".\.venv\Scripts\activate"
Install the necessary libraries by typing : "pip install -r requirements.txt"
Go in the folder of the projet : "cd litreview"
Start the web service : "python.exe manage.py runserver"
Finally, access the site by typing "http://127.0.0.1:8000/" in your favorite navigator
```

--------------------------------------------------------------------------------------------------------------------------------------------------

## How to use
From the home page, create an account by clicking on the *Register* button.  
Fill in the __username__, __password__ and __password verification__ (at least 8 characters, at least one uppercase letter and at least one number).
<p>
 <img alt="logo" src="https://github.com/LeChat76/Projet9OC/assets/119883313/d0a5b491-c8ca-40e7-afaa-6b66a9e81bdb">
</p>
Once account correctly created, you will be redirected on the *flux* page.  
From this page you can create a ticket or a review.
<p>
 <img alt="logo" src="https://github.com/LeChat76/Projet9OC/assets/119883313/67705f30-c1d0-4246-9a4a-ecb7adc6a969">
</p>
You can select users to follow by going to the subscription section: click on the user name in the top left-hand corner or in the top right-hand menu "subscription".  
In that menu you can add users by selecting them in the list or by typing in the charfield zone. You can also remove users you follow, and you can see all users who follow you.
<p>
 <img alt="logo" src="https://github.com/LeChat76/Projet9OC/assets/119883313/8a8f3eb1-974a-46a3-af2b-d5e58c78992a">
</p>
Once selected, you will see some of their ticket and review in the flux menu.  
You can see, edite or delete all of your ticket and review in the post menu.

--------------------------------------------------------------------------------------------------------------------------------------------------

## Features
To manage subscriptions, I've created a list selection in addition to manual entry (more practical for searching for people when you've just subscribed).  
Access to html page by typing url is blocked for non authorized users (only creators can access to their own tickets or reviews for modifications and deletion, forbidden page for the others)




