"""RF GDS Library - Convert YAML descriptions of RF components to GDS files."""

# Import core functionality
from rf_gds.core import load_design, Design

# Import PDK functionality
from rf_gds.pdk import PDK, register_pdk, get_pdk, GenericPDK

# Import components to register them
from rf_gds.components.transmission_lines import (
    MicrostripLine, TaperedMicrostripLine, CurvedMicrostripLine,
    CPWLine, CPWBend, CPWTaper
)
from rf_gds.components.passive import (
    SpiralInductor, SymmetricInductor, SolenoidInductor,
    MIMCapacitor, InterdigitatedCapacitor, ParallelPlateCapacitor
)
from rf_gds.components.basic_structures import (
    WilkinsonDivider, BranchLineCoupler, RatRaceCoupler
)

__version__ = "0.1.0"
__all__ = [
    # Core
    "load_design", "Design",
    
    # PDK
    "PDK", "register_pdk", "get_pdk", "GenericPDK",
    
    # Transmission Lines
    "MicrostripLine", "TaperedMicrostripLine", "CurvedMicrostripLine",
    "CPWLine", "CPWBend", "CPWTaper",
    
    # Passive Components
    "SpiralInductor", "SymmetricInductor", "SolenoidInductor",
    "MIMCapacitor", "InterdigitatedCapacitor", "ParallelPlateCapacitor",
    
    # Basic Structures
    "WilkinsonDivider", "BranchLineCoupler", "RatRaceCoupler",
]
