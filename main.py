# main.py
from sqlalchemy.orm import Session
from models import Restaurant, Customer, Review, session

def main():
    # Seed data for testing
    restaurant1 = Restaurant(name='Restaurant 1', price=3)
    customer1 = Customer(first_name='John', last_name='Doe')
    customer2 = Customer(first_name='Jane', last_name='Smith')

    review1 = Review(restaurant=restaurant1, customer=customer1, star_rating=4)
    review2 = Review(restaurant=restaurant1, customer=customer2, star_rating=5)

    session.add_all([restaurant1, customer1, customer2, review1, review2])
    session.commit()

    # Testing the methods
    print("Review 1 Customer:", review1.customer.full_name())  # Should print "John Doe"
    print("Review 1 Restaurant:", review1.restaurant.name)  # Should print "Restaurant 1"

    print("\nRestaurant 1 Reviews:")
    for review in restaurant1.reviews:
        print(review.full_review())

    print("\nRestaurant 1 Customers:")
    for customer in restaurant1.customers:
        print(customer.full_name())

    print("\nCustomer 1 Reviews:")
    for review in customer1.reviews:
        print(review.full_review())

    print("\nCustomer 1 Restaurants:")
    for restaurant in customer1.restaurants:
        print(restaurant.name)

if __name__ == "__main__":
    main()
