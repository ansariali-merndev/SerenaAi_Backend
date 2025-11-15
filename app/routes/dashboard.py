from flask import Blueprint, jsonify
from app.utils.response import error_response
from app.utils.token_decorator import token_required
from app.models.analysis import Analysis
from sqlalchemy import select, desc
from datetime import datetime, timezone, timedelta

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
@token_required
def get_dashboard(user_id):
    try:
        from app.extensions import db
        
        # Fetch all analyses for the user using SQLAlchemy 2.0 syntax
        stmt = (
            select(Analysis)
            .where(Analysis.user_id == user_id)
            .order_by(desc(Analysis.created_at))
            .limit(10)
        )
        result = db.session.execute(stmt)
        analyses = result.scalars().all()
        
        if not analyses:
            return jsonify({
                "success": True,
                "message": "No analysis data found",
                "sessions": [],
                "averages": {
                    "anxiety": 0,
                    "sadness": 0,
                    "happiness": 0,
                    "anger": 0,
                    "stress": 0,
                    "calmness": 0
                }
            }), 200
        
        # Format sessions data with Indian Standard Time (IST = UTC+5:30)
        sessions = []
        IST = timezone(timedelta(hours=5, minutes=30))
        
        for analysis in analyses:
            created_at = analysis.created_at or datetime.now(timezone.utc)
            # Convert UTC to IST
            ist_time = created_at.astimezone(IST)
            
            sessions.append({
                "id": analysis.id,
                "date": ist_time.strftime("%Y-%m-%d"),
                "time": ist_time.strftime("%H:%M"),
                "anxiety": analysis.anxiety,
                "sadness": analysis.sadness,
                "happiness": analysis.happiness,
                "anger": analysis.anger,
                "stress": analysis.stress,
                "calmness": analysis.calmness  # ✅ YE RAHA CALMNESS!
            })
        
        # Calculate averages
        total_sessions = len(analyses)
        averages = {
            "anxiety": round(sum(a.anxiety for a in analyses) / total_sessions),
            "sadness": round(sum(a.sadness for a in analyses) / total_sessions),
            "happiness": round(sum(a.happiness for a in analyses) / total_sessions),
            "anger": round(sum(a.anger for a in analyses) / total_sessions),
            "stress": round(sum(a.stress for a in analyses) / total_sessions),
            "calmness": round(sum(a.calmness for a in analyses) / total_sessions)  # ✅ YE RAHA CALMNESS!
        }
        
        return jsonify({
            "success": True,
            "sessions": sessions,
            "averages": averages
        }), 200
        
    except Exception as e:
        return error_response(e)