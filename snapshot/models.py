import hashlib
import os
from django.db import models
from passlib.hash import bcrypt

class User(models.Model):

  email = models.CharField(max_length = 100, unique = True)
  password = models.CharField(max_length = 60)
  created_at = models.DateTimeField(auto_now_add = True)

  # A copy of the user's original password
  __original_password = None

  def __init__(self, *args, **kwargs):
    """
    Overrides instantiation to keep track of password changes
    """
    super(User, self).__init__(*args, **kwargs)
    # Save a copy of the original password
    self.__original_password = self.password
    return

  def save(self, *args, **kwargs):
    """
    Overrides save method to rehash password if necessary
    """
    self.email = self.email.lower()
    if ((self.pk is None or self.password != self.__original_password) and 
        self.password is not None):
      self.password = bcrypt.encrypt(self.password, rounds = 10)
    super(User, self).save(*args, **kwargs)
    self.__original_password = self.password
    return

  def verify(self, password):
    return bcrypt.verify(password, self.password)

class AccessToken(models.Model):

  user = models.ForeignKey('User')
  token = models.CharField(max_length = 128)
  created_at = models.DateTimeField(auto_now_add = True)

  def save(self, *args, **kwargs):
    if self.token is None:
      self.token = hashlib.sha1(os.urandom(128)).hexdigest()[:128]
    super(AccessToken, self).save(*args, **kwargs)
    return

class Tag(models.Model):

  uid = models.CharField(max_length = 128)
  updated_at = models.DateTimeField(auto_now = True)

class SnapShot(models.Model):

  tag = models.ForeignKey('Tag')
  image = models.ImageField(upload_to = 'uploads/%Y-%m-%d/')
  caption = models.CharField(max_length = 100, blank = True)
  created_by = models.ForeignKey('User')
  created_at = models.DateTimeField(auto_now_add = True)