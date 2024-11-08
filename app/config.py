from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_password: str
    database_name:str
    database_username : str
    secret_key : str
    algorithm: str
    access_token_expire_minutes: int
    
    
    class Config:
        env_file = ".env"

settings = Settings()





# We use base settings for configuration of our Environment variables, make it more secure that we can read the Environment file and output the particulat varibale we need, also for validation of the environment variable been parsed