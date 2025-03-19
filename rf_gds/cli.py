#!/usr/bin/env python3
"""Command-line interface for RF GDS Library."""

import os
import sys
import argparse

import rf_gds


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="RF GDS Library CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert YAML to GDS")
    convert_parser.add_argument("yaml_file", help="YAML file to convert")
    convert_parser.add_argument("--output", "-o", help="Output GDS file")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate YAML file")
    validate_parser.add_argument("yaml_file", help="YAML file to validate")
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.command == "convert":
        convert_yaml_to_gds(args.yaml_file, args.output)
    elif args.command == "validate":
        validate_yaml(args.yaml_file)
    else:
        parser.print_help()


def convert_yaml_to_gds(yaml_file, output_file=None):
    """Convert a YAML file to GDS.
    
    Args:
        yaml_file: Path to the YAML file
        output_file: Path to the output GDS file
    """
    try:
        # Load the design
        design = rf_gds.load_design(yaml_file)
        
        # Set default output file if not provided
        if output_file is None:
            output_file = os.path.splitext(yaml_file)[0] + ".gds"
        
        # Convert to GDS
        gds = design.to_gds(output_file)
        
        print(f"Converted {yaml_file} to {output_file}")
        
    except Exception as e:
        print(f"Error converting {yaml_file}: {e}")
        sys.exit(1)


def validate_yaml(yaml_file):
    """Validate a YAML file.
    
    Args:
        yaml_file: Path to the YAML file
    """
    try:
        import yaml
        from rf_gds.yaml_parser import validate_yaml_schema
        
        # Load the YAML file
        with open(yaml_file, "r") as f:
            yaml_data = yaml.safe_load(f)
        
        # Validate the schema
        errors = validate_yaml_schema(yaml_data)
        
        if errors:
            print(f"Validation failed for {yaml_file}:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print(f"Validation successful for {yaml_file}")
        
    except Exception as e:
        print(f"Error validating {yaml_file}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
