def add(num1:int,num2:int):
    return num1 + num2 

def subtract(num1:int, num2:int):
    return num1 - num2 

def multiply(num1:int,num2:int):
    return num1*num2

def divide(num1:int,num2:int):
    return num1/num2


class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self,starting_balance=0):
        self.balance = starting_balance
        
    def deposit(self,amount):
        self.balance += amount
    
    def withdraw(self,amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficeint funds in account")
        self.balance -= amount
        
    def collect_interest(self):
        self.balance *= 1.1
        
        
        
        
        
        
        
        
# At 13:55:05 for those who wondering what causing the Internal server error. In the postgres docker container the tables are not creating, so we need to create the tables in order perform the requested action on localhost:8000.
# Follow these steps it has worked for me
# 1) Put the command docker ps and find your container ID
# 2) Then enter into the bash -> docker exec -t YOUR_CONTAINER_ID bash
# 3) Now it will enter into the bash, type -> alembic upgrade head
# This will fix the issue by creating the tables to perform the action. Now go to Postman API and run the create user request, it will work. But the only issue is the data is not storing.





# Around 11:55:05 I spend so much time trying to fix an issue here, so hopefully my comment can help someone:
# 1 - Since we use Alembic, the tables are not created when we start our containers so after running docker-compose up -d, you need to go inside the container and manually run the command:
# "docker exec -it <id_container> bash"
# " alembic upgrade head"
# You should be able to create a user now.

# 2- If it says "database fastapi does not exist" whatever you had in the docker-compose file when your first ran it is probably still stored in there. Get rid of all volumes containers and ilages and restart:
# "docker image rm <image_id>"
# "docker volume rm <volume _name>"
# and then docker-compose up -d 
# and then step 1 and you'll be fine :D



# CI/CD 
# Continous Integration - automated process to build,package and test applications
# Continous Delivery - Picks up where continuous integration ends and automates the delivery of applications

# CI/CD tools include jenkins,Travis CI, Circle CI, Travis CI etc
# We will be using Github actions for our CI/CD pipeline because it's already integrated with our github repo and it's hosted on github so there's no need to install anything on our local machine

# What does a CI/CD tool do actually?
# All CI/CD platforms are dead simple
# They provide a runner - Nothing more than a computer(VM) to run the bunch of commands we specify
# These commands are either usually configured in a YAML/JSON file or through a gui
# The different steps/commands we provide makeup all of the actions our pipeline will perform 
# The pipeline will be triggered based off of some event(git push/merge)



# This is if we're deploying to multiple branches
# on: 
#   push: 
#     branches:
#       - "main"
#       - "anotherbranch"
#   pull_request:
#     branches:
#       - "test_branch"




# name: Build and Deploy Code

# on: [push, pull_request]

# jobs:
#   job1: 
#       runs-on: ubuntu-latest
#     steps: 
#       - name: pulling git repo
#         uses: actions/checkout@v4
#       - name: say hi to eniola
#         run: echo "Hello Omotee"



