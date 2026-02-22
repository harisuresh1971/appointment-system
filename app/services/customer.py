from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.customer import Customer


def get_customer_by_phone(db: Session, phone: str) -> Customer | None:
    return db.execute(select(Customer).where(Customer.phone == phone)).scalars().one_or_none()


def get_customer_by_id(db: Session, customer_id: int) -> Customer | None:
    return db.get(Customer, customer_id)


def list_customers(db: Session):
    return db.execute(select(Customer).order_by(Customer.name)).scalars().all()


def get_or_create_customer(db: Session, name: str, phone: str) -> Customer:
    existing = get_customer_by_phone(db, phone)
    if existing:
        return existing
    customer = Customer(name=name, phone=phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def create_customer(db: Session, name: str, phone: str) -> Customer:
    customer = Customer(name=name, phone=phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer: Customer, name: str | None, phone: str | None) -> Customer:
    if name is not None:
        customer.name = name
    if phone is not None:
        customer.phone = phone
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer: Customer) -> None:
    db.delete(customer)
    db.commit()
