import sys
from extractCMRRPhysio import unwrapper


def run():

    if len(sys.argv) != 3:
        print('extract_cmrr_physio dicom_filename output_path')
        sys.exit(1)

    filename = sys.argv[1]
    output_path = sys.argv[2]

    uw = unwrapper.Unwrapper(filename, output_path)
    uw.apply()
