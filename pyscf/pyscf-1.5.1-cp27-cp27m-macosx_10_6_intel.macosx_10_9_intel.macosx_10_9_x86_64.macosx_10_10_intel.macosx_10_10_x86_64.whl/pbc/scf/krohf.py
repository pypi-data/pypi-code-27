#!/usr/bin/env python
# Copyright 2014-2018 The PySCF Developers. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

'''
Restricted open-shell Hartree-Fock for periodic systems with k-point sampling
'''

from functools import reduce
import numpy as np
import scipy.linalg
from pyscf.pbc.scf import khf
from pyscf.pbc.scf import kuhf
from pyscf.pbc.scf import rohf as pbcrohf
from pyscf import lib
from pyscf.lib import logger
from pyscf.pbc.scf import addons
from pyscf.pbc.scf import chkfile
from pyscf import __config__

WITH_META_LOWDIN = getattr(__config__, 'pbc_scf_analyze_with_meta_lowdin', True)
PRE_ORTH_METHOD = getattr(__config__, 'pbc_scf_analyze_pre_orth_method', 'ANO')


def make_rdm1(mo_coeff_kpts, mo_occ_kpts):
    '''Alpha and beta spin one particle density matrices for all k-points.

    Returns:
        dm_kpts : (2, nkpts, nao, nao) ndarray
    '''
    nkpts = len(mo_occ_kpts)
    dma = []
    dmb = []
    for k, occ in enumerate(mo_occ_kpts):
        mo_a = mo_coeff_kpts[k][:,occ> 0]
        mo_b = mo_coeff_kpts[k][:,occ==2]
        dma.append(np.dot(mo_a, mo_a.conj().T))
        dmb.append(np.dot(mo_b, mo_b.conj().T))
    return lib.asarray((dma,dmb))

def get_fock(mf, h1e=None, s1e=None, vhf=None, dm=None, cycle=-1, diis=None,
             diis_start_cycle=None, level_shift_factor=None, damp_factor=None):
    h1e_kpts, s_kpts, vhf_kpts, dm_kpts = h1e, s1e, vhf, dm
    if h1e_kpts is None: h1e_kpts = mf.get_hcore()
    if vhf_kpts is None: vhf_kpts = mf.get_veff(mf.cell, dm_kpts)
    focka = h1e_kpts + vhf_kpts[0]
    fockb = h1e_kpts + vhf_kpts[1]
    f_kpts = get_roothaan_fock((focka,fockb), dm, s1e)
    if cycle < 0 and diis is None:  # Not inside the SCF iteration
        return f_kpts

    if diis_start_cycle is None:
        diis_start_cycle = mf.diis_start_cycle
    if level_shift_factor is None:
        level_shift_factor = mf.level_shift
    if damp_factor is None:
        damp_factor = mf.damp
    if s_kpts is None: s_kpts = mf.get_ovlp()
    if dm_kpts is None: dm_kpts = mf.make_rdm1()

    dm_sf = dm_kpts[0] + dm_kpts[1]
    if diis and cycle >= diis_start_cycle:
        f_kpts = diis.update(s_kpts, dm_sf, f_kpts, mf, h1e_kpts, vhf_kpts)
    if abs(level_shift_factor) > 1e-4:
        f_kpts = [hf.level_shift(s, dm_sf[k]*.5, f_kpts[k], level_shift_factor)
                  for k, s in enumerate(s_kpts)]
    f_kpts = lib.tag_array(lib.asarray(f_kpts), focka=focka, fockb=fockb)
    return f_kpts

def get_roothaan_fock(focka_fockb, dma_dmb, s):
    '''Roothaan's effective fock.

    ======== ======== ====== =========
    space     closed   open   virtual
    ======== ======== ====== =========
    closed      Fc      Fb     Fc
    open        Fb      Fc     Fa
    virtual     Fc      Fa     Fc
    ======== ======== ====== =========

    where Fc = (Fa + Fb) / 2

    Returns:
        Roothaan effective Fock matrix
    '''
    nkpts = len(s)
    nao = s[0].shape[0]
    focka, fockb = focka_fockb
    dma, dmb = dma_dmb
    fock_kpts = []
    for k in range(nkpts):
        fc = (focka[k] + fockb[k]) * .5
        pc = np.dot(dmb[k], s[k])
        po = np.dot(dma[k]-dmb[k], s[k])
        pv = np.eye(nao) - np.dot(dma[k], s[k])
        fock  = reduce(np.dot, (pc.conj().T, fc, pc)) * .5
        fock += reduce(np.dot, (po.conj().T, fc, po)) * .5
        fock += reduce(np.dot, (pv.conj().T, fc, pv)) * .5
        fock += reduce(np.dot, (po.conj().T, fockb[k], pc))
        fock += reduce(np.dot, (po.conj().T, focka[k], pv))
        fock += reduce(np.dot, (pv.conj().T, fc, pc))
        fock_kpts.append(fock + fock.conj().T)
    fock_kpts = lib.tag_array(np.asarray(fock_kpts), focka=focka, fockb=fockb)
    return fock_kpts

def get_occ(mf, mo_energy_kpts=None, mo_coeff_kpts=None):
    '''Label the occupancies for each orbital for sampled k-points.

    This is a k-point version of scf.hf.SCF.get_occ
    '''

    if mo_energy_kpts is None: mo_energy_kpts = mf.mo_energy
    if hasattr(mo_energy_kpts[0], 'mo_ea'):
        mo_ea_kpts = [x.mo_ea for x in mo_energy_kpts]
        mo_eb_kpts = [x.mo_eb for x in mo_energy_kpts]
    else:
        mo_ea_kpts = mo_eb_kpts = mo_energy_kpts

    nkpts = len(mo_energy_kpts)
    nocc_a = mf.nelec[0] * nkpts
    nocc_b = mf.nelec[1] * nkpts

    mo_energy_kpts1 = np.hstack(mo_energy_kpts)
    mo_energy = np.sort(mo_energy_kpts1)
    if nocc_b > 0:
        core_level = mo_energy[nocc_b-1]
    else:
        core_level = -1e9
    if nocc_a == nocc_b:
        fermi = core_level
    else:
        mo_ea_kpts1 = np.hstack(mo_ea_kpts)
        mo_ea = np.sort(mo_ea_kpts1[mo_energy_kpts1 > core_level])
        fermi = mo_ea[nocc_a - nocc_b - 1]

    mo_occ_kpts = []
    for k, mo_e in enumerate(mo_energy_kpts):
        occ = np.zeros_like(mo_e)
        occ[mo_e <= core_level] = 2
        if nocc_a != nocc_b:
            occ[(mo_e > core_level) & (mo_ea_kpts[k] <= fermi)] = 1
        mo_occ_kpts.append(occ)

    if nocc_a < len(mo_energy):
        logger.info(mf, 'HOMO = %.12g  LUMO = %.12g',
                    mo_energy[nocc_a-1], mo_energy[nocc_a])
    else:
        logger.info(mf, 'HOMO = %.12g', mo_energy[nocc_a-1])

    np.set_printoptions(threshold=len(mo_energy))
    if mf.verbose >= logger.DEBUG:
        logger.debug(mf, '                  Roothaan           | alpha              | beta')
        for k,kpt in enumerate(mf.cell.get_scaled_kpts(mf.kpts)):
            core_idx = mo_occ_kpts[k] == 2
            open_idx = mo_occ_kpts[k] == 1
            vir_idx = mo_occ_kpts[k] == 0
            logger.debug(mf, '  kpt %2d (%6.3f %6.3f %6.3f)',
                         k, kpt[0], kpt[1], kpt[2])
            logger.debug(mf, '  Highest 2-occ = %18.15g | %18.15g | %18.15g',
                         max(mo_energy_kpts[k][core_idx]),
                         max(mo_ea_kpts[k][core_idx]), max(mo_eb_kpts[k][core_idx]))
            logger.debug(mf, '  Lowest 0-occ =  %18.15g | %18.15g | %18.15g',
                         min(mo_energy_kpts[k][vir_idx]),
                         min(mo_ea_kpts[k][vir_idx]), min(mo_eb_kpts[k][vir_idx]))
            for i in np.where(open_idx)[0]:
                logger.debug(mf, '  1-occ =         %18.15g | %18.15g | %18.15g',
                             mo_energy_kpts[k][i], mo_ea_kpts[k][i], mo_eb_kpts[k][i])

        logger.debug(mf, '     k-point                  Roothaan mo_energy')
        for k,kpt in enumerate(mf.cell.get_scaled_kpts(mf.kpts)):
            logger.debug(mf, '  %2d (%6.3f %6.3f %6.3f)   %s %s',
                         k, kpt[0], kpt[1], kpt[2],
                         mo_energy_kpts[k][mo_occ_kpts[k]> 0],
                         mo_energy_kpts[k][mo_occ_kpts[k]==0])

    if mf.verbose >= logger.DEBUG1:
        logger.debug1(mf, '     k-point                  alpha mo_energy')
        for k,kpt in enumerate(mf.cell.get_scaled_kpts(mf.kpts)):
            logger.debug1(mf, '  %2d (%6.3f %6.3f %6.3f)   %s %s',
                          k, kpt[0], kpt[1], kpt[2],
                          mo_ea_kpts[k][mo_occ_kpts[k]> 0],
                          mo_ea_kpts[k][mo_occ_kpts[k]==0])
        logger.debug1(mf, '     k-point                  beta  mo_energy')
        for k,kpt in enumerate(mf.cell.get_scaled_kpts(mf.kpts)):
            logger.debug1(mf, '  %2d (%6.3f %6.3f %6.3f)   %s %s',
                          k, kpt[0], kpt[1], kpt[2],
                          mo_eb_kpts[k][mo_occ_kpts[k]==2],
                          mo_eb_kpts[k][mo_occ_kpts[k]!=2])
    np.set_printoptions(threshold=1000)

    return mo_occ_kpts


energy_elec = kuhf.energy_elec


@lib.with_doc(khf.mulliken_meta.__doc__)
def mulliken_meta(cell, dm_ao_kpts, verbose=logger.DEBUG,
                  pre_orth_method=PRE_ORTH_METHOD, s=None):
    '''Mulliken population analysis, based on meta-Lowdin AOs.

    Note this function only computes the Mulliken population for the gamma
    point density matrix.
    '''
    dm = dm_ao_kpts[0] + dm_ao_kpts[1]
    return khf.mulliken_meta(cell, dm, verbose, pre_orth_method, s)


def canonicalize(mf, mo_coeff_kpts, mo_occ_kpts, fock=None):
    '''Canonicalization diagonalizes the ROHF Fock matrix within occupied,
    virtual subspaces separatedly (without change occupancy).
    '''
    if fock is None:
        dm = mf.make_rdm1(mo_coeff_kpts, mo_occ_kpts)
        fock = mf.get_hcore() + mf.get_jk(mf.cell, dm)

    mo_coeff = []
    mo_energy = []
    for k, mo in enumerate(mo_coeff_kpts):
        mo1 = np.empty_like(mo)
        mo_e = np.empty_like(mo_occ_kpts[k])
        coreidx = mo_occ_kpts[k] == 2
        openidx = mo_occ_kpts[k] == 1
        viridx = mo_occ_kpts[k] == 0
        for idx in (coreidx, openidx, viridx):
            if np.count_nonzero(idx) > 0:
                orb = mo[:,idx]
                f1 = reduce(np.dot, (orb.T.conj(), fock[k], orb))
                e, c = scipy.linalg.eigh(f1)
                mo1[:,idx] = np.dot(orb, c)
                mo_e[idx] = e
        if hasattr(fock, 'focka'):
            mo_ea = np.einsum('pi,pi->i', mo1.conj(), fock.focka[k].dot(mo1))
            mo_eb = np.einsum('pi,pi->i', mo1.conj(), fock.fockb[k].dot(mo1))
            mo_e = lib.tag_array(mo_e, mo_ea=mo_ea.real, mo_eb=mo_eb.real)
        mo_coeff.append(mo1)
        mo_energy.append(mo_e)
    return mo_energy, mo_coeff

init_guess_by_chkfile = kuhf.init_guess_by_chkfile


class KROHF(pbcrohf.ROHF, khf.KRHF):
    '''UHF class with k-point sampling.
    '''
    conv_tol = getattr(__config__, 'pbc_scf_KSCF_conv_tol', 1e-7)
    conv_tol_grad = getattr(__config__, 'pbc_scf_KSCF_conv_tol_grad', None)
    direct_scf = getattr(__config__, 'pbc_scf_SCF_direct_scf', False)

    def __init__(self, cell, kpts=np.zeros((1,3)),
                 exxdiv=getattr(__config__, 'pbc_scf_SCF_exxdiv', 'ewald')):
        khf.KSCF.__init__(self, cell, kpts, exxdiv)
        self.nelec = cell.nelec
        self._keys = self._keys.union(['nelec'])

    def dump_flags(self):
        khf.KSCF.dump_flags(self)
        logger.info(self, 'number of electrons per unit cell  '
                    'alpha = %d beta = %d', *self.nelec)
        return self

    build = khf.KSCF.build
    check_sanity = khf.KSCF.check_sanity

#    get_init_guess = khf.KSCF.get_init_guess

    def get_init_guess(self, cell=None, key='minao'):
        if cell is None:
            cell = self.cell
        dm_kpts = None
        if key.lower() == '1e':
            dm_kpts = self.init_guess_by_1e(cell)
        elif getattr(cell, 'natm', 0) == 0:
            logger.info(self, 'No atom found in cell. Use 1e initial guess')
            dm_kpts = self.init_guess_by_1e(cell)
        elif key.lower() == 'atom':
            dm = self.init_guess_by_atom(cell)
        elif key.lower().startswith('chk'):
            try:
                dm_kpts = self.from_chk()
            except (IOError, KeyError):
                logger.warn(self, 'Fail to read %s. Use MINAO initial guess',
                            self.chkfile)
                dm = self.init_guess_by_minao(cell)
        else:
            dm = self.init_guess_by_minao(cell)

        if dm_kpts is None:
            dm_kpts = lib.asarray([dm]*len(self.kpts))

        if cell.dimension < 3:
            ne = np.einsum('xkij,kji->xk', dm_kpts, self.get_ovlp(cell))
            nelec = np.asarray(cell.nelec).reshape(2,1)
            if np.any(abs(ne - nelec) > 1e-7):
                logger.warn(self, 'Big error detected in the electron number '
                            'of initial guess density matrix (Ne/cell = %g)!\n'
                            '  This can cause huge error in Fock matrix and '
                            'lead to instability in SCF for low-dimensional '
                            'systems.\n  DM is normalized to correct number '
                            'of electrons', ne.mean())
                dm_kpts *= (nelec/ne).reshape(2,-1,1,1)
        return dm_kpts

    get_hcore = khf.KSCF.get_hcore
    get_ovlp = khf.KSCF.get_ovlp
    get_jk = khf.KSCF.get_jk
    get_j = khf.KSCF.get_j
    get_k = khf.KSCF.get_k
    get_fock = get_fock
    get_occ = get_occ
    energy_elec = energy_elec

    def get_veff(self, cell=None, dm_kpts=None, dm_last=0, vhf_last=0, hermi=1,
                 kpts=None, kpts_band=None):
        vj, vk = self.get_jk(cell, dm_kpts, hermi, kpts, kpts_band)
        vhf = vj[0] + vj[1] - vk
        return vhf

    def get_grad(self, mo_coeff_kpts, mo_occ_kpts, fock=None):
        if fock is None:
            dm1 = self.make_rdm1(mo_coeff_kpts, mo_occ_kpts)
            fock = self.get_hcore(self.cell, self.kpts) + self.get_veff(self.cell, dm1)

        if hasattr(fock, 'focka'):
            focka = fock.focka
            fockb = fock.fockb
        elif getattr(fock, 'ndim', None) == 4:
            focka, fockb = fock
        else:
            focka = fockb = fock

        def grad(k):
            mo_occ = mo_occ_kpts[k]
            mo_coeff = mo_coeff_kpts[k]
            return pbcrohf.get_grad(mo_coeff, mo_occ, (focka[k], fockb[k]))

        nkpts = len(self.kpts)
        grad_kpts = np.hstack([grad(k) for k in range(nkpts)])
        return grad_kpts

    def eig(self, fock, s):
        e, c = khf.KSCF.eig(self, fock, s)
        if hasattr(fock, 'focka'):
            for k, mo in enumerate(c):
                mo_ea = np.einsum('pi,pi->i', mo.conj(), fock.focka[k].dot(mo))
                mo_eb = np.einsum('pi,pi->i', mo.conj(), fock.fockb[k].dot(mo))
                e[k] = lib.tag_array(e[k], mo_ea=mo_ea.real, mo_eb=mo_eb.real)
        return e, c

    def make_rdm1(self, mo_coeff_kpts=None, mo_occ_kpts=None):
        if mo_coeff_kpts is None: mo_coeff_kpts = self.mo_coeff
        if mo_occ_kpts is None: mo_occ_kpts = self.mo_occ
        return make_rdm1(mo_coeff_kpts, mo_occ_kpts)

    def init_guess_by_chkfile(self, chk=None, project=True, kpts=None):
        if chk is None: chk = self.chkfile
        if kpts is None: kpts = self.kpts
        return init_guess_by_chkfile(self.cell, chk, project, kpts)


    def analyze(self, verbose=None, with_meta_lowdin=WITH_META_LOWDIN,
                **kwargs):
        if verbose is None: verbose = self.verbose
        return khf.analyze(self, verbose, with_meta_lowdin, **kwargs)

    def mulliken_meta(self, cell=None, dm=None, verbose=logger.DEBUG,
                      pre_orth_method=PRE_ORTH_METHOD, s=None):
        if cell is None: cell = self.cell
        if dm is None: dm = self.make_rdm1()
        if s is None: s = self.get_ovlp(cell)
        return mulliken_meta(cell, dm, s=s, verbose=verbose,
                             pre_orth_method=pre_orth_method)

    @lib.with_doc(pbcrohf.ROHF.spin_square.__doc__)
    def spin_square(self, mo_coeff=None, s=None):
        '''Treating the k-point sampling wfn as a giant Slater determinant,
        the spin_square value is the <S^2> of the giant determinant.
        '''
        ss, s = pbcrohf.ROHF.spin_square(self, mo_coeff, s)
        nkpts = len(self.kpts)
        return ss * nkpts, s * nkpts

    get_bands = khf.KSCF.get_bands

    canonicalize = canonicalize

    dump_chk = khf.KSCF.dump_chk

    density_fit = khf.KSCF.density_fit
    # mix_density_fit inherits from khf.KSCF.mix_density_fit

    newton = khf.KSCF.newton
    x2c = x2c1e = sfx2c1e = khf.KSCF.sfx2c1e

    def stability(self,
                  internal=getattr(__config__, 'pbc_scf_KSCF_stability_internal', True),
                  external=getattr(__config__, 'pbc_scf_KSCF_stability_external', False),
                  verbose=None):
        raise NotImplementedError

    def convert_from_(self, mf):
        '''Convert given mean-field object to KUHF'''
        addons.convert_to_rhf(mf, self)
        return self

del(WITH_META_LOWDIN, PRE_ORTH_METHOD)


if __name__ == '__main__':
    from pyscf.pbc import gto
    cell = gto.Cell()
    cell.atom = '''
    He 0 0 1
    He 1 0 1
    '''
    cell.basis = '321g'
    cell.a = np.eye(3) * 3
    cell.mesh = [11] * 3
    cell.verbose = 5
    cell.spin = 2
    cell.build()
    mf = KROHF(cell, [2,1,1])
    mf.kernel()
    mf.analyze()

