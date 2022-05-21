# Modal shortcuts
## Description
This module provides some utility for modal operators.

#### Features:
*   Modal keyboard shortcuts.

*   ModalShortcutsGroup

*   Editing using mouse input.

*   Editing using digits or letters input.

*   Correct (?) interpretation of property subtype and units (using rna_type, or manually).

*   AddonPreferences mix-in class with shortcuts editor and cache.

*   Automatic generation of new shortcuts without duplicates in name or mapping.

#### TODO Planned features:
    Correct UI property value display.

## How to use
(WIP)
Sublass `preferences.ModalShortcutsPreferences` in preferences panel, use `draw_shortcuts_search` to draw shortcuts list.


# Installation
Linux:
```
mkdir -p ~/.config/blender/3.1/scripts/modules
cp -r modal_shortcuts ~/.config/blender/3.1/scripts/modules
```
Or install through `pip` for blender's python.

Windows:
idk

Mac:
idk
