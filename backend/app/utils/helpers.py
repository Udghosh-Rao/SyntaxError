"""Shared utility helpers."""
from datetime import datetime


def parse_iso_date(date_str: str) -> datetime:
    """Safely parse an ISO date string."""
    return datetime.fromisoformat(date_str)


def success_response(data=None, message='Success', status=200):
    from flask import jsonify
    resp = {'message': message}
    if data is not None:
        resp['data'] = data
    return jsonify(resp), status


def error_response(message='An error occurred', status=400):
    from flask import jsonify
    return jsonify({'error': message}), status
