from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseNotFound
from django.http import Http404
from django.views.generic.base import TemplateView

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def handler404(request):
    response = render_to_response('polls/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


# class View404(TemplateView):
#
#     template_name = "404.html"
#
#     def get(self, request):
#         return render(request, 'polls/404.html')
#
# def detail(request, poll_id):
#     try:
#         p = Poll.objects.get(pk=poll_id)
#     except Poll.DoesNotExist:
#         raise Http404("Poll does not exist")
#     return render(request, 'polls/detail.html', {'poll': p})
