"""
make_em_macro.py — stub to generate a hard macro GDS for an EM structure (e.g., spiral inductor)
Requires: gdstk or gdspy (install in your environment)
"""
# pip install gdstk
import math

try:
    import gdstk
except Exception as e:
    print("Install gdstk to run this script: pip install gdstk")
    raise

def spiral_inductor(cell_name="EM1", turns=3, w=5.0, s=5.0, outer=200.0, layer=6, datatype=0):
    lib = gdstk.Library()
    cell = lib.new_cell(cell_name)
    # Simple square spiral
    x = y = 0.0
    L = outer
    path = gdstk.FlexPath([(x, y)], w, layer=layer, datatype=datatype, bend_radius=0.0)
    dir_seq = [(1,0), (0,1), (-1,0), (0,-1)]
    step = 0
    for t in range(turns*4):
        dx, dy = dir_seq[t % 4]
        path.segment((path.points[-1][0] + dx*L, path.points[-1][1] + dy*L))
        step += 1
        if step % 2 == 0:
            L -= (w + s)
    cell.add(path)
    # Simple pins as squares at ends
    pin = gdstk.rectangle((-w, -w), (w, w), layer=layer, datatype=datatype)
    cell.add(pin)
    # add text labels "P1"/"P2" at approximate ends
    cell.add(gdstk.Label("P1", (0, 0), layer=layer))
    cell.add(gdstk.Label("P2", (path.points[-1][0], path.points[-1][1]), layer=layer))
    return lib

if __name__ == "__main__":
    lib = spiral_inductor(turns=3, w=5.0, s=5.0, outer=200.0, layer=6)
    lib.write_gds("EM1_macro.gds")
    print("Wrote EM1_macro.gds")
