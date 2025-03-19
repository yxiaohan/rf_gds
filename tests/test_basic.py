"""Basic tests for RF GDS Library."""

import os
import sys
import pytest

# Add the parent directory to the path to import rf_gds
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rf_gds
from rf_gds.components.transmission_lines.microstrip import MicrostripLine
from rf_gds.components.transmission_lines.cpw import CPWLine
from rf_gds.components.passive.inductor import SpiralInductor
from rf_gds.components.passive.capacitor import MIMCapacitor
from rf_gds.components.basic_structures.power_divider import WilkinsonDivider


def test_microstrip_line():
    """Test creating a microstrip line."""
    line = MicrostripLine(
        name="test_line",
        length=100,
        width=10,
        layer=(1, 0),
    )
    
    # Convert to GDS
    gds = line.to_gds()
    
    # Check that the GDS component was created
    assert gds is not None
    assert gds.name == "test_line"
    
    # Check that the ports were created
    assert "in" in gds.ports
    assert "out" in gds.ports
    
    # Check port positions
    assert gds.ports["in"].center[0] == 0
    assert gds.ports["out"].center[0] == 100


def test_cpw_line():
    """Test creating a CPW line."""
    line = CPWLine(
        name="test_cpw",
        length=100,
        width=10,
        gap=5,
        ground_width=20,
        layer=(1, 0),
    )
    
    # Convert to GDS
    gds = line.to_gds()
    
    # Check that the GDS component was created
    assert gds is not None
    assert gds.name == "test_cpw"
    
    # Check that the ports were created
    assert "in" in gds.ports
    assert "out" in gds.ports
    
    # Check port positions
    assert gds.ports["in"].center[0] == 0
    assert gds.ports["out"].center[0] == 100


def test_spiral_inductor():
    """Test creating a spiral inductor."""
    inductor = SpiralInductor(
        name="test_inductor",
        n_turns=3.5,
        width=5,
        spacing=5,
        inner_radius=20,
        layer=(1, 0),
    )
    
    # Convert to GDS
    gds = inductor.to_gds()
    
    # Check that the GDS component was created
    assert gds is not None
    assert gds.name == "test_inductor"
    
    # Check that the ports were created
    assert "in" in gds.ports
    assert "out" in gds.ports


def test_mim_capacitor():
    """Test creating a MIM capacitor."""
    cap = MIMCapacitor(
        name="test_cap",
        width=50,
        length=50,
        top_layer=(1, 0),
        bottom_layer=(2, 0),
        dielectric_layer=(3, 0),
    )
    
    # Convert to GDS
    gds = cap.to_gds()
    
    # Check that the GDS component was created
    assert gds is not None
    assert gds.name == "test_cap"
    
    # Check that the ports were created
    assert "p1" in gds.ports
    assert "p2" in gds.ports


def test_wilkinson_divider():
    """Test creating a Wilkinson divider."""
    divider = WilkinsonDivider(
        name="test_divider",
        radius=100,
        width=5,
        isolation_resistor_width=5,
        isolation_resistor_length=20,
        layer=(1, 0),
        resistor_layer=(2, 0),
    )
    
    # Convert to GDS
    gds = divider.to_gds()
    
    # Check that the GDS component was created
    assert gds is not None
    assert gds.name == "test_divider"
    
    # Check that the ports were created
    assert "in" in gds.ports
    assert "out1" in gds.ports
    assert "out2" in gds.ports


def test_yaml_parsing():
    """Test parsing a YAML file."""
    # Get the path to the example YAML file
    yaml_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "examples",
        "schema.yaml",
    )
    
    # Load the design
    design = rf_gds.load_design(yaml_path)
    
    # Check that the design was loaded
    assert design is not None
    assert design.name == "example_rf_design"
    assert len(design.components) > 0
    
    # Convert to GDS
    gds = design.to_gds()
    
    # Check that the GDS component was created
    assert gds is not None
    assert gds.name == "example_rf_design"
