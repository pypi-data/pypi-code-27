<<<<<<< HEAD
    
        IonStr : the same as the `ionStr` argument, such as `fe_12`.
        Z : `int`, the nuclear charge, 26 for `fe_12`.
        Ion : `int`, the ionization stage, 12 for `fe_12`.
        Dielectronic : `bool`, true if the ion is a 'dielectronic' ion where the levels
            are populated by dielectronic recombination.
        Spectroscopic : `str`, the spectroscopic notation for the ion, such as `Fe XII` for `fe_12`.
        Filename : `str`, the complete name of the file `generic` filename in the CHIANTI database, such as `$XUVTOP/fe/fe_12/fe_12`.
        Ip : `~numpy.float64`, the ionization potential of the ion
        Fip : `~numpy.float64`, the first ionization potential of the element
        Defaults : `dict`, with keys
            these are specified by the software unless a `chiantirc` file is found in $HOME/.chianti
            `abundfile`, the elemental abundance file, unless specified in 'chiantirc' this is defaults to `sun_photospheric_1998_grevesse`.
            `ioneqfile`, the ionization equilibrium file name.  Unless specified in 'chiantirc' this is defaults to `chianti`.  Other choices are availble in $XUVTOP/ioneq
                `wavelength`, the units of wavelength (Angstroms, nm, or kev), unless specified in the 'chiantirc' this is defaults to 'angstrom'.
                `flux`, specified whether the line intensities are give in energy or photon fluxes, unless specified in the 'chiantirc' this is defaults to `energy`.
                `gui`, specifies whether to use gui selection widgets (True) or to make selections on the command line (False).  Unless specified in the 'chiantirc' this is defaults to `False`.
    """
            
        
        
    def __init__(self, ionStr, temperature=None, eDensity=None, pDensity='default', radTemperature=0,  rStar=0, abundanceName=0, abundance=0,  verbose=0, setup=True, em=0):
        """
        Parameters
        ----------
            
        ionStr : `str`
            CHIANTI notation for the given ion, e.g. 'fe_12' that corresponds to the `Fe XII` ion.
        temperature : `~numpy.float64` or `~numpy.ndarray`, optional
            Temperature array (Kelvin)
        eDensity : `~numpy.float64` or `~numpy.ndarray`, optional
            Electron density array (:math:`\mathrm{cm^{-3}}` )
        pDensity : `~numpy.float64` or `~numpy.ndarray`, optional
            Proton density (:math:`\mathrm{cm}^{-3}` )
        radTemperature : `~numpy.float64` or `~numpy.ndarray`, optional
            Radiation black-body temperature (in Kelvin)
        rStar : `~numpy.float64` or `~numpy.ndarray`, optional
            Distance from the center of the star (in stellar radii)
        abundanceName : `str`, optional
            Name of Chianti abundance file to use, without the '.abund' suffix, e.g. 'sun_photospheric_1998_grevesse'. Ignored if `abundance` is set.
        abundance : `float or ~numpy.float64`, optional
            Elemental abundance relative to Hydrogen
        setup : `bool or str`, optional
            If True, run ion setup function
            Otherwise, provide a limited number of attributes of the selected ion
            
        em : `~numpy.float64` or `~numpy.ndarray`, optional
            Emission Measure, for the line-of-sight emission measure (:math:`\mathrm{\int \, n_e \, n_H \, dl}`) (:math:`\mathrm{cm}^{-5}`.), for the volumetric emission measure :math:`\mathrm{\int \, n_e \, n_H \, dV}` (:math:`\mathrm{cm^{-3}}`).
        
        note :  the keyword arguments temperature, eDensity, radTemperature, rStar, em must all be either a float or have the same dimension as the rest if specified as lists, tuples or arrays.            
     
        """
=======
    ionStr : `str`
        Spectroscopic notation for the given ion, e.g. 'c_5' that corresponds to the C V ion.
    temperature : `~numpy.float64` or `~numpy.ndarray`
        Temperature array (Kelvin)
    eDensity : `~numpy.float64` or `~numpy.ndarray`
        Electron density array (:math:`\mathrm{cm^{-3}}` )
    pDensity : `~numpy.float64` or `~numpy.ndarray`, optional
        Proton density (:math:`\mathrm{cm}^{-3}` )
    radTemperature : `~numpy.float64` or `~numpy.ndarray`, optional
        Radiation black-body temperature (in Kelvin)
    rStar : `~numpy.float64` or `~numpy.ndarray`, optional
        Distance from the center of the star (in stellar radii)
    abundanceName : `str`, optional
        Name of Chianti abundance file to use, without the '.abund' suffix, e.g. 'sun_photospheric_1998_grevesse'. Ignored if `abundance` is set.
    abundance : `float or ~numpy.float64`
        Elemental abundance relative to Hydrogen
    setup : `bool or str`
        If True, run ion setup function
        Otherwise, provide a limited number of attributes of the selected ion

    em : `~numpy.float64` or `~numpy.ndarray`
        Emission Measure, for the line-of-sight emission measure (:math:`\mathrm{\int \, n_e \, n_H \, dl}`) (:math:`\mathrm{cm}^{-5}`.), for the volumetric emission measure :math:`\mathrm{\int \, n_e \, n_H \, dV}` (:math:`\mathrm{cm^{-3}}`).

    note:  the keyword arguments temperature, eDensity, radTemperature, rStar, em must all be either a float or have the same dimension as the rest if specified as lists, tuples or arrays.
    """
    def __init__(self, ionStr, temperature=None, eDensity=None, pDensity='default', radTemperature=0,  rStar=0, abundanceName=0, abundance=0, setup=True, em=0):
        ''' this is the doc string for the ion init method

        '''
>>>>>>> 2e0b4dc83d98e2cc60afc2df5db3c66a350647fc
