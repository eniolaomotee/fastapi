from fastapi import FastAPI
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
    return {"message":"Hello World pushing to Ubuntu "}






# Dockerizing our application
# You'd have to create an image that would contain your codes amongst others

# Bind mount(volume) - allows us to sync with a folder on our local machine with a folder on our container