from . import api
from ..models import Node, File
from .. import db
from flask import jsonify, request, flash, make_response, render_template
from flask_json import JsonError, json_response, as_json
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from os import path

@api.route('/files/')
@as_json
def get_all_files():
	files = File.query.all()
	return  dict(files=[f.to_json() for f in files])

@api.route('/nodes/<int:id>/files')
@as_json
def get_files(id):
	files = File.query.filter_by(node_id=id).all()
	print files
	return  dict(files=[f.to_json() for f in files])

@api.route('/files/<int:id>')
@as_json
def get_file(id):
	file = File.query.get_or_404(id)
	return  file.to_json()

@api.route('/nodes/<int:id>/files', methods=['POST'])
@as_json
def post_file(id):
	n = Node.query.get_or_404(id)
	f = File.from_json(request.json)
	f.node = n
	f.code = render_template('code/default.cpp');
	print n._folder()
	print f.filename
	f.filename = path.join(n._folder(), f.filename)
	db.session.add(f)
	try:
		db.session.commit()
		f.save()
	except IntegrityError:
		db.session.rollback()
		flash('File already in Database')
		raise JsonError(error='File already in Database')
	return json_response( response='ok')

@api.route('/files/<int:id>/', methods=['PUT'])
@as_json
def put_file(id):
	f = File.query.get_or_404(id)
	f.code = request.json.get('code', f.code)
	f.last_edit = datetime.utcnow()
	db.session.add(f)
	f.save()
	return json_response(response='ok')


@api.route('/files/<int:id>/', methods=['DELETE'])
@as_json
def delete_file(id):
	f = File.query.filter_by(id=id).first()
	if f is not None:
		f.delete()
		return json_response(response='ok')
	raise JsonError(error='node not in database')


'''
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
'''
