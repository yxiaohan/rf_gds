# YAML Schema

The RF GDS Library uses a YAML schema to describe RF designs. This page documents the schema and provides examples.

## Top-Level Structure

The top-level structure of a YAML design file includes:

```yaml
name: design_name
technology: technology_name
units: um  # micrometers, nm, etc.
metadata:
  # Optional metadata
  author: Author Name
  date: 2025-03-19
  description: Design description
components:
  # List of components
  - name: component1
    type: component_type
    parameters:
      # Component-specific parameters
    position: [x, y]
    rotation: angle
    connections:
      # List of connections
```

## Fields

### Top-Level Fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `name` | string | Name of the design |
| `technology` | string | Technology name |
| `units` | string | Units for dimensions (um, nm, etc.) |
| `metadata` | object | Optional metadata |
| `components` | array | List of components |

### Component Fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `name` | string | Name of the component |
| `type` | string | Type of the component |
| `parameters` | object | Component-specific parameters |
| `position` | array | Position of the component [x, y] |
| `rotation` | number | Rotation of the component in degrees |
| `connections` | array | List of connections |

### Connection Fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `port` | string | Name of the port on this component |
| `target` | string | Name of the target component |
| `target_port` | string | Name of the port on the target component |

## Component Types

The library supports the following component types:

### Transmission Lines

- `microstrip_line`: A simple microstrip transmission line
- `tapered_microstrip_line`: A tapered microstrip transmission line
- `curved_microstrip_line`: A curved microstrip transmission line
- `cpw_line`: A coplanar waveguide transmission line
- `cpw_bend`: A coplanar waveguide bend
- `cpw_taper`: A coplanar waveguide taper

### Passive Components

- `spiral_inductor`: A spiral inductor
- `symmetric_inductor`: A symmetric spiral inductor
- `solenoid_inductor`: A 3D solenoid inductor
- `mim_capacitor`: A metal-insulator-metal capacitor
- `interdigitated_capacitor`: An interdigitated capacitor
- `parallel_plate_capacitor`: A parallel plate capacitor

### Basic RF Structures

- `wilkinson_divider`: A Wilkinson power divider
- `branch_line_coupler`: A branch-line coupler (90° hybrid)
- `rat_race_coupler`: A rat-race coupler (180° hybrid)

## Examples

### Microstrip Line

```yaml
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

### Spiral Inductor

```yaml
- name: inductor1
  type: spiral_inductor
  parameters:
    n_turns: 3.5
    width: 5
    spacing: 5
    inner_radius: 20
    layer: [1, 0]
  position: [100, 100]
  rotation: 0
  connections:
    - port: in
      target: line1
      target_port: out
```

### Wilkinson Divider

```yaml
- name: divider1
  type: wilkinson_divider
  parameters:
    radius: 100
    width: 5
    isolation_resistor_width: 5
    isolation_resistor_length: 20
    layer: [1, 0]
    resistor_layer: [2, 0]
  position: [200, 100]
  rotation: 0
  connections:
    - port: in
      target: inductor1
      target_port: out
```
