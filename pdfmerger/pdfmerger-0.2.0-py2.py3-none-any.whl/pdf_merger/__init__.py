from PyPDF2 import PdfFileMerger


def merge(input_file_objs, output_file_obj):
    merger = PdfFileMerger()
    for file_obj in input_file_objs:
        merger.append(file_obj)

    merger.write(output_file_obj)

    merger.close()


__all__ = [
    'merge',
]
