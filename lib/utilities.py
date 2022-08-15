#!/usr/bin/env python3
import sys
import yaml
from bs4 import BeautifulSoup

def log_err(message):
  print(message, file=sys.stderr)

def import_tasks(path):
  retval = None
  with open(path, 'r') as f:
    try:
      retval = yaml.safe_load(f)
    except yaml.YAMLError as err:
      log_err(err)
  return retval

def get_forms(html, verbose=False):
  forms = []
  soup = BeautifulSoup(html, 'html.parser')
  for form in soup.find_all('form'):
    form_obj = {}
    form_obj["id"] = form.get('id')
    form_obj["name"] = form.get('name')
    form_obj["action"] = form.get('action')
    form_obj["method"] = form.get('method')
    for item in form.descendants:
      if item.name == 'input':
        if not "form_data" in form_obj:
          form_obj["form_data"] = {}
        form_obj["form_data"][item.get("name")] = item.get("value")
    forms.append(form_obj)
  if verbose:
    for form in forms:
      print_form(form)
  return forms

def make_request(url, method, session, query_params=None, form_data=None, json_data=None):
  if method.lower() == "get":
    return session.get(url, params=query_params).content
  elif method.lower() == "post":
    return session.post(url, params=query_params, data=form_data, json=json_data).content
  elif method.lower() == "put":
    return session.put(url, params=query_params, data=form_data, json=json_data).content
  elif method.lower() == "delete":
    return session.delete(url).content
  elif method.lower() == "options":
    return session.options(url, params=data).content
  elif method.lower() == "head":
    return session.head(url).content
  else:
    log_err("Error: Unsupported HTTP verb.")
    return None

def sub_vars(data, variables):
  if type(data) == dict:
    loopy = data.keys()
  else:
    loopy = range(len(data))
  for item in loopy:
    if type(data[item]) == str:
      for var in [v for v in variables if type(variables[v]) == str]:
        data[item] = data[item].replace("~~{}~~".format(var), variables[var])
    elif type(data[item]) in [dict, list]:
      sub_vars(data[item], variables)

def print_form(form_data):
  if "id" in form_data:
    print("id: {}".format(form_data["id"]))
  if "name" in form_data:
    print("name: {}".format(form_data["name"]))
  print("method: {}".format(form_data["method"]))
  print("action: {}".format(form_data["action"]))
  print("query_params:")
  for v in form_data["query_params"] if "query_params" in form_data else []:
    print(" {}: {}".format(v, form_data["query_params"][v]))
  print("form_data:")
  for v in form_data["form_data"] if "form_data" in form_data else []:
    print(" {}: {}".format(v, form_data["form_data"][v]))
  print("json_data:")
  for v in form_data["json_data"] if "json_data" in form_data else []:
    print(" {}: {}".format(v, form_data["form_data"][v]))
 
