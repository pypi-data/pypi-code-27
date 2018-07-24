import tempfile
from pathlib import Path
from typing import TypeVar

import tkpod

ToolOutput = TypeVar("ToolOutput")


class ToolBase:
    @classmethod
    def get_temp_dir(cls, *unique_ids) -> Path:
        temp_dir = (
            Path(tempfile.mkdtemp()).joinpath(tkpod.__name__, cls.__name__, *unique_ids).resolve()
        )
        temp_dir.mkdir(parents=True, exist_ok=True)
        return temp_dir


class SequenceTool(ToolBase):
    @classmethod
    def build(cls, sequence: str = None, **kwargs) -> ToolOutput:
        raise NotImplementedError


class StructureTool(ToolBase):
    @classmethod
    def build(cls, structure: str = None, **kwargs) -> ToolOutput:
        raise NotImplementedError


class ResidueAnalyzer:
    @classmethod
    def analyze_residue(cls, mutation: str, data: ToolOutput) -> dict:
        raise NotImplementedError


class MutationAnalyzer:
    @classmethod
    def analyze_mutation(cls, mutation: str, data: ToolOutput) -> dict:
        raise NotImplementedError
