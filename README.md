# Reittiopas

Route planner application originally created for the Solidabis Code Challenge in 2020.

## Live Demo

👉 https://reittiopas-j05x.onrender.com

## Background

The task was to implement a simplified public transport route planner based on a predefined data set.

The input data describes a fictional bus network in JSON format, consisting of:

- **Stops** (`pysakit`)
- **Roads between stops** (`tiet`), each with a travel duration
- **Bus lines** (`linjastot`), where each line serves a specific sequence of stops and is identified by a color

The challenge was to build an application where the user selects:
- a **starting stop**
- a **destination stop**

and the system computes:
- which **bus line(s)** should be taken
- where a **line change** is required (if any)
- which **stops are passed along the route**

The goal was to find the shortest valid route while respecting the available bus lines.  
Transfers were allowed without waiting time, and roads not served by any bus line were ignored.

The input data uses Finnish naming (`pysakit`, `tiet`, `linjastot`), but the application logic and code are written in English.

## Details

  * Backend is made with Flask (Python) 
  * Frontend is just HTML + CSS + Vanilla JavaScript
  * Originally developed on Windows 10

## About the implementation

  * The routing logic focuses on finding the shortest valid path through the network while respecting the available bus lines
  * Application uses Dijkstra's algorithm for searching shortest path from origin stop to destination stop
  * The roads which don't have any bus lines are discarded before algorithm is used
  * If transfer has to be made during the trip the preference is given for the line which continues in the route in later road sections
  * If some routes are served by multiple lines the app just selects one randomly (since the assignment states that you don't have to wait at all when changing buses)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. These instructions are for Windows, although the setup for Python and Flask shouldn't be very complicated on other operating systems.

### Prerequisites

  * [Python 3](https://www.python.org/downloads/windows/) 
  * Flask

  * (Optional) venv module

```
1. Install Python 3
```

Optionally at this point you can install venv so you can test Python code in encapsulated environment. 

```
2a. Install virtual environment: 'py -m venv .venv'
2b. Activate virtual environment: '.venv\Scripts\activate'
2c. Install the dependencies: 'pip install -r requirements.txt'
```

### Installing

Open a terminal and go to the project root folder.

Activate the virtual environment and run:

```
run.bat
```

This starts the Flask development server.  
Open your browser at:

```
localhost:5000
```

### Running without run.bat (cross-platform)

From the project root:

```
python -m routeplanner.main
```

This runs the app as a Python module, which is required for package-relative imports.

## Built Using

* [Simple Responsive Table in CSS](https://codepen.io/AllThingsSmitty/pen/MyqmdM) by Matt Smith
* [attention.js](https://github.com/janmarkuslanger/attention.js) - by janmarkuslanger
* [select-css](https://github.com/filamentgroup/select-css) - by filament group
* [Bus icon](https://www.iconsdb.com/black-icons/bus-icon.html) - by iconsDB.com

## Author

* **Taneli Rautio**

## Deployment

The app is deployed as a Python web service using Gunicorn.
The production environment runs the application as a module:

```
gunicorn routeplanner.main:app
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
