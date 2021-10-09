# Bingeread

Bingeread is a web application used to browse books. The project is built using the Django framework, and retrieves book metadata from the Google Books API.


## Features

- Search and browse through lists of books
- View information about a book
- Register a new account
- Add books to your custom lists
- Manage your bookshelf
- Rate an review books


## Requirements

* asgiref version 3.3.1
* certifi version 2020.12.5
* chardet version 4.0.0
* Django version 3.1.6
* idna version 2.10
* pytz version 2021.1
* requests version 2.25.1
* sqlparse version 0.4.1
* urllib3 version 1.26.3


## Installation

Install the required packages using your enviroment of choice.

**Pipenv:**
```bash
$ cd project_folder
$ pipenv install -r requirements.txt
```

**Virtualenv:**
```bash
$ cd project_folder
$ pip3 install -r requirements.txt
```

## Tests

The project has 62 tests across 7 apps. Run the tests using this command:

```bash
$ python3 manage.py test bingeread/apps/<appname>
```
<appname> is optional and can be one of the following values:
* accounts
* bookpage
* bookshelf
* core
* reviews
* scores
* search

<appname> specifies which app's tests to run. If not specified, all 62 tests are executed.


## How to run

1. Start the web application using these commands:

```bash
$ python3 manage.py migrate
$ python3 manage.py runserver
```

2. Open the web application in a web browser (Firefox is preferred). The web application is found on the URL http://localhost:8000/ or http://127.0.0.1:8000/.


## Credits

* Abdimalik Abukar
* Jon Anders Hopland Myklebust
* Marcel Andre Grønvold
* Sangeerth Sathiskumar
* Torbjørn Lier
