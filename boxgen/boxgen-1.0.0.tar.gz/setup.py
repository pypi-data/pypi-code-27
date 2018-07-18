from distutils.cmd import Command
import setuptools

from pathlib import Path

class TwineUploadCommand(Command):
    description = "use Twine to upload your package."
    # TODO: Allow specifying +dist+ directory.
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from twine.cli import dispatch as twine
        files = map(str, Path().glob("dist/*"))
        twine(["upload", *files])

setuptools.setup(
    cmdclass={"release": TwineUploadCommand},
)
