from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Enum
)

import colander

from .meta import Base


class CusConst(object):
    """ Constants for the Customer entity """
    NAME_LEN = 30
    EMAIL_LEN = 40
    CONTRACT_TYPE_ENUM = ["One Time",
                          "Monthly Retainer",
                          "Yearly Retainer"]
    CUSTOMER_TYPE_ENUM = ["Direct", "Affiliate"]


class Customer(Base):
    """ A mapper for the customer table"""
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(CusConst.NAME_LEN), unique=True)
    email = Column(Unicode(CusConst.EMAIL_LEN), unique=True)
    contract_type = Column(Enum(*CusConst.CONTRACT_TYPE_ENUM), nullable=False)
    customer_type = Column(Enum(*CusConst.CUSTOMER_TYPE_ENUM), nullable=False)

    __table_args__ = (
        Index('customer_name_idx', "name"),
    )


class CustomerSchema(colander.MappingSchema):
    """ A schema for validating customer data"""
    name = colander.SchemaNode(colander.String(),
                               validator=colander.Length(max=CusConst.NAME_LEN),
                               name="name")
    email = colander.SchemaNode(colander.String(),
                                validator=colander.All(
                                          colander.Length(max=CusConst.EMAIL_LEN),
                                          colander.Email())
                                )
    contract_type = colander.SchemaNode(colander.String(),
                                        validator=colander.OneOf(CusConst.CONTRACT_TYPE_ENUM))
    customer_type = colander.SchemaNode(colander.String(),
                                        validator=colander.OneOf(CusConst.CUSTOMER_TYPE_ENUM))
