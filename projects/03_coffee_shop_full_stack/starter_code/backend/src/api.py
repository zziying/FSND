import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

#db_drop_and_create_all()

## ROUTES
@app.route('/drinks')
def get_all_drinks():
    """
    Get all drinks' name.
    """
    all_drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in all_drinks]
    })

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    """
    Get all drinks' detail.
    """
    all_drinks = Drink.query.all()

    return jsonify({
    "success": True,
    "drinks": [drink.long() for drink in all_drinks]
    })

@app.route('/drinks', methods = ['POST'])
@requires_auth('post:drinks')
def post_new_drink(payload):
    """
    Post a new drink to menu.
    """
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if (title is None) or  (recipe is None):
        abort (400)
    else: 
        try:
            new_drink = Drink(title = title, recipe = json.dumps(recipe))
            new_drink.insert()

            return jsonify({
                "success": True,
                "drinks": [new_drink.long()]
            })
        except:
            abort(422)

@app.route('/drinks/<id>', methods = ['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    """ 
    Update a drink's recipe or title name by id.
    """
    body = request.get_json()

    drink = Drink.query.filter(Drink.id == id).one_or_none()

    update_title = body.get('title', None)
    update_recipe = body.get('recipe', None)

    if ((update_title is None) and (update_recipe is None)):
        abort(400)
    elif not update_title:
        drink.recipe = json.dumps(update_recipe)
    elif not update_recipe:
        drink.title = update_title
    else:
        drink.recipe = json.dumps(update_recipe)
        drink.title = update_title
    try: 
        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        abort(422)

@app.route('/drinks/<id>', methods = ['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    """
    Delete a drink (by id) from menu.
    """
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    try:
        drink.delete()

        return jsonify({
            'success': True,
            'delete': id
        })
    except:
        abort(404)



## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "permission not found"
    }), 403

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized request"
    }), 401

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500

@app.errorhandler(AuthError)
def authError(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error
    }), e.status_code