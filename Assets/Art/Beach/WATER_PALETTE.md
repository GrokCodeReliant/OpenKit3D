# Beach water palette

Art supplies these colours for the Levels `OK_Water` graph (URP 17.4). The surf mesh `fx-surf-strip` carries the foam mask in vertex alpha. No water texture is required; one small noise is optional inside the graph, not in this set.

Sand `#D9C49A` and rock `#8A7B68` are the beach neighbours. Every swatch stays in that grey-teal family. Nothing here is purple or magenta.

| Swatch | Hex | Role |
| --- | --- | --- |
| Sea shallow | `#7ECFC4` | Shoreline and the top of the depth fade. Lighter than the tide pool so wet sand still reads as sand. |
| Sea deep | `#1B454C` | Open water past the shelf. Same teal, darker, slightly bluer. |
| Tide-pool water | `#3F7C78` | Matches `M_Beach_Water` (`_BaseColor` 63, 124, 120). The pools are already that colour. |
| Crypt still water | `#1E3B32` | Darker and greener than the sea, murky. For the flooded nave, not the beach. |
| Foam | `#F4F0E6` | Warm off-white, toward the sand. Vertex RGB on `fx-surf-strip` is white; this is the preview tint. |

`water_palette.png` (600×120) is the labelled swatch strip.

## Depth fade for OK_Water

Distances are metres of **depth below the water surface** (the graph's depth-fade), not horizontal distance from the mesh.

| Water | Shallow holds | Full deep | Notes |
| --- | ---: | ---: | --- |
| Beach sea | 0.40 | 5.0 | Shallow `#7ECFC4` from 0 to 0.40 m, lerp to `#1B454C` by 5.0 m. |
| Tide pool | — | — | Still. Use `#3F7C78` flat. If the graph wants a fade, 0.20 m is the whole pool. |
| Crypt still | 0.15 | 1.2 | `#1E3B32` by 1.2 m so the nave goes dark quickly. No swell. |
| Foam | — | — | Foam-fade **0.40 m** of shoreline depth. Multiply by the strip's vertex alpha. |

The foam strip is 6.0 m along X and 1.0 m across the shoreline. Its alpha is already 1 on the wave line and 0 inland and seaward, so the 0.40 m fade is the graph's extra shoreline term, not a second mask.
