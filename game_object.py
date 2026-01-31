from abc import ABC, abstractmethod

class GameObject(ABC):
    """Abstract base class for all game objects."""

    @abstractmethod
    def update(self):
        """Update the state of the object (e.g., position, physics)."""
        pass

    @abstractmethod
    def draw(self, screen):
        """Draw the object onto the screen."""
        pass
