from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .serializers import MovieSerializer, RatingSerializer

from .models import Movie, Rating


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):

        if 'score' in request.data:
            movie = Movie.objects.get(id=pk)
            score = request.data['score']
            # user = request.user
            user = User.objects.get(id=1)

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.score = score
                rating.save()
                rating_serializer = RatingSerializer(rating, many=False)
                response = {'message': "Movie rating updated!", 'result': rating_serializer.data}

            except ObjectDoesNotExist:
                rating = Rating.objects.create(user=user, movie=movie, score=score)
                rating_serializer = RatingSerializer(rating, many=False)
                response = {'message': "Movie rating created!", 'result': rating_serializer.data}

            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': "You need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
