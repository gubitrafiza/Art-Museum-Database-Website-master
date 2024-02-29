### 2023 Art Museum Database Website
https://museumcosc.cofecat.com/

### Techstack:
Python, HTML, CSS, PostgreSQL

### Breakdown of our files:

#### sql
This is where we store our SQL files to set up and bring down our queries easily in order to modify them on the go. 
<br> <br>
`create.sql` -> sets up the schema
<br>
`drop.sql` -> tears down the schema
<br>
`input.sql` -> inputs test data

#### src
This is where the majority of our Python files go. They are query and report functions to be used in the `app.py` (which is located outside of the subfolders).

#### static
Contains a subfolder (`img`) of images that were used on the website to make it look more presentable. Also contains a main css file that is used throughout the website.

#### templates
This is where all the html files go to render the website.

#### requirements.txt
A file that stores information about the libraries or modules used.
