# models.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

restaurant_customer_association = Table(
    'restaurant_customer_association',
    Base.metadata,
    Column('restaurant_id', Integer, ForeignKey('restaurants.id')),
    Column('customer_id', Integer, ForeignKey('customers.id'))
)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    reviews = relationship('Review', back_populates='restaurant', cascade='all, delete-orphan')
    customers = relationship('Customer', secondary=restaurant_customer_association, back_populates='restaurants')

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    restaurants = relationship('Restaurant', secondary=restaurant_customer_association, back_populates='customers')

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def favorite_restaurant(self):
        return session.query(Restaurant).join(Review).filter(Review.customer == self).order_by(Review.star_rating.desc()).first()

    def add_review(self, restaurant, rating):
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        session.query(Review).filter(Review.customer == self, Review.restaurant == restaurant).delete()
        session.commit()

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

# Create an SQLite in-memory database for testing purposes
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
