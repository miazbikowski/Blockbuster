from blockbusters import Customer, Movie, Rental, Store, store, engine
import sys

class Menu:
    """Display a menu and interact with the options in the dictionary when ran."""
    
    def __init__(self):
        """Initialize the menu"""
        self.store = Store(engine) 
        self.options = {
            "0": self.exit, 
            "1": self.search_movie,
            "2": self.view_movie, 
            "3": self.rent_movie,
            "4": self.return_movie,
            "5": self.add_movie,
            "6": self.delete_movie,
            "7": self.search_customer,
            "8": self.view_customer,
            "9": self.add_customer,
            "10": self.delete_customer            
        }

    def display_menu(self):
        """Display the menu."""
        print(
    
    """
    MENU

    1. Search movie
    2. View movie
    3. Rent a movie
    4. Return a movie
    5. Add a movie
    6. Delete a movie
    7. Search customer
    8. View customer
    9. Add a customer
    10. Delete a customer

    ***TO EXIT THE MENU PRESS 0***
    """
        )

    def run(self):
        """Display the menu and respond to choices."""
        while True:
            self.display_menu()
            option = input("Enter an option: ")
            action = self.options.get(option)
            if action:
                action()
                action = None
            else:
                print("Please, try again! {0} is not a valid option".format(option))

    #Option 1: Search a movie 
    def search_movie(self):
        """Search movies by title and returns the info about that movies and or the number of copies available."""
        title = input("Search for movie title: ")
        movies = self.store.search_movie(title) 
        return movies

    #Option 2: View movie
    def view_movie(self):
        """Search movie by id and returns the info about that specific movie."""
        movie_id = input("Movie's id: ")
        movie = self.store.view_movie(movie_id)
        return movie

    #Option 3 : Rent a movie
    def rent_movie(self):
        """Rent a movie using the customer's and the movie's ids."""
        customer_id = input("Customer's id: ")
        movie_id = input("Movie's id: ")
        rental = self.store.rent_movie(customer_id, movie_id) 
        return rental

    #Option 4: Return a movie
    def return_movie(self):
        """Return a movie rental using the customer's id and the movie's id."""
        customer_id = input("Customer's id: ")
        movie_id = input("Movie's id: ")
        rental = self.store.return_movie(customer_id, movie_id) 
        return rental

    #Option 5: Add a movie
    def add_movie(self):
        """Add a new movie to our inventory."""
        title = input("Movie's title: ")
        movie = self.store.add_movie(title) 
        return movie

    #Option 6: Delete a movie
    def delete_movie(self):
        """Delete a movie using it's id."""
        movie_id = input("Movie's id: ")
        movie = self.store.delete_movie(movie_id) 
        return movie

    #Option 7: Search a customer
    def search_customer(self):  
        """Search a customer by their name and returns the info about them or a list of customers alike."""
        name = input("Search for customer's name: ")
        customer = self.store.search_customer(name) 
        return customer

    #Option 8: View customer
    def view_customer(self):
        """Search customer by id and returns the info about that specific customer."""
        customer_id = input("Customer's id: ")
        customer = self.store.view_customer(customer_id)
        return customer

    #Option 9: Add a customer
    def add_customer(self):
        """Add a new customer by asking for it's first and last names."""
        first = input("Customer's first name: ")
        last = input("Customer's last name: ")
        customer = self.store.add_customer(first, last) 
        return customer

    #Option 10: Delete a customer
    def delete_customer(self):
        """Delete a customer using it's id."""
        customer_id = input("Customer's id: ")
        customer = self.store.delete_customer(customer_id) 
        return customer
    
    #Option 0: Exit the menu
    def exit(self):
        """Lets you exit the main menu."""
        print("Goodbye! See you soon!")
        sys.exit()

if __name__ == "__main__":
    Menu().run()


# """
# REFERENCES:
   
#    https://stackoverflow.com/questions/19964603/creating-a-menu-in-python

# """