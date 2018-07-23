from __future__ import print_function
import argparse
import time
import import_factory
import sys
import configuration

def diet_main():
    parser = argparse.ArgumentParser(description='Dash Import and Export Tool')

    parser.add_argument('direction', choices=['import', 'export'], type=str,
                        help='Action to perform')
    parser.add_argument('target', choices=list(import_factory.get_importer()), type=str,
                        help='The target of the import/export')
    parser.add_argument('files', metavar='file', type=file, nargs='+',
                        help='Files to import')

    args = parser.parse_args()

    config = configuration.DietConfiguration.load_from_home_dir()

    if args.direction == 'import':
        importer = import_factory.get_importer(configuration=config)

        for import_file in args.files:
            importer[args.target].import_from_file(file=import_file)
            import_file.close()
    elif args.direction == 'export':
        print("Export has not been implemented yet")
