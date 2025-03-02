# iA Assessment

## Overview
This repo contains the iA Coding Challenge completed by James Smith including all required deliverables. 

## Running the Project
This project is launched using Docker Compose, so ensure that your local machine is running the Docker engine. For information on how to run Docker on your local machine, please see Docker's official documentation MAKE THIS A LINK HERE. 

1. Start by cloning down the repo to your local machine. With the Docker engine running, run the command from the compose.yaml level of the project **docker-compose build** command to build the Docker image.

2. Once the image is built, you can build the compose stack by running the command **docker-compose up -d && docker-compose exec cli python /opt/iarx/cli.py**. This command starts up the Postgres DB, the backend API, generates random seed data and pushes it to the DB, and opens the CLI to interface with the program. 

3. At this point, x and y coordinates can be input into the CLI by following the provided prompts. To exit the interactive CLI, enter **n** when prompted if you would like to enter an additional coordinate. 

## Assumptions
Several assumptions were made while completing this assessment. This section will detail those assumptions.

1. A DB should be used to 