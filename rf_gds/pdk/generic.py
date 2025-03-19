"""Generic PDK for RF GDS Library."""

from typing import Dict, ClassVar

from rf_gds.pdk.base import PDK, Layer, register_pdk


@register_pdk
class GenericPDK(PDK):
    """Generic PDK with basic layers for RF designs."""
    
    name: ClassVar[str] = "generic"
    
    def __init__(self, **data):
        """Initialize the Generic PDK."""
        super().__init__(**data)
        
        # Set description
        self.description = "Generic PDK with basic layers for RF designs"
        
        # Define layers
        self.layers = {
            "metal1": Layer(name="metal1", layer=1, datatype=0, description="Metal 1 layer"),
            "metal2": Layer(name="metal2", layer=2, datatype=0, description="Metal 2 layer"),
            "metal3": Layer(name="metal3", layer=3, datatype=0, description="Metal 3 layer"),
            "via12": Layer(name="via12", layer=4, datatype=0, description="Via between Metal 1 and Metal 2"),
            "via23": Layer(name="via23", layer=5, datatype=0, description="Via between Metal 2 and Metal 3"),
            "resistor": Layer(name="resistor", layer=6, datatype=0, description="Resistor layer"),
            "dielectric": Layer(name="dielectric", layer=7, datatype=0, description="Dielectric layer"),
            "substrate": Layer(name="substrate", layer=8, datatype=0, description="Substrate layer"),
            "text": Layer(name="text", layer=9, datatype=0, description="Text layer"),
            "drawing": Layer(name="drawing", layer=10, datatype=0, description="Drawing layer"),
        }
        
        # Define design rules
        self.design_rules = {
            # Minimum widths
            "min_width_metal1": 2.0,
            "min_width_metal2": 2.0,
            "min_width_metal3": 2.0,
            "min_width_via12": 2.0,
            "min_width_via23": 2.0,
            
            # Minimum spacings
            "min_spacing_metal1": 2.0,
            "min_spacing_metal2": 2.0,
            "min_spacing_metal3": 2.0,
            "min_spacing_via12": 2.0,
            "min_spacing_via23": 2.0,
            
            # RF-specific rules
            "min_transmission_line_width": 5.0,
            "min_transmission_line_spacing": 5.0,
            "min_inductor_width": 5.0,
            "min_inductor_spacing": 5.0,
            "min_capacitor_width": 5.0,
            "min_capacitor_spacing": 5.0,
        }
