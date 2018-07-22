from glob import glob
from urllib.parse import parse_qs
import json
import os

from notebook.base.handlers import IPythonHandler

class GitRestoreHandler(IPythonHandler):

    file_suffix = "-jupygit___.ipynb"

    def post(self):
        data = parse_qs(self.request.body.decode('utf8'))
        dirty_path = data["path"][0]
        
        clean_path = dirty_path[:-len(self.file_suffix)] + ".ipynb"
        os.remove(clean_path)

        self.write({'status':200,'content':'Hola'})
        self.flush()


class GitCleanHandler(IPythonHandler):

    file_suffix = "-jupygit___.ipynb"

    def post(self):
        data = parse_qs(self.request.body.decode('utf8'))
        clean_path = data["path"][0]
        self.add_gitignore_entry(os.path.dirname(clean_path)) 

        dirty_path = clean_path[:-6] + self.file_suffix

        with open(dirty_path, "r") as r:
            dirty = json.load(r)

        self.clean_nb(dirty)

        with open(clean_path, "w") as w:
            json.dump(dirty, w, indent=1)

        self.write({'status':200,'content':'Hola'})
        self.flush()

    def clean_nb(self, dirty, outputs_to_remove=[]):
        cells = dirty.get('cells', [])
        to_remove = set(outputs_to_remove)
        for cell in cells:
            if cell["cell_type"] != "code": continue
            cell["execution_count"] = None
            if to_remove: # WIP
                ix_to_remove = []
                for output in cell["outputs"]:
                    if 'data' in output:
                        keys = output['data'].keys()
                        print(keys)
                    elif 'name' in output:
                        print(output)
                    else:
                        print(output)
            else:
                cell["outputs"] = []

    def add_gitignore_entry(self, path):
        suffix = "*" + self.file_suffix
        gitignore_path = os.path.join(path,".gitignore")
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w") as w:
                w.write("# jupygit file \"extension\"\n")
                w.write(suffix)
        else:
            with open(gitignore_path, "r") as r:
                entries = set([s.strip() for s in r.readlines()])
            if suffix not in entries:
                with open(gitignore_path, "a") as w:
                    w.write("\n# jupygit file \"extension\"\n")
                    w.write(suffix)    