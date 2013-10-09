from django.http import HttpResponse, HttpResponseServerError
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from models import Event
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from oabutton.common import SigninForm

from django.contrib.auth import get_user_model
from oabutton.apps.bookmarklet.models import User

import json

def show_map(req):
    # TODO: we need to make this smarter.  Coallescing the lat/long
    # data on a nightly basis and folding that down into clustered
    # points would mean we throw less data down to the browser
    json_data = Event.objects.all().to_json()
    count = Event.objects.count()
    context = {'title': 'Map', 'events': json_data, 'count': count}
    return render_to_response(req, 'bookmarklet/site/map.html', context)

def get_json(req):
    # Dump all data as JSON.  This seems like a terrible idea when the
    # dataset gets large.
    json_data = serializers.serialize("json", Event.objects.all())
    return HttpResponse(json_data, content_type="application/json")


@csrf_protect
def signin(request):
    """
    One time signin to create a bookmarklet using HTTP POST.

    The only required field is the email address
    
    Create a new user and return the URL to the user bookmarklet
    """
    if request.method == 'POST': # If the form has been submitted...
        form = SigninForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # TODO: do stuff here
            manager = get_user_model()._default_manager
            data = dict(form.cleaned_data)
            data['username'] = data['email']

            try:
                user = User.objects.get(username=data['email'])
                # TODO: update the user information here?
                # We should probably archive the old one and save a
                # new one.
            except User.DoesNotExist:
                # Default the username to be email address
                user = manager.create_user(**data)

            return HttpResponse(json.dumps({'url': user.get_bookmarklet_url()}), content_type="application/json")
    return HttpResponseServerError(form._errors.items())


def add(req):
    c = {}
    c.update(csrf(req))
    # Display an entry page
    # How does the DOI get in automatically?  This seems really wrong.
    # At the least, we need a test here to illustrate why this should
    # work at all.

    # TODO: use a form thing here
    doi = ''
    url = ''
    if 'url' in req.GET:
        url = req.GET['url']

    if 'doi' in req.GET:
        doi = req.GET['doi']

    c.update({'url': url, 'doi': doi})

    return render_to_response('bookmarklet/index.html', c)

def add_post(req):
    evt_dict = {}
    for k in Event._fields.keys():
        if k == 'id':
            continue
        evt_dict[k] = req.POST.get(k, '')

        if evt_dict[k] == '':
            evt_dict[k] = None

    lat, lng = evt_dict['coords'].split(',')
    evt_dict['coords'] = {'lat': float(lat), 'lng': float(lng)}
    if evt_dict['accessed'] != '':
        evt_dict['accessed'] = datetime.strptime(evt_dict['accessed'], "%a, %d %b %Y %H:%M:%S %Z")

    event = Event(**evt_dict)
    event.save()

    scholar_url = ''
    if req.POST['doi']:
        scholar_url = 'http://scholar.google.com/scholar?cluster=http://dx.doi.org/%s' % req.POST[
            'doi']
    return render_to_response('bookmarklet/success.html', {'scholar_url': scholar_url, 'oid': str(event.id)})

def generate_bookmarklet(req, user_id): 
    return render_to_response('bookmarklet/bookmarklet.html',
            {'user_id': user_id}, content_type="application/javascript")
