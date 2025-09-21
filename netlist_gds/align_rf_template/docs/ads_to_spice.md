# ADS → SPICE/ALIGN mapping notes (RF/MW)

**ADS snippet (simplified):**
```
MomCmpt:em_data  P1 P2 name=em_data_name modelFile=... ModelType="MOMRF"
USC_PF25_SMIM:C924 N__65 N__77 l=120 um w=100 um
GRM15:C930  N__91 0 PartNumber=793  (off-chip)
S_Param:SP1 ... (simulation block)  --> drop for layout synthesis
```

**ALIGN-friendly SPICE-like:**
```
XEM1   n_in n_out  EM1  L=120u W=100u N=3      * EM macro/PCell with pins P1/P2
XCMIM  n65  n77    CMIM L=120u W=100u          * Parametric MIM capacitor
XPAD1  n91         PAD                          * Off-chip path exposed as PAD
```

- `EM1` can be **(A) hard GDS macro** you place and pin, or **(B) a PCell** you generate from parameters (e.g., spiral, CPW segment, slot).
- `CMIM` maps to a MIM/MOM capacitor **PCell** with geometry derived from `L/W`/target-C.
- `GRM15` is an **off-chip** component; expose its node via `PAD` and implement the capacitor in package/PCB.
- Remove `S_Param` control blocks from the layout netlist.

**Constraints to consider:**
- `SymmetricNets` for diff pairs
- `GuardRing` around noisy/sensitive blocks
- `PortLocation` to pin EM macro orientation
- `NetConst` for width/spacing/preferred direction on critical nets
- `BlockDistance` / keep-out around inductors/transformers
