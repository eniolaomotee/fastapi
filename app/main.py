from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post,user,auth,votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware



# models.Base.metadata.create_all(bind=engine)
app = FastAPI()


origins =["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message":"Hello there"}

# Middleware is a function that runs before any of our requests

# CORS 
# This allows you to make requests from a web browser on one domain to a server on a different domain, by default our API will only allow web browsers running on the same domain as our server to make requests to it.


# ENV variables are always set up in a string, you'd then do the validation on your end for the particular data type you want it to be.


# Using alembic which is a lightweight tool allows you to make changes and roll them back on your db, so you can create tables etc with alembic. It gives you a GIT kinda use when using it,

# So once you install alembic you'd want to import Base from your Models.py cause this is the models alembic would be building your tables on.You'd also want to import settings so you have access to your basesettings object for setting your sqlalchemy url.


# When settting up your env.py you'd need to set your target.metadata to Base.metadata and also override the alembic.ini config on you env.py file as well.

# After this is set you can now begin to create your tables a. alembic revision -m "the name of the column you want to create" this would create a new file with 2 function: upgrade and downgrade, you'd define what you're creating on the upgrade nd if you want to delete the table you'd use downgrade. You'd also want to commit your changes to your DB using alembic upgrade head which is the current file you're working on or alembic upgrade the revision number.

# So we can keep track of the changes just like GIT we can also get current file with alembic direct as well as downgrade(delete) with -1 and upgrade to wiht +1

# We can also autogenerate our version via alembic, so alembic does this in such a way that it mirrors the models and database and then create this, what you'd have to do is to upgrade the changes so it can reflect on your tables 