#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev

DB_URL = 'sqlite:///freebies.db'

def run_seed():
    engine = create_engine(DB_URL, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    session.query(Company).delete()
    session.query(Dev).delete()
    session.commit()

    c1 = Company(name='Stripe', founding_year=2010)
    c2 = Company(name='GitHub', founding_year=2008)
    c3 = Company(name='HashiCorp', founding_year=2012)

    d1 = Dev(name='Ada')
    d2 = Dev(name='Linus')
    d3 = Dev(name='Grace')

    session.add_all([c1, c2, c3, d1, d2, d3])
    session.commit()

    f1 = c1.give_freebie(d1, 'T-shirt', 20)
    f2 = c1.give_freebie(d1, 'Sticker pack', 2)
    f3 = c2.give_freebie(d2, 'Laptop sticker', 1)
    f4 = c3.give_freebie(d3, 'Beanie', 15)

    session.add_all([f1, f2, f3, f4])
    session.commit()

    print("Seed complete.")
    session.close()


if __name__ == '__main__':
    run_seed()

