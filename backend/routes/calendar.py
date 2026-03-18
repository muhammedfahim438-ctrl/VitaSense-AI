# ══════════════════════════════════════════════════════════════
# VitaSense AI - Sugar Tracker Calendar API Route
# Catalyst Crew | Nehru Arts and Science College, Coimbatore
# POST   /api/calendar/add    → Add daily sugar log
# GET    /api/calendar        → Get all calendar entries
# GET    /api/calendar/month  → Get entries for a month
# DELETE /api/calendar/delete → Delete an entry
# GET    /api/calendar/stats  → Get weekly stats
# ══════════════════════════════════════════════════════════════

from flask import Blueprint, request, jsonify
from models import db, CalendarEntry
from datetime import datetime, timedelta

calendar_bp = Blueprint('calendar', __name__)

# ══════════════════════════════════════════════════════════════
# HELPER — GET SUGAR STATUS
# ══════════════════════════════════════════════════════════════
def get_sugar_status(sugar_level):
    if sugar_level < 70:
        return 'Low'           # Blue  — hypoglycemia
    elif sugar_level <= 99:
        return 'Normal'        # Green — healthy
    elif sugar_level <= 125:
        return 'Prediabetes'   # Yellow — at risk
    else:
        return 'High'          # Red   — diabetes range

def get_status_color(status):
    colors = {
        'Low':         '#3B82F6',   # Blue
        'Normal':      '#10B981',   # Green
        'Prediabetes': '#F59E0B',   # Yellow
        'High':        '#EF4444',   # Red
    }
    return colors.get(status, '#6B7280')

# ══════════════════════════════════════════════════════════════
# POST /api/calendar/add
# Add a new daily sugar log entry
# ══════════════════════════════════════════════════════════════
@calendar_bp.route('/api/calendar/add', methods=['POST'])
def add_entry():
    try:
        data        = request.get_json()
        date        = data.get('date', '').strip()
        sugar_level = data.get('sugar_level')
        notes       = data.get('notes', '').strip()

        # ── VALIDATE ─────────────────────────────────────────
        if not date:
            return jsonify({
                'status':  'error',
                'message': 'Date is required'
            }), 400

        if sugar_level is None:
            return jsonify({
                'status':  'error',
                'message': 'Sugar level is required'
            }), 400

        try:
            sugar_level = float(sugar_level)
        except (ValueError, TypeError):
            return jsonify({
                'status':  'error',
                'message': 'Sugar level must be a number'
            }), 400

        if not (20 <= sugar_level <= 600):
            return jsonify({
                'status':  'error',
                'message': 'Sugar level must be between 20 and 600 mg/dL'
            }), 400

        # ── CHECK IF ENTRY EXISTS FOR THIS DATE ──────────────
        existing = CalendarEntry.query.filter_by(date=date).first()

        if existing:
            # Update existing entry
            existing.sugar_level  = sugar_level
            existing.sugar_status = get_sugar_status(sugar_level)
            existing.notes        = notes
            db.session.commit()

            return jsonify({
                'status':       'success',
                'message':      'Entry updated successfully',
                'id':            existing.id,
                'date':          existing.date,
                'sugar_level':   existing.sugar_level,
                'sugar_status':  existing.sugar_status,
                'status_color':  get_status_color(existing.sugar_status),
                'notes':         existing.notes,
                'updated':       True
            }), 200

        # ── CREATE NEW ENTRY ─────────────────────────────────
        sugar_status = get_sugar_status(sugar_level)
        entry = CalendarEntry(
            date         = date,
            sugar_level  = sugar_level,
            sugar_status = sugar_status,
            notes        = notes
        )
        db.session.add(entry)
        db.session.commit()

        return jsonify({
            'status':       'success',
            'message':      'Entry saved successfully',
            'id':            entry.id,
            'date':          entry.date,
            'sugar_level':   entry.sugar_level,
            'sugar_status':  entry.sugar_status,
            'status_color':  get_status_color(sugar_status),
            'notes':         entry.notes,
            'updated':       False
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500


# ══════════════════════════════════════════════════════════════
# GET /api/calendar
# Get all calendar entries
# ══════════════════════════════════════════════════════════════
@calendar_bp.route('/api/calendar', methods=['GET'])
def get_all_entries():
    try:
        entries = CalendarEntry.query\
            .order_by(CalendarEntry.date.desc()).all()

        return jsonify({
            'status':  'success',
            'count':    len(entries),
            'entries': [{
                **e.to_dict(),
                'status_color': get_status_color(e.sugar_status)
            } for e in entries]
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500


# ══════════════════════════════════════════════════════════════
# GET /api/calendar/month?year=2026&month=3
# Get entries for a specific month
# ══════════════════════════════════════════════════════════════
@calendar_bp.route('/api/calendar/month', methods=['GET'])
def get_month_entries():
    try:
        year  = request.args.get('year',  datetime.now().year,  type=int)
        month = request.args.get('month', datetime.now().month, type=int)

        # Filter entries for this month
        prefix  = f"{year}-{month:02d}"
        entries = CalendarEntry.query\
            .filter(CalendarEntry.date.like(f"{prefix}%"))\
            .order_by(CalendarEntry.date).all()

        return jsonify({
            'status':  'success',
            'year':     year,
            'month':    month,
            'count':    len(entries),
            'entries': [{
                **e.to_dict(),
                'status_color': get_status_color(e.sugar_status),
                'day': int(e.date.split('-')[2])
            } for e in entries]
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500


# ══════════════════════════════════════════════════════════════
# DELETE /api/calendar/delete/<id>
# Delete a calendar entry
# ══════════════════════════════════════════════════════════════
@calendar_bp.route('/api/calendar/delete/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    try:
        entry = CalendarEntry.query.get(entry_id)

        if not entry:
            return jsonify({
                'status':  'error',
                'message': 'Entry not found'
            }), 404

        db.session.delete(entry)
        db.session.commit()

        return jsonify({
            'status':  'success',
            'message': 'Entry deleted successfully',
            'id':       entry_id
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500


# ══════════════════════════════════════════════════════════════
# GET /api/calendar/stats
# Get weekly sugar stats for chart
# ══════════════════════════════════════════════════════════════
@calendar_bp.route('/api/calendar/stats', methods=['GET'])
def get_stats():
    try:
        # Last 7 days
        today     = datetime.now().date()
        week_ago  = today - timedelta(days=6)

        entries   = CalendarEntry.query\
            .filter(CalendarEntry.date >= str(week_ago))\
            .order_by(CalendarEntry.date).all()

        # Build 7-day data
        week_data = []
        for i in range(7):
            day     = week_ago + timedelta(days=i)
            day_str = str(day)
            entry   = next((e for e in entries if e.date == day_str), None)
            week_data.append({
                'date':         day_str,
                'day':          day.strftime('%a'),
                'sugar_level':  entry.sugar_level  if entry else None,
                'sugar_status': entry.sugar_status if entry else None,
                'status_color': get_status_color(entry.sugar_status) if entry else '#E5E7EB',
                'logged':       entry is not None
            })

        # All time stats
        all_entries = CalendarEntry.query.all()
        total       = len(all_entries)

        if total > 0:
            avg_sugar  = round(sum(e.sugar_level for e in all_entries) / total, 1)
            normal_pct = round(sum(1 for e in all_entries if e.sugar_status == 'Normal')  / total * 100)
            high_pct   = round(sum(1 for e in all_entries if e.sugar_status == 'High')    / total * 100)
            low_pct    = round(sum(1 for e in all_entries if e.sugar_status == 'Low')     / total * 100)
            pre_pct    = round(sum(1 for e in all_entries if e.sugar_status == 'Prediabetes') / total * 100)
        else:
            avg_sugar  = 0
            normal_pct = high_pct = low_pct = pre_pct = 0

        return jsonify({
            'status':       'success',
            'week_data':     week_data,
            'total_entries': total,
            'avg_sugar':     avg_sugar,
            'normal_pct':    normal_pct,
            'high_pct':      high_pct,
            'low_pct':       low_pct,
            'prediabetes_pct': pre_pct
        }), 200

    except Exception as e:
        return jsonify({
            'status':  'error',
            'message': str(e)
        }), 500