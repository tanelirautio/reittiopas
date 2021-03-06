# Reittiopas

Routeplanner app made for [Solidabis Code Challenge](https://koodihaaste.solidabis.com/) in the year 2020.

## Demo

The demo of the app is running in Heroku: https://reittiopas.herokuapp.com/

## Details

  * Backend is made with Flask (Python) 
  * Frontend is just HTML + CSS + Vanilla JavaScript
  * Development was made in Windows 10
  * Variables, comments and documentation are written in English. However, the user interface for app is in Finnish (assignment was in Finnish)

## About the implementation

  * Application uses Dijkstra's algorithm for searching shortest path from origin stop to destination stop
  * The roads which don't have any bus lines are discarded before algorithm is used
  * If transfer has to be made during the trip the preference is given for the line which continues in the route in later road sections
  * If some routes are served by multiple lines the app just selects one randomly (since the assignment states that you don't have to wait at all when changing buses)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. These instructions are for Windows, although the setup for Python and Flask shouldn't be very complicated on other operating systems.

### Prerequisites

  * [Python 3](https://www.python.org/downloads/windows/) 
  * Flask

  * (Optional) VirtualEnv
  * (Optional) VirtualEnvWrapper-win

```
1. Install Python 3
```

Optionally at this point you can install VirtualEnv so you can test Python code in encapsulated environment. Below is a brief explanation of steps. Better tutorial for setting up VirtualEnv in Windows can be found [here](https://timmyreilly.azurewebsites.net/python-flask-windows-development-environment-setup/). 

```
2a. Install VirtualEnv with the command 'pip install virtualenv'
2b. Install VirtualEnvWrapper-win with the command 'pip install virtualenvwrapper-win'
2c. Create virtual environment for project: 'mkvirtualenv reittiopas' (or whatever name you desire)
2d. In the root of the reittiopas project run command: 'setprojectdir'
```

In the project dir you need install some Python libraries:

```
3. 'pip install flask'
4. 'pip install flask-table'
```

### Installing

Open command prompt and go to project root folder. Run:

```
 'run.bat'
```
This will start the built-in development web server in Flask. You can then open your favourite web browser and go to: 

```
localhost:5000
```

## Built Using

* [Simple Responsive Table in CSS](https://codepen.io/AllThingsSmitty/pen/MyqmdM) by Matt Smith
* [attention.js](https://github.com/janmarkuslanger/attention.js) - by janmarkuslanger
* [select-css](https://github.com/filamentgroup/select-css) - by filament group
* [Bus icon](https://www.iconsdb.com/black-icons/bus-icon.html) - by iconsDB.com

## Author

* **Taneli Rautio**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
