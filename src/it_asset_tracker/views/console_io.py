import os
from abc import ABC, abstractmethod

class IInputProvider(ABC):
    @abstractmethod
    def get_input(self, prompt: str = "") -> str:
        pass

class IOutputDisplay(ABC):
    @abstractmethod
    def display(self, message: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

class ConsoleIO(IInputProvider, IOutputDisplay):
    def get_input(self, prompt: str = "") -> str:
        return input(prompt)

    def display(self, message: str) -> None:
        print(message)

    def clear(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')