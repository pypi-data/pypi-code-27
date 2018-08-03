from .markdown import MdFmtRenderer, MdFmtMarkdown


class Table():

    def __init__(self, renderer):
        self.renderer = renderer

    def __call__(self, data):
        content = self.renderer(data)
        markdown_renderer = MdFmtRenderer()
        markdown = MdFmtMarkdown(renderer=markdown_renderer)
        return markdown(content)