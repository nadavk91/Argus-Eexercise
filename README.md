# Argus-Eexercise
Argus Backend Automation Exercise
In order to run the script you need to follow the next steps:

Step 1: Create MongoDB docker

in your linux machine run the command

sudo docker pull mongo

afther that, type

sudo docker run -d -p 27017:27017 mongo

Step 2:
download the script "GitHubScrapper.py" to your machine

Step 3:
Pull the docker which the python script will run from.
the docker contains python, chorme and selenium chrome driver,
and python modules selenium and pymongo

to pull the docker type:
sudo docker pull nadavk91/python-sel

step 4:
before running the docker and the script, make sure you know your ip.
It will be used when you run the script in order to connect to the mongo db

Step 5:
change your working directory so it will be where the python script is located and type

sudo docker run -it -v $(pwd):/usr/workspace nadavk91/python-sel sh

Step 6:
as the shell open
type
python GitHubScrapper.py [LocalIp]
dont forget to add the localIP as an argument to the script.

There you go. the script is running, and I jope everything worked well :)

Nadav Kalma
