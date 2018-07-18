from fanstatic import Library, Resource, Group

library = Library('cookieconsent', 'resources')

cookieconsent_js = Resource(
    library,
    'cookieconsent.js',
    minified='cookieconsent.min.js',
    bottom=True)


cookieconsent_css = Resource(
    library,
    'cookieconsent.min.css')

cookieconsent = Group([
    cookieconsent_js,
    cookieconsent_css,
])
