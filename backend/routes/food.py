# ══════════════════════════════════════════════════════════════
# VitaSense AI - Food Checker API Route
# Catalyst Crew | Nehru Arts and Science College, Coimbatore
# POST /api/food      → Check if food is safe for diabetics
# GET  /api/food/list → Get all foods in database
# ══════════════════════════════════════════════════════════════

from flask import Blueprint, request, jsonify
from food_checker import check_food, get_all_safe_foods, get_all_avoid_foods, FOOD_DATABASE

food_bp = Blueprint('food', __name__)

# ══════════════════════════════════════════════════════════════
# POST /api/food
# Accepts food name → returns safety info
# ══════════════════════════════════════════════════════════════
@food_bp.route('/api/food', methods=['POST'])
def check_food_safety():
    try:
        data      = request.get_json()
        food_name = data.get('food_name', '').strip()

        if not food_name:
            return jsonify({
                'status':  'error',
                'message': 'Please enter a food name'
            }), 400

        if len(food_name) > 100:
            return jsonify({
                'status':  'error',
                'message': 'Food name is too long'
            }), 400

        result = check_food(food_name)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500


# ══════════════════════════════════════════════════════════════
# GET /api/food/list
# Returns all foods categorized by safety
# ══════════════════════════════════════════════════════════════
@food_bp.route('/api/food/list', methods=['GET'])
def get_food_list():
    try:
        safe     = []
        moderate = []
        avoid    = []

        for name, info in FOOD_DATABASE.items():
            entry = {
                'name':     name.title(),
                'gi':       info['gi'],
                'category': info['category'],
                'portion':  info['portion']
            }
            if info['status'] == 'safe':
                safe.append(entry)
            elif info['status'] == 'moderate':
                moderate.append(entry)
            else:
                avoid.append(entry)

        return jsonify({
            'status':   'success',
            'total':     len(FOOD_DATABASE),
            'safe':      safe,
            'moderate':  moderate,
            'avoid':     avoid
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500


# ══════════════════════════════════════════════════════════════
# GET /api/food/safe
# Returns only safe foods list
# ══════════════════════════════════════════════════════════════
@food_bp.route('/api/food/safe', methods=['GET'])
def get_safe_foods():
    try:
        return jsonify({
            'status': 'success',
            'foods':   get_all_safe_foods()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ══════════════════════════════════════════════════════════════
# GET /api/food/avoid
# Returns only avoid foods list
# ══════════════════════════════════════════════════════════════
@food_bp.route('/api/food/avoid', methods=['GET'])
def get_avoid_foods():
    try:
        return jsonify({
            'status': 'success',
            'foods':   get_all_avoid_foods()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500