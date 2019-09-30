Cashcog
=======================

The Cashcog-API only offers events about newly created expenses. The application consumes the expense events provided by the Cashcog Expense-API, validates and store them in mongo db. A front-end web application powered by zinggrid which is intuitive and responsive that will query/filter and sort them, and approve or decline them



Table of Contents
-----------------
- [Prerequisite](#prerequisited)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)


Prerequisites
-------------

- Install [Python](https://www.python.org/downloads/)
- Install [pipenv](https://pypi.org/project/pipenv/)
- Install [Mongo DB](https://docs.mongodb.com/v3.2/administration/install-community/)

Getting Started
---------------

```bash
# Get the latest snapshot
git clone https://github.com/navroze/cashcog.git

# Change the dir
cd cashcog

# Install python dependencies
pipenv install

# Activate environment
pipenv shell

# Run the command to populate expenses database(Depending on the amount of data the web-application might take time to load)
python consumer.py

# Run the server
python run.py

# To test your application. Before running the test make sure to run consumer.py as test will run on data
pytest

#Start the web application by visiting 127.0.0.1:5000 on the browser
```

**Show Expenses**
----
  Returns json data about expense or multiple expenses.

* **URL**

  /query

* **Method:**

  `GET`
  
*  **URL Params**

   **Optional**
 
   `first_name=[string]`
   
   `last_name=[string]`
   
   `amount=[interger]`
   
   `currency=[string]`

* **Data Params**

  None

* **Success Response:**

  * **Status Code:** 200 <br />
    **Content:** 
    ```
    {
        "data": [
            {
                "amount": 7497,
                "currency": "MNT",
                "description": "Repellat officiis omnis quae hic.",
                "first_name": "Nico",
                "last_name": "Junken",
                "uuid": "b14fe64a-461c-4851-9831-eca7b3d033ce"
            }
        ]
    }
    ```
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ "data": [] }`

* **Sample Call:**

```http://127.0.0.1:5000/query?first_name=Laila&last_name=Hellwig&amount=8368&currency=SCR```

**Validate Expenses Approve or Decline**
----
  Returns json data if expenses is approved or declined with status.

* **URL**

  /validate/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

  **Required**
  
  `uuid=[string, uuid]`
   
   `status=[approve, deny]`

* **Success Response:**

  * **Status Code:** 200 <br />
    **Content:** 
    ```
    {
        "status": "approve",
        "success": true
    }
    ```
 
* **Error Response:**

  * **Code:** 400 NOT FOUND <br />
    **Content:** 
    ```
    {
        "errors": {
            "uuid": [
                "Not a valid UUID."
            ]
        }
    }
    ```

* **Sample Call:**

```http://127.0.0.1:5000/validate/```


Project Structure
-----------------

| Name                               | Description                                                  |
| ---------------------------------- | ------------------------------------------------------------ |
| |
| **tests/**             | Folder for automated testing using pytest              |
| **models/**             | Mongoengine model used for validating and inserting data from consumer.py              |
| **serializers**/             | Serializer for validate and query REST api             |
| **static**/                 | Static files for serving the web application.                          |                       |
| **utils**/currencies.py                | List of acceptable currencies for validation                          |                       |
| **views**/                 | View for handling exchange and validate API.                                     |
| .gitignore                         | Folder and files ignored by git.                             |
| consumer.py             | python script for consuming data from cashcog api and storing in mongo db              
| run.py                             | File to start the server.                                   |
| config.py                             | Web application configuration.                                   |
| Pipfile                       | Python dependencies.
                           