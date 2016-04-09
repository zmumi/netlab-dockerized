import json

from django.http import HttpResponse
from django.template import loader

from configurator.logic import generation


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def generate(request):
    edges = json.loads(request.POST['edges'])
    nodes = json.loads(request.POST['nodes'])
    print edges
    print nodes
    generation.run(nodes, edges, loader)
    return HttpResponse()
