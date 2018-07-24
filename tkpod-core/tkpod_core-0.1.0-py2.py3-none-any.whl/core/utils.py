import functools
import importlib
import itertools
import json
import logging
import pkgutil
from typing import List, TypeVar

import kmbio.PDB
import numpy as np
import pandas as pd

from tkpod.core.types import Mutation

logger = logging.getLogger(__name__)

# =============================================================================
# Helpers
# =============================================================================


def find_leaf_subclasses(cls):
    """Find the leaf subclasses of `cls`."""
    subclasses = cls.__subclasses__()
    if not subclasses:
        return [cls]
    else:
        leaves = []
        for subclass in subclasses:
            leaves.extend(find_leaf_subclasses(subclass))
        return leaves


T = TypeVar("T", dict, pd.DataFrame)


def features_to_differences(data: T) -> T:
    data = data.copy()
    for key in data:
        key_wt = key[: -len("_mut")] + "_wt"
        key_change = key[: -len("_mut")] + "_change"
        if key.endswith("_mut") and key_wt in data:
            data[key_change] = data[key] - data[key_wt]
            del data[key]
    return data


def dumps_results(fn):
    """Decorator which converts dictionary results to a JSON string."""
    from kmtools import py_tools

    @functools.wraps(fn)
    def wrapped(self, *args, **kwargs):
        results = fn(self, *args, **kwargs)
        build_results = {}
        for key, value in self.cache.items():
            if isinstance(value, (float, int)):
                build_results[key] = value
        if build_results:
            results["build_results"] = build_results
        results = {str(k): v for k, v in results.items()}
        return json.dumps(results, cls=py_tools.JSONEncoderNumPy)

    return wrapped


def find_plugins():
    import tkpod.plugins

    ns_pkg = tkpod.plugins
    plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")
    }
    return plugins


# =============================================================================
# Mutations
# =============================================================================


def parse_mutations(pdb_mutations: str) -> List[Mutation]:
    """Process PDB mutations into a list of `Mutation` objects.

    Examples:
        >>> parse_mutations('A-M1A.B-A2C')
        [Mutation(chain_id='A', residue_wt='M', residue_idx=0, residue_mut='A'),
        Mutation(chain_id='B', residue_wt='A', residue_idx=1, residue_mut='C')]
    """
    return [Mutation.from_string(mut) for mut in pdb_mutations.split(".")]


# =============================================================================
# Structure
# =============================================================================


def is_hetatm(chain) -> bool:
    """Check if the chain contains only hetatm residues."""
    return all(r.id[0] != " " for r in chain.residues)


def get_min_distance(coord, target_array) -> float:
    """Calculate minimum distance between `coord` and `target_array`."""
    return (((target_array - coord) ** 2).sum(axis=1) ** 0.5).min()


def _choose_closest_chain(residue, nss, chains):
    """Return `chain` in chains which is closest to `residue`.

    Note
    ----
    The first chain in `chains` will be returned if none of the chains
    are within 5 Å of `residue`.

    Args:
        residue: Residue for which to measure distance.
        nss: List of `kmbio.PDB.NeighborSearch` objects, one for each chain in `chains`.
        chains: List of chains, one of which will be returned.
    """
    assert len(nss) == len(chains)
    contacts = [
        list(itertools.chain(*[nss[i].search(a.coord, 5, "R") for a in residue]))
        for i in range(len(nss))
    ]
    logger.debug("contacts: %s", contacts)

    # List of bools indicating whether contacts were found for chain
    contacts_found = [bool(c) for c in contacts]

    if not any(contacts_found):
        return chains[0]
    elif sum(contacts_found) == 1:
        chain_idx = contacts_found.index(True)
        return chains[chain_idx]
    else:
        contact_arrays = [
            np.array([a.coord for r in contacts[i] for a in r]) for i in range(len(contacts))
        ]
        min_distances = [
            min(get_min_distance(a.coord, contact_arrays[i]) for a in residue)
            for i in range(len(contacts))
        ]
        chain_idx = min_distances.index(min(min_distances))
        return chains[chain_idx]


def _distribute_hetatm_residues(structure, structure_ligand, structure_target) -> None:
    """Move hetatm residues from hetatm chains into `structure_ligand` or `structure_target`.

    Decide where to move the residues based on shortest distance.
    """
    remaining_chains = [
        chain
        for chain in structure.chains
        if all(chain.id != c.id for c in structure_ligand.chains)  #
        and all(chain.id != c.id for c in structure_target.chains)
    ]
    logger.debug("remaining_chains: %s", remaining_chains)
    assert remaining_chains

    ns_ligand = kmbio.PDB.NeighborSearch(list(structure_ligand.atoms))
    ns_target = kmbio.PDB.NeighborSearch(list(structure_target.atoms))

    for chain in remaining_chains:
        chain_ligand = kmbio.PDB.Chain(chain.id)
        chain_target = kmbio.PDB.Chain(chain.id)
        for residue in chain:
            logger.debug("residue id: %s", residue.id)
            closest_chain = _choose_closest_chain(
                residue, [ns_ligand, ns_target], [chain_ligand, chain_target]
            )
            closest_chain.add(residue.copy())
        assert chain_ligand or chain_target
        if chain_ligand:
            structure_ligand[0].add(chain_ligand)
        if chain_target:
            structure_target[0].add(chain_target)


def extract_ligand_and_target(structure: kmbio.PDB.Structure, target_chain_id: str):  #
    """Divide `structure` into the structure of the ligand and the structure of the target."""
    # Structure of target
    structure_target = kmbio.PDB.Structure(structure.id + "-target")
    structure_target.add(kmbio.PDB.Model(0))
    structure_target[0].add(structure[0][target_chain_id].copy())

    # Structure of ligand
    structure_ligand = kmbio.PDB.Structure(structure.id + "-ligand")
    structure_ligand.add(kmbio.PDB.Model(0))
    for chain in structure.chains:
        if chain.id != target_chain_id and not is_hetatm(chain):
            structure_ligand[0].add(chain.copy())

    if len(list(structure.chains)) != len(
        list(structure_target.chains) + list(structure_ligand.chains)
    ):
        _distribute_hetatm_residues(structure, structure_ligand, structure_target)
        _together_chains = set(c.id for c in structure.chains)
        _split_chains = set(c.id for c in structure_ligand.chains) | set(
            c.id for c in structure_target.chains
        )
        assert not _together_chains ^ _split_chains

    return structure_ligand, structure_target
