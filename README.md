# GDELT-ANALYSIS

_In this repository you will be able to find some scripts about how to use datasets from "The GDELT Project" with Python and MongoDB_

<!-- GETTING STARTED -->
## Getting started 🚀

_These instructions will allow you to get a copy of the project running on your local machine for development and testing purposes._

### Prerequisites 📋

_What things do you need to prepare the environment. In the following links there are explained how to install the software and how to use them._

* [Python](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html)
* [MongoDB](https://docs.mongodb.com/manual/installation/)
* [Spyder](https://docs.spyder-ide.org/current/installation.html)


### Project installation 🔧

1. Clone the repository
```sh
git clone https://github.com/revadhawan/GDELT-Analysis.git
```
2. Install NPM packages
```sh
npm install
```

<!-- USAGE EXAMPLES -->
## Usage ⚙️

1.	Execute the following commands in order to create the database and collection in mongoDB:
```sh
use GDELT
```
```sh
db.createCollection("Events")
```

2. Download the data from [GDELT Project website](http://data.gdeltproject.org/events/index.html). For that, execute the following script on Spyder:

* [01_download.py](https://github.com/revadhawan/GDELT-Analysis/blob/master/01_download.py)

3. Import the data to the recently database created on mongoDB. For that, execute the following script on Spyder:

* [02_import.py](https://github.com/revadhawan/GDELT-Analysis/blob/master/02_import.py)


4. Clean the datase to get rid of unnecessary data. For that, execute the following script on Spyder:

* [03_cleanDatabase.py](https://github.com/revadhawan/GDELT-Analysis/blob/master/03_cleanDatabase.py)

Once you have the entire environment prepared, you are ready to obtain the graphs shown in this project. For that, you can execute the rest of scripts that are available on the repository.

## Developing tools 🛠️

* [Python](https://www.python.org/) - Programming language
* [MongoDB](https://www.mongodb.com/) - The database used
* [Spyder](https://www.spyder-ide.org/) - Development environment

<!-- CONTACT -->
## Contact
* [LinkedIn](https://www.linkedin.com/in/revadhawan/)
* [Gmail](revadhawan21@gmail.com)
