import json
from functools import wraps
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render
from snapshot.models import *

def login_required():
  def login_required_decorator(method):
    def login_required_method(request=None, *args, **kwargs):
      if request is None:
        request = kwargs['request']
      token = request.REQUEST.get('token', None)
      try:
        token = AccessToken.objects.get(token = token)
      except ObjectDoesNotExist:
        return HttpResponseForbidden()
      kwargs['user'] = token.user
      return method(request, *args, **kwargs)
    return wraps(method)(login_required_method)
  return login_required_decorator

def login(request):
  email = request.REQUEST.get('email', None)
  password = request.REQUEST.get('password', None)
  user = None
  try:
    user = User.objects.get(email = email)
  except ObjectDoesNotExist:
    response = {
      'status': 'FAIL',
      'message': 'The email/password combo is incorrect.'
    }
    return JsonResponse(response)
  if not user.verify(password):
    response = {
      'status': 'FAIL',
      'message': 'The email/password combo is incorrect.'
    }
    return JsonResponse(response)
  token = AccessToken(user = user)
  token.save()
  response = {
    'status': 'OK',
    'token': token.token
  }
  return JsonResponse(response)

def fblogin(request):
  fbid = request.REQUEST.get('fbid', None)
  user, created = User.objects.get_or_create(fbid = fbid)
  token = AccessToken(user = user)
  token.save()
  response = {
    'status': 'OK', 
    'token': token.token
  }
  return JsonResponse(response)

def register(request):
  email = request.REQUEST.get('email', None)
  password = request.REQUEST.get('password', None)
  if User.objects.filter(email = email).exists():
    response = {
      'status': 'FAIL',
      'message': 'This email has already been registered.'
    }
    return JsonResponse(response)
  if len(password) < 6:
    response = {
      'status': 'FAIL',
      'message': 'The password must be over 6 characters.'
    }
    return JsonResponse(response)
  user = User(email = email, password = password)
  user.save()
  token = AccessToken(user = user)
  token.save()
  response = {
    'status': 'OK',
    'token': token.token
  }
  return JsonResponse(response)

@login_required()
def create(request, user):
  tag = request.REQUEST.get('tag', None)
  try:
    tag = Tag.objects.get(uid = tag)
  except ObjectDoesNotExist:
    raise Http404
  image = request.FILES.get('image', None)
  if image is None:
    return HttpResponseBadRequest()
  caption = request.REQUEST.get('caption', '')
  snapshot = SnapShot(tag = tag, image = image, caption = caption, created_by = user)
  snapshot.save()
  response = {
    'status': 'OK'
  }
  return JsonResponse(response)

@login_required()
def list(request, user):
  tag = request.REQUEST.get('tag', None)
  try:
    tag = Tag.objects.get(uid = tag)
  except ObjectDoesNotExist:
    raise Http404
  snapshots = SnapShot.objects.filter(tag = tag)
  response = {
    'status': 'OK',
    'snapshots': json.loads(serializers.serialize('json', snapshots))
  }
  return JsonResponse(response)