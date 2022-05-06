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
    A list of options presented to the user. 
    Number input (1-6) determines the action taken.
    """
    print("What would you like to do?\n")
    print("1. View existing products")
    print("2. View potential new products")
    print("3. View all products")
    print("4. View most popular products\n   (based on customer survey)")
    # print("5. View most popular new products\n   (based on customer survey)")
    print("5. Add products to 'new menu short list' worksheet")
    print("6. Exit the program\n")
    
    option = input("Enter your choice here (1-6):\n")
    print(f"You selected {option}")


main_user_interface()

current_products = SHEET.worksheet("current products")
data = current_products.get_all_values()
print(data)
