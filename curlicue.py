#!/usr/bin/env python3
import sys
import yaml
import requests
import argparse
from bs4 import BeautifulSoup

def import_tasks(path):
  retval = None
  with open(path, 'r') as f:
    try:
      retval = yaml.safe_load(f)
    except yaml.YAMLError as err:
      print(err, file=sys.stderr)
  return retval

def get_forms(html):
  forms = []
  soup = BeautifulSoup(html, 'html.parser')
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

def make_request(url, method, session, headers, data=None):
  if method.lower() == "get":
    return session.get(url, params=data, headers=headers).content
  elif method.lower() == "post":
    return session.post(url, data=data, headers=headers).content
  elif method.lower() == "put":
    return session.put(url, data=data, headers=headers).content
  elif method.lower() == "delete":
    return session.delete(url, headers=headers).content
  elif method.lower() == "options":
    return session.options(url, params=data, headers=headers).content
  elif method.lower() == "head":
    return session.head(url, headers=headers).content
  else:
    print("Error: Unsupported HTTP verb.", file=sys.stderr)
    return None

def sub_vars(data, variables):
  for item in data.keys():
    if type(data[item]) == str:
      for var in variables:
        data[item] = data[item].replace("~~{}~~".format(var), variables[var])
    else:
      sub_vars(data[item], variables)

if __name__ == "__main__":

  parser = argparse.ArgumentParser("Curlicue: A yaml based browser scripting engine")
  parser.add_argument('-f', '--file', dest="file", required=True, help='The path to your curlicue yaml script file.')
  args = parser.parse_args()

  session = requests.Session()
  headers = { 'User-Agent': 'curlicue/0.1' }

  script = import_tasks(args.file)
  if "user_agent" in script:
    headers["User-Agent"] = script["user_agent"]

  variables = {}
  for raw_action in script["actions"]:
    sub_vars(raw_action, variables)
    action_name = [i for i in raw_action][0]
    action = raw_action[action_name]

    if action_name == "get_user_input":
      variables[action["store"]] = input(action["prompt"])
    
    elif action_name == "fetch_from_url":
      data = make_request(action["url"], "get", session, headers)
      with open(action["save_response"], "wb") as f:
        f.write(data)
    
    elif action_name == "get_form":
      data = make_request(action["url"], "get", session, headers)
      forms = get_forms(data)
    
    elif action_name == "create_form":
      variables[action["store"]] = { "values": [] }
      form_data = variables[action["store"]]
      form_data["method"] = action["method"]
      form_data["action"] = action["action"]
      for new_val in action["values"]:
        form_data["values"].append(new_val)
    
    elif action_name == "update_form":
      form_data = variables[action["store"]]
      form_data["method"] = action["method"]
      form_data["action"] = action["action"]
      for new_val in action["values"]:
        for old_val in form_data["values"]:
          if new_val["name"] == old_val["name"]:
            old_val["value"] = new_val["value"]
            break
        else:
          form_data["values"].append(new_val)
    
    elif action_name == "display_form":
      form_data = variables[action["store"]]
      print("method: {}".format(form_data["method"]))
      print("action: {}".format(form_data["action"]))
      print("values:")
      for v in form_data["values"]:
        print(" - name: {}".format(v["name"]))
        print("   value: {}".format(v["value"]))
    
    elif action_name == "submit_form":
      data = make_request(action["url"], action["method"], session, headers, variables[action["store"]])
      if "save_response" in action:
        with open(action["save_response"], "wb") as f:
          f.write(data)
 
    else:
      print("Error: Unexpected command name.", file=sys.stderr)



