from django.urls import path
from .views import ArticleList, PollDetail, get_articles, get_article

urlpatterns = [

    path("articles/", ArticleList.as_view(), name="articles_list"),
    path("polls/", get_articles, name="polls_list"),
    path("polls/<pk>", get_article, name="polls_list"),
]
#   path("polls/<int:pk>/", PollDetail.as_view(), name="polls_detail")
