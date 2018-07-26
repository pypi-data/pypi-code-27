from . import impl as _impl


def complete_symmetrical_components(V0,V1,V2):
    """Calculates three three-phase "abc" sets from symmetrical components.

    Parameters
    ----------
    V0 : same type as input
        Zero-sequence component of phase "a".
    V1 : same type as input
        Positive-sequence component of phase "a".
    V2 : same type as input
        Negative-sequence component of phase "a".

    Returns
    -------
    V0abc, V1abc, V2abc : Phasors3ph tuple
        "abc" phasor set of zero-component, positive-component and negative-component respectively.

    Examples
    --------
    >>> Va = Phasor(mag=5, angle=53)
    >>> Vb = Phasor(mag=7, angle=-164)
    >>> Vc = Phasor(mag=7, angle=105)
    >>> V0, V1, V2 = symmetrical_components(Va, Vb, Vc)
    >>> [[Va0, Vb0, Vc0], [Va1, Vb1, Vc1], [Va2, Vb2, Vc2]] = complete_symmetrical_components(V0, V1, V2)

    See Also
    --------
    typhoon.test.transformations.symmetrical_components
    typhoon.test.transformations.inv_symmetrical_components
    """
    return _impl.complete_symmetrical_components(V0,V1,V2)


def symmetrical_components(Va, Vb, Vc):
    """Calculates symmetrical values abc phasors.

    Parameters
    ----------
    Va : complex or phasor
        Phase "a" component.
    Vb : complex or phasor
        Phase "b" component.
    Vc : complex or phasor
        Phase "c" component.

    Returns
    -------
    V0 : same type as input
        Zero-sequence component of phase "a".
    V1 : same type as input
        Positive-sequence component of phase "a".
    V2 : same type as input
        Negative-sequence component of phase "a".

    Examples
    --------
    >>> from typhoon.types.phasors import Phasor
    >>> from typhoon.test.transformations import symmetrical_components

    >>> Va = Phasor(mag=5, angle=53)
    >>> Vb = Phasor(mag=7, angle=-164)
    >>> Vc = Phasor(mag=7, angle=105)
    >>> V0, V1, V2 = symmetrical_components(Va, Vb, Vc)

    See Also
    --------
    typhoon.test.transformations.inv_symmetrical_components
    typhoon.test.transformations.complete_symmetrical_components
    """
    return _impl.symmetrical_components(Va, Vb, Vc)


def inv_symmetrical_components(V0, V1, V2):
    """Calculates the a, b and c phasors from symmetrical components.

    Parameters
    ----------
    V0 : complex or Phasor
        Zero-sequence component of phase "a".
    V1 : complex or Phasor
        Positive-sequence component of phase "a".
    V2 : complex or Phasor
        Negative-sequence component of phase "a".

    Returns
    -------
    Va : same type as input
        Phase "a" component.
    Vb : same type as input
        Phase "b" component.
    Vc : same type as input
        Phase "c" component.

    Examples
    --------
    >>> from typhoon.types.phasors import Phasor
    >>> from typhoon.test.transformations import inv_symmetrical_components

    >>> Va = Phasor(mag=5, angle=53)
    >>> Vb = Phasor(mag=7, angle=-164)
    >>> Vc = Phasor(mag=7, angle=105)
    >>> V0, V1, V2 = symmetrical_components(Va, Vb, Vc)

    >>> Va_round, Vb_round, Vc_round = inv_symmetrical_components(V0, V1, V2)
    >>> assert Va_round == Va
    >>> assert Vb_round == Vb
    >>> assert Vc_round == Vc

    See Also
    --------
    typhoon.test.transformations.symmetrical_components
    typhoon.test.transformations.complete_symmetrical_components
    """
    return _impl.inv_symmetrical_components(V0, V1, V2)
