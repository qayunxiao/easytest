from django.test import TestCase

# Create your tests here.
import requests

r=requests.get("http://httpbin.org/get",).text
print(r)