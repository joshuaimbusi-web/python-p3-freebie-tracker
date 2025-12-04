# helpers.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

DB_URL = "sqlite:///freebies.db"

# Create engine and session factory
engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)

# Ensure tables exist if Alembic wasn't run (safe in dev)
Base.metadata.create_all(engine)


def get_session():
    """Return a new SQLAlchemy session (caller should close/commit as needed)."""
    return Session()


# --- Find helpers ---
def find_company_by_id(session, company_id):
    return session.query(Company).get(company_id)


def find_company_by_name(session, name):
    return session.query(Company).filter(Company.name == name).first()


def find_dev_by_id(session, dev_id):
    return session.query(Dev).get(dev_id)


def find_dev_by_name(session, name):
    return session.query(Dev).filter(Dev.name == name).first()


def find_freebie_by_id(session, freebie_id):
    return session.query(Freebie).get(freebie_id)


# --- List helpers ---
def list_companies(session):
    return session.query(Company).order_by(Company.id).all()


def list_devs(session):
    return session.query(Dev).order_by(Dev.id).all()


def list_freebies(session):
    return session.query(Freebie).order_by(Freebie.id).all()


# --- Create / Update / Delete helpers ---
def create_company(session, name, founding_year=None):
    c = Company(name=name, founding_year=founding_year)
    session.add(c)
    session.commit()
    return c


def create_dev(session, name):
    d = Dev(name=name)
    session.add(d)
    session.commit()
    return d


def give_freebie(session, company: Company, dev: Dev, item_name: str, value: int):
    """Use Company.give_freebie to create the Freebie and persist it."""
    freebie = company.give_freebie(dev, item_name, value)
    session.add(freebie)
    session.commit()
    return freebie


def transfer_freebie(session, from_dev: Dev, to_dev: Dev, freebie: Freebie):
    """Attempt to transfer a freebie from one dev to another. Return bool."""
    success = from_dev.give_away(to_dev, freebie)
    if success:
        session.add(freebie)
        session.commit()
    return success


def delete_freebie(session, freebie: Freebie):
    session.delete(freebie)
    session.commit()


# Utility small-print helpers for CLI formatting
def company_summary(c: Company) -> str:
    return f"[{c.id}] {c.name} (founded: {c.founding_year})"


def dev_summary(d: Dev) -> str:
    return f"[{d.id}] {d.name}"


def freebie_summary(f: Freebie) -> str:
    dev_name = f.dev.name if f.dev else "None"
    company_name = f.company.name if f.company else "None"
    return f"[{f.id}] {f.item_name} (value: {f.value}) - {dev_name} <-- {company_name}"
