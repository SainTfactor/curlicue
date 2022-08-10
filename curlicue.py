#!/usr/bin/env python3
import requests
import argparse

import actions
import utilities

if __name__ == "__main__":

  parser = argparse.ArgumentParser("Curlicue: A yaml based browser scripting engine")
  parser.add_argument('-f', '--file', dest="file", required=True, help='The path to your curlicue yaml script file.')
  args = parser.parse_args()

  session = requests.Session()
  headers = { 'User-Agent': 'curlicue/0.1' }

  script = utilities.import_tasks(args.file)
  if "user_agent" in script:
    headers["User-Agent"] = script["user_agent"]

  session.headers.update(headers)

  variables = {}
  for raw_action in script["actions"]:
    utilities.sub_vars(raw_action, variables)
    action_name = [i for i in raw_action][0]
    action = raw_action[action_name]

    if action_name == "get_user_input":
      actions.get_user_input(action, variables)
    elif action_name == "fetch_from_url":
      actions.fetch_from_url(action, variables, session) 
    elif action_name == "get_form":
      actions.get_form(action, variables, session) 
    elif action_name == "create_form":
      actions.create_form(action, variables)
    elif action_name == "update_form":
      actions.update_form(action, variables)
    elif action_name == "display_form":
      actions.display_form(action, variables, session) 
    elif action_name == "submit_form":
      actions.submit_form(action, variables, session) 
    else:
      utilities.log_err("Error: Unexpected command name.")



