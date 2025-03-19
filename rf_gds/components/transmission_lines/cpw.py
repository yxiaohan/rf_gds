"""Coplanar Waveguide (CPW) transmission line components."""

from typing import Dict, Any, Tuple, Optional, ClassVar

import gdsfactory as gf
import numpy as np

from rf_gds.components.base import TransmissionLine, register_component


@register_component
class CPWLine(TransmissionLine):
    """A simple coplanar waveguide transmission line."""

    type: ClassVar[str] = "cpw_line"
    length: float
    width: float  # Center conductor width
    gap: float  # Gap width
    ground_width: float = 10.0  # Ground plane width
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the CPW line to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Create the center conductor
        center = component.add_polygon(
            [
                (0, -self.width/2),
                (self.length, -self.width/2),
                (self.length, self.width/2),
                (0, self.width/2),
            ],
            layer=self.layer,
        )
        
        # Create the ground planes
        total_width = self.width + 2 * self.gap + 2 * self.ground_width
        
        # Top ground plane
        top_ground = component.add_polygon(
            [
                (0, self.width/2 + self.gap),
                (self.length, self.width/2 + self.gap),
                (self.length, self.width/2 + self.gap + self.ground_width),
                (0, self.width/2 + self.gap + self.ground_width),
            ],
            layer=self.layer,
        )
        
        # Bottom ground plane
        bottom_ground = component.add_polygon(
            [
                (0, -self.width/2 - self.gap - self.ground_width),
                (self.length, -self.width/2 - self.gap - self.ground_width),
                (self.length, -self.width/2 - self.gap),
                (0, -self.width/2 - self.gap),
            ],
            layer=self.layer,
        )
        
        # Add ports
        component.add_port(
            name="in",
            center=(0, 0),
            width=self.width,
            orientation=180,
            layer=self.layer,
        )
        
        component.add_port(
            name="out",
            center=(self.length, 0),
            width=self.width,
            orientation=0,
            layer=self.layer,
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
class CPWBend(TransmissionLine):
    """A coplanar waveguide bend."""

    type: ClassVar[str] = "cpw_bend"
    radius: float
    width: float  # Center conductor width
    gap: float  # Gap width
    ground_width: float = 10.0  # Ground plane width
    angle: float = 90  # Default 90 degree bend
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the CPW bend to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Calculate the arc
        angle_rad = np.radians(self.angle)
        n_points = max(10, int(self.angle / 5))  # More points for larger angles
        theta = np.linspace(0, angle_rad, n_points)
        
        # Center conductor
        inner_radius = self.radius - self.width/2
        outer_radius = self.radius + self.width/2
        
        inner_points = [(inner_radius * np.cos(t), inner_radius * np.sin(t)) for t in theta]
        outer_points = [(outer_radius * np.cos(t), outer_radius * np.sin(t)) for t in reversed(theta)]
        
        # Create the center conductor polygon
        center_points = inner_points + outer_points
        center = component.add_polygon(center_points, layer=self.layer)
        
        # Ground planes
        # Inner ground
        inner_ground_inner = self.radius - self.width/2 - self.ground_width
        inner_ground_outer = self.radius - self.width/2 - self.gap
        
        inner_ground_inner_points = [(inner_ground_inner * np.cos(t), inner_ground_inner * np.sin(t)) for t in theta]
        inner_ground_outer_points = [(inner_ground_outer * np.cos(t), inner_ground_outer * np.sin(t)) for t in reversed(theta)]
        
        inner_ground_points = inner_ground_inner_points + inner_ground_outer_points
        inner_ground = component.add_polygon(inner_ground_points, layer=self.layer)
        
        # Outer ground
        outer_ground_inner = self.radius + self.width/2 + self.gap
        outer_ground_outer = self.radius + self.width/2 + self.gap + self.ground_width
        
        outer_ground_inner_points = [(outer_ground_inner * np.cos(t), outer_ground_inner * np.sin(t)) for t in theta]
        outer_ground_outer_points = [(outer_ground_outer * np.cos(t), outer_ground_outer * np.sin(t)) for t in reversed(theta)]
        
        outer_ground_points = outer_ground_inner_points + outer_ground_outer_points
        outer_ground = component.add_polygon(outer_ground_points, layer=self.layer)
        
        # Calculate port positions and orientations
        in_pos = (self.radius, 0)
        in_orientation = 180
        
        out_angle = np.radians(self.angle)
        out_pos = (self.radius * np.cos(out_angle), self.radius * np.sin(out_angle))
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


@register_component
class CPWTaper(TransmissionLine):
    """A coplanar waveguide taper."""

    type: ClassVar[str] = "cpw_taper"
    length: float
    width_in: float  # Input center conductor width
    width_out: float  # Output center conductor width
    gap_in: float  # Input gap width
    gap_out: float  # Output gap width
    ground_width: float = 10.0  # Ground plane width
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the CPW taper to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Create the center conductor
        center = component.add_polygon(
            [
                (0, -self.width_in/2),
                (self.length, -self.width_out/2),
                (self.length, self.width_out/2),
                (0, self.width_in/2),
            ],
            layer=self.layer,
        )
        
        # Create the ground planes
        # Top ground plane
        top_ground = component.add_polygon(
            [
                (0, self.width_in/2 + self.gap_in),
                (self.length, self.width_out/2 + self.gap_out),
                (self.length, self.width_out/2 + self.gap_out + self.ground_width),
                (0, self.width_in/2 + self.gap_in + self.ground_width),
            ],
            layer=self.layer,
        )
        
        # Bottom ground plane
        bottom_ground = component.add_polygon(
            [
                (0, -self.width_in/2 - self.gap_in - self.ground_width),
                (self.length, -self.width_out/2 - self.gap_out - self.ground_width),
                (self.length, -self.width_out/2 - self.gap_out),
                (0, -self.width_in/2 - self.gap_in),
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
