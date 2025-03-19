#!/usr/bin/env python3
"""Example script demonstrating the RF GDS Library."""

import os
import sys
import argparse

import gdsfactory as gf

# Add the parent directory to the path to import rf_gds
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rf_gds


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="RF GDS Library Example")
    parser.add_argument("--yaml", type=str, default="schema.yaml", help="YAML file to load")
    parser.add_argument("--output", type=str, default="output.gds", help="Output GDS file")
    args = parser.parse_args()
    
    # Get the absolute path to the YAML file
    yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.yaml)
    
    print(f"Loading design from {yaml_path}...")
    
    # Load the design
    design = rf_gds.load_design(yaml_path)
    
    print(f"Design '{design.name}' loaded with {len(design.components)} components")
    
    # Convert to GDS
    print(f"Converting to GDS...")
    gds = design.to_gds()
    
    # Save to file
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.output)
    gds.write_gds(output_path)
    
    print(f"GDS written to {output_path}")
    
    # Optionally show the design
    # gds.show()


if __name__ == "__main__":
    main()
