from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from environs import Env

env = Env()
env.read_env()

session_maker = sessionmaker(bind=create_engine(env("URL")))
session = session_maker()

