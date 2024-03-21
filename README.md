#  Server-side 3GPP  RAG App 
 This application is written in Python and provides three API endpoints for managing User IDs, searching the vector database, and posting logs to the database.
 The purpose of this project is to enable users to perform similarity search of 3GPP (3rd Generation Partnership Project) documentation in a chat-like environment.

## Project Design
<img src="{{ url_for('static', filename='images/slide3.jpg') }}" alt="Picture 1">

## Server Design
<img src="{{ url_for('static', filename='images/slide4.jpg') }}" alt="Picture 2">

## Project Structure

 _project/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── milvus_controller.py
│   └── models.py
├── venv/               
├── config/
│   ├── __init__.py
│   └── settings.py
├── tests/
│   ├── __init__.py
│   └── test_routes.py
├── requirements.txt
├── run.py
└── README.md

## Functionality
1. User ID Management
Endpoint: /user
Description: Manages User IDs within the system.
Methods:
GET: Retrieves information about a specific User ID.
POST: Creates a new User ID.
2. Vector Database Search
Endpoint: /search
Description: Conducts similarity search in the vector database.
Methods:
POST: Performs a search based on user query and retrieves the best hits.
3. Logging
Endpoint: /logs
Description: Posts logs to the relational database.
Methods:
POST: Records logs in the database.
##  Usage
Ensure you have Python installed on your system.
Install the required dependencies using pip install -r requirements.txt.
Set up your configuration in config/settings.py.
Activate the virtual environment (venv) using source venv/bin/activate.
Run the application using python run.py.
Access the API endpoints using appropriate HTTP methods and URIs as described above.
Additional Information
This project connects to two databases: Milvus (vector database) and MySQL (relational database).
It utilizes similarity search to retrieve the best hits from the vector database.
The retrieved hits are passed to a generative model to generate answers to user queries.
Finally, the application provides users with answers to their questions along with the source information returned in the server response from the search call.
For more detailed information, refer to the codebase and documentation within the project.

Contributing
Contributions are welcome! Please refer to the contribution guidelines in the CONTRIBUTING.md file for more details.