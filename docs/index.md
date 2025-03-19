# RF GDS Library Documentation

Welcome to the RF GDS Library documentation. This library allows you to convert human-readable YAML descriptions of RFIC (Radio Frequency Integrated Circuit) designs into GDS(II) files ready for simulation, using gdsfactory as the backend.

## Overview

RF GDS Library provides:

- A simple YAML schema for describing RF components and designs
- A comprehensive library of RF-specific components
- Integration with gdsfactory for GDS generation
- Tools for validation and verification

## Installation

To install the library, clone the repository and install it using pip:

```bash
git clone https://github.com/yourusername/rf_gds.git
cd rf_gds
pip install -e .
```

## Quick Start

Here's a simple example of how to use the library:

```python
import rf_gds

# Load a design from a YAML file
design = rf_gds.load_design("my_design.yaml")

# Convert to GDS
gds = design.to_gds()

# Save to file
gds.write_gds("my_design.gds")
```

## YAML Schema

The library uses a simple YAML schema to describe RF designs. Here's an example:

```yaml
name: example_rf_design
technology: generic
units: um  # micrometers

# Components section defines all the components in the design
components:
  # Microstrip transmission line
  - name: line1
    type: microstrip_line
    parameters:
      length: 100
      width: 5
      layer: [1, 0]
    position: [0, 0]
    rotation: 0
    connections: []
```

See the [YAML Schema](yaml_schema.md) page for more details.

## Component Library

The library includes a comprehensive set of RF components:

- [Transmission Lines](components/transmission_lines.md)
- [Passive Components](components/passive.md)
- [Basic RF Structures](components/basic_structures.md)
- [Advanced RF Structures](components/advanced_structures.md)

## API Reference

For detailed API documentation, see the [API Reference](api/index.md) section.
