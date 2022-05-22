[![Python application](https://github.com/0djentd/modal_shortcuts/actions/workflows/python-app.yml/badge.svg)](https://github.com/0djentd/modal_shortcuts/actions/workflows/python-app.yml)
# Modal shortcuts
## Description
Some utility for UI-oriented modal operators in Blender.

#### Features:
*   Modal keyboard shortcuts.

*   ModalShortcutsGroup

*   Editing using mouse input.

*   Editing using digits or letters input.

*   Correct (?) interpretation of property subtype and units (using rna_type, or manually).

*   AddonPreferences mix-in class with shortcuts editor and cache.

*   Automatic generation of new shortcuts without duplicates in name or mapping.

#### TODO Planned features:
* Correct UI property value display.

## How to use
(WIP)
Sublass `preferences.ModalShortcutsPreferences` in preferences panel, use `draw_shortcuts_search` to draw shortcuts list.


# Installation
Linux:
Symlink `~/.config/blender/3.1/scripts/modules/modal_shortcuts` to `src`

Windows:
idk

Mac:
idk
