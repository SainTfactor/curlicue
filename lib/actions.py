#!/usr/bin/env python3
import maskpass

import lib.utilities as utilities

def get_user_input(action, variables):
  if "hidden" in action and action["hidden"]:
    variables[action["store"]] = maskpass.askpass(prompt=action["prompt"], mask='*')
  else:
    variables[action["store"]] = input(action["prompt"])

def fetch_from_url(action, variables, session):
  data = utilities.make_request(action["url"], "get", session)
  with open(action["save_response"], "wb") as f:
    f.write(data)

def get_form(action, variables, session):
  data = utilities.make_request(action["url"], "get", session)
  forms = utilities.get_forms(data, action["verbose"] if "verbose" in action else False)
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
  variables[action["store"]] = {}
  form_data = variables[action["store"]]
  form_data["method"] = action["method"]
  form_data["action"] = action["action"]
  if "query_params" in action:
    form_data["query_params"] = []
    for new_val in action["query_params"]:
      form_data["query_params"].append(new_val)
  if "form_data" in action:
    form_data["form_data"] = []
    for new_val in action["form_data"]:
      form_data["form_data"].append(new_val)
  if "json_data" in action:
    form_data["json_data"] = []
    for new_val in action["json_data"]:
      form_data["json_data"].append(new_val)

def update_form(action, variables):
  form_data = variables[action["store"]]
  if "method" in action:
    form_data["method"] = action["method"]
  if "action" in action:
    form_data["action"] = action["action"]
  for new_val in action["query_params"] if "query_params" in action else []:
    if not "query_params" in form_data:
      form_data["query_params"] = []
    for old_val in form_data["query_params"]:
      if new_val == old_val:
        form_data["query_params"][new_val] = action["query_params"][new_val]
        break
    else:
      form_data["query_params"].append(new_val)
  for new_val in action["form_data"] if "form_data" in action else []:
    if not "form_data" in form_data:
      form_data["form_data"] = []
    for old_val in form_data["form_data"]:
      if new_val == old_val:
        form_data["form_data"][new_val] = action["form_data"][new_val]
        break
    else:
      form_data["form_data"].append(new_val)
  for new_val in action["json_data"] if "json_data" in action else []:
    if not "json_data" in form_data:
      form_data["json_data"] = []
    for old_val in form_data["json_data"]:
      if new_val == old_val:
        form_data["json_data"][new_val] = action["json_data"][new_val]
        break
    else:
      form_data["json_data"].append(new_val)

def display_form(action, variables, session):
  if "store" in action:
    form_data = variables[action["store"]]
    utilities.print_form(form_data)
  elif "url" in action:
    data = utilities.make_request(action["url"], "get", session)
    forms = utilities.get_forms(data, True)

def submit_form(action, variables, session):
  form_data = variables[action["store"]]
  data = utilities.make_request(
    form_data["action"], 
    form_data["method"], 
    session, 
    form_data["query_params"] if "query_params" in form_data else None, 
    form_data["form_data"] if "form_data" in form_data else None, 
    form_data["json_data"] if "json_data" in form_data else None
  )
  if "debug" in action and action["debug"]:
    print(data)
  if "save_response" in action:
    with open(action["save_response"], "wb") as f:
      f.write(data)
 
