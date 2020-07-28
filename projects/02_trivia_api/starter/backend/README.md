# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints

### GET '/categories'
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
- Sample: curl http://127.0.0.1:5000/categories
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

### GET '/questions'
- General:
    - Fetches all questions in the database.
    - Request Arguments: None
    - Returns: An json object with indicating whether the response is successful, all the questions (paginated 10 questions per page), number of total questions, all the categories formatted as id: category_string key: value pairs.
- Sample: curl http://127.0.0.1:5000/questions
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```
### DELETE /questions/<question_id>
- General:
    - Delete a sepcific question by id.
    - Request argument: None.
    - Return: An json object indicating whether response is successful, the id of deleted question.
- Sample: curl -X DELETE http://127.0.0.1:5000/questions/15   
```
{
  "deleted": 15, 
  "success": true
}
```  

### POST /questions
- General:
    - Create a new question 
    - Request argument: the content of question, the answer to the question, the difficulty, and the category.
    - Return: A json object with indicating whether repsonse is successful, and the id of the created question.
- Sample: curl -X POST -H "Content-Type: application/json" -d '{"question":"How are you", "answer": "good", "difficulty": 1, "category": "1"}' http://127.0.0.1:5000/questions
```
{
  "created": 25, 
  "success": true
}
```

### POST /questions/search
- General:
    - Search question by keyword (case insensitive)
    - Request argument: a search term 
    - Return: a json object indicating whether response is successful, the search result, the number of result question, and the involving categories.
- Sample: curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"how"}' http://127.0.0.1:5000/questions/search
```
{
  "current_category": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography"
  }, 
  "questions": [
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "good", 
      "category": 3, 
      "difficulty": 1, 
      "id": 24, 
      "question": "How are you?"
    }, 
    {
      "answer": "good", 
      "category": 1, 
      "difficulty": 1, 
      "id": 25, 
      "question": "How are you"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

### GET /categories/<int:category_id>/questions
- General:
    - Get questions by category id
    - Request argument: None
    - Return: A json object with indicating whether the response is successful, all the result question, and number of total result question, and the category we are currently searching.
- Sample: curl http://127.0.0.1:5000/categories/4/questions
```
{
  "current_category": 4, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}

```

### POST /quizzes
- General: 
    - Select a category and randomly play quiz regrading to it.
    - Request argument: the category of quiz to be played, and previous quiz has been played.
    - Return: a json object indicating whether the response is successful, and the quiz to be play in a formatted form.
- Sample: curl -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"type": "Science", "id": "1"}, "previous_questions": ["12"]}' http://127.0.0.1:5000/quizzes
```
{
  "question": {
    "answer": "Blood", 
    "category": 1, 
    "difficulty": 4, 
    "id": 22, 
    "question": "Hematology is a branch of medicine involving the study of what?"
  }, 
  "success": true
}
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```