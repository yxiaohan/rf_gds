"""YAML parsing functionality for RF GDS Library."""

from typing import Dict, Any, List, Tuple, Optional, Type, cast

import yaml
from pydantic import ValidationError

from rf_gds.components import Component
from rf_gds.components.base import get_component_class


def parse_yaml_to_design(yaml_data: Dict[str, Any]) -> "Design":
    """Parse YAML data into a Design object.
    
    Args:
        yaml_data: The YAML data as a dictionary
        
    Returns:
        A Design object
    """
    from rf_gds.core import Design
    
    # Extract top-level design information
    design_data = {
        "name": yaml_data.get("name", "unnamed_design"),
        "technology": yaml_data.get("technology", "generic"),
        "units": yaml_data.get("units", "um"),
        "metadata": yaml_data.get("metadata", {}),
    }
    
    # Create empty design
    design = Design(**design_data)
    
    # Parse components
    components_data = yaml_data.get("components", [])
    components = []
    
    for comp_data in components_data:
        try:
            component = parse_component(comp_data)
            components.append(component)
        except ValidationError as e:
            raise ValueError(f"Error parsing component {comp_data.get('name', 'unknown')}: {e}")
        except KeyError as e:
            raise ValueError(f"Missing required field in component {comp_data.get('name', 'unknown')}: {e}")
    
    design.components = components
    return design


def parse_component(component_data: Dict[str, Any]) -> Component:
    """Parse a component from YAML data.
    
    Args:
        component_data: The component data as a dictionary
        
    Returns:
        A Component object
    """
    # Get the component type
    component_type = component_data.get("type")
    if not component_type:
        raise KeyError("type")
    
    # Get the component class
    component_class = get_component_class(component_type)
    
    # Extract position and rotation
    position = component_data.get("position", (0, 0))
    rotation = component_data.get("rotation", 0)
    
    # Extract parameters
    parameters = component_data.get("parameters", {})
    
    # Extract connections
    connections_data = component_data.get("connections", [])
    
    # Create the component
    component = component_class(
        name=component_data.get("name", f"{component_type}_unnamed"),
        parameters=parameters,
        position=position,
        rotation=rotation,
    )
    
    # Add connections
    for conn_data in connections_data:
        component.add_connection(
            port=conn_data.get("port"),
            target=conn_data.get("target"),
            target_port=conn_data.get("target_port"),
        )
    
    return component


def validate_yaml_schema(yaml_data: Dict[str, Any]) -> List[str]:
    """Validate YAML data against the schema.
    
    Args:
        yaml_data: The YAML data as a dictionary
        
    Returns:
        A list of validation errors, empty if valid
    """
    errors = []
    
    # Validate top-level fields
    required_fields = ["name", "technology"]
    for field in required_fields:
        if field not in yaml_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate components
    if "components" not in yaml_data:
        errors.append("Missing required field: components")
    else:
        components = yaml_data["components"]
        if not isinstance(components, list):
            errors.append("Components must be a list")
        else:
            for i, component in enumerate(components):
                component_errors = validate_component(component)
                for error in component_errors:
                    errors.append(f"Component {i}: {error}")
    
    return errors


def validate_component(component_data: Dict[str, Any]) -> List[str]:
    """Validate a component against the schema.
    
    Args:
        component_data: The component data as a dictionary
        
    Returns:
        A list of validation errors, empty if valid
    """
    errors = []
    
    # Validate required fields
    required_fields = ["name", "type"]
    for field in required_fields:
        if field not in component_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate position
    if "position" in component_data:
        position = component_data["position"]
        if not isinstance(position, (list, tuple)) or len(position) != 2:
            errors.append("Position must be a tuple of (x, y)")
    
    # Validate connections
    if "connections" in component_data:
        connections = component_data["connections"]
        if not isinstance(connections, list):
            errors.append("Connections must be a list")
        else:
            for i, connection in enumerate(connections):
                if not isinstance(connection, dict):
                    errors.append(f"Connection {i} must be a dictionary")
                else:
                    required_conn_fields = ["port", "target", "target_port"]
                    for field in required_conn_fields:
                        if field not in connection:
                            errors.append(f"Connection {i}: Missing required field: {field}")
    
    return errors
