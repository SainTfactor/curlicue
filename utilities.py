#!/usr/bin/env python3
import sys
import yaml

def log_err(message)
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
    form_obj = {"values" : []}
    form_obj["id"] = form.get('id')
    form_obj["name"] = form.get('name')
    form_obj["action"] = form.get('action')
    form_obj["method"] = form.get('method')
    for item in form.descendants:
      if item.name == 'input':
        form_obj["values"].append({ 
          "name" : item.get("name"), 
          "value" : item.get("value")
        })
    forms.append(form_obj)
  if verbose:
    for form in forms:
      print_form(form)
  return forms

def make_request(url, method, session, data=None):
  if method.lower() == "get":
    return session.get(url, params=data).content
  elif method.lower() == "post":
    return session.post(url, data=data).content
  elif method.lower() == "put":
    return session.put(url, data=data).content
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
    elif type(data[item]) != bool:
      sub_vars(data[item], variables)

def print_form(form_data):
  if "id" in form_data:
    print("id: {}".format(form_data["id"]))
  if "name" in form_data:
    print("name: {}".format(form_data["name"]))
  print("method: {}".format(form_data["method"]))
  print("action: {}".format(form_data["action"]))
  print("values:")
  for v in form_data["values"]:
    print(" - name: {}".format(v["name"]))
    print("   value: {}".format(v["value"]))
 
