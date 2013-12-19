from pyramid.view import view_config
from bson.json_util import dumps

import ast
import datetime
import simplejson as json

import logging
log = logging.getLogger(__name__)

class PostitEncoder(json.JSONEncoder):
  def default(self, obj):
    log.debug(str(obj))
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    elif isinstance(obj, datetime.date):
      return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
      return (datetime.datetime.min + obj).time().isoformat()
    else:
      return super(PostitEncoder, self).default(obj)

@view_config(route_name='postits', renderer='json')
def postits(request):
  cursor = request.db['postits'].find()
  postits = [ x for x in cursor ]
  return { 'postits': ast.literal_eval(PostitEncoder().encode(postits)) }