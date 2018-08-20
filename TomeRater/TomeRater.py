
class User:

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}
        self.valid_ratings = []

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print('Email has been updated to {email}'.format(email = self.email))

    def __repr__(self):
        return "User: " + self.name + ", E-Mail: " + self.email + ", books read: " + str(len(self.books))

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

#rating=None is "false" as long as no parameter is given, else it returns the parameter
    def read_books(self, book, rating = None):
        self.books[book] = rating
        if rating is not None:
            self.valid_ratings.append(rating)

#copied from solutions, still having problems while error testing...
    def get_average_rating(self):
        average = 0
        rated_books = 0
        for value in self.books.values():
            if value:
                average += value
                rated_books += 1
        average = average / rated_books
        return average

class Book:

    def __init__(self, title, isbn, price):
        self.title = str(title)
        self.isbn = int(isbn)
        self.ratings = []
        self.price = int(price)

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print('\nISBN of {title} has been changed to {isbn}'.format(isbn=self.isbn, title=self.title))

    #making sure rating exists and that it is within the allowed range
    def add_rating(self, rating):
        if self.valid_rating(rating):
            self.ratings.append(rating)
        else:
            print("Invalid Rating...")

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

#for loop through self.ratings that returns the average of all ratings for self, if > 0 to prevent ZeroDivisonError
    #switched to solution one due to AttributeError
    #AttributeError still occurs sometimes...
    def get_average_rating(self):
        average = 0
        for rating in self.ratings:
            average += rating
        average = average/len(self.ratings)
        return average


    def valid_rating(self, rating):
        if rating is not None:
            if 0 <= rating <= 4:
                return True
        return False

    def __hash__(self):
        return hash((self.title, self.isbn))

#__repr__ to print books that are neither fiction nor non-fiction, prevents print of memory location
    def __repr__(self):
        return '\n{title}, average rating of: {rating:.1f}'.format(title=self.title, rating=self.get_average_rating())

class Fiction(Book):

    def __init__(self, title, author, isbn, price):
        # inherit title and isbn from Book
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author} has an average rating of {rating}".format(title = self.title, author = self.author, rating = self.get_average_rating())

#print(Fiction("Alice in Wonderland", "Lewis Carroll", 1234234))



class Non_Fiction(Book):

    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject} has an average rating of {rating}".format(title = self.title, level = self.level, subject = self.subject, rating = self.get_average_rating())

#print(Non_Fiction("Society of Mind", "Artificial Intelligence", "beginner", 34523))



class TomeRater:

    def __init__(self):
        self.users = {}
        self.books = {}
        self.books_price = {}

    def create_book(self, title, isbn, price=None):
        if self.check_isbn(isbn):
            new_book = Book(title, isbn, price)
            if self.check_price(price):
                self.books_price[title] = price
        return new_book

    def create_novel(self, title, author, isbn, price=None):
        if self.check_isbn(isbn):
            new_novel = Fiction(title, author, isbn, price)
            if self.check_price(price):
                self.books_price[title] = price
        return new_novel

    def create_non_fiction(self, title, subject, level, isbn, price=None):
        if self.check_isbn(isbn):
            new_non_fiction = Non_Fiction(title, subject, level, isbn, price)
            if self.check_price(price):
                self.books_price[title] = price
        return new_non_fiction


#tricky, self.books[book} = 1?
    def add_book_to_user(self, book, email, rating=None):
        if self.check_user(email):
            self.users[email].read_books(book, rating)
            book.add_rating(rating)
            if self.check_book(book):
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print('No user with email {email}.'.format(email = email))

#creates a new user to the dict users and adds books to the user in the dic
    def add_user(self, name, email, user_books=None):
        if self.check_user(email):
            print('This User already exists')
        else:
            if self.validate_email(email):
                self.users[email] = User(name, email)
                if user_books is not None:
                    for book in user_books:
                        self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users:
            print(self.users[user])

    def print_price_catalog(self):
        for title in self.books_price:
            print('{title} has a price of {price}'.format(title = title, price = self.books_price[title]))

#simple counter method to search for highest reading counter in self.books dict
    def get_most_read_book(self):
        for book in self.books:
            if self.books[book] == max(self.books.values()):
                return book

#for loop searching for highest averaged rating in self.books using get_average_rating in Book
    def highest_rated_book(self):
        highest_rating = float("-inf")
        best_book = None
        for book in self.books:
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
                best_book = book
        return best_book

#for loop through average rating in User
    def most_positive_user(self):
        highest_rating = float("-inf")
        result_user = None
        for key in self.users:
            if self.users[key].get_average_rating() > highest_rating:
                highest_rating = self.users[key].get_average_rating()
                result_user = self.users[key]
        return result_user

#for loop through list containing the key="times the book has been read" from self.books; sorted in reverse, starting with the highest
    def list_most_most_read(self, number):
        most_read_books = sorted(self.books, key=self.books.get, reverse=True)
        for book in range(number):
            print(most_read_books[book])

#for loop through list containing the key="bookprice" from self.books_price; sorted in reverse, starting with the highest
    def list_most_expensive(self, number):
        most_expensive_books = sorted(self.books_price, key=self.books_price.get, reverse=True)
        for price in range(number):
            print(most_expensive_books[price])

#check for user
    def check_user(self, email):
        if email in self.users:
            return True
        else:
            return False

    def check_book(self, book):
        if book in self.books:
            return True
        else:
            return False

#makes sure price is given
    def check_price(self, price):
        if price is not None:
            return True
        else:
            return False

#makes sure isbn does not already exist
    def check_isbn(self, isbn):
        for book in self.books:
            if isbn == book.isbn:
                print('ISBN is already taken.')
                return False
        return True

#tricky email check, couldn't get it to work properly
#would have imported regex for proper validation, not sure if it works on github
    def validate_email(self, email):
        valid_ending = ['.com', '.edu', '.org']
        if ('@' in email) and (valid_ending in email):
            return True
        print('Invalid Email.')
        return False

