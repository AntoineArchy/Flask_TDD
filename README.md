# gudlift-registration

1. Why
   
   The given source material state : 

""This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.""

The goal is to pursue the early development and handle any existing or arising issues during the development of the next phase of the project

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)
 

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing
   
   Testing is done using Pytest. All tests are located in the directory tests/<test_type>. To run the tests :
   - Run the command line : <code>pytest</code>
   After running pytest, a pytest report and a coverage report will be displayed in the terminal, additionally these reports will be generated in html and can be found in the /reports directory of the projects.


   [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) is used to check code coverage while running pytest. This is set automatically via setup.cfg.

   Locust is set as a load testing, all params are in locust.conf. To run Locust:
   - Make sure that your Flask server is up and running
   - Make sure that your server adresse is in pair with the host set in locust.conf (default : host = http://127.0.0.1:5000/)
   - Run the command line : <code>locust</code>
   After running locust, a report will be displayed in the terminal, additionally this report will be generated in html and can be found in the /reports directory of the projects.
   
   Right now, locust is set to run primarily in terminal, but the UI is also available if you want to go this way. 

   