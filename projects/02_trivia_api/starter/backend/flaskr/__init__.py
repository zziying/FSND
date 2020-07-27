import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type = int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_question = questions[start:end]

  return current_question

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app)

  @app.after_request
  def after_request(response):
    """
    Set access control.
    """
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/categories')
  def get_all_categories():
    """
    Handle a get request for getting all categories.
    """
    categories = Category.query.order_by(Category.type).all()
    
    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })

  @app.route('/questions')
  def get_questions():
    """
    Handle Get requests for questions, including pagination (every 10 questions).
    """
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    categories = Category.query.order_by(Category.type).all()

    if len(current_questions) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
        'categories': {category.id: category.type for category in categories},
        'current_category': None
    })

  @app.route("/questions/<question_id>", methods=['DELETE'])
  def delete_question(question_id):
    """
    Handle a delete request to delete a specific question by id.
    """
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      selection = Question.query.order_by(Question.id).all()
      current_question = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'list_of_questions': current_question,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)


  @app.route("/questions", methods=['POST'])
  def create_new_question():
    """
    Handle POST request to post a new question.
    """
    body = request.get_json()

    if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
      abort(422)

    try:
      new_question = Question(
        question=body.get('question'),
        answer=body.get('answer'),
        difficulty=body.get('difficulty'),
        category=body.get('category')
      )

      new_question.insert()

      return jsonify({
          'success': True,
          'created': new_question.id,
      })

    except:
      abort(422)

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    """
    Handle POST request to get questions based on a search term.
    """
    body = request.get_json()

    if ('searchTerm' not in body):
      abort(422)
    
    search_term = body.get('searchTerm', '')

    try:
      selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term))).all()
      result = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'questions': result,
        'total_questions': len(selection),
        'current_category': None
      })
    
    except:
      abort(404)

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def retrieve_questions_by_category(category_id):
    """ 
    Handle GET request to get questions based on category.
    """
    selection = Question.query.filter(Question.category == category_id).all()
    current_question = paginate_questions(request, selection)

    if len(current_question) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_question,
      'total_questions': len(selection),
      'current_category': category_id
    })

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    """
    Handle POST request to get questions to play the quiz.
    """
    body = request.get_json()

    category = body.get('quiz_category')
    previous_question = body.get('previous_questions')

    if (category is None) or (previous_question is None):
      abort(422)

    # If all is selected, load all questions, else, select a specific category type by id
    if (category['id'] == 0):
      questions = Question.query.all()
    else:
      questions = Question.query.filter(Question.category == category['id']).all()

    def generate_a_question():
      return questions[random.randrange(0, len(questions), 1)]

    # Iterate through the questions and find which one is not shown in the previous
    next_question = generate_a_question()
    is_in_prev = True

    while (is_in_prev):
      if next_question.id in previous_question:
        next_question = generate_a_question()
      else:
        is_in_prev = False

    return jsonify({
        'success': True,
        'question': next_question.format()
    })

  # Error handlers
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422

  return app
