# iA Assessment

## Overview
This repo contains the iA Coding Challenge completed by James Smith including all required deliverables. 

## Running the Project
This project is launched using Docker Compose, so ensure that your local machine is running the Docker engine. For information on how to run Docker on your local machine, please see Docker's official documentation **[HERE](https://www.docker.com/blog/getting-started-with-docker-desktop/)**. 

1. Start by cloning down the repo to your local machine. With the Docker engine running, run the command from the compose.yaml level of the project **docker-compose build** command to build the Docker image.

2. Once the image is built, you can build the compose stack by running the command **docker-compose up -d && docker-compose exec cli python /opt/iarx/cli.py**. This command starts up the Postgres DB, the backend API, generates random seed data and pushes it to the DB, and opens the CLI to interface with the program. 

3. At this point, x and y coordinates can be input into the CLI by following the provided prompts. To exit the interactive CLI, enter **n** when prompted if you would like to enter an additional coordinate. 

## Assumptions
Several assumptions were made while completing this assessment. This section will detail those assumptions.

1. A DB was created to house the seeded values, since a DB would be used in a warehouse to keep track of stations, meds, and their prices. Therefore, seeded data was pushed to the DB instead of being stored in memory. 

2. The API was decoupled from the CLI service instead of wrapping the application into one monolith repo. This was done to allow the API to change and scale as needed without affecting the CLI as needed in the future if this were actual business code. 

3. The number of seeded fill stations is between 6 and 15. This was done so there would not be an excessive number of fill stations immediately surrounding the given coordinates while still allowing for enough stations to be able to verify the Manhattan Distance is being computed correctly. 

4. The price of the medications was kept between $1.00 and $100.00. This was done simply to limit the range of values for the assessment. 

5. Docker containers were not explicitly requested in the instrucitons, but using them makes the code portable and able to be run on any machine with Docker running, so they were utilized. 
