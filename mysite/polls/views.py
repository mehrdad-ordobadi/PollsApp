from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import F

from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def question_text(request, question_id):
    try: 
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return HttpResponse(f"Sorry, there is no question with id {question_id} yet!")
    response = f'The text for question {question_id} is: \n{question.question_text}'
    return HttpResponse(response)

def cast_vote(request, question_id, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    question = get_object_or_404(Question, pk=question_id)
    choice.votes = F('votes') + 1
    choice.save()
    question = choice.question
    responses = [
        (response.choice_text, response.votes) 
        for response in question.choice_set.all()
    ]
    context = {'question': question, 'responses': responses}
    return render(request, "polls/view-votes.html", context)