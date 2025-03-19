"""Base component classes for RF GDS Library."""

from typing import Dict, List, Tuple, Optional, Any, Type, ClassVar, Union
from abc import ABC, abstractmethod

import gdsfactory as gf
from pydantic import BaseModel, Field


class Port(BaseModel):
    """Represents a port on a component."""

    name: str
    position: Tuple[float, float]
    width: float
    layer: Tuple[int, int]
    orientation: float = 0  # in degrees


class Connection(BaseModel):
    """Represents a connection between two ports."""

    port: str
    target: str
    target_port: str


class Component(BaseModel, ABC):
    """Base class for all RF components."""

    name: str
    type: ClassVar[str]
    parameters: Dict[str, Any] = Field(default_factory=dict)
    position: Tuple[float, float] = (0, 0)
    rotation: float = 0
    ports: Dict[str, Port] = Field(default_factory=dict)
    connections: List[Connection] = Field(default_factory=list)
    
    def add_port(self, name: str, position: Tuple[float, float], width: float, 
                 layer: Tuple[int, int], orientation: float = 0) -> None:
        """Add a port to the component.
        
        Args:
            name: Port name
            position: Port position (x, y)
            width: Port width
            layer: Port layer (layer, datatype)
            orientation: Port orientation in degrees
        """
        self.ports[name] = Port(
            name=name,
            position=position,
            width=width,
            layer=layer,
            orientation=orientation,
        )
    
    def add_connection(self, port: str, target: str, target_port: str) -> None:
        """Add a connection to another component.
        
        Args:
            port: Name of the port on this component
            target: Name of the target component
            target_port: Name of the port on the target component
        """
        self.connections.append(
            Connection(port=port, target=target, target_port=target_port)
        )
    
    @abstractmethod
    def to_gds(self) -> gf.Component:
        """Convert the component to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        pass


class TransmissionLine(Component, ABC):
    """Base class for transmission line components."""

    type: ClassVar[str] = "transmission_line"
    length: float
    width: float
    
    @abstractmethod
    def to_gds(self) -> gf.Component:
        pass


class PassiveComponent(Component, ABC):
    """Base class for passive components."""

    type: ClassVar[str] = "passive"
    
    @abstractmethod
    def to_gds(self) -> gf.Component:
        pass


class BasicStructure(Component, ABC):
    """Base class for basic RF structures."""

    type: ClassVar[str] = "basic_structure"
    
    @abstractmethod
    def to_gds(self) -> gf.Component:
        pass


class AdvancedStructure(Component, ABC):
    """Base class for advanced RF structures."""

    type: ClassVar[str] = "advanced_structure"
    
    @abstractmethod
    def to_gds(self) -> gf.Component:
        pass


# Registry of component classes
_component_registry: Dict[str, Type[Component]] = {}


def register_component(cls: Type[Component]) -> Type[Component]:
    """Register a component class.
    
    Args:
        cls: The component class to register
        
    Returns:
        The component class
    """
    _component_registry[cls.type] = cls
    return cls


def get_component_class(component_type: str) -> Type[Component]:
    """Get a component class by type.
    
    Args:
        component_type: The component type
        
    Returns:
        The component class
        
    Raises:
        ValueError: If the component type is not registered
    """
    if component_type not in _component_registry:
        raise ValueError(f"Unknown component type: {component_type}")
    return _component_registry[component_type]
