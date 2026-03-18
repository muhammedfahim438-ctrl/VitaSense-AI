# ══════════════════════════════════════════════════════════════
# VitaSense AI - Chatbot API Route
# Catalyst Crew | Nehru Arts and Science College, Coimbatore
# POST /api/chatbot          → Get chatbot reply
# GET  /api/chatbot/history  → Get chat history
# GET  /api/chatbot/replies  → Get quick reply suggestions
# ══════════════════════════════════════════════════════════════

from flask import Blueprint, request, jsonify
from models import db, ChatHistory
from chatbot_model import get_response, get_quick_replies

chatbot_bp = Blueprint('chatbot', __name__)

# ══════════════════════════════════════════════════════════════
# POST /api/chatbot
# Accepts user message → returns bot reply
# ══════════════════════════════════════════════════════════════
@chatbot_bp.route('/api/chatbot', methods=['POST'])
def chat():
    try:
        data         = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                'status':  'error',
                'message': 'Please type a message'
            }), 400

        if len(user_message) > 500:
            return jsonify({
                'status':  'error',
                'message': 'Message too long. Keep it under 500 characters.'
            }), 400

        # ── GET BOT REPLY ────────────────────────────────────
        result = get_response(user_message)

        if result['status'] == 'error':
            return jsonify(result), 500

        # ── SAVE TO DATABASE ─────────────────────────────────
        chat = ChatHistory(
            user_message = user_message,
            bot_reply    = result['reply']
        )
        db.session.add(chat)
        db.session.commit()

        return jsonify({
            'status':  'success',
            'reply':    result['reply'],
            'chat_id':  chat.id
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500


# ══════════════════════════════════════════════════════════════
# GET /api/chatbot/history
# Returns last 20 chat messages
# ══════════════════════════════════════════════════════════════
@chatbot_bp.route('/api/chatbot/history', methods=['GET'])
def chat_history():
    try:
        chats = ChatHistory.query\
            .order_by(ChatHistory.created_at.desc())\
            .limit(20).all()

        return jsonify({
            'status': 'success',
            'count':   len(chats),
            'chats':  [c.to_dict() for c in reversed(chats)]
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500


# ══════════════════════════════════════════════════════════════
# GET /api/chatbot/replies
# Returns quick reply button suggestions
# ══════════════════════════════════════════════════════════════
@chatbot_bp.route('/api/chatbot/replies', methods=['GET'])
def quick_replies():
    try:
        return jsonify({
            'status':  'success',
            'replies':  get_quick_replies()
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500