

def get_all_actions(swagger):
    actions = {} # name: action
    for path, methods in swagger["paths"].items():
        for method, details in methods.items():
            action_name = method.upper() + "-" + path
            actions[action_name] = details
    return actions
