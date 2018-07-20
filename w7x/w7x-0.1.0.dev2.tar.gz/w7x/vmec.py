"""
vmec tools revolving around the Run class
"""
import copy
import json
import os
import numpy as np
import time
import logging
import warnings
import pathlib
import tfields
import sympy
from symfit import Variable, Fit, Model, parameters, variables
import w7x
try:
    import transcoding as tc
except ImportError:
    warnings.warn("transcoding not found. You will not be able to parse files.",
                  ImportWarning)
    tc = None


class TooLongError(ValueError):
    pass


THISDIR = pathlib.Path(__file__).resolve()


def fit(fun, x, y):
    """
    Fit a sympy function fun with data x, y
    """
    f = Variable("f")
    model = Model({f: fun})
    fit = Fit(model, x, y)
    res = fit.execute()
    fun = model[f]
    for p in res.params:
        fun = fun.subs(p, res.params.get_value(p))
    return fun


def pad(seq, targetLength, padding=None):
    """
    Extend the sequence seq with padding (default: None) so as to make
    its length up to targetLength. Return copy of seq. If seq is already
    longer than targetLength, raise TooLongError.

    Examples:
        >>> from w7x.vmec import pad
        >>> pad([], 5, 1)
        [1, 1, 1, 1, 1]
        >>> pad([1, 2, 3], 7)
        [1, 2, 3, None, None, None, None]
        >>> pad([1, 2, 3], 2)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
          ...
        TooLongError: sequence too long (3) for target length 2

    """
    seq = seq[:]
    length = len(seq)
    if length > targetLength:
        raise TooLongError("sequence too long ({}) for target length {}"
                           .format(length, targetLength))
    seq.extend([padding] * (targetLength - length))
    return seq


class Points3D(w7x.flt.Points3D):
    ws_server = w7x.Server.addr_vmec_server


class VMECBase(w7x.core.Base):
    ws_server = w7x.Server.addr_vmec_server


class Profile(VMECBase):
    prop_defaults = {
        'ProfileType': None,
        'coefficients': []
    }

    ws_class = "Profile"

    def __init__(self, *args, **kwargs):
        '''Remove 0s from coefficients'''
        if 'coefficients' in kwargs:
            while True:
                if len(kwargs['coefficients']) == 0:
                    break
                if kwargs['coefficients'][-1] != 0:
                    break
                kwargs['coefficients'].pop(-1)
        super(Profile, self).__init__(*args, **kwargs)

    def __call__(self, value):
        raise NotImplementedError("A Profile must implement the __call__"
                                  "function")

    def normalized(self):
        raise NotImplementedError("A Profile must implement the normalized"
                                  "function")

    def scale(self, scale):
        self.coefficients = [c * scale for c in self.coefficients]

    def deviation(self, other):
        """
        Returns the normalized deviation of the profiles.
        """
        if self.ProfileType != other.ProfileType:
            return np.inf
        l = max(len(self.coefficients), len(other.coefficients))
        dev = np.sqrt(float(sum(map(lambda x: (x[0] - x[1])**2,
                                    zip(pad(self.normalized(), l, padding=0),
                                        pad(other.normalized(), l, padding=0))))))
        return dev

    def plot(self, **kwargs):
        raise NotImplementedError("A Profile must implement the plot function")


class PowerSeries(Profile):
    prop_defaults = Profile.prop_defaults
    prop_defaults['ProfileType'] = 'power_series'
    prop_defaults['coefficients'] = [0]

    @property
    def norm(self):
        """
        the first coefficient
        """
        if len(self.coefficients) == 0:
            return 0
        return self.coefficients[0]

    @norm.setter
    def norm(self, norm):
        self.coefficients = [norm * x for x in self.normalized()]

    def normalized(self):
        """
        Returns:
            normalized coefficients
        """
        if len(self.coefficients) == 0:
            return []
        return [x * 1. / self.norm for x in self.coefficients]

    @classmethod
    def createDefaultPressure(cls, *args, **kwargs):
        kwargs['coefficients'] = kwargs.pop('coefficients', [1e-6, -1e-6])
        return cls(*args, **kwargs)

    def __call__(self, value):
        poly = np.polynomial.polynomial.Polynomial(self.coefficients)
        return poly.__call__(value)

    def plot(self, **kwargs):
        tfields.plotting.plot_function(self, **kwargs)


def createProfile(*args, **kwargs):
    """
    Factory method for profile creation
    """
    log = logging.getLogger()
    profileType = kwargs['ProfileType']
    if profileType == 'power_series' or 'spline' in profileType:
        return PowerSeries(*args, **kwargs)
    else:
        log.error("No Profile subclass matches type {profileType}.")
        return Profile(*args, **kwargs)


class FourierCoefficients(VMECBase):
    ws_class = "FourierCoefficients"
    prop_defaults = {
        'coefficients': None,
        'poloidalModeNumbers': None,  # m
        'toroidalModeNumbers': None,  # n
        'numRadialPoints': 0
    }

    def __init__(self, *args, **kwargs):
        super(FourierCoefficients, self).__init__(*args, **kwargs)
        # check coefficients for negative m=0,n<0 to be 0
        for i, n in enumerate(self.toroidalModeNumbers):
            # m = 0
            if n < 0:
                log = logging.getLogger()
                log.verbose("For m=0, n<0 coefficients may not be != 0. "
                            "Set them to be 0.")
                if self.coefficients[i] != 0.:
                    self.coefficients[i] = 0.
            else:
                break
        nCoeffs = len(self.coefficients)
        nTor = len(self.toroidalModeNumbers)
        mPol = len(self.poloidalModeNumbers)
        if not nCoeffs == nTor * mPol:
            raise ValueError("len(coeffs)({nCoeffs}) != nTor({nTor}) *"
                             " mPol({mPol})".format(**locals()))


class SurfaceCoefficients(VMECBase):
    ws_class = "surfaceCoefficients"
    prop_defaults = {
        'RCos': None,
        'ZSin': None,
        'RSin': None,
        'ZCos': None
    }

    def __init__(self, *args, **kwargs):
        super(SurfaceCoefficients, self).__init__(*args, **kwargs)
        """
        The wsDoku says you need to define hybrid but haukes code shows cylindrical.
        I will take default hybrid grid.
        It appears to not have any effect to change between the two.
        """
        if self.RCos is None:
            self.RCos = FourierCoefficients()
        if self.ZSin is None:
            self.ZSin = FourierCoefficients()

    def __call__(self, phi, theta):
        partsR = []
        partsZ = []

        i = 0
        for m in self.RCos.poloidalModeNumbers:
            for n in self.RCos.toroidalModeNumbers:
                part = self.RCos.coefficients[i] * np.cos(m * theta -
                                                          5 * n * phi)
                partsR.append(part)
                i += 1

        j = 0
        for m in self.ZSin.poloidalModeNumbers:
            for n in self.ZSin.toroidalModeNumbers:
                part = self.ZSin.coefficients[j] * np.sin(m * theta -
                                                          5 * n * phi)
                partsZ.append(part)
                j += 1
        return sum(partsR), sum(partsZ)

    @classmethod
    def createDefaultMagneticAxis(cls, *args, **kwargs):
        rcos = FourierCoefficients(coefficients=[5.54263e00, 1.84047e-1],
                                   poloidalModeNumbers=[0],
                                   toroidalModeNumbers=[0, 1],
                                   numRadialPoints=1)
        zsin = FourierCoefficients(coefficients=[0.00000, 1.57481e-01],
                                   poloidalModeNumbers=[0],
                                   toroidalModeNumbers=[0, 1],
                                   numRadialPoints=1)
        return cls(*args,
                   RCos=kwargs.pop('RCos', rcos),
                   ZSin=kwargs.pop('ZSin', zsin),
                   **kwargs)

    @classmethod
    def createDefaultBoundary(cls, *args, **kwargs):
        rcos = FourierCoefficients(
            coefficients=[-1.8275e-03, -2.8507e-04, -2.1739e-03,
                          2.6718e-01, 5.5289e+00, 2.6718e-01,
                          -2.1739e-03, -2.8507e-04, -1.8275e-03,
                          1.6341e-03, 1.2163e-03, 3.0809e-03,
                          3.4528e-02, 4.4872e-01, -2.7085e-01,
                          -4.9284e-03, 4.9911e-04, 6.5184e-05,
                          4.8734e-04, 1.4054e-03, 4.8047e-03,
                          1.5134e-02, 3.5687e-02, 4.9779e-02,
                          6.5200e-02, -1.1350e-02, -1.6119e-03,
                          1.0339e-04, -3.2332e-04, -3.4468e-04,
                          -1.5729e-03, -2.0611e-03, -1.4756e-02,
                          -1.9949e-02, -8.5802e-03, 3.8516e-03,
                          1.1352e-04, 3.6285e-04, 2.4647e-04,
                          6.2828e-04, 2.7421e-03, 4.9943e-03,
                          7.4223e-03, -5.0041e-04, -5.9196e-04],
            poloidalModeNumbers=[0, 1, 2, 3, 4],
            toroidalModeNumbers=[-4, -3, -2, -1, 0, 1, 2, 3, 4],
            numRadialPoints=1
        )
        zsin = FourierCoefficients(
            coefficients=[2.0185e-03, 1.9493e-03, 4.1458e-03,
                          2.0666e-01, -0.0000e+00, -2.0666e-01,
                          -4.1458e-03, -1.9493e-03, 2.0185e-03,
                          3.4400e-03, 7.7506e-03, 1.4961e-02,
                          4.0227e-02, 5.6892e-01, 2.0596e-01,
                          -5.7604e-03, -5.6140e-03, -4.2485e-03,
                          4.5363e-04, 3.1625e-04, 3.5963e-04,
                          8.3725e-03, 1.1405e-03, 2.3889e-02,
                          -6.0502e-02, 8.9796e-03, 9.1004e-04,
                          -3.7464e-04, -4.2385e-05, 5.3668e-04,
                          -1.7563e-03, -4.2733e-03, -4.4707e-03,
                          9.5155e-03, 1.0233e-02, -2.8137e-03,
                          1.2480e-04, -8.7567e-05, 7.6525e-05,
                          6.1672e-04, 3.6261e-03, -2.8280e-03,
                          7.3549e-03, -5.6303e-03, -2.8346e-04],
            poloidalModeNumbers=[0, 1, 2, 3, 4],
            toroidalModeNumbers=[-4, -3, -2, -1, 0, 1, 2, 3, 4],
            numRadialPoints=1
        )
        return cls(*args,
                   RCos=kwargs.pop('RCos', rcos),
                   ZSin=kwargs.pop('ZSin', zsin),
                   **kwargs)


def startVmecString(inData, **kwargs):
    """
    Args:
        inData (str): filePath to input file or content of input file
    Examples:
        # >>> startVmecString('~/Data/VMEC/w7x_ref_60_input.txt')
        # >>> startVmecString('~/Data/VMEC/w7x_ref_60_boundarySymmetryTerms_input.txt')
        # >>> startVmecString('~/Data/VMEC/w7x_ref_60_boundarySymmetryTerms0_input.txt')
        # >>> startVmecString('w7x_ref_60', vmec_id='dboe_w7x_ref_60_fromOnlineString')
    """
    defaultVmecId = None
    vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
    inFilePath = tfields.lib.in_out.resolve(inData)
    if os.path.isfile(inFilePath):
        # input file given
        defaultVmecId = os.path.basename(inFilePath).rstrip('_input.txt')
        defaultVmecId = 'dboe_vmec2_' + defaultVmecId
        with file(inFilePath, 'r') as f:
            inData = f.read()
    if '\n' not in inData:
        # get input file from vmec_id to restart a run
        defaultVmecId = inData
        defaultVmecId = 'dboe_vmec2_' + defaultVmecId
        run = Run(inData)
        inData = run.getInputString()

    vmec_id = kwargs.pop('vmec_id', defaultVmecId)
    vmecServer.service.execVmecString(inData, vmec_id)


def vmec_identifierExists(vmec_id):
    vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
    return vmecServer.service.vmec_identifierExists(vmec_id)


def getVolumeLCFS(vmec_id):
    vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
    return vmecServer.service.getVolumeLCFS(vmec_id)


def wasSuccessful(vmec_id):
    vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
    try:
        success = vmecServer.service.wasSuccessful(vmec_id)
    except Exception as err:
        log = logging.getLogger()
        success = False
        log.error("@vmec_id '{vmec_id}': {err.message}".format(**locals()))
    return success


def getVmecIds():
    vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
    res = vmecServer.service.listIdentifiers()
    return res.ReferenceShortIds + res.VmecIds


def getBAxis(vmec_id, phi=0.):
    """
    Args:
        vmec_id (str): vmec identifier
        phi (float): phi in radian
    Returns:
        float: Bax(phi) - magnetic field magnitude on the magnetic
            axis at phi = <phi>
    """
    vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
    points = Points3D(vmecServer.service.getMagneticAxis(vmec_id, phi))
    res = vmecServer.service.magneticField(vmec_id, points.as_input())
    B = Points3D(res)
    return np.linalg.norm(B)


def getVmecInput(**kwargs):
    """
    Args:
        **kwargs
            Necessary:
                magnetic_config (MagneticConfig)
                pressure_profile (Profile)
                currentProfile (Profile)
                magneticAxis (FourierCoefficients)
                boundary (FourierCoefficients)
            Obligatory:
                maxIterationsPerSequence (int): -> NITER
                maxToroidalMagneticFlux (float): -> PHIEDGE

    """
    magnetic_config = kwargs.pop('magnetic_config')
    pressure_profile = kwargs.pop('pressure_profile')
    currentProfile = kwargs.pop('currentProfile')
    magneticAxis = kwargs.pop('magneticAxis')
    boundary = kwargs.pop('boundary')
    iotaProfile = kwargs.pop('iotaProfile', None)
    totalToroidalCurrent = kwargs.pop('totalToroidalCurrent',
                                      w7x.Defaults.VMEC.totalToroidalCurrent)
    maxIterationsPerSequence = kwargs.pop('maxIterationsPerSequence',
                                          w7x.Defaults.VMEC.maxIterationsPerSequence)
    maxToroidalMagneticFlux = kwargs.pop('maxToroidalMagneticFlux',
                                         w7x.Defaults.VMEC.maxToroidalMagneticFlux)
    timeStep = kwargs.pop('timeStep', w7x.Defaults.VMEC.timeStep)
    numGridPointsRadial = kwargs.pop('numGridPointsRadial',
                                     w7x.Defaults.VMEC.numGridPointsRadial)
    forceToleranceLevels = kwargs.pop('forceToleranceLevels',
                                      w7x.Defaults.VMEC.forceToleranceLevels)

    vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
    inData = vmecServer.types.VmecInput(True)

    inData.mgridFile = "mgrid_w7x_nv36_hires.nc"  # 'mgrid_w7x_nv36.nc'
    inData.coilCurrents = magnetic_config.coil_currents('A')

    inData.pressure_profile = pressure_profile.as_input()
    inData.toroidalCurrentProfile = currentProfile.as_input()
    if iotaProfile:
        inData.iotaProfile = iotaProfile.as_input()

    inData.freeBoundary = True
    inData.intervalFullVacuumCalculation = 6
    inData.numFieldPeriods = 5
    inData.numModesPoloidal = 12
    inData.numModesToroidal = 12
    inData.numGridPointsPoloidal = 32
    inData.numGridPointsToroidal = 36
    inData.numGridPointsRadial = numGridPointsRadial
    inData.forceToleranceLevels = forceToleranceLevels
    inData.totalToroidalCurrent = totalToroidalCurrent
    inData.timeStep = timeStep
    inData.tcon0 = 2.
    inData.maxIterationsPerSequence = maxIterationsPerSequence
    inData.intervalConvergenceOutput = 100
    inData.maxToroidalMagneticFlux = maxToroidalMagneticFlux
    inData.gamma = 0

    inData.magneticAxis = magneticAxis.as_input()
    inData.boundary = boundary.as_input()
    return inData


def status(vmec_id, sleepTime=30):
    log = logging.getLogger()
    vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
    while not vmecServer.service.isReady(vmec_id):
        log.info("VMEC run {vmec_id} is still running.".format(**locals()))
        time.sleep(sleepTime)
    state = vmecServer.service.wasSuccessful(vmec_id)
    log.info("VMEC run {vmec_id} has finished. Service returns "
             "'wasSuccessful={state}'.".format(**locals()))
    return state


def findRun(currents,
            relPressureProfile=[1, -1],
            relCurrentProfile=[],
            delta=1e-2,
            currentType='rw',
            minBeta=None,
            maxBeta=None,
            minBAxis=None,
            maxBAxis=None,
            minP0=None,
            maxP0=None,
            idContains=None,
            ready=False):
    log = logging.getLogger()
    currents = [x / currents[0] for x in currents[1:]]
    vmec_ids = getVmecIds()
    pressure_profile = (PowerSeries(coefficients=relPressureProfile)
                        if relPressureProfile is not None else None)
    currentProfile = (PowerSeries(coefficients=relCurrentProfile)
                      if relCurrentProfile is not None else None)
    for vmec_id in vmec_ids:
        log.debug("vmec_id {vmec_id}:".format(**locals()))
        if idContains is not None:
            if not all([word in vmec_id for word in idContains]):
                log.debug("\t\t\t...vmec_id does not contain one of "
                          "idContains({idContains})".format(**locals()))
                continue

        run = Run(vmec_id)
        '''coilCurrents'''
        try:
            runCurrents = run.magnetic_config.coil_currents(currentType)
        except:
            log.debug("\t\t\t...error when getting magneitcConfig")
            continue
        if not run.wasSuccessful():
            if ready:
                log.debug("\t\t\t...not successful")
                continue
            elif run.isReady():
                log.debug("\t\t\t...not successful")
                continue
        dev = np.sqrt(sum(map(lambda x: abs((x[0] - x[1])**2),
                              zip(runCurrents, currents))))

        if dev > delta:
            log.debug("\t\t\t...differing in magnetic_config by {dev}"
                      .format(**locals()))
            continue

        '''Pressure'''
        if pressure_profile is not None:
            if not isinstance(run.pressure_profile, PowerSeries):
                log.debug("\t\t\t...PressureProfile is not PowerSeries")
                continue
            p0 = run.pressure_profile.norm
            if minP0 is not None:
                if p0 < minP0:
                    log.debug("\t\t\t...p0({p0}) < minP0({minP0})"
                              .format(**locals()))
                    continue
            if maxP0 is not None:
                if p0 > maxP0:
                    log.debug("\t\t\t...p0({p0}) > maxP0({maxP0})"
                              .format(**locals()))
                    continue
            devPP = pressure_profile.deviation(run.pressure_profile)
            if devPP > delta:
                log.debug("\t\t\t...differing in relative pressure_profile by"
                          " {devPP}"
                          .format(**locals()))
                continue

        '''Current'''
        if currentProfile is not None:
            if not isinstance(run.currentProfile, PowerSeries):
                log.debug("\t\t\t...CurrentProfile is not PowerSeries")
                continue
            devCP = currentProfile.deviation(run.currentProfile)
            if devCP > delta:
                log.debug("\t\t\t...differing in relative currentProfile by"
                          " {devCP}"
                          .format(**locals()))
                continue

        '''Beta'''
        if minBeta is not None or maxBeta is not None:
            beta = run.getBeta()
        if minBeta is not None:
            if not minBeta < beta:
                log.debug("\t\t\t...minBeta({minBeta}) > beta({beta})"
                          .format(**locals()))
                continue
        if maxBeta is not None:
            if not beta < maxBeta:
                log.debug("\t\t\t...maxBeta({maxBeta}) < beta({beta})"
                          .format(**locals()))
                continue

        '''BAxis'''
        if minBAxis is not None or maxBAxis is not None:
            bAxis = run.getBAxis()
        if minBAxis is not None:
            if not minBAxis < bAxis:
                log.debug("\t\t\t...minBAxis({minBAxis}) > bAxis({bAxis})"
                          .format(**locals()))
                continue
        if maxBAxis is not None:
            if not bAxis < maxBeta:
                log.debug("\t\t\t...maxBAxis({maxBAxis}) < bAxis({bAxis})"
                          .format(**locals()))
                continue
    
        return run


class Run(object):
    RUNARGS = [
        'magnetic_config',
        'pressure_profile',
        'currentProfile',
        'magneticAxis',
        'boundary']

    def __init__(self, *args, **runKwargs):
        self._conv = runKwargs.pop('conv', 0)
        self.parent = runKwargs.pop('parent', None)
        self._runKwargs = {}
        self.runKwargs = runKwargs  # use setter method
        self._vmec_id = None
        if len(args) >= 1:
            vmec_id = args[0]
        else:
            vmec_id = self.buildVmecId()
        self.vmec_id = vmec_id
        self._parsed = []

    def __str__(self):
        string = (
            "{self.__class__} instance\n"
            "\n"
            "\t\t\tvmec_id: {self.vmec_id}\n"
            "\n"
            .format(**locals()))

        ''' add the status '''
        if not vmec_identifierExists(self.vmec_id):
            status = "initializing"
        elif self.wasSuccessful():
            status = "successful"
        else:
            status = "not successful"
        string += (
            "Status: {status}\n"
            .format(**locals()))

        ''' add the input parameters '''
        if self.parent is None:
            parentVmecId = "None"
        elif not vmec_identifierExists(self.parent.vmec_id):
            parentVmecId = "unknown"
        else:
            parentVmecId = self.parent.vmec_id
        string += (
            "Parameters:\n"
            "\tparent: {parentVmecId}\n"
            "\tcoil currents (winding currents in A): {coilCurrents}\n"
            .format(
                coilCurrents=self.magnetic_config.coil_currents('A'),
                **locals()))
        string += (
            "\tpressure_profile:\n"
            "\t\tType: {self.pressure_profile.ProfileType}\n"
            "\t\tcoefficients: {self.pressure_profile.coefficients}\n"
            .format(**locals()))
        string += (
            "\tcurrentProfile:\n"
            "\t\tType: {self.currentProfile.ProfileType}\n"
            "\t\tcoefficients: {self.currentProfile.coefficients}\n"
            .format(**locals()))
        restKwargs = copy.deepcopy(self.runKwargs)
        for key in restKwargs:
            if key not in self.RUNARGS:
                string += (
                    "{key}: {value}\n"
                    .format(key=key,
                            value=restKwargs[key]))

        ''' add the major results '''
        if self.wasSuccessful():
            string += (
                "\n"
                "Results:\n"
                "\tB_Axis(phi=0): {bAxis}\n"
                "\tbeta: {beta}\n"
                "\tvolume LCFS (m^3): {volume}\n"
                "\tforce: {force}\n"
                .format(
                    bAxis=self.getBAxis(),
                    beta=self.getBeta(),
                    volume=self.getVolumeLCFS(),
                    force=self.getForce(),
                    **locals()))
        return string

    @property
    def vmec_id(self):
        return self._vmec_id

    @vmec_id.setter
    def vmec_id(self, vmec_id):
        self._vmec_id = vmec_id

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if isinstance(parent, str):
            parent = Run(parent)
        self._parent = parent

    @property
    def runKwargs(self):
        return self._runKwargs

    @runKwargs.setter
    def runKwargs(self, runKwargs):
        self._runKwargs = runKwargs

    @property
    def magnetic_config(self):
        magnetic_config = self.runKwargs.get('magnetic_config', None)
        if magnetic_config is not None:
            return magnetic_config
        if self.parent is not None:
            return self.parent.magnetic_config
        if self.exists():
            vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
            absoluteCurrents = \
                np.array(vmecServer.service.coil_currents(self.vmec_id))
            npcs = absoluteCurrents[:5] * 108
            plcs = absoluteCurrents[5:7] * 36
            scale = npcs[0]
            npcs = npcs / scale
            plcs = plcs / scale
            relativeCurrents = list(npcs) + list(plcs) + [0., 0.]
            magnetic_config = w7x.MagneticConfig \
                .createWithCurrents(relativeCurrents=relativeCurrents,
                                    scale=scale)
            return magnetic_config

    @magnetic_config.setter
    def magnetic_config(self, config):
        self.runKwargs['magnetic_config'] = config

    @property
    def pressure_profile(self):
        pressure_profile = self.runKwargs.get('pressure_profile', None)
        if pressure_profile is not None:
            return pressure_profile
        if self.parent is not None:
            return self.parent.pressure_profile
        if self.exists():
            self._parseInput()
            pressure_profile = createProfile(
                ProfileType=self._input['pressure_profileProfileType'],
                coefficients=self._input['pressure_profileCoefficients'])
            return pressure_profile

    @pressure_profile.setter
    def pressure_profile(self, profile):
        self.runKwargs['pressure_profile'] = profile

    @property
    def currentProfile(self):
        currentProfile = self.runKwargs.get('currentProfile', None)
        if currentProfile is not None:
            return currentProfile
        if self.parent is not None:
            return self.parent.currentProfile
        if self.exists():
            self._parseInput()
            currentProfile = createProfile(
                ProfileType=self._input['currentProfileProfileType'],
                coefficients=self._input['currentProfileCoefficients'])
            return currentProfile

    @currentProfile.setter
    def currentProfile(self, profile):
        self.runKwargs['currentProfile'] = profile

    @property
    def magneticAxis(self):
        magneticAxis = self.runKwargs.get('magneticAxis', None)
        if magneticAxis is not None:
            return magneticAxis
        if self.parent is not None:
            return self.parent.magneticAxis
        if self.exists():
            self._parseThreed1()
            rcos = FourierCoefficients(coefficients=self._threed1['rac'][:2],
                                       poloidalModeNumbers=[0],
                                       toroidalModeNumbers=[0, 1],
                                       numRadialPoints=1)
            zsin = FourierCoefficients(coefficients=self._threed1['zas'][:2],
                                       poloidalModeNumbers=[0],
                                       toroidalModeNumbers=[0, 1],
                                       numRadialPoints=1)
            magneticAxis = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        return magneticAxis

    @magneticAxis.setter
    def magneticAxis(self, surfaceCoefficients):
        self.runKwargs['magneticAxis'] = surfaceCoefficients

    @property
    def boundary(self):
        boundary = self.runKwargs.get('boundary', None)
        if boundary is not None:
            return boundary
        if self.parent is not None:
            return self.parent.boundary
        if self.exists():
            self._parseThreed1()
            coeffDict = {(m, n): (rbc, zbs)
                         for m, n, rbc, zbs in zip(self._threed1['mb'],
                                                   self._threed1['nb'],
                                                   self._threed1['rbc'],
                                                   self._threed1['zbs'])}

            toroidalModeNumbers = sorted(set([x for x in self._threed1['nb']
                                              if abs(x) <= 6]))
            poloidalModeNumbers = sorted(set([x for x in self._threed1['mb']
                                              if abs(x) <= 6]))
            rbcChoice = []
            zbsChoice = []
            for m in poloidalModeNumbers:
                for n in toroidalModeNumbers:
                    if m == 0 and n < 0:
                        rbcChoice.append(0.)
                        zbsChoice.append(0.)
                        """
                        the latter would be the mathematically correct version
                        Somehow the vmec service does not handle m=0,n<0 correct
                        """
                        # rbcChoice.append(coeffDict[(m, abs(n))][0])
                        # zbsChoice.append(-coeffDict[(m, abs(n))][1])
                    else:
                        rbcChoice.append(coeffDict[(m, n)][0])
                        zbsChoice.append(coeffDict[(m, n)][1])

            rcos = FourierCoefficients(coefficients=rbcChoice,
                                       poloidalModeNumbers=poloidalModeNumbers,
                                       toroidalModeNumbers=toroidalModeNumbers,
                                       numRadialPoints=1)
            zsin = FourierCoefficients(coefficients=zbsChoice,
                                       poloidalModeNumbers=poloidalModeNumbers,
                                       toroidalModeNumbers=toroidalModeNumbers,
                                       numRadialPoints=1)
            boundary = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        return boundary

    @boundary.setter
    def boundary(self, surfaceCoefficients):
        self.runKwargs['boundary'] = surfaceCoefficients

    def mutate(self, **mutationKwargs):
        if 'vmec_id' in mutationKwargs:
            inst = self.__class__(mutationKwargs.pop('vmec_id'), parent=self)
        else:
            inst = self.__class__(parent=self)
        inst.runKwargs.pop('boundary', None)
        inst.runKwargs.pop('magneticAxis', None)
        inst.runKwargs.update(mutationKwargs)
        return inst

    def buildVmecId(self):
        version = 0
        vmec_id = 'dboe_id_{0}_v_{1:0>2}_pres_{2:0>2}_it_{3}'.format(
            self.magnetic_config.geiger_string(),
            version,
            str(int(round(
                self.pressure_profile.norm / 1e4)
            )),
            self._conv
        )
        if vmec_identifierExists(vmec_id):
            self._conv += 1
            return self.buildVmecId()
        return vmec_id

    def getFieldPeriod(self):
        vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
        return vmecServer.service.getFieldPeriod(self.vmec_id)

    def getClosestVmecRun(self):
        vmec_ids = getVmecIds()

        """
        First deviation test in relative currents
        """
        relCurrs = self.magnetic_config.coil_currents('rw')
        deviations = []
        for vmec_id in vmec_ids:
            run = Run(vmec_id)
            try:
                relCurrsRun = run.magnetic_config.coil_currents('rw')
            except:
                deviations.append(np.inf)
                continue
            if run.wasSuccessful():
                dev = np.sqrt(sum(map(lambda x: abs((x[0] - x[1])**2),
                                      zip(relCurrsRun, relCurrs))))
            else:
                dev = np.inf
            deviations.append(dev)
        dMin = min(deviations)

        """
        Find all runs with deviation dMin
        """
        closeRuns = []
        for vmec_id, dev in zip(vmec_ids, deviations):
            if dev == dMin:
                rTmp = Run(vmec_id)
                closeRuns.append(rTmp)

        if len(closeRuns) == 1:
            return closeRuns[0]
        elif len(closeRuns) == 0:
            raise ValueError("No close runs found")

        """
        Second test on deviation in pressure_profile
        """
        # pDeviations = [abs(r.pressure_profile.norm - self.norm) for r in closeRuns]
        # closest = closeRuns[pDeviations.index(min(pDeviations))]
        pDeviations = []
        log = logging.getLogger()
        for r in closeRuns:
            try:
                r.pressure_profile
            except:
                log.warning("Probably false profile Type for vmec_id "
                            "{vmec_id}".format(vmec_id=r.vmec_id))
                continue
            pDeviations.append(self.pressure_profile.deviation(r.pressure_profile))
        closest = closeRuns[pDeviations.index(min(pDeviations))]
        return closest

    def _completeRunKwargs(self):
        """
        Complete the necessary arguments for starting a vmec run.
        The rest is set as default
        """
        for arg in self.RUNARGS:
            if self.parent is None:
                parent = self.getClosestVmecRun()
                log = logging.getLogger()
                log.info("Parent '{parent.vmec_id}' is "
                         "adopting me ('{self.vmec_id}')".format(**locals()))
                self.parent = parent
            if self.runKwargs.get(arg, None) is None:
                self.runKwargs[arg] = getattr(self.parent, arg)

    def start(self):
        log = logging.getLogger()
        log.info("Preparing run {0} for start.".format(self.vmec_id))
        self._completeRunKwargs()
        inData = getVmecInput(**self.runKwargs)
        vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
        log.highlight("Starting new VMEC run ({0}).".format(self.vmec_id))
        log.info(str(self))
        vmecServer.service.execVmec(inData, self.vmec_id)

    def shiftAxis(self, shift=-0.01):
        """
        shift the magneticAxis by shift
        """
        log = logging.getLogger()
        self.magneticAxis.RCos.coefficients[0] += shift
        log.info("Shifted axis by {shift}.".format(**locals()))

    def converge(self, iteration=0, reducedTolerance=False):
        """
        Returns:
            Run instance of converged run
        """
        log = logging.getLogger()
        if not self.exists():
            self.start()
        else:
            log.info("VMEC run ({0}) already done.".format(self.vmec_id))
        self.wait()
        if not self.wasSuccessful():
            vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
            threed1Content = vmecServer.service.getVmecRunData(self.vmec_id, 'threed1')
            log.info("VMEC run (self.vmec_id) was not successful. - iteration"
                     ": {iteration}".format(**locals()))
            runKwargs = copy.deepcopy(self.runKwargs)
            changed = False
            if 'Plasma Boundary exceeded Vacuum Grid Size' in threed1Content:
                runKwargs['maxToroidalMagneticFlux'] = \
                    runKwargs.get('maxToroidalMagneticFlux',
                                  w7x.Defaults.VMEC.maxToroidalMagneticFlux) * 2. / 3
                log.info("Plasma Boundary exceeded Vacuum Grid Size. "
                         "New phiEdge: {maxToroidalMagneticFlux}"
                         .format(**locals()))
                changed = True
            if iteration < 2 and 'Try increasing NITER' in threed1Content:
                runKwargs['maxIterationsPerSequence'] = \
                    runKwargs.get('maxIterationsPerSequence',
                                  w7x.Defaults.VMEC.maxIterationsPerSequence) + 50000
                log.info("Try increasing NITER. "
                         "New niter: {maxIterationsPerSequence}"
                         .format(maxIterationsPerSequence=runKwargs['maxIterationsPerSequence']))
                changed = True
            if iteration == 2 and reducedTolerance:
                raise ValueError("Even the tolerance reduced run did not converge.")
            if iteration >= 2:
                log.info("Still not converged try shrinking the magneticAxis.")
                roughRunKwargs = copy.deepcopy(runKwargs)
                forceToleranceLevels = roughRunKwargs.pop('forceToleranceLevels',
                                                          w7x.Defaults.VMEC.forceToleranceLevels)
                lastTolerance = forceToleranceLevels[-1] / 1e2
                if len(forceToleranceLevels) > 1 and lastTolerance < forceToleranceLevels[-2]:
                    lastTolerance = forceToleranceLevels[-2]
                forceToleranceLevels[-1] = lastTolerance
                roughRunKwargs['forceToleranceLevels'] = forceToleranceLevels
                log.info("Try with lower tolerance {lastTolerance}"
                         .format(**locals()))
                roughRun = self.__class__(**roughRunKwargs)
                if self.parent.wasSuccessful():
                    roughRun.parent = self.parent
                roughRun.converge(reducedTolerance=True)
                log.info("Lower tolerance run converged.")
                magneticAxis = roughRun.runKwargs.get('magneticAxis')
                magneticAxis.RCos.coefficients[0] -= 0.01
                runKwargs['magneticAxis'] = magneticAxis
                log.info("Set the magneticAxis 1cm inward.")
                changed = True

            if not changed:
                log.error("No response to non converging run.")
                return self
            newRun = self.__class__(**runKwargs)
            return newRun.converge(iteration=iteration + 1)
        log.info("Run converged successfully")
        return self

    def exists(self):
        if self.vmec_id is None:
            return False
        return vmec_identifierExists(self.vmec_id)

    def isReady(self):
        vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
        return vmecServer.service.isReady(self.vmec_id)

    def wasSuccessful(self):
        return wasSuccessful(self.vmec_id)

    def wait(self, sleepTime=60):
        while not self.isReady():
            log = logging.getLogger()
            log.verbose("Waiting for VMEC run "
                        "{self.vmec_id}.".format(**locals()))
            time.sleep(sleepTime)

    def getBAxis(self):
        return getBAxis(self.vmec_id)

    def getVolumeLCFS(self):
        self._parseThreed1()
        return self._threed1['PlasmaVolume']

    def getConfigAndPressureProfileEstimate(self, bAxis=2.5, tolerance=0.001):
        """
        Args:
            bAxis (float): magneticField strength on axis [T]
        """
        bAxisOld = self.getBAxis()
        f = bAxis / bAxisOld
        if abs(1 - f) < tolerance:
            log = logging.getLogger()
            log.warning("Tolerance of {tolerance} was met "
                        "already.".format(**locals()))
        magnetic_config = self.magnetic_config.copy()
        pressure_profile = self.pressure_profile.copy()
        magnetic_config.scale_currents(f)
        pressure_profile.scale(f ** 2)
        return magnetic_config, pressure_profile

    def _parseInput(self):
        if 'input' in self._parsed:
            return
        filePath = tfields.lib.in_out.resolve("~/tmp/VMEC/{self.vmec_id}.input.json"
                                              .format(**locals()))
        if os.path.exists(filePath):
            with open(filePath) as f:
                self._input = json.load(f)
        else:
            vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
            content = vmecServer.service.getVmecRunData(self.vmec_id, 'input')
            iterable = content.split('\n')
            transcoding = tc.getTranscoding(
                os.path.join(THISDIR,
                             "transcodings/vmecInput.py"))
            content = transcoding.read(iterable)
            with open(filePath, 'w') as f:
                json.dump(content, f)
            self._input = content
        self._parsed.append('input')

    def _parseThreed1(self):
        if 'threed1' in self._parsed:
            return
        filePath = tfields.lib.in_out.resolve("~/tmp/VMEC/{self.vmec_id}.threed1.json"
                                              .format(**locals()))
        if os.path.exists(filePath):
            with open(filePath) as f:
                self._threed1 = json.load(f)
        else:
            vmecServer = w7x.get_server(w7x.Server.addr_vmec_server)
            content = vmecServer.service.getVmecRunData(self.vmec_id, 'threed1')
            iterable = content.split('\n')
            transcoding = tc.getTranscoding(
                os.path.join(THISDIR,
                             "transcodings/vmecThreed1.py"))
            content = transcoding.read(iterable)
            with open(filePath, 'w') as f:
                json.dump(content, f)
            self._threed1 = content
        self._parsed.append('threed1')

    def getInputMagneticAxis(self):
        self._parseInput()
        rac, zas = zip(self._input['value0'], self._input['value1'])
        rcos = FourierCoefficients(coefficients=list(rac),
                                   poloidalModeNumbers=[0],
                                   toroidalModeNumbers=[0, 1],
                                   numRadialPoints=1)
        zsin = FourierCoefficients(coefficients=list(zas),
                                   poloidalModeNumbers=[0],
                                   toroidalModeNumbers=[0, 1],
                                   numRadialPoints=1)
        magneticAxis = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        return magneticAxis

    def getMagneticAxis(self):
        self._parseThreed1()
        rcos = FourierCoefficients(coefficients=self._threed1['rac'][:2],
                                   poloidalModeNumbers=[0],
                                   toroidalModeNumbers=[0, 1],
                                   numRadialPoints=1)
        zsin = FourierCoefficients(coefficients=self._threed1['zas'][:2],
                                   poloidalModeNumbers=[0],
                                   toroidalModeNumbers=[0, 1],
                                   numRadialPoints=1)
        magneticAxis = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        return magneticAxis

    def getInputBoundary(self):
        self._parseInput()
        coeffDict = {(m, n): (rbc, zbs)
                     for m, n, rbc, zbs in zip(self._input['m'],
                                               self._input['n'],
                                               self._input['rbc'],
                                               self._input['zbs'])}

        toroidalModeNumbers = sorted(set([x for x in self._input['n']
                                          if abs(x) <= 6]))
        poloidalModeNumbers = sorted(set([x for x in self._input['m']
                                          if abs(x) <= 6]))
        rbcChoice = []
        zbsChoice = []
        for m in poloidalModeNumbers:
            for n in toroidalModeNumbers:
                if m == 0 and n < 0:
                    rbcChoice.append(coeffDict[(m, abs(n))][0])
                    zbsChoice.append(-coeffDict[(m, abs(n))][1])
                else:
                    rbcChoice.append(coeffDict[(m, n)][0])
                    zbsChoice.append(coeffDict[(m, n)][1])

        rcos = FourierCoefficients(coefficients=rbcChoice,
                                   poloidalModeNumbers=poloidalModeNumbers,
                                   toroidalModeNumbers=toroidalModeNumbers,
                                   numRadialPoints=1)
        zsin = FourierCoefficients(coefficients=zbsChoice,
                                   poloidalModeNumbers=poloidalModeNumbers,
                                   toroidalModeNumbers=toroidalModeNumbers,
                                   numRadialPoints=1)
        boundary = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        return boundary

    def getBoundary(self):
        self._parseThreed1()
        coeffDict = {(m, n): (rbc, zbs)
                     for m, n, rbc, zbs in zip(self._threed1['mb'],
                                               self._threed1['nb'],
                                               self._threed1['rbc'],
                                               self._threed1['zbs'])}

        toroidalModeNumbers = sorted(set([x for x in self._threed1['nb']
                                          if abs(x) <= 6]))
        poloidalModeNumbers = sorted(set([x for x in self._threed1['mb']
                                          if abs(x) <= 6]))
        rbcChoice = []
        zbsChoice = []
        for m in poloidalModeNumbers:
            for n in toroidalModeNumbers:
                if m == 0 and n < 0:
                    rbcChoice.append(0.)
                    zbsChoice.append(0.)
                    """
                    the latter would be the mathematically correct version
                    Somehow the vmec service does not handle m=0,n<0 correct
                    """
                    # rbcChoice.append(coeffDict[(m, abs(n))][0])
                    # zbsChoice.append(-coeffDict[(m, abs(n))][1])
                else:
                    rbcChoice.append(coeffDict[(m, n)][0])
                    zbsChoice.append(coeffDict[(m, n)][1])

        rcos = FourierCoefficients(coefficients=rbcChoice,
                                   poloidalModeNumbers=poloidalModeNumbers,
                                   toroidalModeNumbers=toroidalModeNumbers,
                                   numRadialPoints=1)
        zsin = FourierCoefficients(coefficients=zbsChoice,
                                   poloidalModeNumbers=poloidalModeNumbers,
                                   toroidalModeNumbers=toroidalModeNumbers,
                                   numRadialPoints=1)
        boundary = SurfaceCoefficients(RCos=rcos, ZSin=zsin)
        return boundary

    def getBeta(self):
        self._parseThreed1()
        return self._threed1['forceIter'][-1]['BETA'][-1]

    def getForce(self):
        self._parseThreed1()
        forceIter = self._threed1['forceIter'][-1]
        attrs = ['FSQR', 'FSQZ', 'FSQL']
        return max([forceIter[attr][-1] for attr in attrs])

    def getPhiEdgeEstimate(self, minVolume=25, maxVolume=30, islandWidth=0.075):
        self._parseThreed1()
        p0, p1, p2, p3, p4 = parameters('p0, p1, p2, p3, p4')

        """
        Fit iota(r) with known plasma volume -> V = 2 pi^2 R r^2
        """
        R = self._threed1['MajorRadius']
        rmaxCalc = np.sqrt(self.getVolumeLCFS() / (2 * np.pi**2 * R))
        rValues = np.array(self._threed1["S"]) * rmaxCalc
        iotaValues = self._threed1["IOTA"]
        fluxValues = self._threed1["TOROIDAL_FLUX"]

        iota = Variable('iota')
        r = Variable('r')
        rPoly = p0 + p1 * r + p2 * r ** 2 + p3 * r ** 3 + p4 * r ** 4
        iotaPoly = p0 + p1 * iota + p2 * iota ** 2 + p3 * iota ** 3 + p4 * iota ** 4
        iotaVsR = fit(rPoly, rValues, iotaValues)
        rVsIota = fit(iotaPoly, iotaValues, rValues)

        """
        Find max r
            -> greater than minVolume
            -> smaller than maxVolume
            -> not bound by major islands
        """
        rmaxUser = np.sqrt(maxVolume / (2 * np.pi**2 * R))
        rminUser = np.sqrt(minVolume / (2 * np.pi**2 * R))

        if rmaxCalc < rminUser:
            rmaxCalc = 0.6 * (rmaxUser + rminUser)
        rmax = min((rmaxCalc, rmaxUser))
        iIsland = [4. / 5., 5. / 5., 6. / 5.]
        rIsland = [rVsIota.subs(iota, i) for i in iIsland]
        for ri in rIsland:
            if abs(rmax - ri) < 0.5 * islandWidth:
                rmax = ri - 0.5 * islandWidth
                break

        """
        fit flux(iota)
        """
        toroidalFlux = p0 + p1 * iota + p2 * iota ** 2 + p3 * iota ** 3 + p4 * iota ** 4
        fluxVsIota = fit(toroidalFlux, iotaValues, fluxValues)

        iotaMax = iotaVsR.subs(r, rmax)
        return fluxVsIota.subs(iota, iotaMax)


def getP0Estimate(betaScanRuns, beta, normTolerance=500):
    ''' Make shure, you fit on the same bField strenghts '''
    norms = [r.magnetic_config.coil_currents('Aw')[0] for r in betaScanRuns]
    if not len(set(norms)) < 2:
        raise ValueError("Runs of beta scan have difference coilCurrent norms"
                         "({norms})".format(**locals()))

    p0s = [0] + [r.pressure_profile.norm for r in betaScanRuns]
    betas = [0] + [r.getBeta() for r in betaScanRuns]

    a, b = parameters('a, b')
    x, y = variables('x, y')
    model = Model({y: a * x + b})
    fit = Fit(model, x=p0s, y=betas)
    res = fit.execute()
    fun = model[y]
    fun = fun.subs(a, res.params['a'])
    fun = fun.subs(b, res.params['b'])
    iFun = sympy.solve(y - fun, x)[0]
    p0 = iFun.subs(y, beta)

    return p0


def adjustBeta(relCurrents, beta, bAxis=2.5, relPressureProfile=[1, -1],
               relCurrentProfile=[0, 1, -1], totalToroidalCurrent=None,
               betaPrecision=0.001, betaScanRuns=None):
    """
    Args:
        relCurrents (parent or relativeCurrents): 7 ratios (1 winding emulation)
        beta (float): beta = 2 * mu_0 * <p> / <B^2>
        bAxis (float): B_toroidal on the axis (s=0). Usually: 2.5
        dIota (float): delta iota to one of the three edge resonances (4/5, 5/5,
            6/5
    """
    log = logging.getLogger()

    if betaScanRuns is None:
        betaScanRuns = []
    else:
        betaScanRuns = [Run(r) for r in betaScanRuns]
    if len(betaScanRuns) > 0:
        norm = betaScanRuns[0].magnetic_config.coil_currents('Aw')[0]
    else:
        norm = 12000 * 108

    magnetic_config = w7x.MagneticConfig.createWithCurrents(
        relativeCurrents=relCurrents,
        scale=norm)
    currentProfile = PowerSeries(coefficients=relCurrentProfile)
    currentKwargs = dict(
        currentProfile=currentProfile,
        totalToroidalCurrent=totalToroidalCurrent)

    betaScanRunKwargs = dict(
        magnetic_config=magnetic_config,
        maxIterationsPerSequence=60000,
        numGridPointsRadial=[4, 9, 28, 51],
        forceToleranceLevels=[1e-3, 1e-5, 1e-9, 1e-11])
    betaScanRunKwargs.update(currentKwargs)

    if len(betaScanRuns) == 0:
        pressure_profile = PowerSeries(
            coefficients=[6e4 * x for x in relPressureProfile])
        run = Run(pressure_profile=pressure_profile,
                  **betaScanRunKwargs)
        run.converge()
        if not run.wasSuccessful():
            raise RuntimeError("First run was not successful.")
        else:
            betaScanRuns.append(run)

    pressure_profile = PowerSeries(coefficients=relPressureProfile)
    '''1) Find correct p0 '''
    log.highlight("1) estimate p0")
    matchingBetaRuns = {}
    for run in betaScanRuns:
        # any run already has the correct beta?
        if abs(run.getBeta() - beta) < betaPrecision:
            matchingBetaRuns[run.getForce()] = run
    if matchingBetaRuns:
        # get most precise run from the matching ones
        grandParent = matchingBetaRuns[min(matchingBetaRuns.keys())]
        log.highlight("Found run with correct beta in given runs: "
                      "{grandParent.vmec_id}".format(**locals()))
    else:
        # approach correct beta.
        pDev = [pressure_profile.deviation(r.pressure_profile) for r in betaScanRuns]
        greatGrandParent = betaScanRuns[pDev.index(min(pDev))]
        while True:
            p0 = getP0Estimate(betaScanRuns, beta=beta)
            phiEdge = greatGrandParent.getPhiEdgeEstimate()
            pressure_profile.norm = p0
            grandParent = Run(parent=greatGrandParent,
                              pressure_profile=pressure_profile,
                              maxToroidalMagneticFlux=phiEdge,
                              **betaScanRunKwargs)
            log.info("Start run with p0 estimate: {p0}. "
                     "Also adjust phiEdge to {phiEdge}"
                     .format(**locals()))
            grandParent.converge()
            foundBeta = grandParent.getBeta()
            if abs(foundBeta - beta) < betaPrecision:
                log.info("Retrieved beta({foundBeta}) matches "
                         "Requested({beta}) within tolerance.".format(**locals()))
                break
            else:
                log.info("Retrieved beta({foundBeta}) not close enough to "
                         "Requested({beta}).".format(**locals()))
                greatGrandParent = grandParent
                betaScanRuns.append(greatGrandParent)

    '''2) Become more precise '''
    log.highlight("2) calculate more precise")
    forceTolerance = 1e-12
    if grandParent.getForce() < forceTolerance:
        parent = grandParent
        log.info("Forces in grandParent are sufficiently small. ")
    else:
        parent = grandParent.mutate(
            maxIterationsPerSequence=60000,
            numGridPointsRadial=[4, 9, 28, 51],
            forceToleranceLevels=[1e-3, 1e-5, 1e-9, forceTolerance])
        parent.converge(iteration=2)

    '''3) Find phiEdge and magnetic_config/p0 for correct Volume/bAxis '''
    log.highlight("3) Get phiEdge and magnetic_config/p0 estimate for correct "
                  "Volume/bAxis")
    phiEdge = -1.8  # parent.getPhiEdgeEstimate()
    magnetic_config, pressure_profile = parent.getConfigAndPressureProfileEstimate()

    '''4) Run again with parameters found'''
    log.highlight("4) converge run with phiEdge = {phiEdge} and magnetic_config"
                  "to reach bAxis = {bAxis}".format(**locals()))
    finalForceTolerance = 1e-14
    finalRun = Run(maxToroidalMagneticFlux=phiEdge,
                   maxIterationsPerSequence=100000,
                   magnetic_config=magnetic_config,
                   pressure_profile=pressure_profile,
                   forceToleranceLevels=[1e-3, 1e-5, 1e-9, finalForceTolerance],
                   parent=parent,
                   **currentKwargs)
    finalRun.converge()
    log.highlight(str(finalRun))
    return finalRun


standard = [1., 1., 1., 1., 1., 0., 0., 0., 0.]
highIota = [1., 1., 1., 1., 1., -0.23, -0.23, 0., 0.]
lowIota = [1., 1., 1., 1., 1., 0.25, 0.25, 0., 0.]
inwardShifted = [1., 1., 1., 1., 1., 0.1, -0.2, 0., 0.]
outwardShifted = [1., 1., 1., 1., 1., -0.14, 0.14, 0., 0.]
highIotaA = [1., 1., 1., 1., 1., -0.25, 0., 0., 0.]
highIotaB = [1., 1., 1., 1., 1., 0., -0.25, 0., 0.]
lowIotaA = [1., 1., 1., 1., 1., 0.25, 0., 0., 0.]
lowIotaB = [1., 1., 1., 1., 1., 0., 0.25, 0., 0.]


if __name__ == '__main__':
    pass
    # for iTor in np.linspace(0, 50000, 11):
    #     adjustBeta(standard, 0.0, totalToroidalCurrent=iTor)
