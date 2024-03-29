from webapp.api import bp
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def bad_request(message):
  return error_response(400, message)


def error_response(status_code, message=None):
  payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
  if message:
    payload['message'] = message
    responses = jsonify(payload)
    responses.status_code = status_code
    return responses
