# Runtime sanctuary art

`sanctuary-kit.glb` contains six meshes extracted from the project's authored Blender diorama: armor, head, seed, crystal, rock, and tree. The export applies modifiers and omits the presentation camera, lights, diorama board, materials, and static snake path. The game supplies shared materials and cell-based transforms. There are no embedded textures or animation clips.

`arcane-stone.jpg` is a 1024px JPEG derivative of the GPT-generated texture in `output/blender/cosmic-serpent/textures/arcane-stone.png`. Its original prompt is in that folder's README. Both the original texture and the geometry were created for this project; no third-party model service is required at runtime.

To re-export geometry with Blender on PATH:

```sh
blender -b output/blender/cosmic-serpent/cosmic-serpent.blend --python scripts/export-sanctuary.py
```

The saved `Runtime export kit` scene is the editable source for these normalized pieces. Keep the six mesh names stable. Source Blender axes are X/right, Y/forward, Z/up; the loader converts glTF Y-up back to the game's face-local +Z normal, then scales each mesh to its gameplay footprint.
