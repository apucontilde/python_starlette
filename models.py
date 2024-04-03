from typing import List
from typing import Optional
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship, ForeignKey, String
from sqlalchemy.orm import RelationshipProperty


class Base(SQLModel):
    def as_dict(self) -> dict:
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if "_id" not in c.name
        }


class User(Base, table=True):
    __tablename__ = "user_account"
    id: int | None = Field(primary_key=True)
    name: str = Field(String(30))
    fullname: Optional[str] = None
    addresses: List["Address"] = Relationship(back_populates="user")

    def as_dict(self) -> dict:
        return {
            **super().as_dict(),
            **{"adresses": [a.as_dict() for a in self.addresses]},
        }

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base, table=True):
    __tablename__ = "address"
    id: int | None = Field(default=None, primary_key=True)
    email_address: str
    user_id: int | None = Field(default=None, foreign_key="user_account.id")
    user: User = Relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


class Company(Base, table=True):
    __tablename__ = "company"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(String(30))
    website: str
    logo_url: str


class CompensationFreq(float, Enum):
    monthly = 30.437
    yearly = 365.25
    hourly = 1.0


class Currency(Base, table=True):
    __tablename__ = "currency"
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(String(3))
    min_denomination_decimals: int

    def __repr__(self) -> str:
        return f"Currency(id={self.id!r}, code={self.code!r})"


class Listing(Base, table=True):
    __tablename__ = "listing"
    id: int | None = Field(default=None, primary_key=True)
    title: str
    user_id: int | None = Field(default=None, foreign_key="user_account.id")
    user: "User" = Relationship()
    compensation: int
    compensation_freq: CompensationFreq
    currency_id: int | None = Field(default=None, foreign_key="currency.id")
    currency: "Currency" = Relationship()
    company_id: int | None = Field(default=None, foreign_key="company.id")
    company: "Company" = Relationship()

    def as_dict(self):
        return (
            super()
            .as_dict()
            .update(
                {
                    "user": self.user.as_dict(),
                    "currency": self.currency.as_dict(),
                }
            )
        )

    def __repr__(self) -> str:
        return f"Listing(id={self.id!r}, title={self.title!r})"
