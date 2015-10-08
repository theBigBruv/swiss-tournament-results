# swiss-tournament-results
This project is a Python module that uses the PostgreSQL database to keep track of players and matches in a Swiss game tournament.

### Requirements ###
1. Python 2.7 or above should be installed on your computer. Instructions for checking if python is installed, or for downloading and installing it, can be found here: https://wiki.python.org/moin/BeginnersGuide/Download
2. Vagrant Virtual machine and VirtualBox. The Vagrant VM has already been installed and configured on the repo you'll download, so you do not need to worry about that. For Virtual Box, instructions for downloading and installing it for your OS can be found here: https://www.virtualbox.org/wiki/Downloads
3. repo already has PostgreSQL server installed, as well as the psql command line interface (CLI)

### Getting Started ###
You can test out all the functions that have been created in this project:
1. Download the repo as a zip file to your computer (swiss-tournament-results-master.zip).
2. Unzip the downloaded file, save the extracted folder to a location of your choice.
3. To use the Vagrant virtual machine, launch terminal on MAc or the Command prompt on Windows, and navigate to where you stored the unzipped folder.
4. Then navigate to swiss-tournament-results > vagrant > tournament.
5. Powers on the virtual machine by typing the command vagrant up.
6. Then log into the virtual machine by typing the command vagrant ssh.
7. Change directory to the synced folders by typing the command cd /vagrant/tournament
8. Build the database, tables and views by running the command psql followed by \i tournament.sql. This will run the database configuration file (tournament.sql), 
9. Exit out of psql by typing the command \q
10. Run the python test for the functions in this project by typing the command Python tournament_test.py.
