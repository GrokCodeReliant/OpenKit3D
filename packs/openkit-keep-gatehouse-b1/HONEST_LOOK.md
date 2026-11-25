# Look and limits

- Stone blocks and slabs have chamfered edges like the kit's own modules. There is little wear or chipping, so the masonry looks cleaner and more regular than a real keep wall.
- The portcullis is closed and does not open. Its bars are square with simple pointed bottoms. Collision covers the opening with one thin solid panel, so characters cannot pass; whether rays or projectiles pass the gaps is up to your setup.
- The arrow-slit is a tall splayed loophole in an otherwise solid wall. The iron sighting lip is easy to miss from a distance. Collision leaves the slit itself open (too narrow for a character; rays may pass).
- The wide splay is the front (interior) face; the slim slot is at the back.
- The right-flank collision gap above the slit was closed.
- The collision seam under the cap, between the flank hull tops and the cap, was closed.
- The left-side collision gap above the slit was closed by making the upper box symmetric.
- The barred window is small and high. Its five bars look faceted up close. Collision covers the opening with a thin solid panel, same caveat as the portcullis.
- The floor channel is a shallow gutter with a dark silt surface, not a deep sewer and not water. From a high camera it can read as a dark stripe rather than a run of open channel. Collision fills the gutter, so nothing falls into it.
- The pressure plate is only 0.8 mm proud of the walking surface, so it is easy to miss in a typical camera view. The joint gap around the plate is the main cue. It does not depress or trigger.
- The cresset reads clearly as a standing iron fire basket with a few coals. Its collision is one convex envelope around the whole prop, so nothing can pass between the legs.
- An independent GLB parse (not the official Blender validator) still reports coplanar same-facing overlaps where separate parts meet, and unpaired edges on the portcullis after vertex welding. Official Blender re-import integrity and kit-snap gates passed. These leftover contacts were not all welded away.
- All observations above come from Blender previews only. Nothing has been checked under game-engine lighting, against a character, or with a camera-fade shader.
