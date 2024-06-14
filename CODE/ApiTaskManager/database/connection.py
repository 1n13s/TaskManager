from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
import os

database_file_name = "../../../DATABASE/taskmanager.db"
current_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f"sqlite:///{os.path.join(current_dir,database_file_name)}"

DATABASE_URL='postgresql://postgres:22348936@localhost/TaskManagerDatabase'

engine = create_engine(DATABASE_URL, echo=False)

session = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()