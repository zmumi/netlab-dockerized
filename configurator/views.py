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


def get_project(request):
    content = open('out/project.zip').read()
    response = HttpResponse(content, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('project.zip')
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
    do_stop()

    edges = json.loads(request.POST['edges'])
    nodes = json.loads(request.POST['nodes'])
    generation.run(nodes, edges, loader, 'out')

    cmd = "cp -r out netlab-dockerised && cd netlab-dockerised && chmod a+x up.sh && ./up.sh"
    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = {'result': 'ok', 'stdout': popen.stdout.read(), 'stderr': popen.stderr.read()}

    print 'RUN stdout:', result['stdout']
    print 'RUN stdout:', result['stderr']
    return HttpResponse(json.dumps(result))


def stop(request):
    result = do_stop()
    return HttpResponse(json.dumps(result))


def do_stop():
    cmd = "cd netlab-dockerised && docker-compose kill && docker-compose down && cd .. && rm -r netlab-dockerised"
    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = {'result': 'ok', 'stdout': popen.stdout.read(), 'stderr': popen.stderr.read()}
    print 'STOP stdout:', result['stdout']
    print 'STOP stdout:', result['stderr']
    return result


def _load_design():
    try:
        context = json.loads(open('out/design.json').read())
    except:
        context = {'edges': [], 'nodes': [], 'error': 'Unable to load design file'}
    return context
