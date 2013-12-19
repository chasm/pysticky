from pyramid.view import view_config

@view_config(route_name='testing', renderer='json')
def testing(request):
  return {'name': 'world'}
