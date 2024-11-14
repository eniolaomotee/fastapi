from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas,models
from app.config import settings
from app.database import get_db,Base
import pytest
from alembic import command
from app.oauth2 import create_access_token



# Conftest is package specific

SQLALCHEMY_DATABASE_URL =f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)


# Base.metadata.create_all(bind=engine)


# # Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
        
# So we can't be using our dev DB for testing in this case we'd need have another instance of our DB which would be a dependency and would be overridden as well.
# app.dependency_overrides[get_db] = override_get_db




# So here i'm basically creating fixtures and I can creating my test db and after the test finishes I'm dropping the table as well.

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
    
 # #run our code before we run our test
    # Base.metadata.create_all(bind=engine)
    # yield TestClient(app)
    # Base.metadata.drop_all(bind=engine)
    #  # run our code after our test finishes
     
     
     
    
    # If we're using alembic
    # command.upgrade("head")
    # yield TestClient(app)
    # command.downgrade("base")
    
    

# We create this fixture here to provide the user on our login test with the correct credentials when testing his login.

@pytest.fixture
def create_test_user(client):
    user_data = {"email":"virgil@gmail.com","password":"virgil"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def create_test_user2(client):
    user_data = {"email":"virgil123@gmail.com","password":"virgil"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def token(create_test_user):
    return create_access_token({"user_id":create_test_user['id']})


@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    
    return client
    
    
    
@pytest.fixture
def test_post(create_test_user,session, create_test_user2):
    posts_data = [{
        "title":"first title",
        "content":"first content",
        "owner_id": create_test_user['id']
    },{
        "title":"second title",
        "content":"2nd content",
        "owner_id": create_test_user['id']
    },
    {
        "title":"third title",
        "content":"3rd Content",
        "owner_id": create_test_user['id']
    },{
        "title":"third title",
        "content":"3rd Content",
        "owner_id": create_test_user2['id']
    }]

    # So for creating our post we need to store it in our Post DB, and to do this we can either add it manually or use a map function to execute this as well, which we have done below.
    def create_post_model(post):
        return models.Post(**post)
        
    post_map = map(create_post_model,posts_data)

    posts = list(post_map)
        
        
    session.add_all(posts)   


# session.add_all([models.User(title="first title",content="first content",owner_id=create_test_user['id']),
# models.Users(title="2nd title",content="2nd content", owner_id=create_test_user['id'])],models.Users(title="3nd title",content="3rd content", owner_id=create_test_user['id']) )
    
    session.commit()

    posts = session.query(models.Post).all()
    return posts