from __future__ import print_function
import argparse
import time
from dash_import.import_factory import ImportFactory
import sys
import configuration

def diet_main():
    parser = argparse.ArgumentParser(description='Dash Import and Export Tool')

    parser.add_argument('direction', choices=['import', 'export'], type=str,
                        help='Action to permform')
    parser.add_argument('target', type=str,
                        help='The target of the import/export')
    parser.add_argument('files', metavar='file', type=file, nargs='+',
                        help='Files to import')

    args = parser.parse_args()

    config = configuration.DietConfiguration.load_from_home_dir()

    if args.direction == 'import':
        importer = ImportFactory().get_importer(target=args.target, configuration=config)

        if importer is None:
            print('Invalid target given')
            sys.exit(1)
        else:
            for import_file in args.files:
                importer.import_from_file(file=import_file)
                import_file.close()
    elif args.direction == 'export':
        print("Export has not been implemented yet")
