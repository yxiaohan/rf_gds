"""Inductor components for RF GDS Library."""

from typing import Dict, Any, Tuple, Optional, ClassVar, List
import math

import gdsfactory as gf
import numpy as np

from rf_gds.components.base import PassiveComponent, register_component


@register_component
class SpiralInductor(PassiveComponent):
    """A spiral inductor."""

    type: ClassVar[str] = "spiral_inductor"
    n_turns: float  # Number of turns (can be fractional)
    width: float  # Trace width
    spacing: float  # Spacing between traces
    inner_radius: float  # Inner radius
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the spiral inductor to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Calculate spiral parameters
        n_points = max(100, int(self.n_turns * 20))  # More points for more turns
        theta = np.linspace(0, 2 * np.pi * self.n_turns, n_points)
        
        # Calculate the spiral radius at each point
        # r = inner_radius + spacing * theta / (2 * pi)
        radius = self.inner_radius + self.spacing * theta / (2 * np.pi)
        
        # Calculate the x, y coordinates
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        # Create the spiral path
        points = list(zip(x, y))
        spiral_path = component.add_path(points, width=self.width, layer=self.layer)
        
        # Calculate the outer radius
        outer_radius = self.inner_radius + self.spacing * self.n_turns
        
        # Add a straight segment to the outer port
        # Calculate the end point of the spiral
        end_x = x[-1]
        end_y = y[-1]
        
        # Calculate the angle of the end point
        end_angle = theta[-1] % (2 * np.pi)
        
        # Calculate the direction vector
        dir_x = np.cos(end_angle + np.pi/2)
        dir_y = np.sin(end_angle + np.pi/2)
        
        # Create a straight path to the edge
        straight_length = outer_radius + self.width
        
        straight_path = component.add_path(
            [(end_x, end_y), (end_x + dir_x * straight_length, end_y + dir_y * straight_length)],
            width=self.width,
            layer=self.layer,
        )
        
        # Add ports
        # Inner port (at the center)
        component.add_port(
            name="in",
            center=(x[0], y[0]),
            width=self.width,
            orientation=0,  # This will need to be calculated based on the spiral
            layer=self.layer,
        )
        
        # Outer port
        outer_port_x = end_x + dir_x * straight_length
        outer_port_y = end_y + dir_y * straight_length
        
        component.add_port(
            name="out",
            center=(outer_port_x, outer_port_y),
            width=self.width,
            orientation=(np.degrees(end_angle) + 90) % 360,
            layer=self.layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="in",
            position=(x[0], y[0]),
            width=self.width,
            layer=self.layer,
            orientation=0,
        )
        
        self.add_port(
            name="out",
            position=(outer_port_x, outer_port_y),
            width=self.width,
            layer=self.layer,
            orientation=(np.degrees(end_angle) + 90) % 360,
        )
        
        return component


@register_component
class SymmetricInductor(PassiveComponent):
    """A symmetric spiral inductor with two ports on opposite sides."""

    type: ClassVar[str] = "symmetric_inductor"
    n_turns: float  # Number of turns (can be fractional)
    width: float  # Trace width
    spacing: float  # Spacing between traces
    inner_radius: float  # Inner radius
    underpass_layer: Tuple[int, int] = (2, 0)  # Layer for the underpass
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the symmetric inductor to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Calculate spiral parameters
        n_points = max(100, int(self.n_turns * 20))  # More points for more turns
        theta = np.linspace(0, 2 * np.pi * self.n_turns, n_points)
        
        # Calculate the spiral radius at each point
        # r = inner_radius + spacing * theta / (2 * pi)
        radius = self.inner_radius + self.spacing * theta / (2 * np.pi)
        
        # Calculate the x, y coordinates
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        # Create the spiral path
        points = list(zip(x, y))
        spiral_path = component.add_path(points, width=self.width, layer=self.layer)
        
        # Calculate the outer radius
        outer_radius = self.inner_radius + self.spacing * self.n_turns
        
        # Add an underpass to connect to the center
        # First, calculate the angle for the underpass
        underpass_angle = np.pi  # 180 degrees, opposite to the start
        
        # Calculate the underpass path
        underpass_x1 = -outer_radius - self.width
        underpass_y1 = 0
        underpass_x2 = -self.inner_radius
        underpass_y2 = 0
        
        underpass_path = component.add_path(
            [(underpass_x1, underpass_y1), (underpass_x2, underpass_y2)],
            width=self.width,
            layer=self.underpass_layer,
        )
        
        # Add ports
        # Port 1 (at the center)
        component.add_port(
            name="p1",
            center=(x[0], y[0]),
            width=self.width,
            orientation=0,
            layer=self.layer,
        )
        
        # Port 2 (at the underpass)
        component.add_port(
            name="p2",
            center=(underpass_x1, underpass_y1),
            width=self.width,
            orientation=180,
            layer=self.underpass_layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="p1",
            position=(x[0], y[0]),
            width=self.width,
            layer=self.layer,
            orientation=0,
        )
        
        self.add_port(
            name="p2",
            position=(underpass_x1, underpass_y1),
            width=self.width,
            layer=self.underpass_layer,
            orientation=180,
        )
        
        return component


@register_component
class SolenoidInductor(PassiveComponent):
    """A 3D solenoid inductor."""

    type: ClassVar[str] = "solenoid_inductor"
    n_turns: int  # Number of turns (integer)
    width: float  # Trace width
    length: float  # Length of the solenoid
    diameter: float  # Diameter of the solenoid
    via_size: float = 1.0  # Size of the vias
    top_layer: Tuple[int, int] = (1, 0)  # Top metal layer
    bottom_layer: Tuple[int, int] = (2, 0)  # Bottom metal layer
    via_layer: Tuple[int, int] = (3, 0)  # Via layer
    
    def to_gds(self) -> gf.Component:
        """Convert the solenoid inductor to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Calculate parameters
        segment_length = self.length / self.n_turns
        
        # Create the solenoid
        for i in range(self.n_turns):
            # Calculate the position of this turn
            x_start = i * segment_length
            x_end = (i + 1) * segment_length
            
            # Top segment
            if i % 2 == 0:
                top_segment = component.add_polygon(
                    [
                        (x_start, -self.diameter/2 - self.width/2),
                        (x_end, -self.diameter/2 - self.width/2),
                        (x_end, -self.diameter/2 + self.width/2),
                        (x_start, -self.diameter/2 + self.width/2),
                    ],
                    layer=self.top_layer,
                )
            else:
                top_segment = component.add_polygon(
                    [
                        (x_start, self.diameter/2 - self.width/2),
                        (x_end, self.diameter/2 - self.width/2),
                        (x_end, self.diameter/2 + self.width/2),
                        (x_start, self.diameter/2 + self.width/2),
                    ],
                    layer=self.top_layer,
                )
            
            # Bottom segment
            if i % 2 == 0:
                bottom_segment = component.add_polygon(
                    [
                        (x_start, self.diameter/2 - self.width/2),
                        (x_end, self.diameter/2 - self.width/2),
                        (x_end, self.diameter/2 + self.width/2),
                        (x_start, self.diameter/2 + self.width/2),
                    ],
                    layer=self.bottom_layer,
                )
            else:
                bottom_segment = component.add_polygon(
                    [
                        (x_start, -self.diameter/2 - self.width/2),
                        (x_end, -self.diameter/2 - self.width/2),
                        (x_end, -self.diameter/2 + self.width/2),
                        (x_start, -self.diameter/2 + self.width/2),
                    ],
                    layer=self.bottom_layer,
                )
            
            # Add vias at the ends of the segments
            if i < self.n_turns - 1:
                # Via at the end of this turn
                if i % 2 == 0:
                    via = component.add_polygon(
                        [
                            (x_end - self.via_size/2, -self.diameter/2 - self.via_size/2),
                            (x_end + self.via_size/2, -self.diameter/2 - self.via_size/2),
                            (x_end + self.via_size/2, -self.diameter/2 + self.via_size/2),
                            (x_end - self.via_size/2, -self.diameter/2 + self.via_size/2),
                        ],
                        layer=self.via_layer,
                    )
                else:
                    via = component.add_polygon(
                        [
                            (x_end - self.via_size/2, self.diameter/2 - self.via_size/2),
                            (x_end + self.via_size/2, self.diameter/2 - self.via_size/2),
                            (x_end + self.via_size/2, self.diameter/2 + self.via_size/2),
                            (x_end - self.via_size/2, self.diameter/2 + self.via_size/2),
                        ],
                        layer=self.via_layer,
                    )
        
        # Add ports
        # Port 1 (at the start)
        if self.n_turns % 2 == 0:
            p1_y = self.diameter/2
            p1_layer = self.bottom_layer
        else:
            p1_y = -self.diameter/2
            p1_layer = self.bottom_layer
        
        component.add_port(
            name="p1",
            center=(0, p1_y),
            width=self.width,
            orientation=180,
            layer=p1_layer,
        )
        
        # Port 2 (at the end)
        if self.n_turns % 2 == 1:
            p2_y = self.diameter/2
            p2_layer = self.top_layer
        else:
            p2_y = -self.diameter/2
            p2_layer = self.top_layer
        
        component.add_port(
            name="p2",
            center=(self.length, p2_y),
            width=self.width,
            orientation=0,
            layer=p2_layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="p1",
            position=(0, p1_y),
            width=self.width,
            layer=p1_layer,
            orientation=180,
        )
        
        self.add_port(
            name="p2",
            position=(self.length, p2_y),
            width=self.width,
            layer=p2_layer,
            orientation=0,
        )
        
        return component
