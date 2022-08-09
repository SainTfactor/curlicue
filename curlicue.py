#!/usr/bin/env python3
import yaml
import requests
from bs4 import BeautifulSoup

def import_test(path):
  retval = None
  with open(path, 'r') as f:
    try:
      retval = yaml.safe_load(f)
    except yaml.YAMLError as err:
      print(err)
  return retval

def soup_test(text):
  forms = []
  soup = BeautifulSoup(text, 'html.parser')
  for form in soup.find_all('form'):
    form_obj = {"values" : []}
    form_obj["action"] = form.get('action')
    form_obj["method"] = form.get('method')
    for item in form.descendants:
      if item.name == 'input':
        form_obj["values"].append({ 
          "name" : item.get("name"), 
          "value" : item.get("value")
        })
    forms.append(form_obj)
  return forms

data = requests.get("http://stackoverflow.com/").text
forms = soup_test(data)
print(forms)

output = import_test('example.yaml')
print(output)
