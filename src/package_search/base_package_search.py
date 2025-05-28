from abc import ABC, abstractmethod

class PackageSearch(ABC):
    """Abstract package search."""

    @abstractmethod
    def search(self, value) -> list:
        """Search for a package with the value."""
        pass
