# Lateshow API

## Description

The **Lateshow API** is designed to manage episodes and guest appearances on a late-night show. The API allows users to create, read, update, and delete information about episodes, guests, and their appearances. Each episode features one or more guests, and each guest can appear in multiple episodes. Appearances are tracked and rated based on the guest's performance.

## Demo

To explore or contribute to the project, follow the setup instructions below.

## Setup/Installation Requirements

To get started, you need the following:

- **Python 3.12** installed on your system.
- A **SQLite3** database for managing episodes, guests, and appearances data.
- A terminal (Linux, macOS, or Windows) for running the API.

### Setup Steps:

1. **Clone the Repository**:
   - Go to the repository URL: `https://github.com/E-ugine/lateshow-api`.
   - Copy the SSH URL.
   - In your terminal, navigate to your preferred directory and run:
     ```bash
     git clone <SSH URL>
     ```

2. **Install Dependencies**:
   - Open the cloned repository:
     ```bash
     cd server/
     ```
   - Install required Python libraries using pip:
     ```bash
     $ pipenv install 
     $ pipenv shell
     ```

3. **Run Migrations**:
   - Migrate the database to create the necessary tables:
     ```bash
     flask db upgrade
     ```

4. **Seed Data**:
   - Seed the database with initial data using the provided CSV file:
     ```bash
     python seed.py
     ```

5. **Run the Application**:
   - Start the Flask API:
     ```bash
     flask run/python app.py

     ```

6. **Test the API**:
   - Use Postman/Insomnia to test the endpoints 

## Models

The Lateshow API uses three models: `Episode`, `Guest`, and `Appearance`. 

- **Episode**: Represents an episode of the show, with attributes such as `id`, `date`, and `number`.
- **Guest**: Represents a guest on the show, with attributes like `id`, `name`, and `occupation`.
- **Appearance**: Links a `Guest` to an `Episode` and includes a `rating` for the guest's appearance.

### Relationships

- An `Episode` has many `Guests` through `Appearance`.
- A `Guest` has many `Episodes` through `Appearance`.
- An `Appearance` belongs to a `Guest` and an `Episode`.

## Technologies Used

- **Python 3.12**: Core language used to build the API.
- **Flask**: Web framework for building the API.
- **SQLite3**: Database for storing episode, guest, and appearance information.
- **SQLAlchemy**: ORM used for database interactions and ensuring data integrity.
- **Flask-Migrate**: Extension for handling database migrations.
- **Postman**: Tool for testing API endpoints.

---