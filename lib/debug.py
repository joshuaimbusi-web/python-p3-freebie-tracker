#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Company, Dev, Freebie

DB_URL = 'sqlite:///freebies.db'

if __name__ == '__main__':
    engine = create_engine(DB_URL, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    if session.query(Company).count() == 0:
        print("No companies found. Run `python seed.py` to create sample data.")

    import ipdb; ipdb.set_trace()
