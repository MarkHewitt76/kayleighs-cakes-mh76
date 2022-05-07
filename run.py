import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('kayleighs-cakes-mh76')


def main_user_interface():
    """
    A list of options presented to the user.\
    Number input (1-5) determines the action taken.
    """
    while True:
        print("What would you like to do?\n")
        print("1. View existing products")
        print("2. View potential new products")
        print("3. View most popular products\n   (based on customer survey)")
        print("4. Add products to 'new menu short list' worksheet")
        print("5. Exit the program\n")
        option = input("Enter your choice here (1-6):\n")

        if validate_input(option, 1, 6):
            print("Input valid!")
            print("Working...\n")
            break

    return option


def validate_input(value, range_start, range_stop):
    """
    Uses a try statement to raise an error if the user's
    input is not a number between 1 and 6.
    """
    try:
        if int(value) not in range(range_start, range_stop):
            raise ValueError(f"You entered {value}.")
    except ValueError as e:
        print(
            f"Invalid: {e}\nPlease enter {range_start} to {range_stop - 1}.\n"
            )
        return False

    return True


class Product:
    """
    Base class for individual products.
    """
    def __init__(self, name, cost_price):
        self.name = name
        self.cost_price = cost_price

    def details(self):
        """
        Method to return product details as a string.
        """
        return f"Product: {self.name}\n"\
            f"Cost Price: €{self.cost_price:.2f}\n"


class GrossProfitMixin:
    """
    Mixin to calculate GP
    """
    def _calculate_gp(self, cost_price, sale_price):
        """
        Method to return GP as an integer,
        rounded to 2 decimal places,
        if given cost_price and sale_price.
        """
        gp = round((sale_price - cost_price) / sale_price * 100, 2)
        return f"Current GP: {gp}%\n"


class RecPriceMixin:
    """
    Mixin to calculate recommended price.
    """
    def _calculate_rec_price(self, cost_price):
        """
        Mixin to calculate recommended sale price,
        based on Irish standard food GP of 65%,
        if given cost_price.
        """
        rec_price = round(cost_price / (1 - (65 / 100)), 2)
        return f"Recommended sale price: €{rec_price}\n"


class ExistingProduct(GrossProfitMixin, RecPriceMixin, Product):
    """
    Class for existing products, inheriting from Product
    superclass, RecPriceMixin and GrossProductMixin.
    """
    def __init__(self, name, cost_price, sale_price):
        self.sale_price = sale_price
        Product.__init__(self, name, cost_price)

    def get_details(self):
        """
        Method to return all product details as a string.
        Utilises details() method from Product superclass,
        as well as methods from GrossProductMixin and RecPriceMixin.
        """
        return Product.details(self) + \
            f"Sale Price: €{self.sale_price:.2f}\n" + \
            self._calculate_gp(self.cost_price, self.sale_price) + \
            self._calculate_rec_price(self.cost_price)


class NewProduct(RecPriceMixin, Product):
    """
    Class for new products, inheriting from Product
    class and RecPriceMixin
    """
    def __init__(self, name, cost_price):
        Product.__init__(self, name, cost_price)

    def get_details(self):
        """
        Method to return all product details as a string.
        Utilises details() method from Product superclass,
        as well as _calculate_rec_price() method from RecPriceMixin.
        """
        return Product.details(self) + \
            self._calculate_rec_price(self.cost_price)


def get_product_data(worksheet):
    """
    Gets all info from the requested worksheet,
    deletes the row of headings and returns the
    remaining data.
    """
    products = SHEET.worksheet(worksheet)
    product_data = products.get_all_values()
    del product_data[0]
    return product_data


def build_current_product_list(product_data):
    """
    Takes the spreadsheet data from the get_product_data()
    function and adds the data to the ExistingProduct class.
    Returns a list of class objects.
    """
    product_list = []
    for data in product_data:
        product_list.append(
            ExistingProduct(data[0], float(data[1]), float(data[2]))
            )

    return product_list


def build_new_product_list(product_data):
    """
    Takes the spreadsheet data from the get_product_data()
    function and adds the data to the NewProduct class.
    Returns a list of class objects.
    """
    product_list = []
    for data in product_data:
        product_list.append(
            NewProduct(data[0], float(data[1]))
            )

    return product_list


def show_products(product_list):
    """
    Takes the list of product objects and prints it to
    the terminal in a readable format.
    """
    for i in range(0, int(len(product_list))):
        print(product_list[i].get_details())


def get_customer_ratings():
    """
    Gets the customer survey data from Google sheets
    and returns a tuple containing data from each worksheet.
    """
    current_product_ratings = SHEET.worksheet("ratings current")
    current_ratings = []
    for ind in range(1, 6):
        ratings = current_product_ratings.col_values(ind)
        current_ratings.append(ratings)

    new_product_ratings = SHEET.worksheet("ratings new")
    new_ratings = []
    for ind in range(1, 7):
        ratings = new_product_ratings.col_values(ind)
        new_ratings.append(ratings)

    return current_ratings, new_ratings


def calculate_average_ratings(customer_ratings):
    """
    Calculates each product's average rating from the
    returned survey data and returns a tuple of dictionaries
    containing 'product: rating' pairs.
    """
    current_ratings, new_ratings = customer_ratings

    current_average_ratings = {}
    for product in current_ratings:
        int_list = [int(num) for num in product[1:]]
        average = round(sum(int_list) / len(int_list), 2)
        current_average_ratings[product[0]] = average

    new_average_ratings = {}
    for product in new_ratings:
        int_list = [int(num) for num in product[1:]]
        average = round(sum(int_list) / len(int_list), 2)
        new_average_ratings[product[0]] = average

    return current_average_ratings, new_average_ratings


def show_most_popular(average_ratings):
    """
    Unpacks the 'average ratings' tuple into its respective
    dictionaries, sorts them by their values and prints their
    key: value pairs to the console in descending order.
    I found the handy(ish) method for sorting the dictionaries
    here: https://stackabuse.com/how-to-sort-dictionary-by-value-in-python/
    """
    current_average_ratings, new_average_ratings = average_ratings

    sorted_current_averages = {}
    sorted_current_keys = sorted(
        current_average_ratings, key=current_average_ratings.get, reverse=True
        )
    for j in sorted_current_keys:
        sorted_current_averages[j] = current_average_ratings[j]

    sorted_new_averages = {}
    sorted_new_keys = sorted(
        new_average_ratings, key=new_average_ratings.get, reverse=True
        )
    for k in sorted_new_keys:
        sorted_new_averages[k] = new_average_ratings[k]

    print("Existing products: average ratings out of 5")
    print("-------------------------------------------\n")
    for key, value in sorted_current_averages.items():
        print(f"Product: {key}\nRating: {value}\n")

    input("Press Enter to continue\n")

    print("Potential new products: average ratings out of 5")
    print("------------------------------------------------\n")
    for key, value in sorted_new_averages.items():
        print(f"Product: {key}\nRating: {value}\n")


def main():
    """
    Run all program functions or exit the program,
    based on user input.
    """
    while True:
        user_option = (int(main_user_interface()))
        if user_option == 1:
            print("Current Products")
            print("----------------\n")
            existing_products = get_product_data("current products")
            current_product_list = build_current_product_list(
                                    existing_products)
            show_products(current_product_list)
            input("Press Enter to continue.\n")
        elif user_option == 2:
            print("Potential New Products")
            print("----------------------\n")
            new_products = get_product_data("new products")
            new_product_list = build_new_product_list(new_products)
            show_products(new_product_list)
            input("Press Enter to continue.\n")
        elif user_option == 3:
            customer_ratings = get_customer_ratings()
            average_ratings = calculate_average_ratings(customer_ratings)
            show_most_popular(average_ratings)
            input("Press Enter to continue\n")
        else:
            print("Exiting...\n")
            print("Goodbye!")
            exit()


print("Welcome to Kayleigh's Cakes product analysis!\n")
main()
