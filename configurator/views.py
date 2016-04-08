from django.http import HttpResponse
from django.template import loader


def index(request):

    template = loader.get_template('index.html')
    context = {
        'latest_question_list': True,
    }
    return HttpResponse(template.render(context, request))