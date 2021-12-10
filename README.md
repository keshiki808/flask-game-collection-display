# flask-game-collection-display
<div id="top"></div>


  <h3 align="center">A Flask 'Game display' web app</h3>

  <p align="center">
    A web app used to improve my skills in Python, Flask, Javascript, Bootstrap, jQuery, HTML, CSS, and SQL.
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started-and-installation">Getting Started and Installation</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project demonstrates using the Flask microframework to create a website or webapp that allows generating a 'collection' of something,
in this instance a game collection, generated from a form submission and file upload. It uses a template and python to dynamically generate
the HTML markup and webpages. The project utilizes a login system and also allows removal of entries from the collection. The data is stored using
SQlite.

### Built With


* Flask
* Python
* Javascript
* Bootstrap
* JQuery
* HTML
* CSS
* SQL

Additional plugins and numerous libraries were utilized as well, including JQuery rates which provided a star rating form submission, lightbox for allowing popping the images out in the collection. WTForms was used for form generation.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started and Installation
-Install Python if necessary </br>
-Clone the repo into the folder of your choosing </br>
-Open the project folder in Pycharm </br>
-Create a virtual environment </br>
-Activate virtual environment and run pip install -r requirements.txt to install all project dependencies </br>
-Using the powershell terminal type '$env:FLASK_APP = "application.py"' </br>
-Next type 'flask run' to run the local server </br>
-Click the IP address in the terminal provided by Pycharm to load the project in your web browser </br>
-Login using the following credentials: </br> 
* Email Address: fakeuser@fakemail.com
* Password: gaming123


### Prerequisites

Python, Pip, and an IDE such as Pycharm should be installed in advance for smooth operation of the webapp. </br>


<!-- USAGE EXAMPLES -->
## Usage

Login to access the site using the Email Address 'fakeuser@fakemail.com' and password 'gaming123' </br>
![image](https://user-images.githubusercontent.com/84114638/145594401-afc533ae-063b-487e-a6d0-379096d6845b.png)
</br>

From the top of the page you'll see a navigation bar: </br>
![image](https://user-images.githubusercontent.com/84114638/145594566-62520186-33b5-4783-9fa7-98cd7ea26811.png)
</br>

The 'Home' page is the landing page after logging in.</br>
![image](https://user-images.githubusercontent.com/84114638/145594676-308da83f-c215-4faf-b7b3-cb4319e7a2e1.png)
</br>

The 'Upload' page presents a form the user fills out to upload game details and an image representing the game to the server and database.</br>
![image](https://user-images.githubusercontent.com/84114638/145594807-0249c299-133b-4f58-9b34-e9ddf4dc9c39.png)
</br>

The 'Collection' page dynamically formats the HTML markup from the details provided in the form that are stored in the database to create a 'game collection' </br>
![image](https://user-images.githubusercontent.com/84114638/145594963-346c33ab-59f7-42ad-851d-a5c040467781.png)
</br>

The 'Remove' page provides a dropdown list to remove a game from the collection which deletes it from the database and removes the stored file from the server.
![image](https://user-images.githubusercontent.com/84114638/145595356-9d5acf27-8a9c-41a0-9523-ec715a8bafc6.png)
</br>

The 'logout' section of the navigation bar logs the user out of the webapp.



<p align="right">(<a href="#top">back to top</a>)</p>

