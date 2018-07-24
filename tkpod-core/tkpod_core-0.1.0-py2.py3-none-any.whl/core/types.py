import re
from typing import NamedTuple

MUTATION_REGEX = re.compile(
    "([^-_\.]*[-_]{1})?([GVALICMFWPDESTYQNKRH])([0-9]+)([GVALICMFWPDESTYQNKRH]?)"
)


class Mutation(NamedTuple):
    chain_id: str
    residue_wt: str
    residue_idx: int
    residue_mut: str

    def __str__(self) -> str:
        return f"{self.chain_id}_{self.residue_wt}{self.residue_idx + 1}{self.residue_mut}"

    @classmethod
    def from_string(cls, mutation: str) -> "Mutation":
        matches = MUTATION_REGEX.findall(mutation)
        assert len(matches) == 1
        chain_id, residue_wt, residue_id, residue_mut = matches[0]
        chain_id = chain_id.strip("-_")
        residue_idx = int(residue_id) - 1  # Zero-based
        return cls(chain_id, residue_wt, residue_idx, residue_mut)
