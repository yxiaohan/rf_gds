#!/usr/bin/env python3
"""Script to visualize individual RF components."""

import os
import sys
import argparse

import gdsfactory as gf

# Add the parent directory to the path to import rf_gds
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf_gds.components.transmission_lines.microstrip import MicrostripLine, TaperedMicrostripLine, CurvedMicrostripLine
from rf_gds.components.transmission_lines.cpw import CPWLine, CPWBend, CPWTaper
from rf_gds.components.passive.inductor import SpiralInductor, SymmetricInductor, SolenoidInductor
from rf_gds.components.passive.capacitor import MIMCapacitor, InterdigitatedCapacitor, ParallelPlateCapacitor
from rf_gds.components.basic_structures.power_divider import WilkinsonDivider, BranchLineCoupler, RatRaceCoupler


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Visualize RF GDS components")
    parser.add_argument("--component", type=str, required=True, help="Component type to visualize")
    parser.add_argument("--output", type=str, default="component.gds", help="Output GDS file")
    args = parser.parse_args()
    
    # Create the component
    component = None
    
    if args.component == "microstrip":
        component = MicrostripLine(
            name="microstrip",
            length=100,
            width=10,
            layer=(1, 0),
        )
    elif args.component == "tapered_microstrip":
        component = TaperedMicrostripLine(
            name="tapered_microstrip",
            length=100,
            width_in=5,
            width_out=15,
            layer=(1, 0),
        )
    elif args.component == "curved_microstrip":
        component = CurvedMicrostripLine(
            name="curved_microstrip",
            radius=50,
            width=10,
            angle=90,
            layer=(1, 0),
        )
    elif args.component == "cpw":
        component = CPWLine(
            name="cpw",
            length=100,
            width=10,
            gap=5,
            ground_width=20,
            layer=(1, 0),
        )
    elif args.component == "cpw_bend":
        component = CPWBend(
            name="cpw_bend",
            radius=50,
            width=10,
            gap=5,
            ground_width=20,
            angle=90,
            layer=(1, 0),
        )
    elif args.component == "cpw_taper":
        component = CPWTaper(
            name="cpw_taper",
            length=100,
            width_in=5,
            width_out=15,
            gap_in=3,
            gap_out=8,
            ground_width=20,
            layer=(1, 0),
        )
    elif args.component == "spiral_inductor":
        component = SpiralInductor(
            name="spiral_inductor",
            n_turns=3.5,
            width=5,
            spacing=5,
            inner_radius=20,
            layer=(1, 0),
        )
    elif args.component == "symmetric_inductor":
        component = SymmetricInductor(
            name="symmetric_inductor",
            n_turns=3.5,
            width=5,
            spacing=5,
            inner_radius=20,
            layer=(1, 0),
            underpass_layer=(2, 0),
        )
    elif args.component == "solenoid_inductor":
        component = SolenoidInductor(
            name="solenoid_inductor",
            n_turns=5,
            width=5,
            length=100,
            diameter=30,
            via_size=5,
            top_layer=(1, 0),
            bottom_layer=(2, 0),
            via_layer=(3, 0),
        )
    elif args.component == "mim_capacitor":
        component = MIMCapacitor(
            name="mim_capacitor",
            width=50,
            length=50,
            top_layer=(1, 0),
            bottom_layer=(2, 0),
            dielectric_layer=(3, 0),
        )
    elif args.component == "interdigitated_capacitor":
        component = InterdigitatedCapacitor(
            name="interdigitated_capacitor",
            n_fingers=5,
            finger_length=50,
            finger_width=5,
            finger_spacing=5,
            layer=(1, 0),
        )
    elif args.component == "parallel_plate_capacitor":
        component = ParallelPlateCapacitor(
            name="parallel_plate_capacitor",
            width=50,
            length=50,
            plate_spacing=10,
            layer=(1, 0),
        )
    elif args.component == "wilkinson_divider":
        component = WilkinsonDivider(
            name="wilkinson_divider",
            radius=100,
            width=5,
            isolation_resistor_width=5,
            isolation_resistor_length=20,
            layer=(1, 0),
            resistor_layer=(2, 0),
        )
    elif args.component == "branch_line_coupler":
        component = BranchLineCoupler(
            name="branch_line_coupler",
            size=100,
            width=5,
            layer=(1, 0),
        )
    elif args.component == "rat_race_coupler":
        component = RatRaceCoupler(
            name="rat_race_coupler",
            radius=100,
            width=5,
            layer=(1, 0),
        )
    else:
        print(f"Unknown component type: {args.component}")
        sys.exit(1)
    
    # Convert to GDS
    gds = component.to_gds()
    
    # Save to file
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.output)
    gds.write_gds(output_path)
    
    print(f"Component '{args.component}' written to {output_path}")
    
    # Show the component
    gds.show()


if __name__ == "__main__":
    main()
