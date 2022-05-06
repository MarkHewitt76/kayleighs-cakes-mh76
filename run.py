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
    Number input (1-6) determines the action taken.
    """
    while True:
        print("What would you like to do?\n")
        print("1. View existing products")
        print("2. View potential new products")
        print("3. View all products")
        print("4. View most popular products\n   (based on customer survey)")
        print("5. Add products to 'new menu short list' worksheet")
        print("6. Exit the program\n")
        option = input("Enter your choice here (1-6):\n")

        if validate_input(option):
            print("Input valid!")
            print("Working...\n")
            break

    return option


def validate_input(value):
    """
    Uses a try statement to raise an error if the user's
    input is not a number between 1 and 6.
    """
    try:
        if int(value) not in range(1, 7):
            raise ValueError(f"You entered {value}.")
    except ValueError as e:
        print(f"Invalid entry: {e}\nPlease enter a number between 1 and 6.\n")
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


def get_products(worksheet):
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
    Takes the spreadsheet data from the get_products()
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
    Takes the spreadsheet data from the get_products()
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


def main():
    """
    Run all program functions.
    """
    user_option = int(main_user_interface())
    if user_option == 1:
        existing_products = get_products("current products")
        current_product_list = build_current_product_list(existing_products)
        show_products(current_product_list)
    elif user_option == 2:
        new_products = get_products("new products")
        new_product_list = build_new_product_list(new_products)
        show_products(new_product_list)


print("Welcome to Kayleigh's Cakes product analysis!\n")
main()
