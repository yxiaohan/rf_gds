# RF GDS Library

A Python library for converting human-readable YAML descriptions of RFIC (Radio Frequency Integrated Circuit) designs into GDS(II) files ready for simulation, built on top of gdsfactory.

## Features

- Convert YAML descriptions to GDS(II) files
- Focus on RF-specific components and requirements
- Built on top of gdsfactory for robust GDS generation
- Extensive library of RF components:
  - Transmission lines (microstrip, CPW, stripline)
  - Passive components (resistors, capacitors, inductors, transformers)
  - Basic RF structures (power dividers, couplers, filters, matching networks)
  - Advanced RF structures (resonators, baluns, phase shifters, etc.)

## Installation

```bash
pip install -e .
```

## Quick Start

```python
import rf_gds

# Load a YAML design file
design = rf_gds.load_design("my_design.yaml")

# Generate GDS
gds = design.to_gds()

# Save to file
gds.write_gds("my_design.gds")
```

## Documentation

For full documentation, visit [docs/](./docs/).

## License

MIT
