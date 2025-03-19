"""Capacitor components for RF GDS Library."""

from typing import Dict, Any, Tuple, Optional, ClassVar, List
import math

import gdsfactory as gf
import numpy as np

from rf_gds.components.base import PassiveComponent, register_component


@register_component
class MIMCapacitor(PassiveComponent):
    """A Metal-Insulator-Metal (MIM) capacitor."""

    type: ClassVar[str] = "mim_capacitor"
    width: float  # Width of the capacitor
    length: float  # Length of the capacitor
    top_layer: Tuple[int, int] = (1, 0)  # Top metal layer
    bottom_layer: Tuple[int, int] = (2, 0)  # Bottom metal layer
    dielectric_layer: Tuple[int, int] = (3, 0)  # Dielectric layer
    
    def to_gds(self) -> gf.Component:
        """Convert the MIM capacitor to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Create the bottom plate (slightly larger than the top plate)
        bottom_margin = 1.0  # Extra margin for the bottom plate
        bottom_plate = component.add_polygon(
            [
                (-bottom_margin, -self.width/2 - bottom_margin),
                (self.length + bottom_margin, -self.width/2 - bottom_margin),
                (self.length + bottom_margin, self.width/2 + bottom_margin),
                (-bottom_margin, self.width/2 + bottom_margin),
            ],
            layer=self.bottom_layer,
        )
        
        # Create the dielectric layer (same size as the top plate)
        dielectric = component.add_polygon(
            [
                (0, -self.width/2),
                (self.length, -self.width/2),
                (self.length, self.width/2),
                (0, self.width/2),
            ],
            layer=self.dielectric_layer,
        )
        
        # Create the top plate
        top_plate = component.add_polygon(
            [
                (0, -self.width/2),
                (self.length, -self.width/2),
                (self.length, self.width/2),
                (0, self.width/2),
            ],
            layer=self.top_layer,
        )
        
        # Add ports
        # Port 1 (to the top plate)
        component.add_port(
            name="p1",
            center=(self.length/2, self.width/2 + 1),
            width=self.width/4,
            orientation=90,
            layer=self.top_layer,
        )
        
        # Port 2 (to the bottom plate)
        component.add_port(
            name="p2",
            center=(self.length/2, -self.width/2 - 1),
            width=self.width/4,
            orientation=270,
            layer=self.bottom_layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="p1",
            position=(self.length/2, self.width/2 + 1),
            width=self.width/4,
            layer=self.top_layer,
            orientation=90,
        )
        
        self.add_port(
            name="p2",
            position=(self.length/2, -self.width/2 - 1),
            width=self.width/4,
            layer=self.bottom_layer,
            orientation=270,
        )
        
        return component


@register_component
class InterdigitatedCapacitor(PassiveComponent):
    """An interdigitated capacitor."""

    type: ClassVar[str] = "interdigitated_capacitor"
    n_fingers: int  # Number of fingers
    finger_length: float  # Length of each finger
    finger_width: float  # Width of each finger
    finger_spacing: float  # Spacing between fingers
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the interdigitated capacitor to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Calculate the total width
        total_width = (self.n_fingers + 1) * self.finger_spacing + self.n_fingers * self.finger_width
        
        # Create the left bus
        left_bus = component.add_polygon(
            [
                (-self.finger_width, -total_width/2),
                (0, -total_width/2),
                (0, total_width/2),
                (-self.finger_width, total_width/2),
            ],
            layer=self.layer,
        )
        
        # Create the right bus
        right_bus = component.add_polygon(
            [
                (self.finger_length, -total_width/2),
                (self.finger_length + self.finger_width, -total_width/2),
                (self.finger_length + self.finger_width, total_width/2),
                (self.finger_length, total_width/2),
            ],
            layer=self.layer,
        )
        
        # Create the fingers
        for i in range(self.n_fingers):
            y_pos = -total_width/2 + self.finger_spacing + i * (self.finger_width + self.finger_spacing)
            
            # Alternate between left and right fingers
            if i % 2 == 0:
                # Left finger
                finger = component.add_polygon(
                    [
                        (0, y_pos),
                        (self.finger_length, y_pos),
                        (self.finger_length, y_pos + self.finger_width),
                        (0, y_pos + self.finger_width),
                    ],
                    layer=self.layer,
                )
            else:
                # Right finger
                finger = component.add_polygon(
                    [
                        (0, y_pos),
                        (self.finger_length, y_pos),
                        (self.finger_length, y_pos + self.finger_width),
                        (0, y_pos + self.finger_width),
                    ],
                    layer=self.layer,
                )
        
        # Add ports
        # Port 1 (left)
        component.add_port(
            name="p1",
            center=(-self.finger_width, 0),
            width=self.finger_width,
            orientation=180,
            layer=self.layer,
        )
        
        # Port 2 (right)
        component.add_port(
            name="p2",
            center=(self.finger_length + self.finger_width, 0),
            width=self.finger_width,
            orientation=0,
            layer=self.layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="p1",
            position=(-self.finger_width, 0),
            width=self.finger_width,
            layer=self.layer,
            orientation=180,
        )
        
        self.add_port(
            name="p2",
            position=(self.finger_length + self.finger_width, 0),
            width=self.finger_width,
            layer=self.layer,
            orientation=0,
        )
        
        return component


@register_component
class ParallelPlateCapacitor(PassiveComponent):
    """A simple parallel plate capacitor."""

    type: ClassVar[str] = "parallel_plate_capacitor"
    width: float  # Width of the plates
    length: float  # Length of the plates
    plate_spacing: float  # Spacing between plates
    layer: Tuple[int, int] = (1, 0)  # Default layer
    
    def to_gds(self) -> gf.Component:
        """Convert the parallel plate capacitor to a GDS component.
        
        Returns:
            A gdsfactory Component
        """
        # Create a new component
        component = gf.Component(name=f"{self.name}")
        
        # Create the top plate
        top_plate = component.add_polygon(
            [
                (0, self.plate_spacing/2),
                (self.length, self.plate_spacing/2),
                (self.length, self.plate_spacing/2 + self.width),
                (0, self.plate_spacing/2 + self.width),
            ],
            layer=self.layer,
        )
        
        # Create the bottom plate
        bottom_plate = component.add_polygon(
            [
                (0, -self.plate_spacing/2 - self.width),
                (self.length, -self.plate_spacing/2 - self.width),
                (self.length, -self.plate_spacing/2),
                (0, -self.plate_spacing/2),
            ],
            layer=self.layer,
        )
        
        # Add ports
        # Port 1 (top plate)
        component.add_port(
            name="p1",
            center=(self.length/2, self.plate_spacing/2 + self.width),
            width=self.width/2,
            orientation=90,
            layer=self.layer,
        )
        
        # Port 2 (bottom plate)
        component.add_port(
            name="p2",
            center=(self.length/2, -self.plate_spacing/2 - self.width),
            width=self.width/2,
            orientation=270,
            layer=self.layer,
        )
        
        # Update our internal ports
        self.add_port(
            name="p1",
            position=(self.length/2, self.plate_spacing/2 + self.width),
            width=self.width/2,
            layer=self.layer,
            orientation=90,
        )
        
        self.add_port(
            name="p2",
            position=(self.length/2, -self.plate_spacing/2 - self.width),
            width=self.width/2,
            layer=self.layer,
            orientation=270,
        )
        
        return component
