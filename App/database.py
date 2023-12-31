from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import psycopg2
import time 
from .Config import settings
### bad practice to hard code sensitive info; username, password, ip... etc.
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='FastAPI', 
                                user='postgres', password='Juan1898',
                                cursor_factory=RealDictCursor)
        
        cursor = conn.cursor()
        print('Database connection was sucessfull')
        break
    except Exception as e:
        print(f"Connection to database failed: {e} ")
        time.sleep(2)