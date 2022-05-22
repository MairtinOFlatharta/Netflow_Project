<div id="top"></div>

<h3 align="center">Netflow Project</h3>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li>
          <a href="#built-with">Built With</a>
          <ul>
            <li><a href="#tools">Tools</a></li>
            <li><a href="#python-libraries">Python Libraries</a></li>
          </ul>
        </li>
      </ul>
    </li>
    <li><a href="#web-app-screenshots">Web App Screenshots</a></li>
    <li>
      <a href="#setup">Setup</a>
      <ul>
        <li><a href="#collector-setup">Collector Setup</a></li>
        <li><a href="#application-setup">Application Setup</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About the Project
This project is being graded as a final year project for the course of Computer Science and Information Technology in the
National University of Ireland, Galway.

The main goal of this project is to create a web application
which reads Netflow data from the current server and to display it for monitoring purposes.
The intended users of this web application are network administrators who wish to gain a general overview of which network users
are using which web services and to also monitor potentially malicious network activity.

The app is currently being tested while using softflowd as a network probe and using nfdump to generate aggregations of network connections.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- BUILT WITH -->
### Built With

<!-- TOOLS -->
#### Tools:
* [Python](https://www.python.org/)
* [MongoDB](https://www.mongodb.com/)
* [softflowd](https://github.com/irino/softflowd)
* [nfdump](https://github.com/phaag/nfdump)
* [Flake8](https://flake8.pycqa.org/en/latest/)
* [arp-scan](https://github.com/royhills/arp-scan)

<!-- PYTHON LIBRARIES -->
#### Python libraries:
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Flask-Login](https://pypi.org/project/Flask-Login/)
* [pandas](https://pypi.org/project/pandas/)
* [pyarrow](https://pypi.org/project/pyarrow/)
* [pyasn](https://pypi.org/project/pyasn/)
* [mongoengine](https://pypi.org/project/mongoengine/)
* [setuptools](https://pypi.org/project/setuptools/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- WEB APP SCREENSHOTS -->
## Web App Screenshots
![Dashboard Page](https://user-images.githubusercontent.com/46865705/169703768-b613e1ba-01ba-43bc-835a-61ddc4ad16e1.png)
![Longest Connection Table](https://user-images.githubusercontent.com/46865705/169703786-fa53cd1c-f943-4728-9932-d93e02dfbe5c.png)
![Most Active Connection Table](https://user-images.githubusercontent.com/46865705/169703795-13849dc9-5e10-43e4-bd37-e46b6f71cc2c.png)
![Port Monitoring Form](https://user-images.githubusercontent.com/46865705/169703802-8c81e5da-d28d-49e6-afac-ca55070a762f.png)

<!-- SETUP -->
## Setup

<!-- COLLECTOR SETUP -->
### Collector Setup
To set up the Netflow collector, ensure that nfdump, nfcapd, and softflowd are
all installed on the host machine. Then, both nfdump and softflowd must be
configured to store Netflow records in the ```/var/cache/nfdump/``` directory.
To do this, edit the ```/etc/softflowd/default.conf``` and insert the
following lines:<br>
```
interface='any'
options='-n 127.0.0.1:9995'
```
Then, enter the following lines into the command line:<br>
```
sudo /etc/init.d/softflowd start
sudo nfcapd -D -l /var/cache/nfdump/
```
After a few minutes, nfcapd files should start appearing in the specified directory.

<!-- APPLICATION SETUP -->
### Application Setup
Install Python 3, arp-scan, and all the specified [Python libraries](#python-libraries) using pip (install and
set up a local MongoDB instance as well if that's what you intend to use). Then,
run [setup.py](./setup.py) to set up some initial data needed for the running
of the application. If you wish to associate local hostnames with local IP addresses,
run the [get_private_hosts.sh](./scripts/get_private_hosts.sh) script. You can
also run [get_arp_manufacturers.sh](./scripts/get_arp_manufacturers.sh) to view
the manufacturer of a local device's NIC (requires `sudo`).

Then, the application can be run by running the [start_app.sh](./scripts/start_app.sh)
script and it can be accessed by opening a web browser and navigating to:<br>
`http://127.0.0.1:5000`

<!-- CONTACT -->
## Contact
Máirtín Ó Flatharta - [mairtinflatherty2014@gmail.com](mailto:mairtinflatherty2014@gmail.com) - [Linkedin](https://www.linkedin.com/in/m%C3%A1irt%C3%ADn-%C3%B3-flatharta-842a54178/)

<p align="right">(<a href="#top">back to top</a>)</p>
