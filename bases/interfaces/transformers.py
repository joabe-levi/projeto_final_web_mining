from abc import ABC, abstractmethod


class TransformInterface(ABC):
    
    @abstractmethod
    def do_transform(self, **kwargs):
        """Transforma o DataFrame de entrada e retorna o DataFrame transformado"""
        pass
