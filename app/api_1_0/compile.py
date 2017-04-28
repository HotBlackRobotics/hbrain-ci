from . import api
from ..models import Node
from compiler import Compiler

from flask_json import JsonError, json_response
from flask import Response, request, g, jsonify, current_app
from flask_json import JsonError, json_response, as_json
from flask_cors import CORS, cross_origin

comp = Compiler();


@api.route('/catkin')
def catkin():
	comp.catkin()
	return Response(comp.read_buid_proc(id), mimetype='text/event-stream')

@api.route('/nodes/<int:id>/build')
def build(id):
	n = Node.query.get_or_404(id)
	comp.compile(n)
	return Response(comp.read_buid_proc(id), mimetype='text/event-stream')

@api.route('/nodes/<int:id>/run')
@cross_origin(origin="*", headers=["content-type", "autorization"])
def run_node(id):
	n = Node.query.get_or_404(id)
	comp.run(n)
	return Response(comp.read_run_proc(id), mimetype='text/event-stream')

@api.route('/nodes/<int:id>/status')
@as_json
def status_node(id):
	n = Node.query.filter_by(id=id).first()
	if n is not None:
		return json_response(running=comp.is_runnning(n.id))
	raise JsonError(error='node not in database')

@api.route('/nodes/status')
@as_json
def status_nodes():
	nodes = Node.query.all()
	return dict(nodes=[{'id': n.id, 'running':comp.is_runnning(n.id)} for n in nodes ])



@api.route('/nodes/<int:id>/kill')
@as_json
def api_kill_node(id):
	n = Node.query.filter_by(id=id).first()
	if n is not None:
		comp.kill_node(n.id)
		return json_response(running=comp.is_runnning(n.id))
	raise JsonError(error='node not in database')
