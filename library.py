import time
import threading
import sys

# User object
user = {
    "id": "",
    "name": "",
    "phone": "",
    "username": "",
    "password": "",
    "registered": False,
    "is_admin": False,
}

current_user = {
    "id": "",
    "name": "",
    "phone": "",
    "username": "",
    "password": "",
    "registered": False,
    "is_admin": False,
}

users = [
    {
        "id": 1,
        "name": "administrator",
        "phone": "0000000000",
        "username": "admin",
        "password": "admin",
        "registered": True,
        "is_admin": True,
    },
]

book = {
    "id": "",
    "title": "",
    "author": "",
    "available": True,
    "is_requested": False,
    "requested_by": "",
    "loaned": False,
    "loaned_to": "",
    "period": 0,
    "start_time": "",
    "end_time": 0,
    "remaining_time": 0,
    "reviews": [],
    "countdown_thread": "",
}


books = [
    {
        "id": 1,
        "title": "The Little Prince",
        "author": "Antoine de Saint-Exupéry",
        "available": True,
        "is_requested": False,
        "requested_by": "",
        "loaned": False,
        "loaned_to": "",
        "period": 0,
        "start_time": "",
        "end_time": 0,
        "remaining_time": 0,
        "reviews": [],
        "countdown_thread": "",
    },
    {
        "id": 2,
        "title": "Hunger Games",
        "author": "Suzanne Collins",
        "available": True,
        "is_requested": False,
        "requested_by": "",
        "loaned": False,
        "loaned_to": "",
        "period": 0,
        "start_time": "",
        "end_time": 0,
        "remaining_time": 0,
        "reviews": [],
        "countdown_thread": "",
    },
    {
        "id": 3,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "available": False,
        "is_requested": False,
        "requested_by": "",
        "loaned": True,
        "loaned_to": "admin",
        "period": 0,
        "start_time": "",
        "end_time": 0,
        "remaining_time": 0,
        "reviews": [],
        "countdown_thread": "",
    },
]

review = {
    "id": "",
    "book_id": "",
    "username": "",
    "rating": "",
    "comment": "",
    "created_at": "",
}


library = {
    "name": "Central Library",
    "users": users,
    "books": books,
    "suggested_books": [],
    "requested_books": [],
    "loaned_books": [],
}


# Utility functions
def clear_console():
    print("\033c", end="")


# calculate the elapsed time
def calculate_elapsed_time(start_time):
    current_time = time.time()
    elapsed_time_seconds = current_time - start_time

    hours = int(elapsed_time_seconds // 3600)
    minutes = int((elapsed_time_seconds % 3600) // 60)
    seconds = int(elapsed_time_seconds % 60)

    return hours, minutes, seconds


# show the elapsed time
def show_elapsed_time(start_time):
    hours, minutes, seconds = calculate_elapsed_time(start_time)
    print(f"Time spent: {hours} hours, {minutes} minutes, {seconds} seconds")


# calculate the remaining time
def calculate_remaining_time(start_time, period_days):
    current_time = time.time()
    elapsed_time_seconds = current_time - start_time
    remaining_time_seconds = period_days * 24 * 3600 - elapsed_time_seconds

    if remaining_time_seconds < 0:
        return 0, 0, 0

    remaining_hours = int(remaining_time_seconds // 3600)
    remaining_minutes = int((remaining_time_seconds % 3600) // 60)
    remaining_seconds = int(remaining_time_seconds % 60)

    return remaining_hours, remaining_minutes, remaining_seconds


# show the remaining time
def show_remaining_time(start_time, period_days):
    remaining_hours, remaining_minutes, remaining_seconds = calculate_remaining_time(
        start_time, period_days
    )
    print(
        f"Time remaining: {remaining_hours} hours, {remaining_minutes} minutes, {remaining_seconds} seconds"
    )


def period_done():
    print("The booked period is done. Notification sent!")
    return True


def period_countdown(book, notify_function, end_time):
    while time.time() < end_time:
        time.sleep(1)
    notify_function()


def create_thread_for_period_countdown(book, end_time):
    countdown_thread = threading.Thread(
        target=period_countdown, args=(book, period_done, end_time)
    )
    countdown_thread.start()


def start_countdown(book, period):
    book["start_time"] = time.time()
    end_time = book["end_time"] = book["start_time"] + int(period) * 24 * 3600
    show_remaining_time(book["start_time"], int(period))
    create_thread_for_period_countdown(book, end_time)


def stop_countdown(book):
    if "countdown_thread" in book and isinstance(
        book["countdown_thread"], threading.Thread
    ):
        countdown_thread = book["countdown_thread"]
        countdown_thread.join()
    book["start_time"] = ""
    book["end_time"] = 0
    book["remaining_time"] = 0
    del book["countdown_thread"]


# Books functions
def print_books():
    for book in books:
        print_book(book)


def show_book_loaned_to(book):
    print("Loaned to: " + book["loaned_to"])


def is_book_loaned(book):
    return book["loaned"]


def is_book_available(book):
    if book["available"]:
        print("Available")
    elif is_book_loaned(book):
        show_book_loaned_to(book)
    else:
        print("Not available")


def print_book(book):
    print("Title: " + book["title"])
    print("Author: " + book["author"])
    print("Available: " + is_available(book))
    reviews = [str(review) for review in book["reviews"]]
    print("Reviews: " + ", ".join(reviews))


def is_available(book):
    if book["available"]:
        return "Available"
    else:
        return "Not available"


# search books
def search_book_by_author(author):
    for book in books:
        if book["author"] == author:
            print_book(book)
            return True
    return False


def search_book_by_title(title):
    for book in books:
        if book["title"] == title:
            print_book(book)
            return True
    return False


# available books
def show_available_books():
    for book in books:
        if book["available"]:
            print_book(book)


def is_book_available_by_id(id):
    for book in books:
        if book["id"] == id:
            return book["available"]
    return False


def is_book_available_by_title(title):
    for book in books:
        if book["title"] == title:
            return book["available"]
    return False


# loan a book
def loan_book():
    loan_book_menu()


def loan_book_by_title(title, period):
    if is_book_available_by_title(title):
        book = get_book_by_title(title)
        user = get_current_user()
        book_loaned(book, user, period)
    else:
        print("Book not available")


def get_book_by_id(id):
    for book in books:
        if book["id"] == id:
            return book
    return False


def get_book_by_title(title):
    for book in books:
        if book["title"] == title:
            return book
    return False


def book_loaned(book, user, period):
    book["available"] = False
    book["loaned_to"] = user["username"]
    book["period"] = period
    add_book_to_loan_list(book)
    start_countdown(book, period)
    show_loaned_books()
    return book


def add_book_to_loan_list(book):
    library["loaned_books"].append(book)


def get_loaned_books():
    return library["loaned_books"]


def show_loaned_books():
    print("Loaned books")
    for book in library["loaned_books"]:
        print_book(book)
        print("Loaned to: " + book["loaned_to"])


def show_loaned_period(book):
    print("Loan period: " + book["period"])


def show_loan_period():
    print("available periods: 7, 14, 21 in days")


def get_loan_period():
    period = input("Enter the period in days: ")
    return period


# return a book
def return_book():
    user = get_current_user()

    title = input("Enter the title of the book you want to return: ")
    book = get_book_by_title(title)
    for book in get_loaned_books():
        if book["loaned_to"] == user["username"]:
            book_returned(book)
            stop_countdown(book)
            remove_book_from_loan_list(book)
            break
    for book in get_requested_books():
        if book["requested_by"] == user["username"]:
            book_returned(book)
            remove_book_from_request_list(book)
            break
    clear_console()


def book_returned(book):
    book["available"] = True
    book["loaned"] = False
    book["loaned_to"] = ""
    book["is_requested"] = False
    book["requested_by"] = ""
    book["period"] = 0
    book["start_time"] = ""
    book["end_time"] = 0
    book["remaining_time"] = 0
    show_available_books()
    return book


def remove_book_from_loan_list(book):
    if book in library["loaned_books"]:
        library["loaned_books"].remove(book)
    else:
        print("Book not found")


def show_books_loaned_by_user(user):
    for book in get_loaned_books():
        if book["loaned_to"] == user["username"]:
            print_book(book)


# review a book
def review_book():
    title = input("Review a book by title: ")
    book = get_book_by_title(title)
    book["reviews"].append(create_review(book))


def create_review(book):
    review["id"] = len(book["reviews"]) + 1
    review["book_id"] = book["id"]
    review["username"] = get_current_user()["username"]
    review["rating"] = input("Enter the rating from 1 to 5 stars: ")
    review["comment"] = input("Enter the comment: ")
    review["created_at"] = time.time()
    return review


def show_reviews(book):
    for review in book["reviews"]:
        print(review)


# request a book
def book_request(title):
    if is_book_available_by_title(title):
        book = get_book_by_title(title)
        user = get_current_user()
        book_requested(book, user)
    else:
        print("Book not available")


def is_book_requested(book):
    return book["is_requested"]


def set_book_requested_by(book, user):
    book["is_requested"] = True
    book["requested_by"] = user["username"]
    book["available"] = False
    return book


def book_requested(book, user):
    set_book_requested_by(book, user)
    add_book_to_request_list(book)
    show_requested_books()
    return book


def add_book_to_request_list(book):
    library["requested_books"].append(book)


def remove_book_from_request_list(book):
    if book in library["requested_books"]:
        library["requested_books"].remove(book)
    else:
        print("Book not found")


def get_requested_books():
    return library["requested_books"]


def show_requested_books():
    print("Requested books")
    for book in library["requested_books"]:
        print_book(book)
        print("Requested by: " + book["requested_by"])


# renew a book
def renew_book():
    title = input("Renew a book by title: ")
    book = get_book_by_title(title)
    if is_book_requested(book):
        print("The book is requested")
    else:
        show_loaned_books()
        book_renewed(book)


def book_renewed(book):
    period = input("Enter the period in days 7, 14, 21: ")
    book["period"] = period
    start_countdown(book, book["period"])
    show_loaned_books()
    return book


# add a book
def add_book():
    if is_admin():
        title = input("Enter the title: ")
        author = input("Enter the author: ")
        book = create_new_book(title, author)
        add_book_to_list(books, book)
        print_book(book)


def create_new_book(title, author):
    return {
        "id": create_id(),
        "title": title,
        "author": author,
        "available": True,
        "is_requested": False,
        "requested_by": "",
        "loaned": False,
        "loaned_to": "",
        "period": 0,
        "start_time": "",
        "end_time": 0,
        "remaining_time": 0,
        "reviews": [],
        "countdown_thread": "",
    }


def add_book_to_list(books, book):
    books.append(book)
    return book


# remove a book
def remove_book():
    if is_admin():
        title = input("Enter the title: ")
        book = get_book_by_title(title)
        remove_book_from_list(books, book)
        print("Book removed")


def remove_book_from_list(books, book):
    if book in books:
        books.remove(book)
    else:
        print("Book not found")


# suggest a book
def suggest_book():
    title = input("Enter the title: ")
    author = input("Enter the author: ")
    book = create_new_book(title, author)
    add_book_to_suggested_list(book)
    print_book(book)


def add_book_to_suggested_list(book):
    library["suggested_books"].append(book)


def show_suggested_books():
    print("Suggested books")
    for book in library["suggested_books"]:
        print_book(book)


def get_suggested_books():
    return library["suggested_books"]


# User functions
def print_user():
    print(user)
    print("\n")


def set_current_user(user):
    for key in user:
        current_user[key] = user[key]


def get_current_user():
    return current_user


def get_user_by_username(username):
    for u in users:
        if u["username"] == username:
            return u
    return False


def is_admin():
    if get_current_user()["is_admin"]:
        return True
    else:
        return False


def create_id():
    return len(users) + 1


def create_new_user(name, phone, username, password, is_admin):
    return {
        "id": create_id(),
        "name": name,
        "phone": phone,
        "username": username,
        "password": password,
        "registered": True,
        "is_admin": is_admin,
    }


def add_user_to_list(users, name, phone, username, password, is_admin):
    new_user = create_new_user(name, phone, username, password, is_admin)
    users.append(new_user)
    return new_user


def register():
    create_username()
    create_password()
    set_current_user(
        add_user_to_list(
            users,
            user["name"],
            user["phone"],
            user["username"],
            user["password"],
            user["is_admin"],
        )
    )
    print(get_current_user())


def create_username():
    print("What is your name?")
    name = input()
    user["name"] = name
    clear_console()

    print("What is your phone number?")
    phone = input()
    user["phone"] = phone
    clear_console()

    print("Insert a username")
    username = input()
    user["username"] = username
    clear_console()


def is_user_registered(user):
    for u in users:
        if u["username"] == user:
            return True
    return False


def passwords_are_equals(password, password2):
    return password == password2


def create_password():
    try:
        print("Insert a password")
        password = input()
        clear_console()
        print("Insert the password again")
        password2 = input()
        clear_console()
        if not passwords_are_equals(password, password2):
            print("Passwords do not match")
        else:
            user["password"] = password
            clear_console()
            print("Passwords match")
    except:
        print("Might be a problem with the password")


def login_validation(username, password):
    for u in users:
        if u["username"] == username and u["password"] == password:
            return True
    return False


def is_login():
    username = input("Insert your username: ")
    clear_console()

    print("Insert your password")
    password = input()
    clear_console()

    if login_validation(username, password):
        set_current_user(get_user_by_username(username))
        print("Welcome to the library")
        return True
    else:
        print("Invalid credentials")
        return False


# library menu
def show_menu():
    print("[Welcome to the library]")
    print("1. Register as an user")
    print("2. Login as an user")
    print("0. Exit")


# login menu
def show_login_menu():
    print("[Logged as " + get_current_user()["username"] + "]")
    print("1. Search books")
    print("2. Request a book")
    print("3. Loan a book")
    print("4. Renew a book")
    print("5. Return a book")
    print("6. Review a book")
    print("7. Suggest a book")
    if is_admin():
        print("8. Add a book")
        print("9. Remove a book")
    print("0. Logout")


# login menu
def login():
    while True:
        show_login_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            clear_console()
            search_book()
        elif choice == "2":
            clear_console()
            request_book()
        elif choice == "3":
            clear_console()
            loan_book()
        elif choice == "4":
            clear_console()
            renew_book()
        elif choice == "5":
            clear_console()
            return_book()
        elif choice == "6":
            clear_console()
            review_book()
        elif choice == "7":
            clear_console()
            suggest_book()
        elif choice == "8":
            clear_console()
            add_book()
        elif choice == "9":
            clear_console()
            remove_book()
        elif choice == "0":
            clear_console()
            print("Goodbye :)")
            break
        else:
            print("Invalid choice. Try again.")


# loan book menu
def loan_book_menu():
    while True:
        print("Available books")
        show_available_books()
        title = input("Loan a book by title: ")
        clear_console()

        show_loan_period()
        period = get_loan_period()
        loan_book_by_title(title, period)
        break


# book request menu
def request_book():
    while True:
        print("Available books")
        show_available_books()
        title = input("Enter the title: ")
        if is_book_available_by_title(title):
            book_request(title)
            clear_console()
            break
        else:
            print("The book is not available.")


# search book menu
def search_book():
    while True:
        choice = input(
            "1. Search by title\n"
            "2. Search by author\n"
            "3. Search books requested\n"
            "4. Search books loaned\n"
            "5. Search suggested books\n"
            "6. Search all available books\n"
            "7. Search all books\n"
            "Enter your choice: "
        )
        if choice == "1":
            title = input("Enter the title: ")
            clear_console()
            search_book_by_title(title)
            break
        elif choice == "2":
            author = input("Enter the author: ")
            clear_console()
            search_book_by_author(author)

            break
        elif choice == "3":
            clear_console()
            show_requested_books()
            break
        elif choice == "4":
            clear_console()
            show_loaned_books()
            break
        elif choice == "5":
            clear_console()
            show_suggested_books()
            break
        elif choice == "6":
            clear_console()
            show_available_books()
            break
        elif choice == "7":
            clear_console()
            print_books()
            break
        else:
            print("Invalid choice. Try again.")


# main menu
def menu():
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            register()
        elif choice == "2":
            if is_login():
                clear_console()
                login()
        elif choice == "0":
            print("Goodbye :)")
            sys.exit()
        else:
            print("Invalid choice. Try again.")


def main():
    menu()


if __name__ == "__main__":
    main()
