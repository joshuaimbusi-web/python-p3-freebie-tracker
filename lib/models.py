from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    founding_year = Column(Integer())

    def __repr__(self):
        return f"<Company {self.name}>"

    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        self.freebies.append(new_freebie)
        return new_freebie

    @classmethod
    def oldest_company(cls, session=None):
        if session is None:
            raise RuntimeError("Company.oldest_company requires a SQLAlchemy session. Call Company.oldest_company(session).")
        return session.query(cls).order_by(cls.founding_year.asc()).first()

    @property
    def devs(self):
        return list({f.dev for f in getattr(self, "freebies", []) if f.dev is not None})

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)

    def __repr__(self):
        return f"<Dev {self.name}>"

    @property
    def companies(self):
        return list({f.company for f in getattr(self, "freebies", []) if f.company is not None})

    def received_one(self, item_name: str) -> bool:
        for f in getattr(self, "freebies", []):
            if f.item_name == item_name:
                return True
        return False

    def give_away(self, to_dev, freebie) -> bool:
        if freebie in getattr(self, "freebies", []):
            freebie.dev = to_dev
            return True
        return False

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)

    dev_id = Column(Integer(), ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)

    dev = relationship('Dev', backref=backref('freebies', cascade='all, delete-orphan'))
    company = relationship('Company', backref=backref('freebies', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<Freebie {self.item_name} (value={self.value})>"

    def print_details(self) -> str:
        dev_name = self.dev.name if self.dev else "<no-dev>"
        company_name = self.company.name if self.company else "<no-company>"
        return f"{dev_name} owns a {self.item_name} from {company_name}."

