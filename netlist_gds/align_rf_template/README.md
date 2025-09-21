# ALIGN RF/MW Layout Generation — Starter Scaffolding

This package gives you **runnable-style templates** to adapt your ADS/EM-style design into an **ALIGN-friendly** flow.
It includes:
- A **SPICE-like top netlist** (`netlist/top.spice`) that maps your components to *subcircuits* suitable for layout.
- A minimal **constraints file** (empty) and a **constraints example** with common RF constraints to customize.
- A **PDK JSON skeleton** (`pdk/sky130_like/*.json`) to show how to encode layers and basic rules.
- A **macro/Pcell approach note** (in `docs/ads_to_spice.md`) to convert EM/MOM blocks and MIMs into shaped geometry or macro cells.
- A **Python stub** (`scripts/make_em_macro.py`) that illustrates how you would generate a hard macro GDS for an EM structure (spiral/CPW/etc.).

> ⚠️ These are **templates**. You should adapt names, layer IDs, widths/spaces, and constraints to your actual PDK and ALIGN version.
> For production use, replace placeholders and verify against your PDK/DRC and ALIGN's current schema.
