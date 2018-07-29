import abjad
import abjadext.book
import docutils
import os
import posixpath
import pytest
import shutil
import types
from uqbar.strings import normalize
from sphinx.util import FilenameUniqDict


@pytest.fixture
def app():
    app = types.SimpleNamespace()
    app.config = types.SimpleNamespace()
    app.config.abjadbook_ignored_documents = ()
    app.builder = types.SimpleNamespace()
    app.builder.warn = print
    app.builder.current_docname = 'test'
    app.builder.status_iterator = lambda iterable, x, y, z: iter(iterable)
    app.builder.thumbnails = FilenameUniqDict()
    app.builder.outdir = os.path.dirname(os.path.abspath(__file__))
    app.builder.imagedir = '_images'
    app.builder.imgpath = posixpath.join('..', '_images')
    app.builder.srcdir = os.path.join(
        abjad.__path__[0],
        'docs',
        'source',
        )
    app.body = []
    return app


@pytest.fixture
def paths(app):
    paths = types.SimpleNamespace()
    paths.images_directory = os.path.join(
        app.builder.outdir,
        app.builder.imagedir,
        )
    paths.abjadbook_images_directory = os.path.join(
        paths.images_directory,
        'abjadbook',
        )
    if os.path.exists(paths.images_directory):
        shutil.rmtree(paths.images_directory)
    yield paths
    if os.path.exists(paths.images_directory):
        shutil.rmtree(paths.images_directory)


def test_01(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-stylesheet:

        abjad.show(Staff("c'4 d'4 e'4 f'4"))
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-920056dd4296009e841584f9ffdf3bfc8ff2a99a.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-920056dd4296009e841584f9ffdf3bfc8ff2a99a.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 2
    for name in (
        'lilypond-920056dd4296009e841584f9ffdf3bfc8ff2a99a.ly',
        'lilypond-920056dd4296009e841584f9ffdf3bfc8ff2a99a.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_02(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-stylesheet:
        :no-trim:

        abjad.show(Staff("c'4 d'4 e'4 f'4"))
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-a5e7ff68905f8853cb5d94760ec2e292de9a2361.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-a5e7ff68905f8853cb5d94760ec2e292de9a2361.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 2
    for name in (
        'lilypond-a5e7ff68905f8853cb5d94760ec2e292de9a2361.ly',
        'lilypond-a5e7ff68905f8853cb5d94760ec2e292de9a2361.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_03(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-resize:
        :no-stylesheet:
        :no-trim:

        abjad.show(Staff("c'4 d'4 e'4 f'4"))
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 2
    for name in (
        'lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2.ly',
        'lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_04(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-resize:
        :no-stylesheet:
        :no-trim:
        :with-thumbnail:

        abjad.show(Staff("c'4 d'4 e'4 f'4"))
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    assert len(app.builder.thumbnails) == 1
    assert '../_images/abjadbook/lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2.png' in app.builder.thumbnails
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a data-lightbox="group-lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2.ly" href="../_images/abjadbook/lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2-thumbnail.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 3
    for name in (
        'lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2.ly',
        'lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2.png',
        'lilypond-f32de0fef8d7ffd3efdf0378bdf133327ccffde2-thumbnail.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_05(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :stylesheet: default.ily
        :no-trim:

        abjad.show(Staff("c'4 d'4 e'4 f'4"))
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    abjadext.book.SphinxDocumentHandler.on_builder_inited(app)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-6387c547c57c2ecf50db73336b3cb8522b3a1efe.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-6387c547c57c2ecf50db73336b3cb8522b3a1efe.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 3
    for name in (
        'default.ily',
        'lilypond-6387c547c57c2ecf50db73336b3cb8522b3a1efe.ly',
        'lilypond-6387c547c57c2ecf50db73336b3cb8522b3a1efe.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_06(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-stylesheet:

        staff = Staff("c'1 d'1 e'1 f'1 g'1")
        for note in staff[:-1]:
            attach(abjad.LilyPondLiteral(r'\pageBreak', 'after'), note)

        abjad.show(staff)
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page1.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page2.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page3.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page4.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page5.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 6
    for name in (
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page1.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page2.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page3.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page4.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page5.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_07(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-stylesheet:
        :pages: 2-4

        staff = Staff("c'1 d'1 e'1 f'1 g'1")
        for note in staff[:-1]:
            attach(abjad.LilyPondLiteral(r'\pageBreak', 'after'), note)

        abjad.show(staff)
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page2.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page3.png" alt=""/>
        </a>
        <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="abjadbook">
            <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page4.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 6
    for name in (
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page1.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page2.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page3.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page4.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page5.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_08(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-stylesheet:
        :pages: 2-4
        :with-columns: 2

        staff = Staff("c'1 d'1 e'1 f'1 g'1")
        for note in staff[:-1]:
            attach(abjad.LilyPondLiteral(r'\pageBreak', 'after'), note)

        abjad.show(staff)
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <div class="table-row">
            <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page3.png" alt=""/>
            </a>
        </div>
        <div class="table-row">
            <a href="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page4.png" alt=""/>
            </a>
        </div>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 6
    for name in (
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a.ly',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page1.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page2.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page3.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page4.png',
        'lilypond-a744525256944fb6912a0b1d5812462384a6a80a-page5.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_09(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-stylesheet:
        :no-trim:
        :pages: 2-4
        :with-columns: 2

        staff = Staff("c'1 d'1 e'1 f'1 g'1")
        for note in staff[:-1]:
            attach(abjad.LilyPondLiteral(r'\pageBreak', 'after'), note)

        abjad.show(staff)
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <div class="table-row">
            <a href="../_images/abjadbook/lilypond-dd80edb4402648731129273bdb03900346453f6c.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-dd80edb4402648731129273bdb03900346453f6c-page2.png" alt=""/>
            </a>
            <a href="../_images/abjadbook/lilypond-dd80edb4402648731129273bdb03900346453f6c.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-dd80edb4402648731129273bdb03900346453f6c-page3.png" alt=""/>
            </a>
        </div>
        <div class="table-row">
            <a href="../_images/abjadbook/lilypond-dd80edb4402648731129273bdb03900346453f6c.ly" title="" class="table-cell">
                <img src="../_images/abjadbook/lilypond-dd80edb4402648731129273bdb03900346453f6c-page4.png" alt=""/>
            </a>
        </div>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 6
    for name in (
        'lilypond-dd80edb4402648731129273bdb03900346453f6c.ly',
        'lilypond-dd80edb4402648731129273bdb03900346453f6c-page1.png',
        'lilypond-dd80edb4402648731129273bdb03900346453f6c-page2.png',
        'lilypond-dd80edb4402648731129273bdb03900346453f6c-page3.png',
        'lilypond-dd80edb4402648731129273bdb03900346453f6c-page4.png',
        'lilypond-dd80edb4402648731129273bdb03900346453f6c-page5.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_10(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-resize:
        :no-stylesheet:
        :with-thumbnail:

        staff = Staff("c'1 d'1 e'1 f'1 g'1")
        for note in staff[:-1]:
            attach(abjad.LilyPondLiteral(r'\pageBreak', 'after'), note)

        abjad.show(staff)
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <a data-lightbox="group-lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly" href="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page1.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page1-thumbnail.png" alt=""/>
        </a>
        <a data-lightbox="group-lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly" href="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page2.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page2-thumbnail.png" alt=""/>
        </a>
        <a data-lightbox="group-lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly" href="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page3.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page3-thumbnail.png" alt=""/>
        </a>
        <a data-lightbox="group-lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly" href="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page4.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page4-thumbnail.png" alt=""/>
        </a>
        <a data-lightbox="group-lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly" href="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page5.png" title="" data-title="" class="abjadbook thumbnail">
            <img src="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page5-thumbnail.png" alt=""/>
        </a>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 11
    for name in (
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page1.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page1-thumbnail.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page2.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page2-thumbnail.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page3.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page3-thumbnail.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page4.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page4-thumbnail.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page5.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page5-thumbnail.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)


def test_11(app, paths):
    source = r'''
    ..  abjad::
        :hide:
        :no-resize:
        :no-stylesheet:
        :with-columns: 2
        :with-thumbnail:

        staff = Staff("c'1 d'1 e'1 f'1 g'1")
        for note in staff[:-1]:
            attach(abjad.LilyPondLiteral(r'\pageBreak', 'after'), note)

        abjad.show(staff)
    '''
    source = normalize(source)
    handler = abjadext.book.SphinxDocumentHandler()
    document = handler.parse_rst(source)
    handler.on_doctree_read(app, document)
    node = document[0]
    try:
        abjadext.book.SphinxDocumentHandler.visit_abjad_output_block_html(
            app, node)
    except docutils.nodes.SkipNode:
        pass
    handler.on_build_finished(app, None)
    actual = '\n'.join(app.body)
    expected = normalize(r'''
        <div class="table-row">
            <a data-lightbox="group-lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly" href="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page1.png" title="" data-title="" class="table-cell thumbnail">
                <img src="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page1-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly" href="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page2.png" title="" data-title="" class="table-cell thumbnail">
                <img src="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page2-thumbnail.png" alt=""/>
            </a>
        </div>
        <div class="table-row">
            <a data-lightbox="group-lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly" href="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page3.png" title="" data-title="" class="table-cell thumbnail">
                <img src="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page3-thumbnail.png" alt=""/>
            </a>
            <a data-lightbox="group-lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly" href="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page4.png" title="" data-title="" class="table-cell thumbnail">
                <img src="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page4-thumbnail.png" alt=""/>
            </a>
        </div>
        <div class="table-row">
            <a data-lightbox="group-lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly" href="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page5.png" title="" data-title="" class="table-cell thumbnail">
                <img src="../_images/abjadbook/lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page5-thumbnail.png" alt=""/>
            </a>
        </div>
        ''')
    assert actual == expected
    assert len(os.listdir(paths.abjadbook_images_directory)) == 11
    for name in (
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28.ly',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page1.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page1-thumbnail.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page2.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page2-thumbnail.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page3.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page3-thumbnail.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page4.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page4-thumbnail.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page5.png',
        'lilypond-c33b0ca6576087dbb17f3bbcb40114cae5919d28-page5-thumbnail.png',
    ):
        path = os.path.join(paths.images_directory, 'abjadbook', name)
        assert os.path.exists(path)
