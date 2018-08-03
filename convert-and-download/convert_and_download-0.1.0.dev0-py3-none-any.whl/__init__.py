import os
import io

from notebook.base.handlers import IPythonHandler, web, path_regex, FilesRedirectHandler
from notebook.nbconvert.handlers import _format_regex, get_exporter
from notebook.utils import url_path_join
from ipython_genutils import text

from pdfrw import PdfWriter, PdfReader
import thermohw

from ._version import __version__

thermohw_dir = os.path.abspath(os.path.dirname(thermohw.__file__))


def _jupyter_server_extension_paths():
    return [{
        "module": "convert_and_download"
    }]


# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="tree",
        # the path is relative to the `my_fancy_module` directory
        src="static",
        # directory in the `nbextension/` namespace
        dest="convert_and_download",
        # _also_ in the `nbextension/` namespace
        require="convert_and_download/main")]


class DLconvertFileHandler(IPythonHandler):

    SUPPORTED_METHODS = ('GET',)

    @web.authenticated
    def get(self, format, path):

        self.config.PDFExporter.preprocessors = [thermohw.ExtractAttachmentsPreprocessor]
        self.config.PDFExporter.template_file = os.path.join(thermohw_dir, 'homework.tpl')

        exporter = get_exporter(format, config=self.config, log=self.log)
        exporter.writer.build_directory = '.'

        pdfs = []

        path = path.strip('/').strip()
        paths = path.split('.ipynb')

        for path in paths:
            if not path:
                continue
            path += '.ipynb'
            # If the notebook relates to a real file (default contents manager),
            # give its path to nbconvert.
            if hasattr(self.contents_manager, '_get_os_path'):
                os_path = self.contents_manager._get_os_path(path)
                ext_resources_dir, basename = os.path.split(os_path)
            else:
                ext_resources_dir = None

            model = self.contents_manager.get(path=path)
            name = model['name']
            if model['type'] != 'notebook':
                # not a notebook, redirect to files
                return FilesRedirectHandler.redirect_to_files(self, path)

            nb = model['content']

            self.set_header('Last-Modified', model['last_modified'])

            # create resources dictionary
            mod_date = model['last_modified'].strftime(text.date_format)
            nb_title = os.path.splitext(name)[0]

            resource_dict = {
                "metadata": {
                    "name": nb_title,
                    "modified_date": mod_date
                },
                "config_dir": self.application.settings['config_dir']
            }

            if ext_resources_dir:
                resource_dict['metadata']['path'] = ext_resources_dir

            try:
                output, resources = exporter.from_notebook_node(
                    nb,
                    resources=resource_dict
                )
            except Exception as e:
                self.log.exception("nbconvert failed: %s", e)
                raise web.HTTPError(500, "nbconvert failed: %s" % e)

            pdfs.append(io.BytesIO(output))

        writer = PdfWriter()
        for pdf in pdfs:
            writer.addpages(PdfReader(pdf).pages)
        bio = io.BytesIO()
        writer.write(bio)
        bio.seek(0)
        output = bio.read()
        bio.close()

        # Force download if requested
        if self.get_argument('download', 'false').lower() == 'true':
            filename = 'final_output.pdf'
            self.set_header('Content-Disposition',
                            'attachment; filename="%s"' % filename)

        # MIME type
        if exporter.output_mimetype:
            self.set_header('Content-Type',
                            '%s; charset=utf-8' % exporter.output_mimetype)

        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.finish(output)


def load_jupyter_server_extension(nb_server_app):
    """Call when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    # _format_regex = r"(?P<format>\w+)"
    # path_regex = r"(?P<path>(?:(?:/[^/]+)+|/?))"
    route_pattern = url_path_join(web_app.settings['base_url'], r"/dlconvert/%s%s" % (_format_regex, path_regex))
    web_app.add_handlers(host_pattern, [(route_pattern, DLconvertFileHandler)])
