"""Union-Find data structures & helper objects"""


class Partition:

    def __init__(self, name: str, elements):
        self.name: str = name
        self.elements: set = set(elements)

    def __contains__(self, element):
        return element in self.elements

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def __or__(self, other):
        if self.__class__ is other.__class__:
            return self.__class__(
                name=f"{self.name}_{other.name}",
                elements=self.elements | other.elements
            )
        return NotImplemented


class UnionFindSpace:

    def __init__(self, *partitions):
        self._partitions: dict = {p.name: p for p in partitions}
        self._mapping: dict = {e: p.name for p in partitions for e in p}

    def __len__(self):
        return len(self._partitions)

    def find(self, element):
        return self._mapping[element]

    def union(self, partition1_name, partition2_name, new_name=None):

        partition_1 = self._partitions.pop(partition1_name)
        partition_2 = self._partitions.pop(partition2_name)

        new_partition = partition_1 | partition_2
        new_partition.name = new_name or new_partition.name

        self._partitions[new_partition.name] = new_partition
        for e in new_partition:
            self._mapping[e] = new_partition.name

        return new_partition
