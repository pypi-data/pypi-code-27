import json

def render(results, args):
    to_json = []

    for r in results:
        to_json.append({
            'expression': r[0],
            'answer': r[1],
            'explanation': r[2]
            })

    if args.pretty_json:
        print(json.dumps(to_json, indent='  '))
    else:
        print(json.dumps(to_json))
