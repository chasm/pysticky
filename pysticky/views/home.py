from pyramid.view import view_config

@view_config(route_name='home', renderer='pysticky:templates/home.pt')
def home(request):
  return {'project': 'PySticky'}
