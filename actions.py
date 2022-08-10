#!/usr/bin/env python3
import maskpass
from bs4 import BeautifulSoup

import utilities

def get_user_input(action, variables):
  if "hidden" in action and action["hidden"]:
    variables[action["store"]] = maskpass.askpass(prompt=action["prompt"], mask='*')
  else:
    variables[action["store"]] = input(action["prompt"])

def fetch_from_url(action, variables, session):
  data = make_request(action["url"], "get", session)
  with open(action["save_response"], "wb") as f:
    f.write(data)

def get_form(action, variables, session):
  data = make_request(action["url"], "get", session)
  forms = get_forms(data, action["verbose"] if "verbose" in action else False)
  if "id" in action:
    form = [f for f in forms if f["id"] == action["id"]][0]
    variables[action["store"]] = form
  elif "name" in action:
    form = [f for f in forms if f["name"] == action["name"]][0]
    variables[action["store"]] = form
  elif "index" in action:
    variables[action["store"]] = forms[action["index"]]
  else:
    variables[action["store"]] = forms[-1]

def create_form(action, variables):
  variables[action["store"]] = { "values": [] }
  form_data = variables[action["store"]]
  form_data["method"] = action["method"]
  form_data["action"] = action["action"]
  for new_val in action["values"]:
    form_data["values"].append(new_val)

def update_form(action, variables):
  form_data = variables[action["store"]]
  if "method" in action:
    form_data["method"] = action["method"]
  if "action" in action:
    form_data["action"] = action["action"]
  for new_val in action["values"] if "values" in action else []:
    for old_val in form_data["values"]:
      if new_val["name"] == old_val["name"]:
        old_val["value"] = new_val["value"]
        break
    else:
      form_data["values"].append(new_val)

def display_form(action, variables, session):
  if "store" in action:
    form_data = variables[action["store"]]
    print_form(form_data)
  elif "url" in action:
    pass

def submit_form(action, variables, session):
  form_data = variables[action["store"]]
  data = make_request(form_data["action"], form_data["method"], session, form_data["values"])
  if "debug" in action and action["debug"]:
    print(data)
  if "save_response" in action:
    with open(action["save_response"], "wb") as f:
      f.write(data)
 
