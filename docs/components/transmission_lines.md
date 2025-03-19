# Transmission Line Components

This page documents the transmission line components available in the RF GDS Library.

## Microstrip Line

A simple microstrip transmission line.

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `length` | float | Length of the line |
| `width` | float | Width of the line |
| `layer` | tuple | Layer (layer, datatype) |

### Ports

- `in`: Input port
- `out`: Output port

### Example

```yaml
- name: line1
  type: microstrip_line
  parameters:
    length: 100
    width: 5
    layer: [1, 0]
  position: [0, 0]
  rotation: 0
```

## Tapered Microstrip Line

A tapered microstrip transmission line.

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `length` | float | Length of the line |
| `width_in` | float | Width at the input |
| `width_out` | float | Width at the output |
| `layer` | tuple | Layer (layer, datatype) |

### Ports

- `in`: Input port
- `out`: Output port

### Example

```yaml
- name: taper1
  type: tapered_microstrip_line
  parameters:
    length: 50
    width_in: 5
    width_out: 10
    layer: [1, 0]
  position: [100, 0]
  rotation: 0
```

## Curved Microstrip Line

A curved microstrip transmission line.

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `radius` | float | Radius of the curve |
| `width` | float | Width of the line |
| `angle` | float | Angle of the curve in degrees (default: 90) |
| `layer` | tuple | Layer (layer, datatype) |

### Ports

- `in`: Input port
- `out`: Output port

### Example

```yaml
- name: curve1
  type: curved_microstrip_line
  parameters:
    radius: 50
    width: 5
    angle: 90
    layer: [1, 0]
  position: [150, 0]
  rotation: 0
```

## CPW Line

A coplanar waveguide transmission line.

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `length` | float | Length of the line |
| `width` | float | Width of the center conductor |
| `gap` | float | Gap width |
| `ground_width` | float | Width of the ground planes (default: 10.0) |
| `layer` | tuple | Layer (layer, datatype) |

### Ports

- `in`: Input port
- `out`: Output port

### Example

```yaml
- name: cpw1
  type: cpw_line
  parameters:
    length: 80
    width: 10
    gap: 5
    ground_width: 20
    layer: [1, 0]
  position: [200, 0]
  rotation: 0
```

## CPW Bend

A coplanar waveguide bend.

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `radius` | float | Radius of the bend |
| `width` | float | Width of the center conductor |
| `gap` | float | Gap width |
| `ground_width` | float | Width of the ground planes (default: 10.0) |
| `angle` | float | Angle of the bend in degrees (default: 90) |
| `layer` | tuple | Layer (layer, datatype) |

### Ports

- `in`: Input port
- `out`: Output port

### Example

```yaml
- name: bend1
  type: cpw_bend
  parameters:
    radius: 50
    width: 10
    gap: 5
    ground_width: 20
    angle: 90
    layer: [1, 0]
  position: [280, 0]
  rotation: 0
```

## CPW Taper

A coplanar waveguide taper.

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `length` | float | Length of the taper |
| `width_in` | float | Width of the center conductor at the input |
| `width_out` | float | Width of the center conductor at the output |
| `gap_in` | float | Gap width at the input |
| `gap_out` | float | Gap width at the output |
| `ground_width` | float | Width of the ground planes (default: 10.0) |
| `layer` | tuple | Layer (layer, datatype) |

### Ports

- `in`: Input port
- `out`: Output port

### Example

```yaml
- name: taper1
  type: cpw_taper
  parameters:
    length: 50
    width_in: 10
    width_out: 20
    gap_in: 5
    gap_out: 10
    ground_width: 20
    layer: [1, 0]
  position: [330, 0]
  rotation: 0
```
