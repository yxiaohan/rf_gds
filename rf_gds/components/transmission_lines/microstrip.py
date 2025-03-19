"""Microstrip transmission line components."""

from typing import Dict, Any, Tuple, Optional, ClassVar

import gdsfactory as gf
import numpy as np

from rf_gds.components.base import TransmissionLine, register_component


@register_component
class MicrostripLine(TransmissionLine):
    """A simple microstrip transmission line."""

    type: ClassVar[str] = "microstrip_line"
    length: float
    width: float
    layer: Union[Tuple[int, int], str] = (1, 0)  # Default layer or layer name
    
    def to_gds(self) -> gf.Component:
        """Convert the microstrip line to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Get the layer from PDK if available
        layer = self.get_layer(self.layer) if hasattr(self, 'get_layer') else self.layer
        
        # Create the microstrip line
        path = component.add_polygon(
            [
                (0, -self.width/2),
                (self.length, -self.width/2),
                (self.length, self.width/2),
                (0, self.width/2),
            ],
            layer=layer,
        )
        
        # Add ports
        component.add_port(
            name="in",
            center=(0, 0),
            width=self.width,
            orientation=180,
            layer=layer,
        )
        
        component.add_port(
            name="out",
            center=(self.length, 0),
            width=self.width,
            orientation=0,
            layer=layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="in",
            position=(0, 0),
            width=self.width,
            layer=self.layer,
            orientation=180,
        )
        
        self.add_port(
            name="out",
            position=(self.length, 0),
            width=self.width,
            layer=self.layer,
            orientation=0,
        )
        
        return component


@register_component
class TaperedMicrostripLine(TransmissionLine):
    """A tapered microstrip transmission line."""

    type: ClassVar[str] = "tapered_microstrip_line"
    length: float
    width_in: float
    width_out: float
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the tapered microstrip line to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Create the tapered microstrip line
        path = component.add_polygon(
            [
                (0, -self.width_in/2),
                (self.length, -self.width_out/2),
                (self.length, self.width_out/2),
                (0, self.width_in/2),
            ],
            layer=self.layer,
        )
        
        # Add ports
        component.add_port(
            name="in",
            center=(0, 0),
            width=self.width_in,
            orientation=180,
            layer=self.layer,
        )
        
        component.add_port(
            name="out",
            center=(self.length, 0),
            width=self.width_out,
            orientation=0,
            layer=self.layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="in",
            position=(0, 0),
            width=self.width_in,
            layer=self.layer,
            orientation=180,
        )
        
        self.add_port(
            name="out",
            position=(self.length, 0),
            width=self.width_out,
            layer=self.layer,
            orientation=0,
        )
        
        return component


@register_component
class CurvedMicrostripLine(TransmissionLine):
    """A curved microstrip transmission line."""

    type: ClassVar[str] = "curved_microstrip_line"
    radius: float
    width: float
    angle: float = 90  # Default 90 degree bend
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the curved microstrip line to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Calculate the arc
        angle_rad = np.radians(self.angle)
        n_points = max(10, int(self.angle / 5))  # More points for larger angles
        theta = np.linspace(0, angle_rad, n_points)
        
        # Inner and outer radius
        inner_radius = self.radius - self.width/2
        outer_radius = self.radius + self.width/2
        
        # Create points for the arc
        inner_points = [(inner_radius * np.cos(t), inner_radius * np.sin(t)) for t in theta]
        outer_points = [(outer_radius * np.cos(t), outer_radius * np.sin(t)) for t in reversed(theta)]
        
        # Create the polygon
        all_points = inner_points + outer_points
        path = component.add_polygon(all_points, layer=self.layer)
        
        # Calculate port positions and orientations
        in_pos = (inner_radius + self.width/2, 0)
        in_orientation = 180
        
        out_angle = np.radians(self.angle)
        out_pos = ((inner_radius + self.width/2) * np.cos(out_angle), 
                  (inner_radius + self.width/2) * np.sin(out_angle))
        out_orientation = (self.angle + 90) % 360
        
        # Add ports
        component.add_port(
            name="in",
            center=in_pos,
            width=self.width,
            orientation=in_orientation,
            layer=self.layer,
        )
        
        component.add_port(
            name="out",
            center=out_pos,
            width=self.width,
            orientation=out_orientation,
            layer=self.layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="in",
            position=in_pos,
            width=self.width,
            layer=self.layer,
            orientation=in_orientation,
        )
        
        self.add_port(
            name="out",
            position=out_pos,
            width=self.width,
            layer=self.layer,
            orientation=out_orientation,
        )
        
        return component
