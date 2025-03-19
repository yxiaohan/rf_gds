"""Base PDK class for RF GDS Library."""

from typing import Dict, Any, List, Tuple, Optional, Type, ClassVar, Union
from pydantic import BaseModel, Field


class Layer(BaseModel):
    """Represents a layer in a PDK."""
    
    name: str
    layer: int
    datatype: int = 0
    description: str = ""
    
    def as_tuple(self) -> Tuple[int, int]:
        """Return the layer as a tuple (layer, datatype)."""
        return (self.layer, self.datatype)


class PDK(BaseModel):
    """Base class for Process Design Kits (PDKs)."""
    
    name: ClassVar[str]
    description: str = ""
    layers: Dict[str, Layer] = Field(default_factory=dict)
    design_rules: Dict[str, Any] = Field(default_factory=dict)
    
    def get_layer(self, layer_name: str) -> Tuple[int, int]:
        """Get a layer by name.
        
        Args:
            layer_name: The name of the layer
            
        Returns:
            A tuple (layer, datatype)
            
        Raises:
            KeyError: If the layer is not found
        """
        if layer_name not in self.layers:
            raise KeyError(f"Layer {layer_name} not found in PDK {self.name}")
        return self.layers[layer_name].as_tuple()
    
    def get_design_rule(self, rule_name: str) -> Any:
        """Get a design rule by name.
        
        Args:
            rule_name: The name of the design rule
            
        Returns:
            The design rule value
            
        Raises:
            KeyError: If the design rule is not found
        """
        if rule_name not in self.design_rules:
            raise KeyError(f"Design rule {rule_name} not found in PDK {self.name}")
        return self.design_rules[rule_name]


# Registry of PDKs
_pdk_registry: Dict[str, Type[PDK]] = {}


def register_pdk(cls: Type[PDK]) -> Type[PDK]:
    """Register a PDK.
    
    Args:
        cls: The PDK class to register
        
    Returns:
        The PDK class
    """
    _pdk_registry[cls.name] = cls
    return cls


def get_pdk(pdk_name: str) -> PDK:
    """Get a PDK by name.
    
    Args:
        pdk_name: The name of the PDK
        
    Returns:
        An instance of the PDK
        
    Raises:
        ValueError: If the PDK is not registered
    """
    if pdk_name not in _pdk_registry:
        raise ValueError(f"Unknown PDK: {pdk_name}")
    return _pdk_registry[pdk_name]()
