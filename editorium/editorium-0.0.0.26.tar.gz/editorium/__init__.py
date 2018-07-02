"""
Editorium initialisation.

Note that, we don't import any Qt stuff immediately until default_editorium() is called.
    * to avoid crashing PyQt4 apps 
    * to avoid the seg. fault on Linux 
"""
from editorium.controls.editorium_grid import EditoriumGrid, AbstractEditoriumGridLayout
from editorium.defaults import default_editorium, register
from editorium.bases import AbstractEditor, EditorInfo, Editorium, EditMessages, EBoolDisplay 
from editorium.default_editors import AbstractBrowserEditor, AbstractEnumEditor, AbstractFlagsEditor