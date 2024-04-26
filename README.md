# The aim of the project:
The aim of this project is to enhance the daily workflow of medical professionals and optimize the efficiency of their system, reducing overall waiting times by developing a laboratory management system with an integrated predictive model for detecting anaemia based on the morphology of red blood cells. To streamline the diagnostic process and improve the accuracy of anaemia detection, ultimately benefiting both medical professionals and patients.
# Project preview:
The system consists of 3 containers part of the same network :
 - Django container for the MarengoLab medical lab dashboard
 - ML model container for the trained KNN model and its scaler with a FAST-API endpoint to communicate with other services
 - MYSQL container 
# Steps to follow to run the code :
1. Install docker desktop and make sure the engine is running
2. Access the directory where the docker-compose.yml in stored in and run the following code to build the iamges then to start the containers `docker compose build` then run `docker compose up -d`
3. Once you are sure that all three containers are running, test it on your browser following this URL **http://localhost:8000/**
4. If step 3 worked go to step 5 else, try and look at the docker logs within the docker desktop app  to get an idea why its not working, any app running on the same ports as the Django app or mysql would have to be stopped .
5. Run the following command to configure the database `docker compose run app  sh -c " cd /code/MarengoLab/  && python manage.py makemigrations "` and the second command `docker compose run app  sh -c " cd /code/MarengoLab/  && python manage.py migrate"`
6. Run the script to populate the Group,Normal_range and parameters models as well as create a regular user and an admin user :`docker compose run app  sh -c " cd /code/MarengoLab/  && python Scripts/PopulateDB.py "`
7. A message in the terminal will be printed out to confirm If step 6 was successful
8. Use one of the usernames and passwords found in the PopulateDB.py script, which have been added for demo purposes only.
9. Once done, run the following script to stop the running containers `docker compose down`
# Additonal documents:
- https://github.com/SoniaTad/Anemia_model_eval/tree/main
