"""Power divider components for RF GDS Library."""

from typing import Dict, Any, Tuple, Optional, ClassVar, List
import math

import gdsfactory as gf
import numpy as np

from rf_gds.components.base import BasicStructure, register_component


@register_component
class WilkinsonDivider(BasicStructure):
    """A Wilkinson power divider."""

    type: ClassVar[str] = "wilkinson_divider"
    radius: float  # Radius of the quarter-wave sections
    width: float  # Width of the transmission lines
    isolation_resistor_width: float  # Width of the isolation resistor
    isolation_resistor_length: float  # Length of the isolation resistor
    layer: Tuple[int, int] = (1, 0)  # Default layer
    resistor_layer: Tuple[int, int] = (2, 0)  # Layer for the resistor
    
    def to_gds(self) -> gf.Component:
        """Convert the Wilkinson divider to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Create the input line
        input_line_length = self.radius / 2
        input_line = component.add_polygon(
            [
                (-input_line_length, -self.width/2),
                (0, -self.width/2),
                (0, self.width/2),
                (-input_line_length, self.width/2),
            ],
            layer=self.layer,
        )
        
        # Create the quarter-wave sections
        # Number of points for the arcs
        n_points = 50
        
        # Top quarter-wave section
        top_theta = np.linspace(0, np.pi/2, n_points)
        top_inner_radius = self.radius - self.width/2
        top_outer_radius = self.radius + self.width/2
        
        top_inner_points = [(top_inner_radius * np.cos(t), top_inner_radius * np.sin(t)) for t in top_theta]
        top_outer_points = [(top_outer_radius * np.cos(t), top_outer_radius * np.sin(t)) for t in reversed(top_theta)]
        
        top_points = top_inner_points + top_outer_points
        top_quarter_wave = component.add_polygon(top_points, layer=self.layer)
        
        # Bottom quarter-wave section
        bottom_theta = np.linspace(-np.pi/2, 0, n_points)
        bottom_inner_radius = self.radius - self.width/2
        bottom_outer_radius = self.radius + self.width/2
        
        bottom_inner_points = [(bottom_inner_radius * np.cos(t), bottom_inner_radius * np.sin(t)) for t in bottom_theta]
        bottom_outer_points = [(bottom_outer_radius * np.cos(t), bottom_outer_radius * np.sin(t)) for t in reversed(bottom_theta)]
        
        bottom_points = bottom_inner_points + bottom_outer_points
        bottom_quarter_wave = component.add_polygon(bottom_points, layer=self.layer)
        
        # Create the output lines
        output_line_length = self.radius / 2
        
        # Top output line
        top_output_line = component.add_polygon(
            [
                (self.radius, self.radius - self.width/2),
                (self.radius + output_line_length, self.radius - self.width/2),
                (self.radius + output_line_length, self.radius + self.width/2),
                (self.radius, self.radius + self.width/2),
            ],
            layer=self.layer,
        )
        
        # Bottom output line
        bottom_output_line = component.add_polygon(
            [
                (self.radius, -self.radius - self.width/2),
                (self.radius + output_line_length, -self.radius - self.width/2),
                (self.radius + output_line_length, -self.radius + self.width/2),
                (self.radius, -self.radius + self.width/2),
            ],
            layer=self.layer,
        )
        
        # Create the isolation resistor
        resistor = component.add_polygon(
            [
                (self.radius, self.radius - self.isolation_resistor_width/2),
                (self.radius, -self.radius + self.isolation_resistor_width/2),
                (self.radius + self.isolation_resistor_length, -self.radius + self.isolation_resistor_width/2),
                (self.radius + self.isolation_resistor_length, self.radius - self.isolation_resistor_width/2),
            ],
            layer=self.resistor_layer,
        )
        
        # Add ports
        # Input port
        component.add_port(
            name="in",
            center=(-input_line_length, 0),
            width=self.width,
            orientation=180,
            layer=self.layer,
        )
        
        # Top output port
        component.add_port(
            name="out1",
            center=(self.radius + output_line_length, self.radius),
            width=self.width,
            orientation=0,
            layer=self.layer,
        )
        
        # Bottom output port
        component.add_port(
            name="out2",
            center=(self.radius + output_line_length, -self.radius),
            width=self.width,
            orientation=0,
            layer=self.layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="in",
            position=(-input_line_length, 0),
            width=self.width,
            layer=self.layer,
            orientation=180,
        )
        
        self.add_port(
            name="out1",
            position=(self.radius + output_line_length, self.radius),
            width=self.width,
            layer=self.layer,
            orientation=0,
        )
        
        self.add_port(
            name="out2",
            position=(self.radius + output_line_length, -self.radius),
            width=self.width,
            layer=self.layer,
            orientation=0,
        )
        
        return component


@register_component
class BranchLineCoupler(BasicStructure):
    """A branch-line coupler (90° hybrid)."""

    type: ClassVar[str] = "branch_line_coupler"
    size: float  # Size of the square coupler
    width: float  # Width of the transmission lines
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the branch-line coupler to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Create the four sides of the coupler
        # Top side
        top_side = component.add_polygon(
            [
                (0, self.size - self.width/2),
                (self.size, self.size - self.width/2),
                (self.size, self.size + self.width/2),
                (0, self.size + self.width/2),
            ],
            layer=self.layer,
        )
        
        # Right side
        right_side = component.add_polygon(
            [
                (self.size - self.width/2, 0),
                (self.size + self.width/2, 0),
                (self.size + self.width/2, self.size),
                (self.size - self.width/2, self.size),
            ],
            layer=self.layer,
        )
        
        # Bottom side
        bottom_side = component.add_polygon(
            [
                (0, -self.width/2),
                (self.size, -self.width/2),
                (self.size, self.width/2),
                (0, self.width/2),
            ],
            layer=self.layer,
        )
        
        # Left side
        left_side = component.add_polygon(
            [
                (-self.width/2, 0),
                (self.width/2, 0),
                (self.width/2, self.size),
                (-self.width/2, self.size),
            ],
            layer=self.layer,
        )
        
        # Add ports
        # Port 1 (input)
        component.add_port(
            name="p1",
            center=(-self.width/2, 0),
            width=self.width,
            orientation=180,
            layer=self.layer,
        )
        
        # Port 2 (direct)
        component.add_port(
            name="p2",
            center=(self.size, -self.width/2),
            width=self.width,
            orientation=270,
            layer=self.layer,
        )
        
        # Port 3 (isolated)
        component.add_port(
            name="p3",
            center=(self.size + self.width/2, self.size),
            width=self.width,
            orientation=0,
            layer=self.layer,
        )
        
        # Port 4 (coupled)
        component.add_port(
            name="p4",
            center=(0, self.size + self.width/2),
            width=self.width,
            orientation=90,
            layer=self.layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="p1",
            position=(-self.width/2, 0),
            width=self.width,
            layer=self.layer,
            orientation=180,
        )
        
        self.add_port(
            name="p2",
            position=(self.size, -self.width/2),
            width=self.width,
            layer=self.layer,
            orientation=270,
        )
        
        self.add_port(
            name="p3",
            position=(self.size + self.width/2, self.size),
            width=self.width,
            layer=self.layer,
            orientation=0,
        )
        
        self.add_port(
            name="p4",
            position=(0, self.size + self.width/2),
            width=self.width,
            layer=self.layer,
            orientation=90,
        )
        
        return component


@register_component
class RatRaceCoupler(BasicStructure):
    """A rat-race coupler (180° hybrid)."""

    type: ClassVar[str] = "rat_race_coupler"
    radius: float  # Radius of the ring
    width: float  # Width of the transmission lines
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the rat-race coupler to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Create the ring
        # Number of points for the ring
        n_points = 100
        
        # Inner and outer radius
        inner_radius = self.radius - self.width/2
        outer_radius = self.radius + self.width/2
        
        # Create points for the ring
        theta = np.linspace(0, 2*np.pi, n_points)
        inner_points = [(inner_radius * np.cos(t), inner_radius * np.sin(t)) for t in theta]
        outer_points = [(outer_radius * np.cos(t), outer_radius * np.sin(t)) for t in reversed(theta)]
        
        # Create the ring polygon
        ring_points = inner_points + outer_points
        ring = component.add_polygon(ring_points, layer=self.layer)
        
        # Create the four ports
        # Port positions (at 0°, 90°, 180°, and 270°)
        port_angles = [0, np.pi/2, np.pi, 3*np.pi/2]
        port_positions = [(self.radius * np.cos(angle), self.radius * np.sin(angle)) for angle in port_angles]
        
        # Port extensions
        extension_length = self.radius / 2
        
        # Create the port extensions
        for i, (x, y) in enumerate(port_positions):
            # Calculate the extension direction
            angle = port_angles[i]
            dx = np.cos(angle)
            dy = np.sin(angle)
            
            # Create the extension
            extension = component.add_polygon(
                [
                    (x - self.width/2 * dy, y + self.width/2 * dx),
                    (x + extension_length * dx - self.width/2 * dy, y + extension_length * dy + self.width/2 * dx),
                    (x + extension_length * dx + self.width/2 * dy, y + extension_length * dy - self.width/2 * dx),
                    (x + self.width/2 * dy, y - self.width/2 * dx),
                ],
                layer=self.layer,
            )
            
            # Add the port
            orientation = int(np.degrees(angle))
            component.add_port(
                name=f"p{i+1}",
                center=(x + extension_length * dx, y + extension_length * dy),
                width=self.width,
                orientation=orientation,
                layer=self.layer,
            )
            
            # Update our internal ports
            self.add_port(
                name=f"p{i+1}",
                position=(x + extension_length * dx, y + extension_length * dy),
                width=self.width,
                layer=self.layer,
                orientation=orientation,
            )
        
        return component
