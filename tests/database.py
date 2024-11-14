from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db,Base
import pytest
from alembic import command


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/fastapi_test'

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