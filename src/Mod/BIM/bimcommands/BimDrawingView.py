# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2024 Yorik van Havre <yorik@uncreated.net>              *
# *                                                                         *
# *   This file is part of FreeCAD.                                         *
# *                                                                         *
# *   FreeCAD is free software: you can redistribute it and/or modify it    *
# *   under the terms of the GNU Lesser General Public License as           *
# *   published by the Free Software Foundation, either version 2.1 of the  *
# *   License, or (at your option) any later version.                       *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful, but        *
# *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
# *   Lesser General Public License for more details.                       *
# *                                                                         *
# *   You should have received a copy of the GNU Lesser General Public      *
# *   License along with FreeCAD. If not, see                               *
# *   <https://www.gnu.org/licenses/>.                                      *
# *                                                                         *
# ***************************************************************************

"""The BIM DrawingView command"""

import FreeCAD
import FreeCADGui

QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP
translate = FreeCAD.Qt.translate

PARAMS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM")


class BIM_DrawingView:

    """The command definition for the Drawing View command"""

    def GetResources(self):

        return {'Pixmap'  : 'BIM_ArchView',
                'MenuText': QT_TRANSLATE_NOOP("BIM_DrawingView","2D Drawing"),
                'Accel': "V, D",
                'ToolTip': QT_TRANSLATE_NOOP("BIM_DrawingView","Creates a drawing container to contain elements of a 2D view")}

    def IsActive(self):

        v = hasattr(FreeCADGui.getMainWindow().getActiveWindow(), "getSceneGraph")
        return v

    def Activated(self):

        import Draft
        FreeCAD.ActiveDocument.openTransaction(translate("Arch","Create 2D View"))
        FreeCADGui.addModule("Arch")
        FreeCADGui.addModule("Draft")
        FreeCADGui.addModule("WorkingPlane")
        FreeCADGui.doCommand("obj = Arch.make2DDrawing()")
        FreeCADGui.doCommand("Draft.autogroup(obj)")
        s = FreeCADGui.Selection.getSelection()
        if len(s) == 1:
            s = s[0]
            if Draft.getType(s) == "SectionPlane":
                FreeCADGui.doCommand("vobj = Draft.make_shape2dview(FreeCAD.ActiveDocument."+s.Name+")")
                FreeCADGui.doCommand("vobj.Label = \""+translate("BIM","Viewed lines")+"\"")
                FreeCADGui.doCommand("vobj.InPlace = False")
                FreeCADGui.doCommand("obj.addObject(vobj)")
                bb = FreeCAD.BoundBox()
                for so in s.Objects:
                    if hasattr(so, "Shape"):
                        bb.add(so.Shape.BoundBox)
                if bb.isInside(s.Shape.CenterOfMass):
                    FreeCADGui.doCommand("cobj = Draft.make_shape2dview(FreeCAD.ActiveDocument."+s.Name+")")
                    FreeCADGui.doCommand("cobj.Label = \""+translate("BIM","Cut lines")+"\"")
                    FreeCADGui.doCommand("cobj.InPlace = False")
                    FreeCADGui.doCommand("cobj.ProjectionMode = \"Cutfaces\"")
                    FreeCADGui.doCommand("obj.addObject(cobj)")
        FreeCAD.ActiveDocument.commitTransaction()
        FreeCAD.ActiveDocument.recompute()


FreeCADGui.addCommand('BIM_DrawingView', BIM_DrawingView())
