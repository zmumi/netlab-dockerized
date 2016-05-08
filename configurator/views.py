import json
import subprocess

from django.http import HttpResponse
from django.template import loader
from django.utils.encoding import smart_str
from configurator.logic import generation
import shutil

def index(request):
    template = loader.get_template('index.html')
    context = _load_design()
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
    design = request.FILES['design_file'].file.read()
    with open('out/design.json', 'w') as design_file:
        design_file.write(design)
    return HttpResponse('{"result":"ok"}')


def reset_design(request):
    shutil.copyfile('out/design.json.template', 'out/design.json')
    return HttpResponse('{"result":"ok"}')


def run(request):
    edges = json.loads(request.POST['edges'])
    nodes = json.loads(request.POST['nodes'])
    generation.run(nodes, edges, loader, 'out')
    res = subprocess.Popen("cd out && chmod a+x up.sh && ./up.sh", shell=True, stdout=subprocess.PIPE).stdout.read()
    print res  # todo: handle
    return HttpResponse('{"result":"ok"}')


def _load_design():
    try:
        context = json.loads(open('out/design.json').read())
    except:
        print 'Unable to load design file'
        context = {'edges': [], 'nodes': []}
    return context
