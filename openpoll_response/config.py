# configuration is found in /etc/openpoll.yml 

#enable_debug = True
#database_debug = False
#dsn = 'mysql://openpoll:openPOLL!@localhost/openpoll'

#secure configs
import yaml
from flask import current_app
from traceback import format_exc

fh = open('/etc/openpoll.yml','rb')
secure_config = None
try:
	secure_config = yaml.load(fh)
except:
	current_app.logger.error( format_exc() )

if secure_config:
	for k,v in secure_config.iteritems():
		locals()[k] = v

