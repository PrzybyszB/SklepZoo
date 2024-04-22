# SklepZoo

SklepZoo is an e-commerce application written in Python using the Flask framework. It allows users to browse products, add them to cart, make payments. The application was created for learning purposes and to demonstrate practical use of web technologies.

## Requirements

- Python 3.x
- Docker
- Web browser

## Installation

1. Clone the repository to your local machine:

    ```
    git clone <repository_url>
    ```

2. Navigate to the project directory:

    ```
    cd Sklep_zoo
    ```

3. Run the application using Docker Compose:

    ```
    docker-compose up --build
    ```

4. Open a web browser and go to `http://127.0.0.1` to start using the application.

## Features

- **Product browsing:** Users can browse available products in the store, sort them by category, and perform searches.
- **Adding to cart:** Upon finding a product of interest, users can add it to their shopping cart.
- **Cart management:** Users can add, remove, and edit products in the cart before making a payment.
- **Making payments:** After completing shopping, users can proceed to the payment process by providing necessary details.
- **API documentation:** If you want to explore the API documentation, visit (http://127.0.0.1:80/apidocs) when the application is running locally.

## User Accounts

The ShopZoo application includes a special administrator account that has extended permissions to manage the store's content. By default, the user with `user_id = 1` is treated as the administrator.

## Note for Administrators

To access the administrator panel, log in to the application using the user account with `user_id = 1`. After logging in, you will have access to all administrative functions.

## Technologies

- Flask: Micro-framework for building web applications in Python.
- MySQL: Database for storing information about products, users, and orders.
- Docker: Tool for containerizing applications, facilitating management of development environment.



## Author

Created by Bartosz Przybysz.

