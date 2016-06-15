from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.schema import MetaData
from sqlalchemy import Column, Integer
# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.readthedocs.org/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class BaseCls(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        cols = [(c[0], getattr(self, c[0])) for c in self.__table__.columns.items() if c[1].unique]
        template = "<%s id=%s "+("%s=%s "*len(cols))[:-1]+">"
        args = [self.__class__.__name__, self.id]
        args.extend([c for tup in cols for c in tup])
        return template % tuple(args)

Base = declarative_base(metadata=metadata, cls=BaseCls)
