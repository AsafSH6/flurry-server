from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    html = '''
    <p><h3><b>Flurry Project<b><h3><p>

    <br><a href="api/v1/flurry/">API</a></br>
    <br><a href="admin/">Admin Page</a></br>
    '''
    return HttpResponse(html)
