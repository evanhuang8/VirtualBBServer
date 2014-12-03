import json
from django.test import TestCase, Client
from snapshot.models import *

class UserTestCase(TestCase):

  def test_user_register_login(self):
    client = Client()
    response = client.post('/register/', {
      'email': 'johndoe@example.com',
      'password': 'password1',
    })
    self.assertEqual(response.status_code, 200)
    content = json.loads(response.content)
    self.assertEqual(content['status'], 'OK')
    self.assertTrue(content.has_key('token'))
    response = client.get('/login/', {
      'email': 'johndoe@example.com',
      'password': 'password1',
    })
    self.assertEqual(response.status_code, 200)
    content = json.loads(response.content)
    self.assertEqual(content['status'], 'OK')
    self.assertTrue(content.has_key('token'))
    return

  def test_facebook_login(self):
    client = Client()
    response = client.get('/fblogin/', {
      'fbid': '827111174012784',
    })
    self.assertEqual(response.status_code, 200)
    content = json.loads(response.content)
    self.assertEqual(content['status'], 'OK')
    self.assertTrue(content.has_key('token'))
    return

class SnapShotTestCase(TestCase):

  def setUp(self):
    tag = Tag(uid = 'fc5f253e497f07e501ed9d886900494d0bff1c9a')
    tag.save()
    self.tag = tag
    client = Client()
    response = client.post('/register/', {
      'email': 'johndoe@example.com',
      'password': 'password1',
    })
    content = json.loads(response.content)
    self.token = content['token']
    return

  def test_create_list(self):
    client = Client()
    response = None
    with open('snapshot/tests/blackboard.jpg', 'r') as image:
      response = client.post('/create/', {
        'token': self.token,
        'tag': self.tag.uid,
        'image': image,
        'caption': 'Einstein\'s board'
      })
    self.assertEqual(response.status_code, 200)
    content = json.loads(response.content)
    self.assertEqual(content['status'], 'OK')
    response = None
    with open('snapshot/tests/blackboard.jpg', 'r') as image:
      response = client.post('/create/', {
        'token': self.token,
        'tag': self.tag.uid,
        'image': image,
        'caption': 'Newton\'s board'
      })
    self.assertEqual(response.status_code, 200)
    content = json.loads(response.content)
    self.assertEqual(content['status'], 'OK')
    response = self.client.get('/list/', {
      'token': self.token,
      'tag': self.tag.uid
    })
    self.assertEqual(response.status_code, 200)
    content = json.loads(response.content)
    self.assertEqual(content['status'], 'OK')
    self.assertEqual(len(content['snapshots']), 2)
    return