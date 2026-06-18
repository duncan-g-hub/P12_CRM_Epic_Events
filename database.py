from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqlconnector://admin:admin@localhost/epic_events_CRM",
                       echo=True)
Session = sessionmaker(bind=engine)
session = Session()
