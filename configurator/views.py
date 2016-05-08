import json
import subprocess

from django.http import HttpResponse
from django.template import loader
from configurator.logic import generation


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def generate(request):
    _do_generate(request)
    return HttpResponse()


def run(request):
    _do_generate(request)
    res = subprocess.Popen("cd out && chmod a+x up.sh && ./up.sh", shell=True, stdout=subprocess.PIPE).stdout.read()
    print res
    return HttpResponse()


def _do_generate(request):
    edges = json.loads(request.POST['edges'])
    nodes = json.loads(request.POST['nodes'])
    generation.run(nodes, edges, loader, 'out')
