import json
import subprocess

from django.forms import forms
from django.http import HttpResponse
from django.template import loader
from django.utils.encoding import smart_str
from configurator.logic import generation

def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def generate(request):
    edges = json.loads(request.POST['edges'])
    nodes = json.loads(request.POST['nodes'])
    generation.run(nodes, edges, loader, 'out')
    return HttpResponse('{"result":"ok"}')


def get_design(request):
    content = open('out/design.json').read()
    response = HttpResponse(content, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('design.json')
    return response


def set_design(request):
    print request.FILES['design_file'].file.read()
    return HttpResponse('{"result":"ok"}')


def run(request):
    edges = json.loads(request.POST['edges'])
    nodes = json.loads(request.POST['nodes'])
    generation.run(nodes, edges, loader, 'out')
    res = subprocess.Popen("cd out && chmod a+x up.sh && ./up.sh", shell=True, stdout=subprocess.PIPE).stdout.read()
    print res  # todo: handle
    return HttpResponse('{"result":"ok"}')
