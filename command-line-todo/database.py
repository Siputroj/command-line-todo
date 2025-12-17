from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from typing import Generator

Base = declarative_base()

class List(Base):
   __tablename__ = 'list'

   id = Column(Integer, primary_key = True)
   name = Column(String, nullable = False, unique = True)

   tasks = relationship(
      "Task",
      backref = "list",                                     # allow to refer back to the list by doing my_task.list
      cascade = "all, delete-orphan",                       # delete if list is deleted, or if task has no list
      order_by = "Task.id"
   )


class Task(Base):
   __tablename__ = 'tasks'
   
   id = Column(Integer, primary_key = True)                 # Primary key will auto increment
   description = Column(String, nullable = False)
   is_completed = Column(Boolean, default = False)

   list_id = Column(Integer, ForeignKey('list.id'))



# ------------ DB CONNECTION ------------

DATABASE_URL = "sqlite:///./mydb.db"

engine = create_engine(
   DATABASE_URL,
   connect_args = {
      "check_same_thread": False,
   }
)

sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def init_db():
   Base.metadata.create_all(bind = engine)

def get_db() -> Generator[Session, None, None]:
   db = sessionLocal()
   try:
      yield db
   finally:
      db.close()

init_db()