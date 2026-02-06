import importlib
import pkgutil
from abc import ABC
from types import ModuleType

from keneth.di_contracts import ServiceInterface


class ClassResolver(ServiceInterface):
    """ClassResolver service.

    Responsible for dynamically loading modules
    and resolving classes that are subclasses of a given base class.
    """

    def __init__(self) -> None:
        """Initialize the ClassResolver with an empty list of modules."""
        self.modules = []

    def __load_module(self, package: ModuleType) -> None:
        """Load a module and its submodules from a given package.

        Args:
            package (ModuleType): The package to load modules from.
        """
        for _, module_name, _ in pkgutil.walk_packages(
            package.__path__, package.__name__ + "."
        ):
            module = importlib.import_module(module_name)
            self.modules.append(module)

    def load_modules(self, packages: list[ModuleType]) -> None:
        """Load modules from a list of packages.

        Args:
            packages (list[ModuleType]): The list of packages to load modules from.
        """
        for package in packages:
            self.__load_module(package)

    def resolve(self, base_class: type[ABC]) -> list[type[ABC]]:
        """Resolve and return all subclasses of a given base class.

        Args:
            base_class (type[ABC]): The base class to find subclasses of.
        Returns:
            list[type[ABC]]: A list of subclasses of the given base class.
        """
        subclasses = []
        for module in self.modules:
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if (
                    isinstance(attribute, type)
                    and issubclass(attribute, base_class)
                    and attribute is not base_class
                ):
                    subclasses.append(attribute)
        return subclasses
