from flask import render_template, request
from . import main
from flask_json import json_response

@main.app_errorhandler(404)
def page_not_found(e):
	if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
		return json_response(error="not found", status_=404)
	return render_template('main/404.html'), 404

@main.app_errorhandler(405)
def page_not_found(e):
	if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
		return json_response(error="method not allowed", status_=404)
	return render_template('main/404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
	if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
		return json_response(error="internal server error", status_=405)
	return render_template('main/500.html'), 500
