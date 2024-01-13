# seeds.py
from sqlalchemy.orm import Session
from models import Restaurant, Customer, Review
from database import SessionLocal, init_db

def seed_data():
    session = SessionLocal()

    # Your seed data goes here
    restaurant1 = Restaurant(name='Restaurant 1', price=3)
    customer1 = Customer(first_name='John', last_name='Doe')
    customer2 = Customer(first_name='Jane', last_name='Smith')

    session.add_all([restaurant1, customer1, customer2])
    session.commit()

if __name__ == "__main__":
    init_db()
    seed_data()
