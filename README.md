# Rutgers Software Engineering 2017

This is the repository for our Software Engineering course project, ChefBoyRD, which was completed during the spring semester of 2017.

[![Build Status](https://travis-ci.org/ZacBlanco/ChefBoyRD.svg?branch=master)](https://travis-ci.org/ZacBlanco/ChefBoyRD) [![Python 3.3+](https://img.shields.io/badge/Python-3.3%2B-orange.svg)](https://python.org) [![GitHub license](https://img.shields.io/badge/license-AGPL-blue.svg)](https://raw.githubusercontent.com/zacblanco/ChefBoyRD/master/LICENSE)

## Team Members:

* Richard Ahn
* Zachary Blanco
* Benjamin Chen
* Jeffrey Huang
* Jarod Morin
* Seo Bo Shim
* Brandon Smith

## Repository Structure

- `docs/` houses the code documentation for the project
- `chefboyrd/` houses all of the source code for the project
- `reports/` contains all of the submitted reports for the project.

View the README in each folder for more information about what is contain within each directory.

## Developer Quick-Start

All commands below should work in the bash command line with a Debian distribution of GNU/Linux.

**Step 1: Install Dependencies**

- For MacOS users you can [install homebrew](https://brew.sh) and replace all `sudo apt install` commands with `brew install`
- For Windows users - good luck trying to install everything.

See the end of step one for a block of commands to copy-paste for setup.

**Pre-Requisites**:

- python 3.3+ (`sudo apt install python3`)
- python's package manager, pip (`sudo apt install python3-pip`)
- NumPy (`sudo apt install python3-numpy`)
- SciPy (`sudo apt install python3-scipy`)

Below is a command which will install everything (Copy-Paste)

    sudo apt install python3 python3-pip python3-numpy python3-scipy

Once you've run that you need to clone this repository

    git clone https://github.com/zacblanco/ChefBoyRD.git

`cd` into the directory

    cd ChefBoyRD/

Great! Make sure that all of the code is there as expected. We'll need to use `virtualenv` to install our packages locally for our project.

    sudo pip install virtualenv
    virtualenv -p python3 env
    source env/bin/activate

Okay, so now your prompt should look something like:

    (env) zac@ZB-XPS13:~/.../chefboyrd$

Finally we just install our python packages

    pip install -r requirements.txt

That will install the required python package dependencies so that we can import them successfully.

Here's all of the commands together.

    sudo apt install python3 python3-pip python3-numpy python3-scipy
    git clone https://github.com/zacblanco/ChefBoyRD.git
    cd ChefBoyRD/
    sudo pip install virtualenv
    virtualenv -p python3 env
    source env/bin/activate
    pip install -r requirements.txt

**Step 2: Ensure Unit Tests are Running**

So now that we have all of the code and dependencies installed we can try to run the unit tests. While in the root directory of the repository run the following command:

        make test

You should see something like the following

        zac:ChefBoyRD$ make test
        python3 -m unittest discover -s chefboyrd/tests/
        ...
        ----------------------------------------------------------------------
        Ran 3 tests in 0.001s

        OK
        zac:ChefBoyRD$

If you see any failures then you should investigate the issue. If you think there is an error or missing dependency which needs to be installed notify the repository maintainers

To under tests individually, specify the path to the desired test file. Here is an example:

	python3 -m unittest chefboyrd/tests/test_fb.py


## Running the Debug Server

Simply run the command

        make debug

This will start the debugging server at `http://localhost:5000` where you can navigate to app web pages to test the server. You should see an output like the following.

    zac:ChefBoyRD$ make debug
    bash ./flask_debug.sh
      * Serving Flask app "chefboyrd"
      * Forcing debug mode on
      * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
      * Restarting with stat
      * Debugger is active!
      * Debugger pin code: 369-149-264

## The Amazon Alexa Skill

In order to run the Amazon Alexa skill you'll need to

- Install **[ngrok](https://ngrok.com/)**
- Create an AWS developer account

Once you have both you'll need to create a new Amazon Alexa skill that utilizes the same skill schema found under `chefboyrd/alexa/skill.json`. Information on how to create an Alexa skill can be [found here (start from step 2)](https://developer.amazon.com/alexa-skills-kit/alexa-skill-quick-start-tutorial)

When creating the skill select **https endpoint** rather than a lambda function. Leave this screen up.

Open up your bash terminal to the ChefBoyRD repository. Follow the instructions to install all dependencies.

```
cd chefboyrd
virutalenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

After installing dependencies you can run

        python skill.py

Once the skill is running you'll need to open a 2nd terminal and type `ngrok http 5000`. This will open a localhost tunnel to HTTP 5000 on your computer and give you an https endpoint. Copy the https url from ngrok and paste it into the https endpoint on your Alexa skill configuration. Use your echo or go to [https://echosim.io](https://echosim.io) in order to test the chefboyrd skill.

## Deadlines:

| Task	     | Due Date	     |
|:----------:|:-------------:|
| Proposal  | January 30th |
| Report 1 Part 1: Statement of Work & Requirements | February 5th |
| Report 1 Part 2: Functional Requirements Spec & UI | February 12th |
| Report 1: Full | February 19th |
| Report 2 Part 1: Interaction Diagrams | February 26th |
| Report 2 Part 2: Class Diagrams and System Architecture | March 5th |
| Report 2: Full | March 12th |
| First Demo | March 27th | 
| Report 3: Part 1: | April 23rd |
| Second Demo | April 25th |


## Description:

This restaurant automation application, ChefBoyRD, (ChefBoy Restaurant Development) is a software program that offers solutions to the specific problems. These problems include, improving business efficiency by reducing food waste, improviding feedback submissions and processing, and improving the customer experience with a reservation system. The relevant results generated by the program will be accessible by employees, e.g. chefs will have access to dish prediction, hosts and hostesses will see reservations. All of the program's functions can be centrally monitored by the manager.


