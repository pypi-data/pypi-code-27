import multisite
import argutil
import http.server
import os


@argutil.callable()
def run(opts):
    site = multisite.Multisite(opts.config)

    class CustomHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            status, response = site.get(self.path)
            self.send_response(status)
            self.send_header("Content-type", "text-html")
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))

    try:
        server = http.server.HTTPServer(
            ('localhost', opts.port),
            CustomHandler
        )
        print('Waiting for requests...')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down server...')
        server.socket.close()


@argutil.callable('local')
def add_local_site(opts):
    site = multisite.Multisite(opts.config)
    if opts.name is None:
        setattr(opts, 'name', opts.path.basename(opts.source_path))
    site.add_site(opts.name, opts.source_path, source_type='local')


@argutil.callable('archive')
def add_archive_site(opts):
    site = multisite.Multisite(opts.config)
    if opts.name is None:
        bname = opts.path.basename(opts.source_path)
        setattr(opts, 'name', os.path.splitext(bname)[0])
    site.add_site(opts.name, opts.source_path, source_type='archive')


@argutil.callable('git')
def add_git_site(opts):
    site = multisite.Multisite(opts.config)
    if opts.name is None:
        setattr(opts, 'name', opts.source_path.split('/')[-1])
    site.add_site(
        opts.name,
        opts.source_path,
        source_type='git',
        auto_update=opts.auto_update,
        git_branch=opts.branch,
        git_remote=opts.remote
    )


def main():
    parser = argutil.get_parser()
    opts = parser.parse_args()
    if opts.version:
        import sys
        dirname = os.path.dirname(__file__)
        sys.path.insert(0, os.path.dirname(dirname))
        import setup
        print(setup.VERSION)
    else:
        opts.func(opts)
