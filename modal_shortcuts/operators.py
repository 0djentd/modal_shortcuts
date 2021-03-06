# ##### BEGIN GPL LICENSE BLOCK #####
#
# Copyright 2022, Sergey Shapochkin
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import logging

from libemtk.utils.modifier_prop_types import (MODIFIER_TYPES,
                                               get_all_editable_props)

from .shortcuts import (ModalShortcut, ModalShortcutsCache,
                        ModalShortcutsGroup, generate_new_shortcut)

try:
    import bpy
    from bpy.props import (BoolProperty, FloatProperty, IntProperty,
                           StringProperty)
    _WITH_BPY = True
except ModuleNotFoundError:
    _WITH_BPY = False

logger = logging.getLogger(__name__)


class EMTK_OT_start_editing_modal_shortcut(bpy.types.Operator):
    bl_idname = "emtk.start_editing_modal_shortcut"
    bl_label = "Start editing emtk modal operator kbs."
    bl_description = "Start editing modal shortcut"

    # Shortcut name and group
    shortcut_name: StringProperty(
        name="Shortcut to be edited",
        default=""
    )

    shortcut_group: StringProperty(
        name="Group to be edited",
        default=""
    )

    def execute(self, context):
        prefs = context.preferences.addons['emtk'].preferences

        # Deselect
        if prefs.emtk_editing_modal_shortcut_value\
                == self.shortcut_name\
                and prefs.emtk_editing_modal_shortcut_group\
                == self.shortcut_group:
            prefs.emtk_editing_modal_shortcut_value = ""
            prefs.emtk_editing_modal_shortcut_group = ""

        # Select
        else:
            prefs.emtk_editing_modal_shortcut_value\
                = self.shortcut_name
            prefs.emtk_editing_modal_shortcut_group\
                = self.shortcut_group

            group = prefs.modal_shortcuts.find_by_value(
                self.shortcut_group)
            shortcut = group.find_by_shortcut_id(self.shortcut_name)

            prefs.edited_shortcut_event_type = shortcut.event_type
            prefs.edited_shortcut_shift = shortcut.shift
            prefs.edited_shortcut_ctrl = shortcut.ctrl
            prefs.edited_shortcut_alt = shortcut.alt
        return {'FINISHED'}


class EMTK_OT_add_or_update_modal_shortcut(bpy.types.Operator):
    bl_label = "Add or change emtk modal operator kbs."
    bl_idname = "emtk.add_or_update_modal_shortcut"
    bl_description = "Add or update modal shortcut"

    # shortcut_name
    # shortcut_group
    # shortcut_event_type
    # shortcut_shift
    # shortcut_ctrl
    # shortcut_alt

    # Shortcut name and group
    shortcut_name: StringProperty(
        name="Shortcut to be edited",
        default=""
    )

    shortcut_group: StringProperty(
        name="Group to be edited",
        default=""
    )

    # Shortcut attrs
    shortcut_event_type: StringProperty(
        name="Shortcut mapping",
        maxlen=1,
        default="",
    )

    shortcut_shift: BoolProperty(
        name="Shortcut require shift to be pressed",
        default=False
    )

    shortcut_ctrl: BoolProperty(
        name="Shortcut require ctrl to be pressed",
        default=False
    )

    shortcut_alt: BoolProperty(
        name="Shortcut require alt to be pressed",
        default=False
    )

    def execute(self, context):
        prefs = context.preferences.addons['emtk'].preferences
        group = prefs.modal_shortcuts.find_by_value(
            self.shortcut_group)
        shortcut = ModalShortcut(self.shortcut_name,
                                 self.shortcut_event_type,
                                 self.shortcut_shift,
                                 self.shortcut_ctrl,
                                 self.shortcut_alt)

        group.update(shortcut)
        prefs.save_cache()
        prefs.emtk_editing_modal_shortcut_value = ""
        prefs.emtk_editing_modal_shortcut_group = ""
        return {'FINISHED'}


class EMTK_OT_reparse_default_modifiers_props_kbs(
        bpy.types.Operator):
    bl_idname = "object.reparse_default_modifiers_props_kbs"
    bl_label = "EMTK add all modifiers props to kbs"

    replace_kbs: BoolProperty(
        name='Replace existing.',
        default=True
    )

    @classmethod
    def poll(self, context):
        if context.area.type != 'VIEW_3D':
            return False
        elif context.mode != 'OBJECT':
            return False
        elif len(context.selected_objects) != 1:
            return False
        elif context.object.type != 'MESH':
            return False
        return True

    def execute(self, context):
        modifiers = []
        for x in MODIFIER_TYPES:
            mod = bpy.context.object.modifiers.new(x.lower(), x)
            if mod is not None:
                mod.show_viewport = False
                modifiers.append(mod)

        prefs = bpy.context.preferences.addons['emtk'].preferences
        replace = self.replace_kbs

        groups = []
        for x in modifiers:
            props = get_all_editable_props(x, no_ignore=True)

            if replace:
                shortcuts = []
            else:
                shortcuts = prefs.modal_shortcuts.find_by_value(
                    x.type).shortcuts

            shortcuts = []
            for y in props:
                shortcuts.append(generate_new_shortcut(y, shortcuts))

            groups.append(ModalShortcutsGroup(x.type, shortcuts))

        result = ModalShortcutsCache(groups)
        if replace:
            prefs.emtk_modal_operators_serialized_shortcuts\
                = result.serialize()
        else:
            raise ValueError
        return {'FINISHED'}
