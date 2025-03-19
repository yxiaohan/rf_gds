"""Core functionality for RF GDS Library."""

import os
from typing import Dict, List, Optional, Union, Any

import yaml
import gdsfactory as gf
from pydantic import BaseModel, Field

from rf_gds.components import Component
from rf_gds.yaml_parser import parse_yaml_to_design
from rf_gds.pdk import PDK, get_pdk


class Design(BaseModel):
    """Represents a complete RF design."""

    name: str
    technology: str
    units: str = "um"
    components: List[Component] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    _pdk: Optional[PDK] = None
    
    @property
    def pdk(self) -> PDK:
        """Get the PDK for this design.
        
        Returns:
            The PDK instance
        """
        if self._pdk is None:
            self._pdk = get_pdk(self.technology)
        return self._pdk

    def to_gds(self, filename: Optional[str] = None) -> gf.Component:
        """Convert the design to a GDS component.
        
        Args:
            filename: Optional filename to write the GDS to
            
        Returns:
            The top-level gdsfactory Component
        """
        # Create a top-level component
        top = gf.Component(name=self.name)
        
        # Add all components to the top-level component
        for component in self.components:
            # Pass the PDK to the component if it has a set_pdk method
            if hasattr(component, 'set_pdk'):
                component.set_pdk(self.pdk)
                
            gds_component = component.to_gds()
            top.add_ref(gds_component, position=component.position, rotation=component.rotation)
            
        # Write to file if filename is provided
        if filename:
            top.write_gds(filename)
            
        return top


def load_design(yaml_file: Union[str, os.PathLike]) -> Design:
    """Load a design from a YAML file.
    
    Args:
        yaml_file: Path to the YAML file
        
    Returns:
        A Design object
    """
    print(f"Loading design from {yaml_file}...")
    with open(yaml_file, "r") as f:
        yaml_data = yaml.safe_load(f)
    
    design = parse_yaml_to_design(yaml_data)
    
    # Initialize the PDK
    _ = design.pdk
    
    return design
