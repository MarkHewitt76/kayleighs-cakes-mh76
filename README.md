# Kayleigh's Cakes
## A product analysis and menu selection app

Kayleigh's Cakes is a cottage-industry bakery, run in her spare time by a young lady with a passion for baking. Unti recently, Kayleigh has only had a limited menu, with 5 staple items and occasional special orders. With a view to expanding her menu somewhat, she recently conducted a survey of 20 of her most loyal customers, asking them to give a rating out of 5 for both her existing products and those that she's thinking of adding as staple items to her menu.

The purpose of this app is to aid in analysing that survey data by calculating average ratings for each product and sorting them, as well as calculating gross profit margins and recommended pricing for all of the on the menu.

The live version is [here](https://kayleighs-cakes-mh76.herokuapp.com/).

![Screens screenshot](/assets/images/kayleighscakes-responsive.PNG "Screens")

The app is linked to a Google sheets spreadsheet via the Google Sheets and Google Drive APIs and the program utilises the gspread module to handle reading from and writing to the sheet. The program also makes use of the Credentails method of the google-auth module for verification.

The spreadsheet contains all of the data concerning the products and survey results that this program works with and is publicly available to view [here](https://docs.google.com/spreadsheets/d/1LjJeiQbcFzddDmmNEZKWNh8Nm9FZOlTwlCPURNaS_PQ/edit?usp=sharing)

![Sheet screenshot](/assets/images/kayleighscakes-sheet-ratings.PNG)

## Features

### Existing Features

- #### Menu

    A looping menu of 5 items

    - View existing products

    - View potential new products

    - View most popular products

    - Add product to 'new menu short list' worksheet

    - Exit the program

    ![Main menu screenshot](/assets/images/kayleighscakes-intro-screen.PNG)

    The user is asked to enter a number from one to five in order to select an option. This input is validated to ensure that it's a number in the correct range and not any other key. Otherwise a ValueError is raised and an appropriate error message printed to the console, before the user is presented with the menu again.

    ![Error message screenshot](/assets/images/kayleighscakes-error-messages.PNG)

- #### View existing products

    ![Products screenshot](/assets/images/kayleighscakes-products-screen-1.PNG)

    Reads the data from the 'current products' worksheet of the spreadsheet and stores it in various instances of an ExistingPrducts subclass of a Products superclass. The class methods perform operations such as calculating the item's current GP (gross profit), based on its cost price, and a recommended sale price, based on the Irish standard food GP of 65%. The get_details() method of the class instance is then used to print the product details to the console in a structured and easy-to-read format.

- #### View potential new products

    ![Products screenshot 2](/assets/images/kayleighscakes-products-screen-2.PNG)

    Performs similar functions to the above feature, operating on and printing the details of the products that Kayleigh is thinking of adding.

- #### View most popular products

    ![Ratings screenshot](/assets/images/kayleighscakes-ratings-screen.PNG)

    Reads the ratings data from the spreadsheet: a tally of ratings out of 5 for each of the 11 listed products, from a total of 20 respondents. An average rating is calculated from these by the program for every product, then the results are sorted in descending order and printed to the console.

- #### Add product to 'new menu short list' worksheet

    ![Add menu screenshot](/assets/images/kayleighscakes-menu-screen.PNG)

    ![Spreadsheet screenshot](/assets/images/kayleighscakes-sheet-menu-short.PNG)

    Offers the user a list of all the products on the spreadsheet and asks which of them they'd like to add to the shortlist for the new menu. The program again asks the user to enter a number, this time form one to 11, and uses the same validation function as the main menu. Once the user selects a number, the associated product's name and recommended sale price is written onto a new row of the 'menu shortlist' tab in the spreadsheet and the program returns to the main menu so that frther products can be reviewed.

- #### Exit the program

    Quite simply, calls the exit() method :)

    ![Exit screen](/assets/images/kayleighscakes-exit-screen.PNG)

### Features for future implementation

    - Allow the user to add products to the spreadsheet dynamically from the spreadsheet.

## Data Model

I chose to use a Products superclass as my model, with inheriting ExistingProduct and NewProduct subclasses, as well as two mixin classes to calculate GP and recommended sale price. 

The classes store each product's name and cost price and, in the case of existing products, the current sale price. Each class also has a details or get_details method to prepare strings for printing when needed.

## Testing

I have manually tested this project in the following ways.

    - Passed the code through a PEP8 linter and confirmed there are no problems.

    - Given multiple invalid inputs wherever there's an oppportunity for user error: strings where numbers expected and numbers out of range.

    - Tested in my local terminal and the Code Institue Heroku terminal

### Bugs

My validation failed to work on both of the primary occasions I tried it. I realised that I had formatted it wrongly both times. Once sytactically and again positionally within the code.

### Remaining Bugs

No bugs remaining

### Validator Testing

- #### PEP8
    - No errors were returned from [PEP8 Online](http://pep8online.com/checkresult)

    ![PEP8 linter screenshot](/assets/images/pep8-linter-check.PNG)

## Deployment

This project has been deployed using the Code Institute mock terminal for Heroku

- Steps for deployment

    - Fork or clone this repository.

    - Create a new Heroku app.

    - Set the buildbacks to Python and NodeJS, in that order.

    - Link the Heroku app to the repository.

    - Click on 'Deploy'.

## Credits

- Code Institute for the deployment terminal

- Naazneen Jatu's article on [stackabuse.com](https://stackabuse.com/how-to-sort-dictionary-by-value-in-python/) for inspiration when I was struggling with ways to sort a dictionary in descending order by value.