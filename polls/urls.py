from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("specifics/<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/choice/", views.choice, name="choice"),

    path("<int:question_id>/reset_vote/", views.reset_vote, name="reset_vote"),

    path("add_question/", views.add_question, name="add_question"),

    path('update/<int:id>', views.update, name='update'),

    path('delete/<int:id>', views.delete, name='delete'),

]