from . import api
from ..models import Node, File
from .. import db
from flask import jsonify, request, flash, make_response, render_template
from flask_json import JsonError, json_response, as_json
from datetime import datetime

from sqlalchemy.exc import IntegrityError

@api.route('/nodes/')
@as_json
def get_nodes():
	nodes = Node.query.all()
	return dict(nodes=[s.to_json() for s in nodes])


@api.route('/nodes/<int:id>')
@as_json
def get_node(id):
	s = Node.query.get_or_404(id)
	return s.to_json()

@api.route('/nodes/download/<int:id>')
def download_file(id):
	p = Node.query.get_or_404(id)
	response = make_response(p.code)
	response.headers["Content-Disposition"] = "attachment; filename=%s.cpp" % p.title
	return response


@api.route('/nodes/', methods=['POST'])
@as_json
def post_node():
	print 'request:', request.json
	s = Node.from_json(request.json)
	s.code = render_template('code/default.cpp');
	db.session.add(s)
	try:
		db.session.commit()
		s.create()
	except IntegrityError:
		db.session.rollback()
		flash('Title already in Database')
		raise JsonError(error='Title already in Database')
	return json_response( response='ok')



@api.route('/nodes/<int:id>/', methods=['DELETE'])
@as_json
def delete_node(id):
	s = Node.query.filter_by(id=id).first()
	if s is not None:
		db.session.delete(s)
		db.session.commit()
		return json_response(response='ok')
	raise JsonError(error='node not in database')



@api.route('/nodes/', methods=['DELETE'])
@as_json
def delete_all_nodes():
	Node.query.delete()
	db.session.commit()
	return json_response(response='ok')



@api.route('/nodes/<int:id>/', methods=['PUT'])
@as_json
def put_node(id):
	s = Node.query.get_or_404(id)
	s.code = request.json.get('code', s.code)
	s.last_edit = datetime.utcnow()
	db.session.add(s)
	return json_response(response='ok')
