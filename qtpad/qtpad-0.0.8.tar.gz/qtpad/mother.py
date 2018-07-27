#!/usr/bin/python3
import json
import os
import sys

import requests
from PyQt5 import QtGui, QtWidgets, QtCore, QtDBus, uic

try:
    import qtpad.gui_search
    from qtpad.preferences import PreferencesDatabase, PreferencesForm
    from qtpad.child import Child
    from qtpad.common import *
except ImportError:
    from preferences import PreferencesDatabase, PreferencesForm
    from child import Child
    from common import *

# Init common settings
LOCAL_DIR, ICONS_DIR, PREFERENCES_FILE, PROFILES_FILE = getStaticPaths()
logger = getLogger()
logger.info("Init of a new instance")
if "qtpad.common" not in sys.modules:
    logger.warning("Could not load pre-compiled modules")


class Mother(object):
    def __init__(self):
        # Load preferences
        self.preferencesIndexes = {"menu": 0, "css": None}
        self.preferences = PreferencesDatabase()
        self.cssLoad()
        self.clipboard = app.clipboard()

        # Load icons
        self.icon = {}
        for icon in os.listdir(ICONS_DIR):
            iconName = os.path.splitext(icon)
            if iconName[1] == ".svg":
                self.icon[iconName[0]] = QtGui.QIcon(ICONS_DIR + icon)

        # Init search form
        self.lastActive = ""
        self.searchForm = SearchForm(self)

        # Load notes
        configPath = os.path.expanduser("~/.config/qtpad/")
        notesDir = self.preferences.query("general", "notesDb")
        if not os.path.exists(notesDir):
            os.makedirs(notesDir)
        if not os.path.exists(configPath):
            os.makedirs(configPath)

        if self.preferences.query("general", "deleteEmptyNotes"):
            self._noteCleanEmpty()
        self._noteCleanProfiles()
        self._noteCleanUnloaded()
        self.children = {}
        self.folderLoad(notesDir)
        self.folderLoadEnabled()

        # Init system tray icon
        trayIcon = self.icon["tray"].pixmap(64, 64)  # Handle svg to pixmap conversion (KDE compatibility)
        trayIcon = QtGui.QIcon(trayIcon)
        self.menu = QtWidgets.QMenu()
        self.menu.aboutToShow.connect(self._menuRefresh)
        self.trayIcon = QtWidgets.QSystemTrayIcon()
        self.trayIcon.activated.connect(self.clickEvent)
        self.trayIcon.setIcon(trayIcon)
        self._menuRefresh()
        self.trayIcon.setContextMenu(self.menu)
        self.trayIcon.show()

        # Init notes widgets
        if self.preferences.query("actions", "startupAction"):
            action = self.preferences.query("actions", "startupAction")
            cmd = self.preferences.query("actions", "startupCmd")
            self.noteAction(action, cmd)

    def clickEvent(self, event):
        if event == QtWidgets.QSystemTrayIcon.Trigger:
            action = self.preferences.query("actions", "leftAction")
            cmd = self.preferences.query("actions", "leftCmd")
            self.noteAction(action, cmd)

        elif event == QtWidgets.QSystemTrayIcon.MiddleClick:
            action = self.preferences.query("actions", "middleAction")
            cmd = self.preferences.query("actions", "middleCmd")
            self.noteAction(action, cmd)

    def _clipboardFetch(self, newNote=False):
        pixmap = self.clipboard.pixmap()
        path = self.clipboard.text().rstrip()
        textContent = None
        if pixmap.isNull():
            if os.path.isfile(path) and os.stat(path).st_size > 0:
                allowed = ["txt", "gif", "png", "bmp", "jpg", "jpeg", "svg"]
                ext = os.path.splitext(path.lower())[1][1:]
                if ext in allowed:
                    if self.preferences.query("general", "fetchTxt") and ext == "txt":
                        with open(path) as f:
                            textContent = f.read()
                    elif self.preferences.query("general", "fetchFile"):
                        pixmap = QtGui.QPixmap(path)

            elif self.preferences.query("general", "fetchUrl") and (path.startswith("http://") or path.startswith("https://") or path.startswith("www.")):
                if path.lower().find(".pdf") == -1:
                    allowed = ['jpeg', 'gif', 'png', 'bmp', 'svg+xml']
                    try:
                        mimetype = requests.get(path).headers["content-type"].split('/')[1]
                        if mimetype in allowed:
                            fetch = requests.get(path)
                            pixmap.loadFromData(fetch.content)
                    except Exception:
                        logger.warning(str(sys.exc_info()[0]), str(sys.exc_info()[1]))

        if textContent or not pixmap.isNull():
            if newNote:
                if textContent:
                    self.children[self.noteNew(text=textContent)]
                    logger.info("Fetched text from " + path)
                else:
                    self.children[self.noteNew(image=pixmap)]
                    logger.info("Fetched image from " + (path if path else "clipboard"))

                if self.preferences.query("general", "fetchClear"):
                    self.clipboard.setText("")
                    logger.warning("Emptied clipboard content")
            return True
        return False

    def _cmdParse(self, cmd):
        logger.info("Call from command line interface: " + str(cmd))
        actions = []
        if "action" in cmd: actions += cmd["action"]
        if "a" in cmd: actions += cmd["a"]
        for action in actions:
            self.noteAction(action)

    def _folderDelete(self, folder):
        folder = self.preferences.query("general", "notesDb") + folder
        if len(os.listdir(folder)) == 0:
            os.rmdir(folder)
            logger.warning("Removed empty folder '" + folder + "' (user)")
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowFlags(msg.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Delete confirmation")
            msg.setText("Please confirm deletion of folder\n" + folder)
            msg.setStandardButtons(QtWidgets.QMessageBox.Apply | QtWidgets.QMessageBox.Cancel)
            if msg.exec_() == QtWidgets.QMessageBox.Apply:
                for f in os.listdir(folder):
                    os.remove(folder + "/" + f)
                os.rmdir(folder)
                logger.warning("Removed folder '" + folder + "' (user)")
                self._noteCleanOrphans()

    def _folderEnable(self, folder):
        for f in os.listdir(self.preferences.query("general", "notesDb") + folder):
            name = folder + "/" + f
            name = name.rsplit('.', 1)[0]
            if name in self.preferences.db["unloaded"]:
                self.preferences.db["unloaded"].remove(name)
        self.preferences.save()
        self.folderLoadEnabled()

    def _folderLoadAll(self):
        self.preferences.db["unloaded"] = []
        self.preferences.save()
        self.folderLoadEnabled()

    def _folderRename(self, oldName, newName):
        notesDir = self.preferences.query("general", "notesDb")
        try:
            os.rename(notesDir + oldName, notesDir + newName)
        except OSError:
            logger.error("Could not rename folder (name too long?)")
        except FileNotFoundError:
            logger.error("File not found (" + notesDir + oldName + ")")
        else:
            # Rename loaded notes
            for child in self.children:
                if self.children[child].fullname.startswith(oldName + "/"):
                    self.children[child].noteMove(newName, soft=True)

            # Rename folders in unloaded list
            unloaded = map(lambda x: x.replace(oldName + "/", newName + "/"), self.preferences.db["unloaded"])
            self.preferences.db["unloaded"] = list(unloaded)
            self.preferences.save()

            logger.info("Renamed folder '" + oldName + "' to '" + newName + "'")
            self.folderLoadEnabled()

    def _folderUnloadAll(self):
        for child in list(self.children):
            child = self.children[child]
            if child.folder:
                self.preferences.db["unloaded"].append(child.fullname)
                child.noteClose()
        self.preferences.save()

    def _folderRenamePrompt(self, folder):
        msg = QtWidgets.QInputDialog()
        msg.setInputMode(QtWidgets.QInputDialog.TextInput)
        msg.setWindowFlags(msg.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        msg.setWindowTitle("Rename '" + folder + "'")
        msg.setLabelText("Enter the new name:")
        msg.setTextValue(folder)
        msg.setFixedSize(250, 100)
        accept = msg.exec_()
        newName = msg.textValue()
        newName = sanitizeString(newName, '\/:*?"<>|')
        newPath = self.preferences.query("general", "notesDb") + newName
        if accept and newName and not os.path.isfile(newPath) and not os.path.isdir(newPath):
            self._folderRename(folder, newName)

    def _folderUnload(self, folder):
        for f in os.listdir(self.preferences.query("general", "notesDb") + folder):
            name = folder + "/" + f
            name = name.rsplit('.', 1)[0]
            if name in self.children:
                self._noteUnload(self.children[name])
        logger.info("Unloaded folder '%s'" % folder)

    def _menuAddOption(self, option):
        option = option.lower()
        icon = self.icon.get(option.replace(" ", "_"))

        if option == "(separator)":
            self.menu.addSeparator()

        elif option == "preferences":
            self.menu.addAction(icon, "Preferences", lambda: PreferencesForm(self))

        elif option == "quit":
            self.menu.addAction(icon, 'Quit', app.exit)

        elif option == "folders list":
            self._menuListFolders()

        elif option == "notes list":
            self._menuListNotes()

        elif option == "fetch clipboard":
            if self._clipboardFetch():
                self.menu.addAction(icon, option.capitalize(), lambda: self.noteAction(option))

        else:
            self.menu.addAction(icon, option.capitalize(), lambda: self.noteAction(option))

    def _menuListFolders(self):
        notesDir = self.preferences.query("general", "notesDb")
        folderList = self.folderList(notesDir)
        self.foldersMenu = {}
        self.foldersAction = {}
        for folder in folderList:
            self.foldersMenu[folder] = QtWidgets.QMenu()
            path = notesDir + folder + "/"
            enabled = 0
            for total, f in enumerate(sorted(os.listdir(path))):
                fullpath = path + f
                fullname = fullpath[len(notesDir):-len(os.path.splitext(fullpath)[1])]
                self.foldersAction[fullname] = QtWidgets.QAction(f, checkable=True)
                if fullname in self.children:
                    enabled += 1
                    self.foldersAction[fullname].triggered.connect(lambda x, fullname=fullname: self._noteUnload(self.children[fullname]))
                    self.foldersAction[fullname].setChecked(True)
                else:
                    self.foldersAction[fullname].triggered.connect(lambda x, fullpath=fullpath: self._noteLoad(fullpath))
                self.foldersMenu[folder].addAction(self.foldersAction[fullname])

            self.foldersMenu[folder].setTitle(folder + " (" + str(enabled) + "/" + str(total+1) + ")")
            if enabled > 0:
                self.foldersMenu[folder].setIcon(self.icon["folder_active"])
            else:
                self.foldersMenu[folder].setIcon(self.icon["folder_inactive"])
            self.foldersMenu[folder].addSeparator()
            self.foldersMenu[folder].addAction(self.icon["folder_active"], "Load all", lambda folder=folder: self._folderEnable(folder))
            self.foldersMenu[folder].addAction(self.icon["folder_inactive"], "Unload all", lambda folder=folder: self._folderUnload(folder))
            self.foldersMenu[folder].addAction(self.icon["rename"], "Rename folder", lambda folder=folder: self._folderRenamePrompt(folder))
            self.foldersMenu[folder].addAction(self.icon["delete"], "Delete folder", lambda folder=folder: self._folderDelete(folder))
            self.menu.addMenu(self.foldersMenu[folder])

    def _menuListNotes(self):
        noteList = []
        # Sort children list, add notes without folder first
        for name in sorted(self.children, key=str.lower):
            if name.count("/") == 0:
                noteList.append(name)

        for name in sorted(self.children, key=str.lower):
            if name.count("/") > 0:
                noteList.append(name)

        # Define the appropriate icon
        for name in noteList:
            if self.children[name].profile.query("pin"):
                icon = self.icon["file_pinned"]
            elif name in self.preferences.query("actives"):
                icon = self.icon["file_active"]
            elif self.children[name].extension == ".png":
                icon = self.icon["file_image"]
            else:
                icon = self.icon["file_inactive"]
            self.menu.addAction(icon, self.children[name].fullname, self.children[name].noteDisplay)

    def _menuRefresh(self):
        # Monitor changes in the database directory
        self.folderLoad(self.preferences.query("general", "notesDb"))
        self._noteCleanOrphans()
        self._noteCleanProfiles()

        # Generate dynamic menu
        self.menu.clear()
        for option in self.preferences.query("menus", "mother"):
            self._menuAddOption(option)

    def _noteCleanEmpty(self):
        notesDir = self.preferences.query("general", "notesDb")
        for f in os.listdir(notesDir):
            if os.path.isdir(notesDir + f):
                for note in os.listdir(notesDir + f):
                    if os.stat(notesDir + f + "/" + note).st_size == 0:
                        os.remove(notesDir + f + "/" + note)
                        logger.warning("Removed '" + note + "' (empty)")
            else:
                if os.stat(notesDir + f).st_size == 0:
                    os.remove(notesDir + f)
                    logger.warning("Removed '" + f + "' (empty)")

    def _noteCleanOrphans(self):
        for f in list(self.children):
            if not os.path.isfile(self.children[f].path):
                logger.warning("Removed '" + self.children[f].fullname + "' (orphan)")
                self.children[f].noteDelete()

    def _noteCleanProfiles(self):
        if os.path.isfile(PROFILES_FILE):
            notesDir = self.preferences.query("general", "notesDb")
            with open(PROFILES_FILE, "r+") as db:
                profiles = json.load(db)
                for entry in list(profiles):
                    txtPath = notesDir + entry + ".txt"
                    pngPath = notesDir + entry + ".png"
                    if not os.path.isfile(pngPath) and not os.path.isfile(txtPath):
                        del profiles[entry]
                db.seek(0)
                db.truncate()
                db.write(json.dumps(profiles, indent=2, sort_keys=False))

    def _noteCleanUnloaded(self):
        notesDir = self.preferences.query("general", "notesDb")
        for note in self.preferences.db["unloaded"]:
            path = notesDir + note
            if not os.path.isfile(path + ".txt") and not os.path.isfile(path + ".png"):
                self.preferences.db["unloaded"].remove(note)
        self.preferences.save()

    def _noteLoad(self, path):
        notesDir = self.preferences.query("general", "notesDb")
        extension = os.path.splitext(path)[1]
        fullname = path[len(notesDir):-len(extension)]
        if fullname in self.preferences.db["unloaded"]:
            self.preferences.db["unloaded"].remove(fullname)
            self.preferences.save()
        if fullname not in self.children:
            self.children[fullname] = Child(self, path, popup=True)

    def _noteUnload(self, child):
        if child.fullname not in self.preferences.db["unloaded"]:
            self.preferences.db["unloaded"].append(child.fullname)
            self.preferences.save()
        child.noteClose()

    def cssLoad(self):
        configPath = os.path.expanduser("~/.config/qtpad/")
        stylesheet = ""
        for f in os.listdir(configPath):
            if os.path.splitext(f)[1] == ".css":
                with open(configPath + f) as f:
                    stylesheet += f.read() + "\n"
        app.setStyleSheet(stylesheet)

    def folderList(self, root):
        folders = []
        for folder in os.listdir(root):
            if not folder == ".trash" and os.path.isdir(root + folder):
                folders.append(folder)
        return sorted(folders, key=str.lower)

    def folderLoad(self, folder):
        notesDir = self.preferences.query("general", "notesDb")
        folder = folder[len(notesDir):]
        if folder:
            folder = folder + "/"

        # Create a new note if needed
        for f in os.listdir(notesDir + folder):
            name = folder + f.rsplit('.', 1)[0]
            if os.path.isfile(notesDir + folder + f):
                if name not in self.preferences.db["unloaded"] and name not in self.children:
                    path = notesDir + folder + f
                    if f.endswith(".txt"):
                        self.children[name] = Child(self, path)
                    elif f.endswith(".png"):
                        self.children[name] = Child(self, path, image=QtGui.QPixmap(f))

    def folderLoadEnabled(self):
        notesDir = self.preferences.query("general", "notesDb")
        for folder in self.folderList(notesDir):
            self.folderLoad(notesDir + folder)

    def noteAction(self, action, cmd=None):
        action = action.lower()
        if action == "none":
            pass

        elif action == "new note":
            self.noteNew()

        elif action == "load all folders":
            self._folderLoadAll()

        elif action == "unload all folders":
            self._folderUnloadAll()

        elif action == "fetch clipboard":
            fetch = self._clipboardFetch(newNote=True)

        elif action == "fetch clipboard or new note":
            fetch = self._clipboardFetch(newNote=True)
            if not fetch:
                self.noteNew()

        elif action == "toggle actives":
            actives = []
            for name in self.children:
                children = self.children[name]
                if children.profile.query("pin"):
                    children.activateWindow()
                elif children.isVisible():
                    actives.append(children.fullname)

            if actives:
                self.preferences.set("actives", actives)
                self.noteAction("hide all")
            elif self.preferences.query("actives"):
                for note in self.preferences.query("actives"):
                    if note in self.children:
                        self.children[note].noteDisplay()

        elif action == "hide all":
            for name in list(self.children):
                children = self.children[name]
                if children.isVisible() and not children.profile.query("pin"):
                    children.close()

        elif action == "show all":
            for name in self.children:
                if not self.children[name].isVisible():
                    self.children[name].noteDisplay()

        elif action == "reverse all":
            for name in list(self.children):
                children = self.children[name]
                if children.isVisible():
                    if not children.profile.query("pin"):
                        children.close()
                else:
                    children.noteDisplay()

        elif action == "reset positions":
            n = 0
            _x = QtWidgets.QDesktopWidget().screenGeometry().width() - self.preferences.query("styleDefault", "width")
            _y = self.preferences.query("styleDefault", "height") / 2
            width = self.preferences.query("styleDefault", "width")
            height = self.preferences.query("styleDefault", "height")
            for name in self.children:
                children = self.children[name]
                n += 28
                x = _x - n
                y = _y + n
                children.noteDisplay()
                children.setGeometry(x, y, width, height)
                children.profile.load()
                children.profile.set("x", x)
                children.profile.set("y", y)
                children.profile.set("width", width)
                children.profile.set("height", height)
                children.profile.save()

        elif action == "exec":
            if cmd:
                logger.info("Starting '%s'", cmd)
                slave = QtCore.QProcess()
                slave.startDetached(cmd)

        else:
            logger.error("Invalid main menu option '%s'" % action)

    def noteNew(self, image=None, text=None):
        notesDir = self.preferences.query("general", "notesDb")
        if image:
            prefix = self.preferences.query("general", "nameImage")
        else:
            prefix = self.preferences.query("general", "nameText")

        name = getNameIndex(prefix, self.children)
        if image:
            self.children[name] = Child(self, notesDir + name + ".png", popup=True, image=image)
        else:
            self.children[name] = Child(self, notesDir + name + ".txt", popup=True, text=text)
        return name


class SearchForm(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()

        # Load the ui file in case the gui modules are not loaded
        if "qtpad.gui_search" in sys.modules:
            self.ui = qtpad.gui_search.Ui_Form()
            self.ui.setupUi(self)
        else:
            self.ui = uic.loadUi(LOCAL_DIR + 'gui_search.ui', self)

        self.parent = parent
        self.active = None
        self.setFixedSize(490, 100)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.installEventFilter(self)
        self.ui.searchFindButton.clicked.connect(self._find)
        self.ui.searchFindAllButton.clicked.connect(self._findAll)
        self.ui.searchReplaceButton.clicked.connect(self._replace)
        self.ui.searchReplaceAllButton.clicked.connect(self._replaceAll)

    def eventFilter(self, object, event):
        eventType = event.type()
        if eventType == QtCore.QEvent.Show:
            self._updateTitle()
            self.ui.searchFindLine.setText(self.active.ui.textEdit.textCursor().selectedText())
        elif eventType == QtCore.QEvent.FocusIn or eventType == QtCore.QEvent.Enter:
            self._updateTitle()
        return QtCore.QObject.event(object, event)

    def _find(self):
        next = self.active.ui.textEdit.find(self.ui.searchFindLine.text(), self._getFlag())
        if not next and self.ui.searchWrapBox.isChecked():
            self.active.ui.textEdit.moveCursor(QtGui.QTextCursor.Start)
            self.active.ui.textEdit.find(self.ui.searchFindLine.text(), self._getFlag())

    def _findAll(self, find=""):
        # Allow override or searched text
        if not find:
            find = self.ui.searchFindLine.text()

        # Remove previous underlines
        extraSelections = self.active.ui.textEdit.extraSelections()
        for extra in extraSelections:
            extra.format.setFontUnderline(False)

        # Underline all results
        self.active.ui.textEdit.moveCursor(QtGui.QTextCursor.Start)
        while self.active.ui.textEdit.find(find, self._getFlag()):
            extra = QtWidgets.QTextEdit.ExtraSelection()
            extra.cursor = self.active.ui.textEdit.textCursor()
            extra.format.setFontUnderline(True)
            extraSelections.append(extra)

        # Apply result and clear selection
        self.active.ui.textEdit.setExtraSelections(extraSelections)
        self.active.ui.textEdit.moveCursor(QtGui.QTextCursor.Start)

    def _getFlag(self):
        flag = QtGui.QTextDocument.FindFlags(0)
        if self.ui.searchCaseBox.isChecked():
            flag = flag | QtGui.QTextDocument.FindCaseSensitively
        if self.ui.searchWholeBox.isChecked():
            flag = flag | QtGui.QTextDocument.FindWholeWords
        return flag

    def _replace(self):
        find = self.ui.searchFindLine.text()
        replace = self.ui.searchReplaceLine.text()
        cursor = self.active.ui.textEdit.textCursor()
        if find.lower() == cursor.selectedText().lower():
            cursor.insertText(replace)
            self.active.noteTextSave()
        self._find()

    def _replaceAll(self):
        find = self.ui.searchFindLine.text()
        replace = self.ui.searchReplaceLine.text()
        extraSelections = self.active.ui.textEdit.extraSelections()
        cursor = self.active.ui.textEdit.textCursor()

        self.active.ui.textEdit.moveCursor(QtGui.QTextCursor.Start)
        while self.active.ui.textEdit.find(find, self._getFlag()):
            extra = QtWidgets.QTextEdit.ExtraSelection()
            extra.cursor = self.active.ui.textEdit.textCursor()
            end = extra.cursor.position()
            start = end - len(find)
            cursor.setPosition(start)
            cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            cursor.insertText(replace)
            extraSelections.append(extra)
        self.active.ui.textEdit.setExtraSelections(extraSelections)
        self.active.ui.textEdit.moveCursor(QtGui.QTextCursor.Start)
        self._findAll(replace)  # Underline replaced text
        self.active.noteTextSave()

    def _updateActive(self):
        for name in self.parent.children:
            child = self.parent.children[name]
            if child.isVisible() and child.extension == ".txt":
                return child
        return None

    def _updateTitle(self):
        # Fallback to another opened note if last active is deleted or closed
        if not self.parent.lastActive.fullname:
            self.active = self._updateActive()
        elif not self.parent.lastActive.isVisible():
            self.active = self._updateActive()
        else:
            self.active = self.parent.lastActive

        # Hide orphan search form
        if self.active is None:
            self.hide()
        else:
            self.setWindowTitle("Search in '%s'" % self.active.fullname)


class QDBusServer(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.__dbusAdaptor = QDBusServerAdapter(self)


class QDBusServerAdapter(QtDBus.QDBusAbstractAdaptor):
    QtCore.Q_CLASSINFO("D-Bus Interface", "org.qtpad.session")
    QtCore.Q_CLASSINFO("D-Bus Introspection",
    '  <interface name="org.qtpad.session">\n'
    '    <method name="parse">\n'
    '      <arg direction="in" type="s" name="cmd"/>\n'
    '    </method>\n'
    '  </interface>\n')

    def __init__(self, parent):
        super().__init__(parent)

    @QtCore.pyqtSlot(str)
    def parse(self, cmd):
        if cmd:
            # Serialize the string of commands into a dictionnary
            current = ""
            commands = {}
            for arg in cmd.split("%"):
                if arg.startswith("-"):
                    current = arg.lstrip("-")
                elif current:
                    commands[current].append(arg)
                if current not in commands:
                    commands[current] = []

            # Pass the commands object to the main parser
            mother._cmdParse(commands)


def main(cmd=None, arg=None):
    global app, mother
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    bus = QtDBus.QDBusConnection.sessionBus()
    server = QDBusServer()
    bus.registerObject('/org/qtpad/session', server)
    bus.registerService('org.qtpad.session')
    mother = Mother()

    # Handle init command (if any)
    if cmd and arg:
        mother.parse(cmd, arg)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
