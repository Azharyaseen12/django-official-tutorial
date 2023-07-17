from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from . models import Question, Choice
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.template import loader

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)    
    return render(request, "polls/detail.html", {"question": question})
    


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'GET':        
        return render(request, "polls/addchoice.html", {"question": question})
    elif request.method=='POST':  
        user_submited_choice = request.POST["choice"]
        if user_submited_choice:
            new_choice = Choice(
                question=question, choice_text = user_submited_choice,
                )
            new_choice.save()    
    return render(request, "polls/detail.html", {"question": question}) 

def reset_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    for choice in question.choice_set.all():
        choice.votes = 0
        choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def add_question(request):
    if request.method == 'GET':
        return render(request, "polls/new_question.html")
    elif request.method == 'POST':
        user_submited_question = request.POST["question"]
        if not user_submited_question:
            return render(request, "polls/new_question.html",{
                "error_message":"please enter a valid question"
            })
        new_question = Question(question_text=user_submited_question, pub_date = timezone.now(),)
        new_question.save()  
        return HttpResponseRedirect(reverse("polls:index"))   

def update(request, id):
  question = Question.objects.get(id=id)
  if request.method == 'GET':
        return render(request, "polls/update.html", {"question": question})
  if request.method == 'POST':
      new_question = request.POST.get('queston')
      question.question_text = new_question
      question.save()
      return render(request, "polls/detail.html", {"question": question})   
      
def delete(request, id):
    if request.method == 'GET':
        question = Question.objects.get(id=id)
        question.delete()
        return render(request , 'polls/index.html')
  