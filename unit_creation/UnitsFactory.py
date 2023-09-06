from abc import ABC, abstractmethod


class UnitsFactory(ABC):
    @abstractmethod
    def create_range_unit(self):
        pass

    @abstractmethod
    def create_melee_unit(self):
        pass

class TriangularUnitFactory(UnitsFactory):
    def create_range_unit(self):
        return TriangularUnit()

    def create_melee_unit(self):
        return MilitaryUnit()