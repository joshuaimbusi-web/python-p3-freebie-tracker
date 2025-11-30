#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Company, Dev, Freebie

DB_URL = 'sqlite:///freebies.db'

if __name__ == '__main__':
    engine = create_engine(DB_URL, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    # ensure tables exist (Alembic-managed schema will already exist if you ran upgrades)
    Base.metadata.create_all(engine)

    # helpful: if DB has no data, prompt to run seed
    if session.query(Company).count() == 0:
        print("No companies found. Run `python seed.py` to create sample data.")

    # drop into interactive ipdb so you can test methods
    import ipdb; ipdb.set_trace()
