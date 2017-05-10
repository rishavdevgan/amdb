# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models

# Create your models here.


class User(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    username = models.CharField(max_length=255, null=False, blank=False, unique=True)
    email = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10)
    password = models.CharField(max_length=255, null=False, blank=False)
    short_bio = models.CharField(max_length=555)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class AccessToken(models.Model):

    user = models.ForeignKey(User)
    access_token = models.CharField(max_length=255)
    last_request_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)


    def create_token(self):
        self.access_token = uuid.uuid4()



class Movie(models.Model):

    name = models.CharField(max_length=255)
    duration_in_minutes = models.IntegerField(default=120)
    release_date = models.DateTimeField()
    overall_rating = models.DecimalField(decimal_places=2, max_digits=4)
    censor_board_rating = models.CharField(max_length=5)
    poster_picture_url = models.CharField(max_length=255)
    user = models.ForeignKey(User)


class Genre(models.Model):

    name = models.CharField(max_length=255)


class MovieGenre(models.Model):

    movie = models.ForeignKey(Movie)
    genre = models.ForeignKey(Genre)


class MovieReview(models.Model):

    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)
    rating = models.DecimalField(decimal_places=2, max_digits=5)
    review = models.CharField(max_length=255)