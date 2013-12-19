from pyramid.config import Configurator
from urllib.parse import urlparse

import pymongo

def main(global_config, **settings):
  config = Configurator(settings=settings)
  config.include('pyramid_chameleon')
  config.add_static_view('css', 'static/stylesheets', cache_max_age=3600)
  config.add_static_view('js', 'static/javascripts', cache_max_age=3600)
  config.add_static_view('images', 'static/images', cache_max_age=3600)
  config.add_static_view('static', 'static', cache_max_age=3600)

  db_url = urlparse(settings['mongo_uri'])
  config.registry.db = pymongo.Connection(
    host=db_url.hostname,
    port=db_url.port,
    )

  def add_db(request):
    db = config.registry.db[db_url.path[1:]]
    if db_url.username and db_url.password:
      db.authenticate(db_url.username, db_url.password)
    return db

  config.add_request_method(add_db, 'db', reify=True)

  config.add_route('home', '/')
  config.add_route('postits', '/postits')
  config.add_route('postit', '/postits/{id}')
  config.add_route('upvotes', '/postits/{postit_id}/upvotes')
  config.add_route('upvote', '/postits/{postit_id}/upvotes/{id}')
  config.add_route('testing', '/testing')
  config.scan()
  return config.make_wsgi_app()
