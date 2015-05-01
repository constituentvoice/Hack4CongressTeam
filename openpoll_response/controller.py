from flask import Flask, request, url_for, g, render_template,session,flash,redirect
from simplekv.fs import FilesystemStore
from flask_kvsession import KVSessionExtension
from traceback import format_exc
import config
#from models import db, User,Question,Response,TextSession
import twilio.twiml
from twilio.rest import TwilioRestClient
import json
import requests

#from sqlalchemy.orm import exc
#import sunlight
#sunlight.config.API_KEY=config.sunlight_key
#from sunlight.congress import Congress

tclient = TwilioRestClient(config.twilio_sid, config.twilio_secret)


app = Flask(__name__)
store = FilesystemStore('/tmp')
KVSessionExtension(store,app)

#app.config['SQLALCHEMY_DATABASE_URI'] = config.dsn
#app.config['SQLALCHEMY_ECHO'] = config.database_debug
app.config['SECRET_KEY'] = config.secret_key
#db.init_app(app)

@app.route('/dispatch', methods=['POST','GET'])
def dispatch_request():
	body = request.values.get('Body')
	ret_message = None
	if 'STOP' in body:
		ret_message = delete_user( request.values.get('From') )
	else:
		ret_message = process_response( request.values.get('From'), body )

	#elif session.get('text_session_id'): # response to a request for more info (address)
	#	ret_message = process_get_info(session.get('text_session_id', request.values.get('From'), body, _zip=request.values.get('FromZip'),state=request.values.get('FromState')))
	#else: # treat as signup
	#	ret_message = process_signup( request.values.get('From'),body )

	resp = twilio.twiml.Response()
	resp.message(ret_message)
	return str(resp)

@app.route('/broadcast', methods=['POST'])
def broadcast():
	"""
	body = None
	if request.values.get('body'):
		body = request.values.get('body')
	else:
		return jsonify({'status':'ERROR','message':'Please enter a message'})

	users = db.session.query(Users).all()
	for u in users:
		try:
			message = client.messages.create(to=u.cell, from_=config.twilio_number, body=body)
		except:
			pass
	"""
	return jsonify({'status':'SUCCESS','message': 'Messages sent'} )

def delete_user( cell ):
	#db.session.query(User).filter_by(cell=cell).delete()
	#db.session.query(TextResponse).filter_by(cell=cell).delete()
	#db.session.commit()
	
	return "We're sorry to see you go. You have been unsubscribed."

def process_response( _from, message, question_id=None ):
	print _from
	print message
	
	#res = Response( user_id=user.id, text=message, question_id=question_id )
	#db.session.add(res)
	#db.session.commit()

	resp = requests.post('http://76.114.205.220:3000/api/Responses', data={'text':message, 'constituentId': 1,'questionId': 1})
	print resp.text

	return 'Thanks for your input'

def process_get_info(text_session_id, _from, message, **kwargs):
	# TODO
	# read this information and try to find congressional district
	# for now try to find by zip provided by twilio
	"""
	sess_rcd = db.session.query(TextSession).get(text_session_id)
	_zip = kwargs.get('_zip')
	state = kwargs.get('state')
	if sess_rcd:
		sess_rcd.message_state = 'SETADDR'
		if _zip:
			dist = None
			try:
				legs = Congress().lookup_legislators_by_zip()
				if legs:
					for l in legs:
						if l.get('district'):
							dist = l.get('district')
							break
				if dist:
					sess_rcd.district = dist

			except:
				pass
		if state:
			sess_rcd.state = state
		
		db.session.commit()
	"""
	return 'Thank you'

def process_signup( _from, body ):
	if 'SUBSCRIBE' in body:
		"""
		user = User(cell=_from)
		db.session.add(user)

		txt_sess = TextSession(message_state='NEW',cell=_from, user=user)
		db.session.add(txt_sess)

		db.session.commit()

		session['text_session_id'] = txt_sess.id
		"""
	
		return 'Thanks for signing up! Reply with your address so we can verify your district.'
	else:
		return 'Trying to sign-up? Reply with SUBSCRIBE'

if __name__ == '__main__':
	app.run(debug=config.enable_debug)
