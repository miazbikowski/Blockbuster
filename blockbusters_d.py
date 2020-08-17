from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('postgresql://postgres:password@server/filename')

engine.connect()

print(engine)

Base = declarative_base()

class Rental(Base):
	__tablename__= 'rentals'

	id = Column(Integer, primary_key=True)
	movie_id = Column(Integer, ForeignKey('movies.id')) 
	customer_id = Column(Integer, ForeignKey('customers.id')) 
	rental_date = Column(String)
	return_date = Column(String)

	#Create a relationship with the tables "customers" and "movies"
	movies = relationship("Movie") #tablename = relationship("Class")
	customers = relationship("Customer")

	def __repr__(self):
		return f'Rental {self.id} of the movie {self.movie_id}'

class Customer(Base):
	__tablename__ = 'customers'

	id = Column(Integer, primary_key=True)
	full_name = Column(String)
	first_name = Column(String)
	last_name = Column(String)
	creation_date = Column(String)
	
	#Adding a relationship between Rental and Customer class
	rental = relationship(Rental, backref="customer")

	def __repr__(self):
		return f'Customer {self.full_name}' #returns full name

class Movie(Base):
	__tablename__ = 'movies'

	id = Column(Integer, primary_key=True)
	title = Column(String)
	status = Column(String)
	creation_date = Column(String) 

	#Adding a relationship between Rental and Movie class
	rental = relationship(Rental, backref="movie")

	def __repr__(self):
		return f'Movie {self.title}' #returns title

"""Raise exception if tables are not created""" #I am not sure if its actually doing something
try:
	Base.metadata.create_all(engine)
	print("The tables have been created!")
except:
	raise "Tables were not created!"

# Base.metadata.create_all(engine)
# print("The tables have been created!")

class Store:
	"""This class contain all the methods surrounding our movie rental store"""
	global engine 
	def __init__(self, engine):
		"""Initialize our store."""
		Session = sessionmaker(bind=engine)
		self.session = Session()
		self.engine = engine

		print("The store is open!")

	def add_movie(self, title): 
		"""Add new titles to our movie inventory."""

		#Create entries in the "movies" table
		creation_date = datetime.date.today().strftime('%d/%m/%Y')
		movie = Movie(title=title, status="available", creation_date=creation_date) 

		#Add and commit changes to database
		self.session.add(movie)
		self.session.commit()

		print(f"The movie '{movie.title}' was added!")

	def delete_movie(self, movie_id): 
		"""Remove broken, lost or stolen movies from our inventory by their id."""

		#Query the "movies" table by movie_id
		movie = self.session.query(Movie).filter_by(id=movie_id).scalar()

		#Check if we own this movie / If the query returns none:
		if movie == None:
			print(f"There is no movie with the id #{movie_id}!")
			return

		#Add and commit changes to database
		self.session.delete(movie) 
		self.session.commit()

		print(f"The movie '{movie.title}' with the ID #{movie.id} was deleted!")

	def add_customer(self, first_name, last_name):
		"""Add new customer in our customer list using their first and last name."""

		#Create entries in the "customers" table
		creation_date = datetime.date.today().strftime('%d/%m/%Y')
		customer = Customer(first_name=first_name, last_name=last_name, creation_date=creation_date, full_name = first_name + " " + last_name)

		#Add and commit changes to database
		self.session.add(customer)
		self.session.commit()

		print(f"The customer '{customer.full_name}' was added!")

	def delete_customer(self, customer_id):
		"""Remove customer from our customer list by their id."""

		#Query the "customers" table by customer_id
		customer = self.session.query(Customer).filter_by(id = customer_id).one()

		#Check if the customer is in our database / If query returns none:
		if customer == None:
			print(f"There is no customer with the id #{customer_id}!")
			return

		#Add and commit changes to database
		self.session.delete(customer) 
		self.session.commit()

		print(f"The customer '{customer.full_name}' with ID #{customer.id} was deleted!")	

	def view_movie(self, movie_id):
		"""Locate a specific movie with the given id."""

		#Query the "movies" table by movie_id
		movie = self.session.query(Movie).filter(Movie.id == movie_id).scalar()

		#Check if we own this movie / If the query returns none:
		if movie == None:
			print(f"There is no movie with the id #{movie_id}!")
			return

		print("~"*20)
		print(f"Title: {movie.title} \nID: {movie.id} \nStatus: {movie.status}")
		print("~"*20) 

	def view_customer(self, customer_id):
		"""Locate a specific customer with the given id."""

		#Query the "customers" table by customer_id
		customer = self.session.query(Customer).filter(Customer.id == customer_id).scalar()

		#Check if the customer is in our database / If query returns none:
		if customer == None:
			print(f"There is no customer with the id #{customer_id}!")
			return

		print("*"*20)
		print(f"Full name: {customer.full_name} \nFirst name: {customer.first_name} \nLast name: {customer.last_name} \nID: {customer.id}")
		print("*"*20) 

	def search_movie(self, title): 
		"""Find all movies that match the given letter.s, word.s or full title."""

		#Query the "movies" table by title
		all_results = self.session.query(Movie).filter(Movie.title.ilike('%'+title+'%')).all()

		#Check if we have that movie title:
		if all_results == []:
		 	print(f"***There is no movie containing '{title}'! Try again!***")
			#print("This is an empty list")
		 	return

		#Access each element of the instance all_results
		for movie in all_results:

			#Return the list of movies that correspond to the search
			print("~"*20)
			print(f"Title: {movie.title} \nID: {movie.id} \nStatus: {movie.status}")
			print("~"*20)

	def search_customer(self, name):
		"""Find all customers that match the given letter.s, first name, last name or full name."""

		#Query the "customers" table by full_name
		all_results = self.session.query(Customer).filter(Customer.full_name.ilike('%'+name+'%')).all()

		#Check if we have that customer's name in our database:
		if all_results == []:
		 	print(f"***There is no customer name containing '{name}'! Try again!***")
		 	return

		#Access each element of the instance all_results
		for customer in all_results:
			print("*"*20)
			print(f"Full name: {customer.full_name} \nFirst name: {customer.first_name} \nLast name: {customer.last_name} \nID: {customer.id}")
			print("*"*20)			

	def rent_movie(self, customer_id, movie_id):
		"""Lets you rent a movie by it's id and a customer id."""
		rental_date = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S') #rental_date and return_date dont use the same format... --> the difference it that the return date is an update on an entry

		#Query the "customers" table by customer_id
		customer = self.session.query(Customer).filter(Customer.id == customer_id).scalar()

		#Check if the customer is in our database / If query returns none:
		if customer == None:
			print(f"This customer ID doesn't exist in our database.  Please check again!")
			return

		#Query the "movies" table by movie_id
		movie = self.session.query(Movie).filter(Movie.id == movie_id).scalar()

		#Check if we own this movie / If the query returns none:
		if movie == None:
			print(f"We don't own this movie!")
			return

		#Check the movie status, if available, rent the movie
		if movie.status == 'available':
			rental = Rental(customers=customer, movies=movie, rental_date=rental_date, return_date=None)

			#Update the movie status in the movie table
			movie.status = "non-available"

			#Add and commit all changes to database
			self.session.add_all([customer, movie, rental])
			self.session.commit() 

			print(f"{customer.full_name} rented {movie.title} on {rental.rental_date}!")

		else:
			print(f"{movie.title} is {movie.status}!")

	def return_movie(self, customer_id, movie_id):
		"""Lets you return a movie by it's id, changes the movie's status to available
		and add a return_date to the rentals' table"""

		#Query the "movies" table by movie_id
		movie = self.session.query(Movie).filter(Movie.id == movie_id).scalar()

		#Check if this movie is ours / If the query returns none:
		if movie == None:
			print(f"We don't own this movie!")
			return

		#Update the movie's status in the movie table as "available" if it was rented
		if movie.status == 'non-available':
			movie.status = "available"

			#Query the "customers" table by customer_id
			customer = self.session.query(Customer).filter(Customer.id == customer_id).scalar()

			#If the query returns none (with .scalar()):
			if customer == None:
				print(f"There is no customer with the id #{customer_id}!")
				return

			#Query the "rentals" table by movie_id, customer_id and empty return_date
			rental = self.session.query(Rental).filter(Rental.movie_id == movie_id, Rental.customer_id == customer_id, Rental.return_date == None).scalar()

			#If the query returns none:
			if rental == None:
				print(f"There is no rental to return for that movie '{movie.title}' for this customer {customer.full_name}!")
				return

			#Else: Update the return date in the rentals table
			rental.return_date = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S') 

			#Add and commit all changes
			self.session.add_all([movie, rental]) 
			self.session.commit()

			print(f"{movie.title} is now {movie.status} for rental!") 
			print(f"{movie.title} was returned on {rental.return_date} by {customer.full_name}!")
		
		else:
			print(f"The movie '{movie.title}' with id #{movie.id} wasn't rented.")

store = Store(engine) 


"""
REFERENCES
How to query: https://hackersandslackers.com/database-queries-sqlalchemy-orm/
SQLAlchemy tutorial: https://leportella.com/sqlalchemy-tutorial.html?fbclid=IwAR16Ea82TcZLRzNn1AMtD8yjdsKtKRqO9rN0mqijctxmNV0GmK03185zhok
More on querying: https://docs.sqlalchemy.org/en/13/orm/query.html
"""