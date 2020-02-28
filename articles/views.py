from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response


@api_view(['GET'])
def get_articles(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True).data
        # return Response(serializer.data)
        return JsonResponse(serializer, safe=False)


@api_view(['GET'])
def get_article(request, pk):
    if request.method == 'GET':
        try:
            article = Article.objects.get(articleId=pk)
        except Article.DoesNotExist:
            return HttpResponse(status=404)

        serializer = ArticleSerializer(article, many=True).data
        return Response(serializer, safe=False)


class ArticleList(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


def get(request, pk):
    article = get_object_or_404(Article, pk=pk)
    data = ArticleSerializer(article).data
    return Response(data)


class PollDetail(APIView):
    pass
