import argparse
import numpy
import os

# Nice str2bool suggestion from Maxim ( https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse )


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def DICregularGridParser(parser):
    parser.add_argument('-nompi',
                        action="store_false",
                        dest='MPI',
                        help='Activate MPI parallelisation?')

    parser.add_argument('inFiles',
                        nargs='+',
                        type=argparse.FileType('r'),
                        help="A space-separated list of two 3D greyscale tiff files to correlate, in order")

    parser.add_argument('-mf1',
                        '--maskFile1',
                        dest='MASK1',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to tiff file containing the mask of image 1 -- masks  zones not to correlate")

    parser.add_argument('-mf2',
                        '--maskFile2',
                        dest='MASK2',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to tiff file containing the mask of image 2 -- masks correlation windows")

    parser.add_argument('-Ffile',
                        dest='FFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to TSV file containing initial F guess, can be single-point registration or multiple point correlation. Default = None")

    parser.add_argument('-Ffb',
                        '--Ffile-bin-ratio',
                        type=int,
                        default=1,
                        dest='FFILE_BIN_RATIO',
                        help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    parser.add_argument('-glt',
                        '--grey-low-threshold',
                        type=float,
                        default=-numpy.inf,
                        dest='GREY_LOW_THRESH',
                        help="Grey threshold on mean of reference imagette BELOW which the correlation is not performed. Default = -infinity")

    parser.add_argument('-ght',
                        '--grey-high-threshold',
                        type=float,
                        default=numpy.inf,
                        dest='GREY_HIGH_THRESH',
                        help="Grey threshold on mean of reference imagette ABOVE which the correlation is not performed. Default = infinity")

    parser.add_argument('-reg',
                        '--registration',
                        action="store_true",
                        dest='REG',
                        help='Perform an initial registration? Default = False')

    parser.add_argument('-regb',
                        '--registration-binning',
                        type=int,
                        default=1,
                        dest='REG_BIN',
                        help='Binning to apply to input images for registration. Default = 1')

    parser.add_argument('-regm',
                        '--registration-margin',
                        type=float,
                        default=0.1,
                        dest='REG_MARGIN',
                        help='Registration margin in proportions of image size. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-nops',
                        '--no-pixel-search',
                        action="store_false",
                        dest='PS',
                        help='Disactivate pixel search?')

    parser.add_argument('-psr',
                        '--pixel-search-range',
                        nargs=6,
                        type=int,
                        default=[-3, 3, -3, 3, -3, 3],
                        dest='PSR',
                        help='Z- Z+ Y- Y+ X- X+ ranges (in pixels) for the pxiel search. Requires pixel search to be activated. Default = +-3px')

    parser.add_argument('-psf',
                        '--pixel-search-filter',
                        type=int,
                        default=0,
                        dest='PS_FILTER',
                        help='Median filter pixel search results. Default = 0')

    # Default: node spacing equal in all three directions
    parser.add_argument('-ns',
                        '--node-spacing',
                        nargs=1,
                        type=int,
                        default=None,
                        dest='NS',
                        help="Node spacing in pixels (assumed equal in all 3 directions -- see -ns3 for different setting). Default = 10px")

    # Possible: node spacing different in all three directions
    parser.add_argument('-ns3',
                        '--node-spacing-3',
                        nargs=3,
                        type=int,
                        default=None,
                        dest='NS',
                        help="Node spacing in pixels (different in 3 directions). Default = 10, 10, 10px")

    # Default: window size equal in all three directions
    parser.add_argument('-hws',
                        '--half-window-size',
                        nargs=1,
                        type=numpy.uint,
                        default=None,
                        dest='HWS',
                        help="Half correlation window size, measured each side of the node pixel (assumed equal in all 3 directions -- see -hws3 for different setting). Default = 10px")

    # Possible: node spacing different in all three directions
    parser.add_argument('-hws3',
                        '--half-window-size-3',
                        nargs=3,
                        type=int,
                        default=None,
                        dest='HWS',
                        help="Half correlation window size, measured each side of the node pixel (different in 3 directions). Default = 10, 10, 10px")

    parser.add_argument('-nosp',
                        '--no-subpixel',
                        action="store_false",
                        dest='SUBPIXEL',
                        help='Disactivate subpixel refinement?')

    parser.add_argument('-spm',
                        '--sub-pixel-margin',
                        nargs=1,
                        type=numpy.uint,
                        default=[3],
                        dest='SUBPIXEL_MARGIN',
                        help="Subpixel margin for subpixel interpolation. Default = 3px")

    parser.add_argument('-spm3',
                        '--sub-pixel-margin3',
                        nargs=3,
                        type=numpy.uint,
                        default=None,
                        dest='SUBPIXEL_MARGIN',
                        help="Subpixel margin for subpixel interpolation. Default = 3px")

    parser.add_argument('-spi',
                        '--sub-pixel-max-iterations',
                        type=numpy.uint,
                        default=10,
                        dest='SUBPIXEL_MAX_ITERATIONS',
                        help="Subpixel max iterations subpixel search. Default = 10")

    parser.add_argument('-spf',
                        '--sub-pixel-min-f-change',
                        type=numpy.float,
                        default=0.001,
                        dest='SUBPIXEL_MIN_F_CHANGE',
                        help="Subpixel min change in F to stop subpixel search. Default = 0.001")

    parser.add_argument('-spo',
                        '--sub-pixel-interpolation-order',
                        type=numpy.uint,
                        default=1,
                        dest='SUBPIXEL_INTERPOLATION_ORDER',
                        help="Subpixel interpolation order. Default = 1")

    parser.add_argument('-cif',
                        '--correct-input-field',
                        action="store_true",
                        dest='CF',
                        help='Correction of the input F field. Default = True')

    parser.add_argument('-nfi',
                        '--neighbours-for-field-interpolation',
                        type=numpy.uint,
                        default=12,
                        dest='NEIGHBOURS',
                        help="Neighbours for field interpolation. Default = 12")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help="Prefix for output files. Default is basename of input file (without extension)")

    parser.add_argument('-vtk',
                        '--VTKout',
                        action="store_true",
                        dest='VTK',
                        help='Activate VTK output format. Default = False')

    parser.add_argument('-tsv',
                        '--TSVout',
                        action="store_true",
                        dest='TSV',
                        help='Activate TSV output format. Default = False')

    parser.add_argument('-tif',
                        '-tiff',
                        '--TIFFout',
                        '--TIFout',
                        action="store_true",
                        dest='TIF',
                        help='Activate TIF output format. Default = False')

    args = parser.parse_args()

    # 2018-03-24 check for 2D without loading images
    import tifffile
    if len(tifffile.memmap(args.inFiles[0].name).shape) == 2:
        twoD = True
    else:
        twoD = False

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFiles[0].name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                data.DIR_out = os.path.dirname(args.inFiles[0].name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.inFiles[0].name))[0]

    # Catch interdependent node spacing and correlation window sizes
    if args.NS is None:
        print("\nUsing default node spacing: "),
        if args.HWS is None:
            print("2x default half window size"),
            args.HWS = [10]
            print("({}) which is".format(args.HWS[0])),
            args.NS = [args.HWS[0] * 2]
        else:
            print("2x user-set half window size"),
            if len(args.HWS) == 1:
                print("({}) which is".format(args.HWS[0])),
                args.NS = [int(args.HWS[0] * 2)]
            elif len(args.HWS) == 3:
                print("({} -- selecting smallest) which is".format(args.HWS)),
                args.NS = [int(min(args.HWS) * 2)]
        print(args.NS)

    # Catch 3D options
    if len(args.NS) == 1:
        args.NS = [args.NS[0], args.NS[0], args.NS[0]]
    if len(args.HWS) == 1:
        args.HWS = [args.HWS[0], args.HWS[0], args.HWS[0]]
    if len(args.SUBPIXEL_MARGIN) == 1:
        args.SUBPIXEL_MARGIN = [args.SUBPIXEL_MARGIN[0], args.SUBPIXEL_MARGIN[0], args.SUBPIXEL_MARGIN[0]]

    if type(args.SUBPIXEL_MAX_ITERATIONS) == list:
        args.SUBPIXEL_MAX_ITERATIONS = args.SUBPIXEL_MAX_ITERATIONS[0]

    # Catch and overwrite 2D options
    if twoD:
        args.NS[0] = 1
        args.HWS[0] = 0
        args.SUBPIXEL_MARGIN[0] = 0

    # Make sure at least one output format has been asked for
    if args.VTK + args.TSV + args.TIF == 0:
        print("#############################################################")
        print("#############################################################")
        print("###  WARNING: No output type of VTK, TSV and TIF options  ###")
        print("###  Are you sure this is right?!                         ###")
        print("#############################################################")
        print("#############################################################")

    if args.REG_MARGIN > 0.45:
        print("Registration margin cannot be bigger than 0.45 since 0.5 would contain no data!!")

    return args


def DICdiscreteParser(parser):

    parser.add_argument('im1',
                        metavar='im1',
                        type=argparse.FileType('r'),
                        help="Greyscale image of reference state for correlation")

    parser.add_argument('lab1',
                        metavar='lab1',
                        type=argparse.FileType('r'),
                        help="Labelled image of reference state for correlation")

    parser.add_argument('im2',
                        metavar='im2',
                        type=argparse.FileType('r'),
                        help="Greyscale image of deformed state for correlation")

    parser.add_argument('-nops',
                        '--no-pixel-search',
                        action="store_false",
                        dest='PS',
                        help='Disactivate pixel search?')

    parser.add_argument('-psr',
                        '--pixel-search-range',
                        nargs=6,
                        type=int,
                        default=[-3, 3, -3, 3, -3, 3],
                        dest='PSR',
                        help='Z- Z+ Y- Y+ X- X+ ranges (in pixels) for the pxiel search. Requires pixel search to be activated. Default = +-3px')

    parser.add_argument('-nosp',
                        '--no-subpixel',
                        action="store_false",
                        dest='SUBPIXEL',
                        help='Disactivate subpixel refinement?')

    parser.add_argument('-ld',
                        '--label-dilate',
                        type=int,
                        default=1,
                        dest='LABEL_DILATE',
                        help="Number of times to dilate labels. Default = 1")

    parser.add_argument('-vt',
                        '--volume-threshold',
                        type=numpy.uint,
                        default=100,
                        dest='VOLUME_THRESHOLD',
                        help="Volume threshold below which labels are ignored. Default = 100")

    parser.add_argument('-reg',
                        '--registration',
                        action="store_true",
                        dest='REG',
                        help='Perform an initial registration? Default = False')

    parser.add_argument('-regb',
                        '--registration-binning',
                        type=int,
                        default=1,
                        dest='REG_BIN',
                        help='Binning to apply to input images for registration. Default = 1')

    parser.add_argument('-regm',
                        '--registration-margin',
                        type=float,
                        default=0.1,
                        dest='REG_MARGIN',
                        help='Registration margin in proportions of image size. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-Ffile',
                        dest='FFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to TSV file containing initial F guess, can be single-point registration or multiple point correlation. Default = None")

    parser.add_argument('-Ffb',
                        '--Ffile-bin-ratio',
                        type=int,
                        default=1,
                        dest='FFILE_BIN_RATIO',
                        help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    parser.add_argument('-cif',
                        '--correct-input-field',
                        action="store_true",
                        dest='CF',
                        help='Correction of the input F field. Default = True')

    parser.add_argument('-nfi',
                        '--neighbours-for-field-interpolation',
                        type=numpy.uint,
                        default=12,
                        dest='NEIGHBOURS',
                        help="Neighbours for field interpolation. Default = 12")

    parser.add_argument('-nomask',
                        '--no-mask',
                        action="store_false",
                        dest='MASK',
                        help='Don\'t mask each label\'s image')

    parser.add_argument('-spm',
                        '--sub-pixel-margin',
                        type=numpy.uint,
                        default=2,
                        dest='SUBPIXEL_MARGIN',
                        help="Subpixel margin for subpixel interpolation. Default = 3px")

    parser.add_argument('-spi',
                        '--sub-pixel-max-iterations',
                        type=numpy.uint,
                        default=10,
                        dest='SUBPIXEL_MAX_ITERATIONS',
                        help="Subpixel max iterations subpixel search. Default = 10")

    parser.add_argument('-spf',
                        '--sub-pixel-min-f-change',
                        type=numpy.float,
                        default=0.001,
                        dest='SUBPIXEL_MIN_F_CHANGE',
                        help="Subpixel min change in F to stop subpixel search. Default = 0.001")

    parser.add_argument('-spo',
                        '--sub-pixel-interpolation-order',
                        type=numpy.uint,
                        default=1,
                        dest='SUBPIXEL_INTERPOLATION_ORDER',
                        help="Subpixel interpolation order. Default = 3")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help="Prefix for output files. Default is basename of input file (without extension)")

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.lab1.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                data.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    #  sub pixel margin must be at least as big as label dilate
    if args.LABEL_DILATE >= args.SUBPIXEL_MARGIN:
        print("Warning, \"label dilate\" is less than to \"sub pixel margin\", overriding")
        args.SUBPIXEL_MARGIN = args.LABEL_DILATE

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0]+"-"+os.path.splitext(os.path.basename(args.im2.name))[0]

    return args


def multiModalRegistrationParser(parser):
    import spam.DIC.transformationOperator
    import numpy

    parser.add_argument('im1',
                        metavar='im1',
                        type=argparse.FileType('r'),
                        help="Greyscale image of reference state for correlation")

    parser.add_argument('im2',
                        metavar='im2',
                        type=argparse.FileType('r'),
                        help="Greyscale image of deformed state for correlation")

    parser.add_argument('-im1min',
                        type=float,
                        default=None,
                        dest='IM1_MIN',
                        help="Minimum of im1 for greylevel scaling. Default = im1.min()")

    parser.add_argument('-im1max',
                        type=float,
                        default=None,
                        dest='IM1_MAX',
                        help="Maximum of im1 for greylevel scaling. Default = im1.max()")

    parser.add_argument('-im2min',
                        type=float,
                        default=None,
                        dest='IM2_MIN',
                        help="Minimum of im2 for greylevel scaling. Default = im2.min()")

    parser.add_argument('-im2max',
                        type=float,
                        default=None,
                        dest='IM2_MAX',
                        help="Maximum of im2 for greylevel scaling. Default = im2.max()")

    parser.add_argument('-im1th',
                        '--im1-threshold',
                        type=int,
                        default=0,
                        dest='IM1_THRESHOLD',
                        help='Greylevel threshold for image 1. Below this threshold, peaks in the histogram are ignored.')

    parser.add_argument('-im2th',
                        '--im2-threshold',
                        type=int,
                        default=0,
                        dest='IM2_THRESHOLD',
                        help='Greylevel threshold for image 2. Below this threshold, peaks in the histogram are ignored.')

    parser.add_argument('-bin',
                        '--bin-levels',
                        type=int,
                        default=1,
                        dest='NBINS',
                        help='Number of binning levels to apply to the data (if given 3, the binning levels used will be 4 2 1). The -phase option is necessary and should define this many phases (i.e., 3 different numbers in this example)')

    parser.add_argument('-ph',
                        '--phases',
                        nargs='+',
                        type=int,
                        default=[2],
                        dest='PHASES',
                        help='Disactivate subpixel refinement?')

    parser.add_argument('-jhb',
                        '--joint-histogram-bins',
                        # nargs=1,
                        type=int,
                        default=128,
                        dest='JOINT_HISTO_BINS',
                        help='The number of greylevel bins for both images in the joint histogram')

    parser.add_argument('-dst',
                        '--dist-between-max',
                        type=int,
                        default=None,
                        dest='DIST_BETWEEN_MAX',
                        help='Minimal distance between two maxima in the histogram')

    parser.add_argument('-fdi',
                        '--fit-distance',
                        type=float,
                        default=None,
                        dest='FIT_DISTANCE',
                        help='Distance considered around a peak for the Gaussian ellipsoid fitting')

    parser.add_argument('-voc',
                        '--voxel-coverage',
                        type=float,
                        default=1.0,
                        dest='VOXEL_COVERAGE',
                        help='Percentage (between 0 and 1) of voxel coverage of the phases in the joint histogram')

    parser.add_argument('-int',
                        '--interactive',
                        action="store_true",
                        dest='INTERACTIVE',
                        help='Present live-updating plots to the user')

    parser.add_argument('-gra',
                        '--graphs',
                        action="store_true",
                        dest='GRAPHS',
                        help='Save graphs to file')

    parser.add_argument('-ssl',
                        '--show-slice-axis',
                        type=int,
                        default=0,
                        dest='SHOW_SLICE_AXIS',
                        help='Axis of the cut used for the plots')

    # parser.add_argument('-tmp',
    #                     '--writeTemporaryFiles',
    #                     action="store_true",
    #                     dest='DATA',
    #                     help='Save temporary files (joint histogram) to \"dat\" file')

    parser.add_argument('-loadprev',
                        '--load-previous-iteration',
                        action="store_true",
                        dest='LOADPREV',
                        help='Load output pickle files from previous iterations (2* coarser binning)')

    parser.add_argument('-mar',
                        '--margin',
                        type=float,
                        default=0.1,
                        dest='MARGIN',
                        help='Margin of both images. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-cro',
                        '--crop',
                        type=float,
                        default=0.1,
                        dest='CROP',
                        help='Initial crop of both images. Default = 0.1, which means 0.1 * image size from both sides')

    # Remove next two arguments for F input, and replace with displacement and rotation inputs on command line
    # parser.add_argument('-Ffile',
    # dest='FFILE',
    # default = None,
    # type=argparse.FileType('r'),
    # help="Path to TSV file containing initial F guess, can be single-point registration or multiple point correlation. Default = None")

    # parser.add_argument('-Ffb',
    # '--Ffile-bin-ratio',
    # type=int,
    # default=1,
    # dest='FFILE_BIN_RATIO',
    # help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    parser.add_argument('-tra',
                        '--translation',
                        nargs=3,
                        type=float,
                        default=None,
                        dest='TRA',
                        help="Z, Y, X initial displacements to apply at the bin 1 scale")

    parser.add_argument('-rot',
                        '--rotation',
                        nargs=3,
                        type=float,
                        default=None,
                        dest='ROT',
                        help="Z, Y, X components of rotation vector to apply at the bin 1 scale")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help="Prefix for output files. Default is basename of input file (without extension)")

    args = parser.parse_args()

    # The number of bin levels must be the same as the number of phases
    if (args.NBINS != len(args.PHASES)):
        print("\toptionsParser.multiModalRegistrationParser(): Number of bin levels and number of phases not the same, exiting")
        exit()

    # For back compatibility, generate list of bins
    args.BINS = []
    for i in range(args.NBINS)[::-1]:
        args.BINS.append(2**i)

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.im1.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                data.DIR_out = os.path.dirname(args.im1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Get initial guesses
    if args.TRA is not None or args.ROT is not None:
        transformation = dict({})
        if args.TRA is not None:
            transformation['t'] = args.TRA
        if args.ROT is not None:
            transformation['r'] = args.ROT
        Fguess = spam.DIC.transformationOperator.computeTransformationOperator(transformation)
        args.FGUESS = Fguess
    else:
        args.FGUESS = numpy.eye(4)

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0]+"-"+os.path.splitext(os.path.basename(args.im2.name))[0]

    return args
