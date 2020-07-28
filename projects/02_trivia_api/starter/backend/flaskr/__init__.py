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

def format_categories(categories):
  return {category.id: category.type for category in categories}

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
    try:
      categories = Category.query.all()

      return jsonify({
        'success': True,
        'categories': format_categories(categories)
      })
    except:
      abort(404)

  @app.route('/questions')
  def get_questions():
    """
    Handle Get requests for questions, including pagination (every 10 questions).
    """
    try:
      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)
      categories = Category.query.all()

      # get all associated categories:
      current_categories_id = []
      for question in questions:
        current_categories_id.append(question.category)
      
      current_categories = Category.query.filter(Category.id.in_(current_categories_id)).all()

      return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(questions),
          'categories': format_categories(categories),
          'current_category': format_categories(current_categories)
      })
    except:
      abort(404)


  @app.route("/questions/<int:question_id>", methods=['DELETE'])
  def delete_question(question_id):
    """
    Handle a delete request to delete a specific question by id.
    """
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      question.delete()

      selection = Question.query.order_by(Question.id).all()
      current_question = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id
      })

    except:
      abort(422)


  @app.route("/questions", methods=['POST'])
  def create_new_question():
    """
    Handle POST request to post a new question.
    """
    try:
      body = request.get_json()

      if ('question' not in body and 'answer' not in body
         and 'difficulty' not in body and 'category' not in body):
          abort(400)

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
    try:
      body = request.get_json()

      if ('searchTerm' not in body):
        abort(400)
      
      search_term = body.get('searchTerm', '')

      selection = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{search_term}%')).all()
      result = paginate_questions(request, selection)

      # find all associated categories
      relevant_categories_id = []
      for question in selection:
        relevant_categories_id.append(question.category)

      categories = Category.query.filter(Category.id.in_(relevant_categories_id)).all()

      return jsonify({
        'success': True,
        'questions': result,
        'total_questions': len(selection),
        'current_category': format_categories(categories)
      })
    except:
      abort(500)
  

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def retrieve_questions_by_category(category_id):
    """ 
    Handle GET request to get questions based on category.
    """
    try:
      selection = Question.query.filter(Question.category == category_id).all()
      current_question = paginate_questions(request, selection)

      if len(selection) == 0:
        abort (404)

      return jsonify({
        'success': True,
        'questions': current_question,
        'total_questions': len(selection),
        'current_category': category_id
      })

    except:
      abort(422)

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    """
    Handle POST request to get questions to play the quiz.
    """
    try:
      body = request.get_json()

      category = body.get('quiz_category')
      previous_question = body.get('previous_questions')

      if (previous_question is None):
        abort(400)

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
    except:
      abort(404)

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

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    }), 500

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  return app
