from PyPDF2 import PdfFileMerger


def merge(paths, output):
    merger = PdfFileMerger()
    for path in paths:
        merger.append(path)

    with open(output, 'wb') as f:
        merger.write(f)


__all__ = [
    'merge',
]
