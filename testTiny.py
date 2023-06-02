import sys
import toolutils

outputitem = None
inputindex = -1
inputitem = None
outputindex = -1

num_args = 1
h_extra_args = ''
pane = toolutils.activePane(kwargs)
if not isinstance(pane, hou.NetworkEditor):
    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if pane is None:
        hou.ui.displayMessage(
            'Cannot create node: cannot find any network pane')
        sys.exit(0)
else:  # We're creating this tool from the TAB menu inside a network editor
    pane_node = pane.pwd()
    if "outputnodename" in kwargs and "inputindex" in kwargs:
        outputitem = pane_node.item(kwargs["outputnodename"])
        inputindex = kwargs["inputindex"]
        h_extra_args += 'set arg4 = "' + kwargs["outputnodename"] + '"\n'
        h_extra_args += 'set arg5 = "' + str(inputindex) + '"\n'
        num_args = 6
    if "inputnodename" in kwargs and "outputindex" in kwargs:
        inputitem = pane_node.item(kwargs["inputnodename"])
        outputindex = kwargs["outputindex"]
        h_extra_args += 'set arg6 = "' + kwargs["inputnodename"] + '"\n'
        h_extra_args += 'set arg9 = "' + str(outputindex) + '"\n'
        num_args = 9
    if "autoplace" in kwargs:
        autoplace = kwargs["autoplace"]
    else:
        autoplace = False
    # If shift-clicked we want to auto append to the current
    # node
    if "shiftclick" in kwargs and kwargs["shiftclick"]:
        if inputitem is None:
            inputitem = pane.currentNode()
            outputindex = 0
    if "nodepositionx" in kwargs and "nodepositiony" in kwargs:
        try:
            pos = [float(kwargs["nodepositionx"]),
                   float(kwargs["nodepositiony"])]
        except:
            pos = None
    else:
        pos = None

    if not autoplace and not pane.listMode():
        if pos is not None:
            pass
        elif outputitem is None:
            pos = pane.selectPosition(inputitem, outputindex, None, -1)
        else:
            pos = pane.selectPosition(inputitem, outputindex,
                                      outputitem, inputindex)

    if pos is not None:
        if "node_bbox" in kwargs:
            size = kwargs["node_bbox"]
            pos[0] -= size[0] / 2
            pos[1] -= size[1] / 2
        else:
            pos[0] -= 0.573625
            pos[1] -= 0.220625
        h_extra_args += 'set arg2 = "' + str(pos[0]) + '"\n'
        h_extra_args += 'set arg3 = "' + str(pos[1]) + '"\n'
h_extra_args += 'set argc = "' + str(num_args) + '"\n'

pane_node = pane.pwd()
child_type = pane_node.childTypeCategory().nodeTypes()

if 'uvtransform::2.0' not in child_type:
    hou.ui.displayMessage(
        'Cannot create node: incompatible pane network type')
    sys.exit(0)

# First clear the node selection
pane_node.setSelected(False, True)

h_path = pane_node.path()
h_preamble = 'set arg1 = "' + h_path + '"\n'
h_cmd = r''' 
if ($argc < 2 || "$arg2" == "") then
   set arg2 = 0
endif
if ($argc < 3 || "$arg3" == "") then
   set arg3 = 0
endif
# Automatically generated script
# $arg1 - the path to add this node
# $arg2 - x position of the tile
# $arg3 - y position of the tile
# $arg4 - input node to wire to
# $arg5 - which input to wire to
# $arg6 - output node to wire to
# $arg7 - the type of this node
# $arg8 - the node is an indirect input
# $arg9 - index of output from $arg6

\set noalias = 1
set saved_path = `execute("oppwf")`
opcf $arg1

# Node $_obj_geo1_attribdelete1 (Sop/attribdelete)
set _obj_geo1_attribdelete1 = `run("opadd -e -n -v attribdelete attribdelete1")`
oplocate -x `$arg2 + 0` -y `$arg3 + 0` $_obj_geo1_attribdelete1
opparm $_obj_geo1_attribdelete1 ptdel ( 'heightA density objval height slope slopeA objectA object occlusion occlusionA attribute1 attribute1A attribute2 attribute2A map mapA noise noiseA curvature curvatureA' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_attribdelete1
opexprlanguage -s hscript $_obj_geo1_attribdelete1
opuserdata -n '___Version___' -v '' $_obj_geo1_attribdelete1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribdelete1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribdelete1
opset -p on $_obj_geo1_attribdelete1
opcf $arg1

# Node $_obj_geo1_init_default (Sop/attribwrangle)
set _obj_geo1_init_default = `run("opadd -e -n -v attribwrangle init_default")`
oplocate -x `$arg2 + -0.42759999999999998` -y `$arg3 + 75.681939999999997` $_obj_geo1_init_default
opparm $_obj_geo1_init_default  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_init_default snippet ( 'f@density=1;\n@Cd= 1;\n' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_init_default
opexprlanguage -s hscript $_obj_geo1_init_default
opuserdata -n '___Version___' -v '' $_obj_geo1_init_default
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_init_default
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_init_default
opset -p on $_obj_geo1_init_default
opcf $arg1

# Node $_obj_geo1_color2 (Sop/color)
set _obj_geo1_color2 = `run("opadd -e -n -v color color2")`
oplocate -x `$arg2 + 5.8162029999999998` -y `$arg3 + 56.584900000000005` $_obj_geo1_color2
opparm $_obj_geo1_color2  ramp ( 2 )
opparm $_obj_geo1_color2 ramp2pos ( 1 ) ramp2c ( 1 1 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_color2
opexprlanguage -s hscript $_obj_geo1_color2
opuserdata -n '___Version___' -v '' $_obj_geo1_color2
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_color2
opuserdata -n '___toolid___' -v 'sop_color' $_obj_geo1_color2
opset -p on $_obj_geo1_color2
opcf $arg1

# Node $_obj_geo1_attribute1_density (Sop/attribwrangle)
set _obj_geo1_attribute1_density = `run("opadd -e -n -v attribwrangle attribute1_density")`
oplocate -x `$arg2 + 73.265263000000004` -y `$arg3 + 9.1425999999999874` $_obj_geo1_attribute1_density
opparm $_obj_geo1_attribute1_density  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_attribute1_density snippet ( '@Cd = @attribute1A;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_attribute1_density
opexprlanguage -s hscript $_obj_geo1_attribute1_density
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute1_density
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_density
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_density
opset -p on $_obj_geo1_attribute1_density
opcf $arg1

# Node $_obj_geo1_slope_density (Sop/attribwrangle)
set _obj_geo1_slope_density = `run("opadd -e -n -v attribwrangle slope_density")`
oplocate -x `$arg2 + 44.637962999999999` -y `$arg3 + 9.0377999999999901` $_obj_geo1_slope_density
opparm $_obj_geo1_slope_density  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_slope_density snippet ( '@Cd = @slopeA;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_slope_density
opexprlanguage -s hscript $_obj_geo1_slope_density
opuserdata -n '___Version___' -v '' $_obj_geo1_slope_density
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_slope_density
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_slope_density
opset -p on $_obj_geo1_slope_density
opcf $arg1

# Node $_obj_geo1_switch_noise (Sop/switch)
set _obj_geo1_switch_noise = `run("opadd -e -n -v switch switch_noise")`
oplocate -x `$arg2 + 0.092899999999999983` -y `$arg3 + 28.569700000000005` $_obj_geo1_switch_noise
chblockbegin
chadd -t 0 0 $_obj_geo1_switch_noise input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enablecurvature")' $_obj_geo1_switch_noise/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch_noise
opexprlanguage -s hscript $_obj_geo1_switch_noise
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch_noise
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch_noise
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch_noise
opset -p on $_obj_geo1_switch_noise
opcf $arg1

# Node $_obj_geo1_pscale_viz (Sop/attribwrangle)
set _obj_geo1_pscale_viz = `run("opadd -e -n -v attribwrangle pscale_viz")`
oplocate -x `$arg2 + 1.976003` -y `$arg3 + 12.415599999999998` $_obj_geo1_pscale_viz
opparm $_obj_geo1_pscale_viz  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_pscale_viz snippet ( '@Cd = @pscale;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_pscale_viz
opexprlanguage -s hscript $_obj_geo1_pscale_viz
opuserdata -n '___Version___' -v '' $_obj_geo1_pscale_viz
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pscale_viz
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pscale_viz
opset -p on $_obj_geo1_pscale_viz
opcf $arg1

# Node $_obj_geo1_attribute2_density (Sop/attribwrangle)
set _obj_geo1_attribute2_density = `run("opadd -e -n -v attribwrangle attribute2_density")`
oplocate -x `$arg2 + 80.889363000000003` -y `$arg3 + 9.4226999999999919` $_obj_geo1_attribute2_density
opparm $_obj_geo1_attribute2_density  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_attribute2_density snippet ( '@Cd = @attribute2A;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_attribute2_density
opexprlanguage -s hscript $_obj_geo1_attribute2_density
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute2_density
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute2_density
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute2_density
opset -p on $_obj_geo1_attribute2_density
opcf $arg1

# Node $_obj_geo1_map_density1 (Sop/attribwrangle)
set _obj_geo1_map_density1 = `run("opadd -e -n -v attribwrangle map_density1")`
oplocate -x `$arg2 + 53.423863000000004` -y `$arg3 + 9.0377999999999901` $_obj_geo1_map_density1
opparm $_obj_geo1_map_density1  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_map_density1 snippet ( '@Cd = @mapA;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_map_density1
opexprlanguage -s hscript $_obj_geo1_map_density1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_density1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_density1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_density1
opset -p on $_obj_geo1_map_density1
opcf $arg1

# Node $_obj_geo1_null1 (Sop/null)
set _obj_geo1_null1 = `run("opadd -e -n -v null null1")`
oplocate -x `$arg2 + -0.77749984999999999` -y `$arg3 + 77.052940000000007` $_obj_geo1_null1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_null1
opexprlanguage -s hscript $_obj_geo1_null1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_null1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_null1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_null1
opset -p on $_obj_geo1_null1
opcf $arg1

# Node $_obj_geo1_switch1 (Sop/switch)
set _obj_geo1_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + -0.31159999999999999` -y `$arg3 + 10.621600000000001` $_obj_geo1_switch1
chblockbegin
chadd -t 0 0 $_obj_geo1_switch1 input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../vissurface")' $_obj_geo1_switch1/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch1
opexprlanguage -s hscript $_obj_geo1_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch1
opset -p on $_obj_geo1_switch1
opcf $arg1

# Node $_obj_geo1_isooffset1 (Sop/isooffset)
set _obj_geo1_isooffset1 = `run("opadd -e -n -v isooffset isooffset1")`
oplocate -x `$arg2 + 6.2762030000000006` -y `$arg3 + 57.703400000000002` $_obj_geo1_isooffset1
chblockbegin
chadd -t 0 0 $_obj_geo1_isooffset1 samplediv
chkey -t 0 -v 50 -m 0 -a 0 -A 0 -T a  -F 'ch("../samplediv")' $_obj_geo1_isooffset1/samplediv
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_isooffset1
opexprlanguage -s hscript $_obj_geo1_isooffset1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_isooffset1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_isooffset1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_isooffset1
opset -p on $_obj_geo1_isooffset1
opcf $arg1

# Node $_obj_geo1_occlusion_control (Sop/attribvop)
set _obj_geo1_occlusion_control = `run("opadd -e -n -v attribvop occlusion_control")`
oplocate -x `$arg2 + 3.9305030000000003` -y `$arg3 + 65.518940000000001` $_obj_geo1_occlusion_control
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "occlusionmin"         label   "min %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "occlusionmax"         label   "max %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switchmode"         label   "switch mode"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_occlusion_control
opmultiparm $_obj_geo1_occlusion_control 'heightY#pos' '../heightdensityramp#pos' 'heightY#value' '../heightdensityramp#value' 'heightY#interp' '../heightdensityramp#interp' 'heightscaleY#pos' '../heightscaleramp#pos' 'heightscaleY#value' '../heightscaleramp#value' 'heightscaleY#interp' '../heightscaleramp#interp' 'heightdensityramp#pos' '../heightdensityramp#pos' 'heightdensityramp#value' '../heightdensityramp#value' 'heightdensityramp#interp' '../heightdensityramp#interp' 'heightscaleramp#pos' '../heightscaleramp#pos' 'heightscaleramp#value' '../heightscaleramp#value' 'heightscaleramp#interp' '../heightscaleramp#interp' 'heightIDramp#pos' '../heightIDramp#pos' 'heightIDramp#value' '../heightIDramp#value' 'heightIDramp#interp' '../heightIDramp#interp' 'occlusiondensityramp#pos' '../occlusiondensityramp#pos' 'occlusiondensityramp#value' '../occlusiondensityramp#value' 'occlusiondensityramp#interp' '../occlusiondensityramp#interp' 'occlusionscaleramp#pos' '../occlusionscaleramp#pos' 'occlusionscaleramp#value' '../occlusionscaleramp#value' 'occlusionscaleramp#interp' '../occlusionscaleramp#interp' 'occlusionIDramp#pos' '../occlusionIDramp#pos' 'occlusionIDramp#value' '../occlusionIDramp#value' 'occlusionIDramp#interp' '../occlusionIDramp#interp'
opparm $_obj_geo1_occlusion_control  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 0 0 $_obj_geo1_occlusion_control occlusionmin
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../occlusionmin")/100' $_obj_geo1_occlusion_control/occlusionmin
chadd -t 0 0 $_obj_geo1_occlusion_control occlusionmax
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../occlusionmax")/100' $_obj_geo1_occlusion_control/occlusionmax
chadd -t 0 0 $_obj_geo1_occlusion_control switchmode
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../occlusionmode")' $_obj_geo1_occlusion_control/switchmode
chblockend
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_geo1_occlusion_control
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_occlusion_control
opexprlanguage -s hscript $_obj_geo1_occlusion_control
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control
opcf $_obj_geo1_occlusion_control

# Node $_obj_geo1_occlusion_control_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_geo1_occlusion_control_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + -3.4408699999999999` -y `$arg3 + -0.43231199999999997` $_obj_geo1_occlusion_control_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_geometryvopglobal1
opexprlanguage -s hscript $_obj_geo1_occlusion_control_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_geo1_occlusion_control_geometryvopglobal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_geometryvopglobal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_geometryvopglobal1

# Node $_obj_geo1_occlusion_control_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_occlusion_control_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 24.9983` -y `$arg3 + -0.31830900000000001` $_obj_geo1_occlusion_control_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_occlusion_control_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_occlusion_control_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_geometryvopoutput1

# Node $_obj_geo1_occlusion_control_bind1 (Vop/bind)
set _obj_geo1_occlusion_control_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 20.969899999999999` -y `$arg3 + -1.5983099999999999` $_obj_geo1_occlusion_control_bind1
opparm -V 18.5.408 $_obj_geo1_occlusion_control_bind1 parmname ( density ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_bind1
opexprlanguage -s hscript $_obj_geo1_occlusion_control_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_bind1

# Node $_obj_geo1_occlusion_control_bind2 (Vop/bind)
set _obj_geo1_occlusion_control_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 5.0366900000000001` -y `$arg3 + 3.7838599999999998` $_obj_geo1_occlusion_control_bind2
opparm -V 18.5.408 $_obj_geo1_occlusion_control_bind2 parmname ( density ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_bind2
opexprlanguage -s hscript $_obj_geo1_occlusion_control_bind2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_bind2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_bind2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_bind2

# Node $_obj_geo1_occlusion_control_multiply1 (Vop/multiply)
set _obj_geo1_occlusion_control_multiply1 = `run("opadd -e -n -v multiply multiply1")`
oplocate -x `$arg2 + 14.666399999999999` -y `$arg3 + 3.5192000000000001` $_obj_geo1_occlusion_control_multiply1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_multiply1
opexprlanguage -s hscript $_obj_geo1_occlusion_control_multiply1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_multiply1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_multiply1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_multiply1

# Node $_obj_geo1_occlusion_control_fit2 (Vop/fit)
set _obj_geo1_occlusion_control_fit2 = `run("opadd -e -n -v fit fit2")`
oplocate -x `$arg2 + 10.511699999999999` -y `$arg3 + 1.7604900000000001` $_obj_geo1_occlusion_control_fit2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_fit2
opexprlanguage -s hscript $_obj_geo1_occlusion_control_fit2
opuserdata -n '___Version___' -v '' $_obj_geo1_occlusion_control_fit2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_fit2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_fit2

# Node $_obj_geo1_occlusion_control_destmin (Vop/parameter)
set _obj_geo1_occlusion_control_destmin = `run("opadd -e -n -v parameter destmin")`
oplocate -x `$arg2 + 7.7417499999999997` -y `$arg3 + 2.59049` $_obj_geo1_occlusion_control_destmin
opparm -V 18.5.408 $_obj_geo1_occlusion_control_destmin parmname ( occlusionmin ) parmlabel ( 'min %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_destmin
opexprlanguage -s hscript $_obj_geo1_occlusion_control_destmin
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_destmin
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_destmin
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_destmin

# Node $_obj_geo1_occlusion_control_destmax (Vop/parameter)
set _obj_geo1_occlusion_control_destmax = `run("opadd -e -n -v parameter destmax")`
oplocate -x `$arg2 + 7.8667800000000003` -y `$arg3 + 0.89029499999999995` $_obj_geo1_occlusion_control_destmax
opparm -V 18.5.408 $_obj_geo1_occlusion_control_destmax parmname ( occlusionmax ) parmlabel ( 'max %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_destmax
opexprlanguage -s hscript $_obj_geo1_occlusion_control_destmax
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_destmax
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_destmax
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_destmax

# Node $_obj_geo1_occlusion_control_bind6 (Vop/bind)
set _obj_geo1_occlusion_control_bind6 = `run("opadd -e -n -v bind bind6")`
oplocate -x `$arg2 + 19.347200000000001` -y `$arg3 + 0.23798` $_obj_geo1_occlusion_control_bind6
opparm -V 18.5.408 $_obj_geo1_occlusion_control_bind6 parmname ( occlusionA ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_bind6
opexprlanguage -s hscript $_obj_geo1_occlusion_control_bind6
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_bind6
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_bind6
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_bind6

# Node $_obj_geo1_occlusion_control_bind8 (Vop/bind)
set _obj_geo1_occlusion_control_bind8 = `run("opadd -e -n -v bind bind8")`
oplocate -x `$arg2 + 2.3686699999999998` -y `$arg3 + 2.0604900000000002` $_obj_geo1_occlusion_control_bind8
opparm -V 18.5.408 $_obj_geo1_occlusion_control_bind8 parmname ( occlusion ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_bind8
opexprlanguage -s hscript $_obj_geo1_occlusion_control_bind8
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_bind8
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_bind8
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_bind8

# Node $_obj_geo1_occlusion_control_switch1 (Vop/switch)
set _obj_geo1_occlusion_control_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 16.892199999999999` -y `$arg3 + -0.70766099999999998` $_obj_geo1_occlusion_control_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_switch1
opexprlanguage -s hscript $_obj_geo1_occlusion_control_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_switch1

# Node $_obj_geo1_occlusion_control_add1 (Vop/add)
set _obj_geo1_occlusion_control_add1 = `run("opadd -e -n -v add add1")`
oplocate -x `$arg2 + 14.3893` -y `$arg3 + -1.2084999999999999` $_obj_geo1_occlusion_control_add1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_add1
opexprlanguage -s hscript $_obj_geo1_occlusion_control_add1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_add1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_add1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_add1

# Node $_obj_geo1_occlusion_control_subtract1 (Vop/subtract)
set _obj_geo1_occlusion_control_subtract1 = `run("opadd -e -n -v subtract subtract1")`
oplocate -x `$arg2 + 14.49` -y `$arg3 + -3.5625599999999999` $_obj_geo1_occlusion_control_subtract1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_subtract1
opexprlanguage -s hscript $_obj_geo1_occlusion_control_subtract1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_subtract1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_subtract1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_subtract1

# Node $_obj_geo1_occlusion_control_parm1 (Vop/parameter)
set _obj_geo1_occlusion_control_parm1 = `run("opadd -e -n -v parameter parm1")`
oplocate -x `$arg2 + 14.8665` -y `$arg3 + -6.8857900000000001` $_obj_geo1_occlusion_control_parm1
opparm -V 18.5.408 $_obj_geo1_occlusion_control_parm1 parmname ( switchmode ) parmlabel ( 'switch mode' ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_occlusion_control_parm1
opexprlanguage -s hscript $_obj_geo1_occlusion_control_parm1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_control_parm1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_control_parm1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_control_parm1
opcf ..
opcf $_obj_geo1_occlusion_control
oporder -e geometryvopglobal1 geometryvopoutput1 bind1 bind2 multiply1 fit2 destmin destmax bind6 bind8 switch1 add1 subtract1 parm1 
opcf ..
opset -p on $_obj_geo1_occlusion_control
opcf $arg1

# Node $_obj_geo1_color1 (Sop/color)
set _obj_geo1_color1 = `run("opadd -e -n -v color color1")`
oplocate -x `$arg2 + 3.6212030000000008` -y `$arg3 + 54.740200000000002` $_obj_geo1_color1
opparm $_obj_geo1_color1  ramp ( 2 )
opparm $_obj_geo1_color1 color ( 0 0 0 ) ramp2pos ( 1 ) ramp2c ( 1 1 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_color1
opexprlanguage -s hscript $_obj_geo1_color1
opuserdata -n '___Version___' -v '' $_obj_geo1_color1
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_color1
opuserdata -n '___toolid___' -v 'sop_color' $_obj_geo1_color1
opset -p on $_obj_geo1_color1
opcf $arg1

# Node $_obj_geo1_pointvop4 (Sop/attribvop)
set _obj_geo1_pointvop4 = `run("opadd -e -n -v attribvop pointvop4")`
oplocate -x `$arg2 + 3.7242029999999997` -y `$arg3 + 34.042000000000002` $_obj_geo1_pointvop4
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "test"         label   "test"         type    ramp_rgb         default { "2" }         range   { 1! 10 }         parmtag { "parmvop" "1" }         parmtag { "rampbasis_var" "test_the_basis_strings" }         parmtag { "rampbasisdefault" "linear" }         parmtag { "rampcolordefault" "1pos ( 0 ) 1c ( 0 0 0 ) 1interp ( linear ) 2pos ( 1 ) 2c ( 1 1 1 ) 2interp ( linear )" }         parmtag { "rampcolortype" "rgb" }         parmtag { "rampkeys_var" "test_the_key_positions" }         parmtag { "rampshowcontrolsdefault" "1" }         parmtag { "rampvalues_var" "test_the_key_values" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_pointvop4
opparm $_obj_geo1_pointvop4  bindings ( 0 ) groupbindings ( 0 ) test ( 2 )
opparm -V 18.5.408 $_obj_geo1_pointvop4 test2pos ( 1 ) test2c ( 1 1 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_pointvop4
opexprlanguage -s hscript $_obj_geo1_pointvop4
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_pointvop4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop4
opcf $_obj_geo1_pointvop4

# Node $_obj_geo1_pointvop4_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_geo1_pointvop4_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + 0.50537799999999999` -y `$arg3 + 0.124917` $_obj_geo1_pointvop4_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop4_geometryvopglobal1
opexprlanguage -s hscript $_obj_geo1_pointvop4_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_geo1_pointvop4_geometryvopglobal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop4_geometryvopglobal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop4_geometryvopglobal1

# Node $_obj_geo1_pointvop4_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_pointvop4_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 9.3786500000000004` -y `$arg3 + 3.44556` $_obj_geo1_pointvop4_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop4_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_pointvop4_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_pointvop4_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop4_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop4_geometryvopoutput1

# Node $_obj_geo1_pointvop4_bind1 (Vop/bind)
set _obj_geo1_pointvop4_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 0.29855799999999999` -y `$arg3 + 3.44556` $_obj_geo1_pointvop4_bind1
opparm -V 18.5.408 $_obj_geo1_pointvop4_bind1 parmname ( curvature ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop4_bind1
opexprlanguage -s hscript $_obj_geo1_pointvop4_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_pointvop4_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop4_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop4_bind1

# Node $_obj_geo1_pointvop4_ramp1 (Vop/rampparm)
set _obj_geo1_pointvop4_ramp1 = `run("opadd -e -n -v rampparm ramp1")`
oplocate -x `$arg2 + 3.2985600000000002` -y `$arg3 + 3.1805599999999998` $_obj_geo1_pointvop4_ramp1
opparm $_obj_geo1_pointvop4_ramp1  rampcolordefault ( 2 ) rampfloatdefault ( 2 )
opparm -V 18.5.408 $_obj_geo1_pointvop4_ramp1 parmname ( test ) rampcolordefault2pos ( 1 ) rampcolordefault2c ( 1 1 1 ) rampfloatdefault2pos ( 1 ) rampfloatdefault2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop4_ramp1
opexprlanguage -s hscript $_obj_geo1_pointvop4_ramp1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_pointvop4_ramp1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop4_ramp1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop4_ramp1
opcf ..
opcf $_obj_geo1_pointvop4
oporder -e geometryvopglobal1 geometryvopoutput1 bind1 ramp1 
opcf ..
opset -p on $_obj_geo1_pointvop4
opcf $arg1

# Node $_obj_geo1_object_density (Sop/attribwrangle)
set _obj_geo1_object_density = `run("opadd -e -n -v attribwrangle object_density")`
oplocate -x `$arg2 + 89.518962999999999` -y `$arg3 + 9.3628999999999962` $_obj_geo1_object_density
opparm $_obj_geo1_object_density  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_object_density snippet ( '@Cd = @objectA;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_object_density
opexprlanguage -s hscript $_obj_geo1_object_density
opuserdata -n '___Version___' -v '' $_obj_geo1_object_density
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_density
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_density
opset -p on $_obj_geo1_object_density
opcf $arg1

# Node $_obj_geo1_noise_density (Sop/attribwrangle)
set _obj_geo1_noise_density = `run("opadd -e -n -v attribwrangle noise_density")`
oplocate -x `$arg2 + 63.697963000000001` -y `$arg3 + 9.1425999999999874` $_obj_geo1_noise_density
opparm $_obj_geo1_noise_density  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_noise_density snippet ( '@Cd = @noiseA;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_noise_density
opexprlanguage -s hscript $_obj_geo1_noise_density
opuserdata -n '___Version___' -v '' $_obj_geo1_noise_density
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_density
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_density
opset -p on $_obj_geo1_noise_density
opcf $arg1

# Node $_obj_geo1_density_viz (Sop/null)
set _obj_geo1_density_viz = `run("opadd -e -n -v null density_viz")`
oplocate -x `$arg2 + -1.5085` -y `$arg3 + 12.4116` $_obj_geo1_density_viz
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_density_viz
opexprlanguage -s hscript $_obj_geo1_density_viz
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_density_viz
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_density_viz
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_density_viz
opset -p on $_obj_geo1_density_viz
opcf $arg1

# Node $_obj_geo1_object_merge1 (Sop/object_merge)
set _obj_geo1_object_merge1 = `run("opadd -e -n -v object_merge object_merge1")`
oplocate -x `$arg2 + -2.939727` -y `$arg3 + 78.877340000000004` $_obj_geo1_object_merge1
opparm $_obj_geo1_object_merge1  numobj ( 1 )
chblockbegin
chadd -t 0 0 $_obj_geo1_object_merge1 objpath1
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chsop("../objpath7")' $_obj_geo1_object_merge1/objpath1
chblockend
opparm -V 18.5.408 $_obj_geo1_object_merge1 xformtype ( local ) objpath1 ( objpath1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_object_merge1
opexprlanguage -s hscript $_obj_geo1_object_merge1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_merge1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_merge1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_merge1
opset -p on $_obj_geo1_object_merge1
opcf $arg1

# Node $_obj_geo1_color3 (Sop/color)
set _obj_geo1_color3 = `run("opadd -e -n -v color color3")`
oplocate -x `$arg2 + 8.6781030000000001` -y `$arg3 + 56.362300000000005` $_obj_geo1_color3
opparm $_obj_geo1_color3  ramp ( 2 )
opparm $_obj_geo1_color3 ramp2pos ( 1 ) ramp2c ( 1 1 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_color3
opexprlanguage -s hscript $_obj_geo1_color3
opuserdata -n '___Version___' -v '' $_obj_geo1_color3
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_color3
opuserdata -n '___toolid___' -v 'sop_color' $_obj_geo1_color3
opset -p on $_obj_geo1_color3
opcf $arg1

# Node $_obj_geo1_attribute1_control2 (Sop/attribvop)
set _obj_geo1_attribute1_control2 = `run("opadd -e -n -v attribvop attribute1_control2")`
oplocate -x `$arg2 + 1.8474029999999999` -y `$arg3 + 59.746499999999997` $_obj_geo1_attribute1_control2
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "attribute2remap"         label   "attribute remap"         type    ramp_flt         default { "2" }         range   { 1! 10 }         parmtag { "parmvop" "1" }         parmtag { "rampbasis_var" "attribute2remap_the_basis_strings" }         parmtag { "rampbasisdefault" "linear" }         parmtag { "rampfloatdefault" "1pos ( 0 ) 1value ( 0 ) 1interp ( linear ) 2pos ( 1 ) 2value ( 1 ) 2interp ( linear )" }         parmtag { "rampkeys_var" "attribute2remap_the_key_positions" }         parmtag { "rampshowcontrolsdefault" "1" }         parmtag { "rampvalues_var" "attribute2remap_the_key_values" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "attribute2min"         label   "min %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "attribute2max"         label   "max %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "attribtue"         label   "attribute"         type    string         default { "" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "switchmode"         label   "switch mode"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_attribute1_control2
opmultiparm $_obj_geo1_attribute1_control2 'attributepscale#pos' '../attributepscale#pos' 'attributepscale#value' '../attributepscale#value' 'attributepscale#interp' '../attributepscale#interp' 'densityattribtue#pos' '../densityattribtue#pos' 'densityattribtue#value' '../densityattribtue#value' 'densityattribtue#interp' '../densityattribtue#interp' 'attribute1IDramp#pos' '../attribute1IDramp#pos' 'attribute1IDramp#value' '../attribute1IDramp#value' 'attribute1IDramp#interp' '../attribute1IDramp#interp' 'attribute2remap#pos' '../attribute2remap#pos' 'attribute2remap#value' '../attribute2remap#value' 'attribute2remap#interp' '../attribute2remap#interp'
opparm $_obj_geo1_attribute1_control2  bindings ( 0 ) groupbindings ( 0 ) attribute2remap ( 2 )
chblockbegin
chadd -t 0 0 $_obj_geo1_attribute1_control2 attribute2remap
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute2remap")' $_obj_geo1_attribute1_control2/attribute2remap
chadd -t 0 0 $_obj_geo1_attribute1_control2 attribute2remap1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute2remap1pos")' $_obj_geo1_attribute1_control2/attribute2remap1pos
chadd -t 0 0 $_obj_geo1_attribute1_control2 attribute2remap1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute2remap1value")' $_obj_geo1_attribute1_control2/attribute2remap1value
chadd -t 0 0 $_obj_geo1_attribute1_control2 attribute2remap1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute2remap1interp")' $_obj_geo1_attribute1_control2/attribute2remap1interp
chadd -t 0 0 $_obj_geo1_attribute1_control2 attribute2min
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute2min")/100' $_obj_geo1_attribute1_control2/attribute2min
chadd -t 0 0 $_obj_geo1_attribute1_control2 attribute2max
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute2max")/100' $_obj_geo1_attribute1_control2/attribute2max
chadd -t 0 0 $_obj_geo1_attribute1_control2 switchmode
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute2mode")' $_obj_geo1_attribute1_control2/switchmode
chadd -t 0 0 $_obj_geo1_attribute1_control2 attribute2remap2pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute2remap2pos")' $_obj_geo1_attribute1_control2/attribute2remap2pos
chadd -t 0 0 $_obj_geo1_attribute1_control2 attribute2remap2value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute2remap2value")' $_obj_geo1_attribute1_control2/attribute2remap2value
chadd -t 0 0 $_obj_geo1_attribute1_control2 attribute2remap2interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute2remap2interp")' $_obj_geo1_attribute1_control2/attribute2remap2interp
chblockend
opparm -V 18.5.408 $_obj_geo1_attribute1_control2 attribute2remap ( attribute2remap ) attribute2remap1pos ( attribute2remap1pos ) attribute2remap1value ( attribute2remap1value ) attribute2remap1interp ( attribute2remap1interp ) attribute2min ( attribute2min ) attribute2max ( attribute2max ) attribtue ( '`chs("../attribute2name")`' ) switchmode ( switchmode ) attribute2remap2pos ( attribute2remap2pos ) attribute2remap2value ( attribute2remap2value ) attribute2remap2interp ( attribute2remap2interp )
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_geo1_attribute1_control2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_attribute1_control2
opexprlanguage -s hscript $_obj_geo1_attribute1_control2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2
opcf $_obj_geo1_attribute1_control2

# Node $_obj_geo1_attribute1_control2_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_attribute1_control2_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 34.341799999999999` -y `$arg3 + 1.4397599999999999` $_obj_geo1_attribute1_control2_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute1_control2_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_geometryvopoutput1

# Node $_obj_geo1_attribute1_control2_bind2 (Vop/bind)
set _obj_geo1_attribute1_control2_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 30.5716` -y `$arg3 + 0.66383899999999996` $_obj_geo1_attribute1_control2_bind2
opparm -V 18.5.408 $_obj_geo1_attribute1_control2_bind2 parmname ( density ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_bind2
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_bind2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_bind2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_bind2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_bind2

# Node $_obj_geo1_attribute1_control2_bind7 (Vop/bind)
set _obj_geo1_attribute1_control2_bind7 = `run("opadd -e -n -v bind bind7")`
oplocate -x `$arg2 + 4.4740399999999996` -y `$arg3 + -0.45509500000000003` $_obj_geo1_attribute1_control2_bind7
opparm -V 18.5.408 $_obj_geo1_attribute1_control2_bind7 parmname ( '`chs("../attribtue")`' ) vectordef ( 1 1 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_bind7
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_bind7
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_bind7
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_bind7
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_bind7

# Node $_obj_geo1_attribute1_control2_vectofloat2 (Vop/vectofloat)
set _obj_geo1_attribute1_control2_vectofloat2 = `run("opadd -e -n -v vectofloat vectofloat2")`
oplocate -x `$arg2 + 8.0678699999999992` -y `$arg3 + -0.080095` $_obj_geo1_attribute1_control2_vectofloat2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_vectofloat2
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_vectofloat2
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute1_control2_vectofloat2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_vectofloat2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_vectofloat2

# Node $_obj_geo1_attribute1_control2_ramp2 (Vop/rampparm)
set _obj_geo1_attribute1_control2_ramp2 = `run("opadd -e -n -v rampparm ramp2")`
oplocate -x `$arg2 + 14.993` -y `$arg3 + 2.7192400000000001` $_obj_geo1_attribute1_control2_ramp2
opparm $_obj_geo1_attribute1_control2_ramp2  rampcolordefault ( 2 ) rampfloatdefault ( 2 )
opparm -V 18.5.408 $_obj_geo1_attribute1_control2_ramp2 parmname ( attribute2remap ) parmlabel ( 'attribute remap' ) ramptype ( flt ) rampcolordefault2pos ( 1 ) rampcolordefault2c ( 1 1 1 ) rampfloatdefault2pos ( 1 ) rampfloatdefault2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_ramp2
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_ramp2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_ramp2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_ramp2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_ramp2

# Node $_obj_geo1_attribute1_control2_multiply3 (Vop/multiply)
set _obj_geo1_attribute1_control2_multiply3 = `run("opadd -e -n -v multiply multiply3")`
oplocate -x `$arg2 + 22.713999999999999` -y `$arg3 + 5.1751699999999996` $_obj_geo1_attribute1_control2_multiply3
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_multiply3
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_multiply3
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_multiply3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_multiply3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_multiply3

# Node $_obj_geo1_attribute1_control2_fit5 (Vop/fit)
set _obj_geo1_attribute1_control2_fit5 = `run("opadd -e -n -v fit fit5")`
oplocate -x `$arg2 + 17.805599999999998` -y `$arg3 + 2.18384` $_obj_geo1_attribute1_control2_fit5
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_fit5
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_fit5
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute1_control2_fit5
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_fit5
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_fit5

# Node $_obj_geo1_attribute1_control2_destmin2 (Vop/parameter)
set _obj_geo1_attribute1_control2_destmin2 = `run("opadd -e -n -v parameter destmin2")`
oplocate -x `$arg2 + 15.527799999999999` -y `$arg3 + -0.166161` $_obj_geo1_attribute1_control2_destmin2
opparm -V 18.5.408 $_obj_geo1_attribute1_control2_destmin2 parmname ( attribute2min ) parmlabel ( 'min %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_destmin2
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_destmin2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_destmin2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_destmin2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_destmin2

# Node $_obj_geo1_attribute1_control2_destmax4 (Vop/parameter)
set _obj_geo1_attribute1_control2_destmax4 = `run("opadd -e -n -v parameter destmax4")`
oplocate -x `$arg2 + 15.3329` -y `$arg3 + -1.93791` $_obj_geo1_attribute1_control2_destmax4
opparm -V 18.5.408 $_obj_geo1_attribute1_control2_destmax4 parmname ( attribute2max ) parmlabel ( 'max %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_destmax4
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_destmax4
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_destmax4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_destmax4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_destmax4

# Node $_obj_geo1_attribute1_control2_bind1 (Vop/bind)
set _obj_geo1_attribute1_control2_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 10.171200000000001` -y `$arg3 + 5.7273500000000004` $_obj_geo1_attribute1_control2_bind1
opparm -V 18.5.408 $_obj_geo1_attribute1_control2_bind1 parmname ( density ) exportcontext ( cvex )
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_bind1
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_bind1

# Node $_obj_geo1_attribute1_control2_bind4 (Vop/bind)
set _obj_geo1_attribute1_control2_bind4 = `run("opadd -e -n -v bind bind4")`
oplocate -x `$arg2 + 23.5806` -y `$arg3 + 1.73384` $_obj_geo1_attribute1_control2_bind4
opparm -V 18.5.408 $_obj_geo1_attribute1_control2_bind4 parmname ( attribute1A ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_bind4
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_bind4
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_bind4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_bind4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_bind4

# Node $_obj_geo1_attribute1_control2_add1 (Vop/add)
set _obj_geo1_attribute1_control2_add1 = `run("opadd -e -n -v add add1")`
oplocate -x `$arg2 + 22.226700000000001` -y `$arg3 + -0.53160600000000002` $_obj_geo1_attribute1_control2_add1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_add1
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_add1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_add1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_add1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_add1

# Node $_obj_geo1_attribute1_control2_switch1 (Vop/switch)
set _obj_geo1_attribute1_control2_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 27.4741` -y `$arg3 + 0.058839000000000002` $_obj_geo1_attribute1_control2_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_switch1
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_switch1

# Node $_obj_geo1_attribute1_control2_parm1 (Vop/parameter)
set _obj_geo1_attribute1_control2_parm1 = `run("opadd -e -n -v parameter parm1")`
oplocate -x `$arg2 + 24.829999999999998` -y `$arg3 + -4.1195000000000004` $_obj_geo1_attribute1_control2_parm1
opparm -V 18.5.408 $_obj_geo1_attribute1_control2_parm1 parmname ( switchmode ) parmlabel ( 'switch mode' ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_parm1
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_parm1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_parm1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_parm1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_parm1

# Node $_obj_geo1_attribute1_control2_subtract1 (Vop/subtract)
set _obj_geo1_attribute1_control2_subtract1 = `run("opadd -e -n -v subtract subtract1")`
oplocate -x `$arg2 + 22.011299999999999` -y `$arg3 + -2.1659899999999999` $_obj_geo1_attribute1_control2_subtract1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control2_subtract1
opexprlanguage -s hscript $_obj_geo1_attribute1_control2_subtract1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control2_subtract1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control2_subtract1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control2_subtract1
opcf ..
opcf $_obj_geo1_attribute1_control2
oporder -e geometryvopoutput1 bind2 bind7 vectofloat2 ramp2 multiply3 fit5 destmin2 destmax4 bind1 bind4 add1 switch1 parm1 subtract1 
opcf ..
opset -p on $_obj_geo1_attribute1_control2
opcf $arg1

# Node $_obj_geo1_map_control (Sop/attribvop)
set _obj_geo1_map_control = `run("opadd -e -n -v attribvop map_control")`
oplocate -x `$arg2 + 7.1002029999999987` -y `$arg3 + 17.615700000000004` $_obj_geo1_map_control
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "visualize_noise"         label   "visualize noise"         type    toggle         default { "0" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "mapmin"         label   "min %"         type    float         default { "0" }         range   { 0 100 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "mapmax"         label   "max  %"         type    float         default { "100" }         range   { 0 100 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "surfaceOn"         label   "surface on"         type    toggle         default { "0" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "vizRGB"         label   "vizRGB"         type    toggle         default { "0" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "mapremap"         label   "map remap"         type    ramp_flt         default { "2" }         range   { 1! 10 }         parmtag { "parmvop" "1" }         parmtag { "rampbasis_var" "mapremap_the_basis_strings" }         parmtag { "rampbasisdefault" "linear" }         parmtag { "rampfloatdefault" "1pos ( 0 ) 1value ( 0 ) 1interp ( linear ) 2pos ( 1 ) 2value ( 1 ) 2interp ( linear )" }         parmtag { "rampkeys_var" "mapremap_the_key_positions" }         parmtag { "rampshowcontrolsdefault" "1" }         parmtag { "rampvalues_var" "mapremap_the_key_values" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switchmode"         label   "switch mode"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_map_control
opmultiparm $_obj_geo1_map_control 'noisedensity#pos' '../noisedensity#pos' 'noisedensity#value' '../noisedensity#value' 'noisedensity#interp' '../noisedensity#interp' 'noisescale#pos' '../noisescale#pos' 'noisescale#value' '../noisescale#value' 'noisescale#interp' '../noisescale#interp' 'heightY#pos' '../heightdensityramp#pos' 'heightY#value' '../heightdensityramp#value' 'heightY#interp' '../heightdensityramp#interp' 'heightscaleY#pos' '../heightscaleramp#pos' 'heightscaleY#value' '../heightscaleramp#value' 'heightscaleY#interp' '../heightscaleramp#interp' 'densitynoise#pos' '../densitynoiseramp#pos' 'densitynoise#value' '../densitynoiseramp#value' 'densitynoise#interp' '../densitynoiseramp#interp' 'scalenoise#pos' '../scalenoiseramp#pos' 'scalenoise#value' '../scalenoiseramp#value' 'scalenoise#interp' '../scalenoiseramp#interp' 'mapdensityramp#pos' '../mapdensityramp#pos' 'mapdensityramp#value' '../mapdensityramp#value' 'mapdensityramp#interp' '../mapdensityramp#interp' 'mapscaleramp#pos' '../mapscaleramp#pos' 'mapscaleramp#value' '../mapscaleramp#value' 'mapscaleramp#interp' '../mapscaleramp#interp' 'mapIDramp#pos' '../mapIDramp#pos' 'mapIDramp#value' '../mapIDramp#value' 'mapIDramp#interp' '../mapIDramp#interp' 'mapremap#pos' '../mapremap#pos' 'mapremap#value' '../mapremap#value' 'mapremap#interp' '../mapremap#interp'
opparm $_obj_geo1_map_control  bindings ( 0 ) groupbindings ( 0 ) mapremap ( 2 )
chblockbegin
chadd -t 0 0 $_obj_geo1_map_control mapmin
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapmin")/100' $_obj_geo1_map_control/mapmin
chadd -t 0 0 $_obj_geo1_map_control mapmax
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapmax")/100' $_obj_geo1_map_control/mapmax
chadd -t 0 0 $_obj_geo1_map_control vizRGB
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../switchRGB")' $_obj_geo1_map_control/vizRGB
chadd -t 0 0 $_obj_geo1_map_control mapremap
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapremap")' $_obj_geo1_map_control/mapremap
chadd -t 0 0 $_obj_geo1_map_control mapremap1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapremap1pos")' $_obj_geo1_map_control/mapremap1pos
chadd -t 0 0 $_obj_geo1_map_control mapremap1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapremap1value")' $_obj_geo1_map_control/mapremap1value
chadd -t 0 0 $_obj_geo1_map_control mapremap1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapremap1interp")' $_obj_geo1_map_control/mapremap1interp
chadd -t 0 0 $_obj_geo1_map_control switchmode
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapmode")' $_obj_geo1_map_control/switchmode
chadd -t 0 0 $_obj_geo1_map_control mapremap2pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapremap2pos")' $_obj_geo1_map_control/mapremap2pos
chadd -t 0 0 $_obj_geo1_map_control mapremap2value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapremap2value")' $_obj_geo1_map_control/mapremap2value
chadd -t 0 0 $_obj_geo1_map_control mapremap2interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapremap2interp")' $_obj_geo1_map_control/mapremap2interp
chblockend
opparm -V 18.5.408 $_obj_geo1_map_control mapmin ( mapmin ) mapmax ( mapmax ) vizRGB ( vizRGB ) mapremap ( mapremap ) mapremap1pos ( mapremap1pos ) mapremap1value ( mapremap1value ) mapremap1interp ( mapremap1interp ) switchmode ( switchmode ) mapremap2pos ( mapremap2pos ) mapremap2value ( mapremap2value ) mapremap2interp ( mapremap2interp )
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_geo1_map_control
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_map_control
opexprlanguage -s hscript $_obj_geo1_map_control
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control
opcf $_obj_geo1_map_control

# Node $_obj_geo1_map_control_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_map_control_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 35.919199999999996` -y `$arg3 + -1.20025` $_obj_geo1_map_control_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_map_control_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_control_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_geometryvopoutput1

# Node $_obj_geo1_map_control_bind1 (Vop/bind)
set _obj_geo1_map_control_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 25.886399999999998` -y `$arg3 + 0.039515500000000002` $_obj_geo1_map_control_bind1
opparm -V 18.5.408 $_obj_geo1_map_control_bind1 parmname ( density ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_bind1
opexprlanguage -s hscript $_obj_geo1_map_control_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_bind1

# Node $_obj_geo1_map_control_bind2 (Vop/bind)
set _obj_geo1_map_control_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 7.9110800000000001` -y `$arg3 + 7.7066499999999998` $_obj_geo1_map_control_bind2
opparm -V 18.5.408 $_obj_geo1_map_control_bind2 parmname ( density ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_bind2
opexprlanguage -s hscript $_obj_geo1_map_control_bind2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_bind2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_bind2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_bind2

# Node $_obj_geo1_map_control_multiply1 (Vop/multiply)
set _obj_geo1_map_control_multiply1 = `run("opadd -e -n -v multiply multiply1")`
oplocate -x `$arg2 + 14.8596` -y `$arg3 + 7.3574200000000003` $_obj_geo1_map_control_multiply1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_multiply1
opexprlanguage -s hscript $_obj_geo1_map_control_multiply1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_multiply1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_multiply1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_multiply1

# Node $_obj_geo1_map_control_fit2 (Vop/fit)
set _obj_geo1_map_control_fit2 = `run("opadd -e -n -v fit fit2")`
oplocate -x `$arg2 + 13.167999999999999` -y `$arg3 + 3.6692` $_obj_geo1_map_control_fit2
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_fit2
opexprlanguage -s hscript $_obj_geo1_map_control_fit2
opuserdata -n '___Version___' -v '' $_obj_geo1_map_control_fit2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_fit2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_fit2

# Node $_obj_geo1_map_control_bind7 (Vop/bind)
set _obj_geo1_map_control_bind7 = `run("opadd -e -n -v bind bind7")`
oplocate -x `$arg2 + 5.35893` -y `$arg3 + -0.51276600000000006` $_obj_geo1_map_control_bind7
opparm -V 18.5.408 $_obj_geo1_map_control_bind7 parmname ( map ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_bind7
opexprlanguage -s hscript $_obj_geo1_map_control_bind7
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_bind7
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_bind7
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_bind7

# Node $_obj_geo1_map_control_parm1 (Vop/parameter)
set _obj_geo1_map_control_parm1 = `run("opadd -e -n -v parameter parm1")`
oplocate -x `$arg2 + 9.1528600000000004` -y `$arg3 + 3.8321700000000001` $_obj_geo1_map_control_parm1
opparm -V 18.5.408 $_obj_geo1_map_control_parm1 parmname ( mapmin ) parmlabel ( 'min %' ) rangeflt ( 0 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_parm1
opexprlanguage -s hscript $_obj_geo1_map_control_parm1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_parm1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_parm1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_parm1

# Node $_obj_geo1_map_control_parm2 (Vop/parameter)
set _obj_geo1_map_control_parm2 = `run("opadd -e -n -v parameter parm2")`
oplocate -x `$arg2 + 9.2688299999999995` -y `$arg3 + 2.0771000000000002` $_obj_geo1_map_control_parm2
opparm -V 18.5.408 $_obj_geo1_map_control_parm2 parmname ( mapmax ) parmlabel ( 'max  %' ) floatdef ( 100 ) rangeflt ( 0 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_parm2
opexprlanguage -s hscript $_obj_geo1_map_control_parm2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_parm2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_parm2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_parm2

# Node $_obj_geo1_map_control_bind8 (Vop/bind)
set _obj_geo1_map_control_bind8 = `run("opadd -e -n -v bind bind8")`
oplocate -x `$arg2 + 21.285` -y `$arg3 + 3.6692` $_obj_geo1_map_control_bind8
opparm -V 18.5.408 $_obj_geo1_map_control_bind8 parmname ( mapA ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_bind8
opexprlanguage -s hscript $_obj_geo1_map_control_bind8
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_bind8
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_bind8
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_bind8

# Node $_obj_geo1_map_control_switch2 (Vop/switch)
set _obj_geo1_map_control_switch2 = `run("opadd -e -n -v switch switch2")`
oplocate -x `$arg2 + 31.488700000000001` -y `$arg3 + -1.35025` $_obj_geo1_map_control_switch2
chblockbegin
chadd -t 0 0 $_obj_geo1_map_control_switch2 switcher
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../vizRGB")' $_obj_geo1_map_control_switch2/switcher
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_switch2
opexprlanguage -s hscript $_obj_geo1_map_control_switch2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_switch2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_switch2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_switch2

# Node $_obj_geo1_map_control_bind13 (Vop/bind)
set _obj_geo1_map_control_bind13 = `run("opadd -e -n -v bind bind13")`
oplocate -x `$arg2 + 29.170300000000001` -y `$arg3 + -3.23841` $_obj_geo1_map_control_bind13
opparm -V 18.5.408 $_obj_geo1_map_control_bind13 parmname ( Cd ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_bind13
opexprlanguage -s hscript $_obj_geo1_map_control_bind13
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_bind13
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_bind13
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_bind13

# Node $_obj_geo1_map_control_floattovec1 (Vop/floattovec)
set _obj_geo1_map_control_floattovec1 = `run("opadd -e -n -v floattovec floattovec1")`
oplocate -x `$arg2 + 29.170300000000001` -y `$arg3 + -0.79048399999999996` $_obj_geo1_map_control_floattovec1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_floattovec1
opexprlanguage -s hscript $_obj_geo1_map_control_floattovec1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_control_floattovec1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_floattovec1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_floattovec1

# Node $_obj_geo1_map_control_ramp1 (Vop/rampparm)
set _obj_geo1_map_control_ramp1 = `run("opadd -e -n -v rampparm ramp1")`
oplocate -x `$arg2 + 9.5527599999999993` -y `$arg3 + -1.1821200000000001` $_obj_geo1_map_control_ramp1
opparm $_obj_geo1_map_control_ramp1  rampcolordefault ( 2 ) rampfloatdefault ( 2 )
opparm -V 18.5.408 $_obj_geo1_map_control_ramp1 parmname ( mapremap ) parmlabel ( 'map remap' ) ramptype ( flt ) rampcolordefault2pos ( 1 ) rampcolordefault2c ( 1 1 1 ) rampfloatdefault2pos ( 1 ) rampfloatdefault2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_ramp1
opexprlanguage -s hscript $_obj_geo1_map_control_ramp1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_ramp1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_ramp1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_ramp1

# Node $_obj_geo1_map_control_add1 (Vop/add)
set _obj_geo1_map_control_add1 = `run("opadd -e -n -v add add1")`
oplocate -x `$arg2 + 17.307700000000001` -y `$arg3 + -1.5571200000000001` $_obj_geo1_map_control_add1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_add1
opexprlanguage -s hscript $_obj_geo1_map_control_add1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_add1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_add1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_add1

# Node $_obj_geo1_map_control_switch1 (Vop/switch)
set _obj_geo1_map_control_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 20.612100000000002` -y `$arg3 + -0.51276600000000006` $_obj_geo1_map_control_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_switch1
opexprlanguage -s hscript $_obj_geo1_map_control_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_switch1

# Node $_obj_geo1_map_control_parm3 (Vop/parameter)
set _obj_geo1_map_control_parm3 = `run("opadd -e -n -v parameter parm3")`
oplocate -x `$arg2 + 18.1082` -y `$arg3 + -5.8710100000000001` $_obj_geo1_map_control_parm3
opparm -V 18.5.408 $_obj_geo1_map_control_parm3 parmname ( switchmode ) parmlabel ( 'switch mode' ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_parm3
opexprlanguage -s hscript $_obj_geo1_map_control_parm3
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_parm3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_parm3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_parm3

# Node $_obj_geo1_map_control_subtract1 (Vop/subtract)
set _obj_geo1_map_control_subtract1 = `run("opadd -e -n -v subtract subtract1")`
oplocate -x `$arg2 + 17.307700000000001` -y `$arg3 + -3.6543199999999998` $_obj_geo1_map_control_subtract1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_control_subtract1
opexprlanguage -s hscript $_obj_geo1_map_control_subtract1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_control_subtract1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_control_subtract1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_control_subtract1
opcf ..
opcf $_obj_geo1_map_control
oporder -e geometryvopoutput1 bind1 bind2 multiply1 fit2 bind7 parm1 parm2 bind8 switch2 bind13 floattovec1 ramp1 add1 switch1 parm3 subtract1 
opcf ..
opset -p on $_obj_geo1_map_control
opcf $arg1

# Node $_obj_geo1_switch3 (Sop/switch)
set _obj_geo1_switch3 = `run("opadd -e -n -v switch switch3")`
oplocate -x `$arg2 + 3.7308029999999994` -y `$arg3 + 35.101599999999998` $_obj_geo1_switch3
chblockbegin
chadd -t 0 0 $_obj_geo1_switch3 input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enableblur")' $_obj_geo1_switch3/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch3
opexprlanguage -s hscript $_obj_geo1_switch3
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch3
opset -p on $_obj_geo1_switch3
opcf $arg1

# Node $_obj_geo1_switch27 (Sop/switch)
set _obj_geo1_switch27 = `run("opadd -e -n -v switch switch27")`
oplocate -x `$arg2 + -0.22549999999999992` -y `$arg3 + 62.082099999999997` $_obj_geo1_switch27
chblockbegin
chadd -t 0 0 $_obj_geo1_switch27 input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enableocclusion")' $_obj_geo1_switch27/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch27
opexprlanguage -s hscript $_obj_geo1_switch27
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch27
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch27
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch27
opset -p on $_obj_geo1_switch27
opcf $arg1

# Node $_obj_geo1_switch9 (Sop/switch)
set _obj_geo1_switch9 = `run("opadd -e -n -v switch switch9")`
oplocate -x `$arg2 + 4.2461029999999997` -y `$arg3 + 26.032899999999998` $_obj_geo1_switch9
chblockbegin
chadd -t 0 0 $_obj_geo1_switch9 input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../useexisting")' $_obj_geo1_switch9/input
chblockend
opparm -V 18.5.408 $_obj_geo1_switch9 input ( input )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch9
opexprlanguage -s hscript $_obj_geo1_switch9
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch9
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch9
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch9
opset -p on $_obj_geo1_switch9
opcf $arg1

# Node $_obj_geo1_height_control1 (Sop/attribvop)
set _obj_geo1_height_control1 = `run("opadd -e -n -v attribvop height_control1")`
oplocate -x `$arg2 + 2.2645029999999999` -y `$arg3 + 46.128` $_obj_geo1_height_control1
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "heightmin"         label   "min %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "heightmax"         label   "max %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "heightremap"         label   "Height remap"         type    ramp_flt         default { "2" }         range   { 1! 10 }         parmtag { "parmvop" "1" }         parmtag { "rampbasis_var" "heightremap_the_basis_strings" }         parmtag { "rampbasisdefault" "linear" }         parmtag { "rampfloatdefault" "1pos ( 0 ) 1value ( 0 ) 1interp ( linear ) 2pos ( 1 ) 2value ( 1 ) 2interp ( linear )" }         parmtag { "rampkeys_var" "heightremap_the_key_positions" }         parmtag { "rampshowcontrolsdefault" "1" }         parmtag { "rampvalues_var" "heightremap_the_key_values" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "type"         label   "Noise Type"         type    string         default { "anoise" }         menu {             "pnoise"        "Perlin Noise"             "onoise"        "Original Perlin Noise"             "snoise"        "Sparse Convolution Noise"             "anoise"        "Alligator Noise"             "xnoise"        "Simplex Noise"             "correctnoise"  "Zero Centered Perlin Noise"         }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "freq"         label   "Frequency"         type    float         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "offset"         label   "Offset"         type    float         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "amp"         label   "Amplitude"         type    float         default { "1" }         range   { -1 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "rough"         label   "Roughness"         type    float         default { "0.5" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "atten"         label   "Attenuation"         type    float         default { "1" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "turb"         label   "Turbulence"         type    integer         default { "5" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "srcmin"         label   "min input"         type    float         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "srcmax"         label   "max input"         type    float         default { "1" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "destmin"         label   "min outpout"         type    float         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "destmax"         label   "contrast amount"         type    float         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "enablenoiseheight"         label   "enable noise height"         type    toggle         default { "off" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switchmode"         label   "switch mode"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_height_control1
opmultiparm $_obj_geo1_height_control1 'heightY#pos' '../heightdensityramp#pos' 'heightY#value' '../heightdensityramp#value' 'heightY#interp' '../heightdensityramp#interp' 'heightscaleY#pos' '../heightscaleramp#pos' 'heightscaleY#value' '../heightscaleramp#value' 'heightscaleY#interp' '../heightscaleramp#interp' 'heightdensityramp#pos' '../heightdensityramp#pos' 'heightdensityramp#value' '../heightdensityramp#value' 'heightdensityramp#interp' '../heightdensityramp#interp' 'heightscaleramp#pos' '../heightscaleramp#pos' 'heightscaleramp#value' '../heightscaleramp#value' 'heightscaleramp#interp' '../heightscaleramp#interp' 'heightIDramp#pos' '../heightIDramp#pos' 'heightIDramp#value' '../heightIDramp#value' 'heightIDramp#interp' '../heightIDramp#interp' 'heightremap#pos' '../heightremap#pos' 'heightremap#value' '../heightremap#value' 'heightremap#interp' '../heightremap#interp'
opparm $_obj_geo1_height_control1  bindings ( 0 ) groupbindings ( 0 ) heightremap ( 4 )
chblockbegin
chadd -t 0 0 $_obj_geo1_height_control1 heightmin
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightmin")/100' $_obj_geo1_height_control1/heightmin
chadd -t 0 0 $_obj_geo1_height_control1 heightmax
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightmax")/100' $_obj_geo1_height_control1/heightmax
chadd -t 0 0 $_obj_geo1_height_control1 heightremap
chkey -t 0 -v 4 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap")' $_obj_geo1_height_control1/heightremap
chadd -t 0 0 $_obj_geo1_height_control1 heightremap1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap1pos")' $_obj_geo1_height_control1/heightremap1pos
chadd -t 0 0 $_obj_geo1_height_control1 heightremap1value
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap1value")' $_obj_geo1_height_control1/heightremap1value
chadd -t 0 0 $_obj_geo1_height_control1 heightremap1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap1interp")' $_obj_geo1_height_control1/heightremap1interp
chadd -t 0 0 $_obj_geo1_height_control1 freq1
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../freq41")' $_obj_geo1_height_control1/freq1
chadd -t 0 0 $_obj_geo1_height_control1 freq2
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../freq42")' $_obj_geo1_height_control1/freq2
chadd -t 0 0 $_obj_geo1_height_control1 freq3
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../freq43")' $_obj_geo1_height_control1/freq3
chadd -t 0 0 $_obj_geo1_height_control1 offset1
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../offset41")' $_obj_geo1_height_control1/offset1
chadd -t 0 0 $_obj_geo1_height_control1 offset2
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../offset42")' $_obj_geo1_height_control1/offset2
chadd -t 0 0 $_obj_geo1_height_control1 offset3
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../offset43")' $_obj_geo1_height_control1/offset3
chadd -t 0 0 $_obj_geo1_height_control1 amp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../amp2")' $_obj_geo1_height_control1/amp
chadd -t 0 0 $_obj_geo1_height_control1 rough
chkey -t 0 -v 0.53500000000000003 -m 0 -a 0 -A 0 -T a  -F 'ch("../rough2")' $_obj_geo1_height_control1/rough
chadd -t 0 0 $_obj_geo1_height_control1 atten
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../atten")' $_obj_geo1_height_control1/atten
chadd -t 0 0 $_obj_geo1_height_control1 turb
chkey -t 0 -v 5 -m 0 -a 0 -A 0 -T a  -F 'ch("../turb2")' $_obj_geo1_height_control1/turb
chadd -t 0 0 $_obj_geo1_height_control1 srcmin
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../srcmin")' $_obj_geo1_height_control1/srcmin
chadd -t 0 0 $_obj_geo1_height_control1 srcmax
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../srcmax")' $_obj_geo1_height_control1/srcmax
chadd -t 0 0 $_obj_geo1_height_control1 destmax
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../destmax")' $_obj_geo1_height_control1/destmax
chadd -t 0 0 $_obj_geo1_height_control1 enablenoiseheight
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enable_noise")' $_obj_geo1_height_control1/enablenoiseheight
chadd -t 0 0 $_obj_geo1_height_control1 switchmode
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightmode")' $_obj_geo1_height_control1/switchmode
chadd -t 0 0 $_obj_geo1_height_control1 heightremap2pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap2pos")' $_obj_geo1_height_control1/heightremap2pos
chadd -t 0 0 $_obj_geo1_height_control1 heightremap2value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap2value")' $_obj_geo1_height_control1/heightremap2value
chadd -t 0 0 $_obj_geo1_height_control1 heightremap2interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap2interp")' $_obj_geo1_height_control1/heightremap2interp
chadd -t 0 0 $_obj_geo1_height_control1 heightremap3pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap3pos")' $_obj_geo1_height_control1/heightremap3pos
chadd -t 0 0 $_obj_geo1_height_control1 heightremap3value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap3value")' $_obj_geo1_height_control1/heightremap3value
chadd -t 0 0 $_obj_geo1_height_control1 heightremap3interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap3interp")' $_obj_geo1_height_control1/heightremap3interp
chadd -t 0 0 $_obj_geo1_height_control1 heightremap4pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap4pos")' $_obj_geo1_height_control1/heightremap4pos
chadd -t 0 0 $_obj_geo1_height_control1 heightremap4value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap4value")' $_obj_geo1_height_control1/heightremap4value
chadd -t 0 0 $_obj_geo1_height_control1 heightremap4interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../heightremap4interp")' $_obj_geo1_height_control1/heightremap4interp
chblockend
opparm -V 18.5.408 $_obj_geo1_height_control1 heightmin ( heightmin ) heightmax ( heightmax ) heightremap ( heightremap ) heightremap1pos ( heightremap1pos ) heightremap1value ( heightremap1value ) heightremap1interp ( heightremap1interp ) freq ( freq1 freq2 freq3 ) offset ( offset1 offset2 offset3 ) amp ( amp ) rough ( rough ) atten ( atten ) turb ( turb ) srcmin ( srcmin ) srcmax ( srcmax ) destmax ( destmax ) enablenoiseheight ( enablenoiseheight ) switchmode ( switchmode ) heightremap2pos ( heightremap2pos ) heightremap2value ( heightremap2value ) heightremap2interp ( heightremap2interp ) heightremap3pos ( heightremap3pos ) heightremap3value ( heightremap3value ) heightremap3interp ( heightremap3interp ) heightremap4pos ( heightremap4pos ) heightremap4value ( heightremap4value ) heightremap4interp ( heightremap4interp )
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_geo1_height_control1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_height_control1
opexprlanguage -s hscript $_obj_geo1_height_control1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1
opcf $_obj_geo1_height_control1

# Node $_obj_geo1_height_control1_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_geo1_height_control1_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + 0.88547299999999995` -y `$arg3 + -2.20757` $_obj_geo1_height_control1_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_geometryvopglobal1
opexprlanguage -s hscript $_obj_geo1_height_control1_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_geo1_height_control1_geometryvopglobal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_geometryvopglobal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_geometryvopglobal1

# Node $_obj_geo1_height_control1_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_height_control1_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 34.930100000000003` -y `$arg3 + -0.93264100000000005` $_obj_geo1_height_control1_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_height_control1_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_height_control1_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_geometryvopoutput1

# Node $_obj_geo1_height_control1_relbbox1 (Vop/relbbox)
set _obj_geo1_height_control1_relbbox1 = `run("opadd -e -n -v relbbox relbbox1")`
oplocate -x `$arg2 + 0.0628301` -y `$arg3 + 3.8491300000000002` $_obj_geo1_height_control1_relbbox1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_relbbox1
opexprlanguage -s hscript $_obj_geo1_height_control1_relbbox1
opuserdata -n '___Version___' -v '' $_obj_geo1_height_control1_relbbox1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_relbbox1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_relbbox1

# Node $_obj_geo1_height_control1_vectofloat1 (Vop/vectofloat)
set _obj_geo1_height_control1_vectofloat1 = `run("opadd -e -n -v vectofloat vectofloat1")`
oplocate -x `$arg2 + 2.6092599999999999` -y `$arg3 + 2.2098` $_obj_geo1_height_control1_vectofloat1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_vectofloat1
opexprlanguage -s hscript $_obj_geo1_height_control1_vectofloat1
opuserdata -n '___Version___' -v '' $_obj_geo1_height_control1_vectofloat1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_vectofloat1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_vectofloat1

# Node $_obj_geo1_height_control1_bind1 (Vop/bind)
set _obj_geo1_height_control1_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 28.926400000000001` -y `$arg3 + -2.0089100000000002` $_obj_geo1_height_control1_bind1
opparm -V 18.5.408 $_obj_geo1_height_control1_bind1 parmname ( density ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_bind1
opexprlanguage -s hscript $_obj_geo1_height_control1_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_bind1

# Node $_obj_geo1_height_control1_bind2 (Vop/bind)
set _obj_geo1_height_control1_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 5.0366900000000001` -y `$arg3 + 3.7838599999999998` $_obj_geo1_height_control1_bind2
opparm -V 18.5.408 $_obj_geo1_height_control1_bind2 parmname ( density ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_bind2
opexprlanguage -s hscript $_obj_geo1_height_control1_bind2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_bind2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_bind2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_bind2

# Node $_obj_geo1_height_control1_multiply1 (Vop/multiply)
set _obj_geo1_height_control1_multiply1 = `run("opadd -e -n -v multiply multiply1")`
oplocate -x `$arg2 + 17.868500000000001` -y `$arg3 + 3.5192000000000001` $_obj_geo1_height_control1_multiply1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_multiply1
opexprlanguage -s hscript $_obj_geo1_height_control1_multiply1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_multiply1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_multiply1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_multiply1

# Node $_obj_geo1_height_control1_fit1 (Vop/fit)
set _obj_geo1_height_control1_fit1 = `run("opadd -e -n -v fit fit1")`
oplocate -x `$arg2 + 5.6092599999999999` -y `$arg3 + 1.5179800000000001` $_obj_geo1_height_control1_fit1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b on -L off -M off -H on -E off $_obj_geo1_height_control1_fit1
opexprlanguage -s hscript $_obj_geo1_height_control1_fit1
opuserdata -n '___Version___' -v '' $_obj_geo1_height_control1_fit1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_fit1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_fit1

# Node $_obj_geo1_height_control1_fit2 (Vop/fit)
set _obj_geo1_height_control1_fit2 = `run("opadd -e -n -v fit fit2")`
oplocate -x `$arg2 + 14.811400000000001` -y `$arg3 + 1.7604900000000001` $_obj_geo1_height_control1_fit2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_fit2
opexprlanguage -s hscript $_obj_geo1_height_control1_fit2
opuserdata -n '___Version___' -v '' $_obj_geo1_height_control1_fit2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_fit2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_fit2

# Node $_obj_geo1_height_control1_destmin (Vop/parameter)
set _obj_geo1_height_control1_destmin = `run("opadd -e -n -v parameter destmin")`
oplocate -x `$arg2 + 8.81142` -y `$arg3 + 2.3479800000000002` $_obj_geo1_height_control1_destmin
opparm -V 18.5.408 $_obj_geo1_height_control1_destmin parmname ( heightmin ) parmlabel ( 'min %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_destmin
opexprlanguage -s hscript $_obj_geo1_height_control1_destmin
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_destmin
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_destmin
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_destmin

# Node $_obj_geo1_height_control1_destmax (Vop/parameter)
set _obj_geo1_height_control1_destmax = `run("opadd -e -n -v parameter destmax")`
oplocate -x `$arg2 + 8.81142` -y `$arg3 + 0.87640300000000004` $_obj_geo1_height_control1_destmax
opparm -V 18.5.408 $_obj_geo1_height_control1_destmax parmname ( heightmax ) parmlabel ( 'max %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_destmax
opexprlanguage -s hscript $_obj_geo1_height_control1_destmax
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_destmax
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_destmax
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_destmax

# Node $_obj_geo1_height_control1_bind6 (Vop/bind)
set _obj_geo1_height_control1_bind6 = `run("opadd -e -n -v bind bind6")`
oplocate -x `$arg2 + 23.793600000000001` -y `$arg3 + 1.53549` $_obj_geo1_height_control1_bind6
opparm -V 18.5.408 $_obj_geo1_height_control1_bind6 parmname ( heightA ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_bind6
opexprlanguage -s hscript $_obj_geo1_height_control1_bind6
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_bind6
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_bind6
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_bind6

# Node $_obj_geo1_height_control1_ramp2 (Vop/rampparm)
set _obj_geo1_height_control1_ramp2 = `run("opadd -e -n -v rampparm ramp2")`
oplocate -x `$arg2 + 8.81142` -y `$arg3 + -1.08264` $_obj_geo1_height_control1_ramp2
opparm $_obj_geo1_height_control1_ramp2  rampcolordefault ( 2 ) rampfloatdefault ( 2 )
opparm -V 18.5.408 $_obj_geo1_height_control1_ramp2 parmname ( heightremap ) parmlabel ( 'Height remap' ) ramptype ( flt ) rampcolordefault2pos ( 1 ) rampcolordefault2c ( 1 1 1 ) rampfloatdefault2pos ( 1 ) rampfloatdefault2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_ramp2
opexprlanguage -s hscript $_obj_geo1_height_control1_ramp2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_ramp2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_ramp2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_ramp2

# Node $_obj_geo1_height_control1_fit3 (Vop/fit)
set _obj_geo1_height_control1_fit3 = `run("opadd -e -n -v fit fit3")`
oplocate -x `$arg2 + 11.811400000000001` -y `$arg3 + -0.42912899999999998` $_obj_geo1_height_control1_fit3
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_fit3
opexprlanguage -s hscript $_obj_geo1_height_control1_fit3
opuserdata -n '___Version___' -v '' $_obj_geo1_height_control1_fit3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_fit3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_fit3

# Node $_obj_geo1_height_control1_turbnoise1 (Vop/turbnoise)
set _obj_geo1_height_control1_turbnoise1 = `run("opadd -e -n -v turbnoise turbnoise1")`
oplocate -x `$arg2 + 7.4204999999999997` -y `$arg3 + -3.9846400000000002` $_obj_geo1_height_control1_turbnoise1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_turbnoise1
opexprlanguage -s hscript $_obj_geo1_height_control1_turbnoise1
opuserdata -n '___Version___' -v '' $_obj_geo1_height_control1_turbnoise1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_turbnoise1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_turbnoise1

# Node $_obj_geo1_height_control1_type (Vop/parameter)
set _obj_geo1_height_control1_type = `run("opadd -e -n -v parameter type")`
oplocate -x `$arg2 + 6.1114199999999999` -y `$arg3 + -2.4414600000000002` $_obj_geo1_height_control1_type
opparm -V 18.5.408 $_obj_geo1_height_control1_type parmname ( type ) parmlabel ( 'Noise Type' ) parmtype ( string ) stringdef ( anoise ) exportcontext ( cvex ) providemenu ( on ) menuchoices ( 'pnoise "Perlin Noise" onoise "Original Perlin Noise" snoise "Sparse Convolution Noise" anoise "Alligator Noise" xnoise "Simplex Noise" correctnoise "Zero Centered Perlin Noise" ' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_type
opexprlanguage -s hscript $_obj_geo1_height_control1_type
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_type
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_type
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_type

# Node $_obj_geo1_height_control1_freq (Vop/parameter)
set _obj_geo1_height_control1_freq = `run("opadd -e -n -v parameter freq")`
oplocate -x `$arg2 + 6.31142` -y `$arg3 + -2.8414600000000001` $_obj_geo1_height_control1_freq
opparm -V 18.5.408 $_obj_geo1_height_control1_freq parmname ( freq ) parmlabel ( Frequency ) parmtype ( float3 ) float3def ( 1 1 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_freq
opexprlanguage -s hscript $_obj_geo1_height_control1_freq
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_freq
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_freq
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_freq

# Node $_obj_geo1_height_control1_offset (Vop/parameter)
set _obj_geo1_height_control1_offset = `run("opadd -e -n -v parameter offset")`
oplocate -x `$arg2 + 6.4114199999999997` -y `$arg3 + -3.0414599999999998` $_obj_geo1_height_control1_offset
opparm -V 18.5.408 $_obj_geo1_height_control1_offset parmname ( offset ) parmlabel ( Offset ) parmtype ( float3 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_offset
opexprlanguage -s hscript $_obj_geo1_height_control1_offset
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_offset
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_offset
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_offset

# Node $_obj_geo1_height_control1_amp (Vop/parameter)
set _obj_geo1_height_control1_amp = `run("opadd -e -n -v parameter amp")`
oplocate -x `$arg2 + 6.5114200000000002` -y `$arg3 + -3.24146` $_obj_geo1_height_control1_amp
opparm -V 18.5.408 $_obj_geo1_height_control1_amp parmname ( amp ) parmlabel ( Amplitude ) floatdef ( 1 ) rangeflt ( -1 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_amp
opexprlanguage -s hscript $_obj_geo1_height_control1_amp
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_amp
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_amp
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_amp

# Node $_obj_geo1_height_control1_rough (Vop/parameter)
set _obj_geo1_height_control1_rough = `run("opadd -e -n -v parameter rough")`
oplocate -x `$arg2 + 6.6114199999999999` -y `$arg3 + -3.4414600000000002` $_obj_geo1_height_control1_rough
opparm -V 18.5.408 $_obj_geo1_height_control1_rough parmname ( rough ) parmlabel ( Roughness ) floatdef ( 0.5 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_rough
opexprlanguage -s hscript $_obj_geo1_height_control1_rough
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_rough
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_rough
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_rough

# Node $_obj_geo1_height_control1_atten (Vop/parameter)
set _obj_geo1_height_control1_atten = `run("opadd -e -n -v parameter atten")`
oplocate -x `$arg2 + 6.7114200000000004` -y `$arg3 + -3.6414599999999999` $_obj_geo1_height_control1_atten
opparm -V 18.5.408 $_obj_geo1_height_control1_atten parmname ( atten ) parmlabel ( Attenuation ) floatdef ( 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_atten
opexprlanguage -s hscript $_obj_geo1_height_control1_atten
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_atten
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_atten
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_atten

# Node $_obj_geo1_height_control1_turb (Vop/parameter)
set _obj_geo1_height_control1_turb = `run("opadd -e -n -v parameter turb")`
oplocate -x `$arg2 + 6.81142` -y `$arg3 + -3.8414600000000001` $_obj_geo1_height_control1_turb
opparm -V 18.5.408 $_obj_geo1_height_control1_turb parmname ( turb ) parmlabel ( Turbulence ) parmtype ( int ) intdef ( 5 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_turb
opexprlanguage -s hscript $_obj_geo1_height_control1_turb
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_turb
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_turb
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_turb

# Node $_obj_geo1_height_control1_fit4 (Vop/fit)
set _obj_geo1_height_control1_fit4 = `run("opadd -e -n -v fit fit4")`
oplocate -x `$arg2 + 9.8614099999999993` -y `$arg3 + -3.9846400000000002` $_obj_geo1_height_control1_fit4
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_fit4
opexprlanguage -s hscript $_obj_geo1_height_control1_fit4
opuserdata -n '___Version___' -v '' $_obj_geo1_height_control1_fit4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_fit4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_fit4

# Node $_obj_geo1_height_control1_srcmin (Vop/parameter)
set _obj_geo1_height_control1_srcmin = `run("opadd -e -n -v parameter srcmin")`
oplocate -x `$arg2 + 7.5614100000000004` -y `$arg3 + -3.3846400000000001` $_obj_geo1_height_control1_srcmin
opparm -V 18.5.408 $_obj_geo1_height_control1_srcmin parmname ( srcmin ) parmlabel ( 'min input' ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_srcmin
opexprlanguage -s hscript $_obj_geo1_height_control1_srcmin
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_srcmin
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_srcmin
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_srcmin

# Node $_obj_geo1_height_control1_srcmax (Vop/parameter)
set _obj_geo1_height_control1_srcmax = `run("opadd -e -n -v parameter srcmax")`
oplocate -x `$arg2 + 7.6614100000000001` -y `$arg3 + -3.5846399999999998` $_obj_geo1_height_control1_srcmax
opparm -V 18.5.408 $_obj_geo1_height_control1_srcmax parmname ( srcmax ) parmlabel ( 'max input' ) floatdef ( 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_srcmax
opexprlanguage -s hscript $_obj_geo1_height_control1_srcmax
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_srcmax
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_srcmax
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_srcmax

# Node $_obj_geo1_height_control1_destmin1 (Vop/parameter)
set _obj_geo1_height_control1_destmin1 = `run("opadd -e -n -v parameter destmin1")`
oplocate -x `$arg2 + 7.7614099999999997` -y `$arg3 + -3.78464` $_obj_geo1_height_control1_destmin1
opparm -V 18.5.408 $_obj_geo1_height_control1_destmin1 parmname ( destmin ) parmlabel ( 'min outpout' ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_destmin1
opexprlanguage -s hscript $_obj_geo1_height_control1_destmin1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_destmin1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_destmin1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_destmin1

# Node $_obj_geo1_height_control1_destmax1 (Vop/parameter)
set _obj_geo1_height_control1_destmax1 = `run("opadd -e -n -v parameter destmax1")`
oplocate -x `$arg2 + 7.8614100000000002` -y `$arg3 + -3.9846400000000002` $_obj_geo1_height_control1_destmax1
opparm -V 18.5.408 $_obj_geo1_height_control1_destmax1 parmname ( destmax ) parmlabel ( 'contrast amount' ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_height_control1_destmax1
opexprlanguage -s hscript $_obj_geo1_height_control1_destmax1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_destmax1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_destmax1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_destmax1

# Node $_obj_geo1_height_control1_switch1 (Vop/switch)
set _obj_geo1_height_control1_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 12.932600000000001` -y `$arg3 + -3.7919100000000001` $_obj_geo1_height_control1_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_switch1
opexprlanguage -s hscript $_obj_geo1_height_control1_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_switch1

# Node $_obj_geo1_height_control1_const1 (Vop/constant)
set _obj_geo1_height_control1_const1 = `run("opadd -e -n -v constant const1")`
oplocate -x `$arg2 + 11.5756` -y `$arg3 + -5.8516500000000002` $_obj_geo1_height_control1_const1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_const1
opexprlanguage -s hscript $_obj_geo1_height_control1_const1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_const1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_const1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_const1

# Node $_obj_geo1_height_control1_parm1 (Vop/parameter)
set _obj_geo1_height_control1_parm1 = `run("opadd -e -n -v parameter parm1")`
oplocate -x `$arg2 + 13.396699999999999` -y `$arg3 + -6.2316500000000001` $_obj_geo1_height_control1_parm1
opparm -V 18.5.408 $_obj_geo1_height_control1_parm1 parmname ( enablenoiseheight ) parmlabel ( 'enable noise height' ) parmtype ( toggle ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_parm1
opexprlanguage -s hscript $_obj_geo1_height_control1_parm1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_parm1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_parm1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_parm1

# Node $_obj_geo1_height_control1_add1 (Vop/add)
set _obj_geo1_height_control1_add1 = `run("opadd -e -n -v add add1")`
oplocate -x `$arg2 + 21.398800000000001` -y `$arg3 + -2.3842099999999999` $_obj_geo1_height_control1_add1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_add1
opexprlanguage -s hscript $_obj_geo1_height_control1_add1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_add1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_add1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_add1

# Node $_obj_geo1_height_control1_switch2 (Vop/switch)
set _obj_geo1_height_control1_switch2 = `run("opadd -e -n -v switch switch2")`
oplocate -x `$arg2 + 24.383199999999999` -y `$arg3 + -2.0089100000000002` $_obj_geo1_height_control1_switch2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_switch2
opexprlanguage -s hscript $_obj_geo1_height_control1_switch2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_switch2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_switch2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_switch2

# Node $_obj_geo1_height_control1_parm2 (Vop/parameter)
set _obj_geo1_height_control1_parm2 = `run("opadd -e -n -v parameter parm2")`
oplocate -x `$arg2 + 21.739100000000001` -y `$arg3 + -6.1872499999999997` $_obj_geo1_height_control1_parm2
opparm -V 18.5.408 $_obj_geo1_height_control1_parm2 parmname ( switchmode ) parmlabel ( 'switch mode' ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_parm2
opexprlanguage -s hscript $_obj_geo1_height_control1_parm2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_parm2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_parm2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_parm2

# Node $_obj_geo1_height_control1_subtract1 (Vop/subtract)
set _obj_geo1_height_control1_subtract1 = `run("opadd -e -n -v subtract subtract1")`
oplocate -x `$arg2 + 20.289999999999999` -y `$arg3 + -4.3047199999999997` $_obj_geo1_height_control1_subtract1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_height_control1_subtract1
opexprlanguage -s hscript $_obj_geo1_height_control1_subtract1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_height_control1_subtract1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_control1_subtract1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_control1_subtract1
opcf ..
opcf $_obj_geo1_height_control1
oporder -e geometryvopglobal1 geometryvopoutput1 relbbox1 vectofloat1 bind1 bind2 multiply1 fit1 fit2 destmin destmax bind6 ramp2 fit3 turbnoise1 type freq offset amp rough atten turb fit4 srcmin srcmax destmin1 destmax1 switch1 const1 parm1 add1 switch2 parm2 subtract1 
opcf ..
opset -p on $_obj_geo1_height_control1
opcf $arg1

# Node $_obj_geo1_map_density_scale1 (Sop/attribwrangle)
set _obj_geo1_map_density_scale1 = `run("opadd -e -n -u -v attribwrangle map_density_scale1")`
oplocate -x `$arg2 + 7.6962029999999988` -y `$arg3 + 18.838500000000003` $_obj_geo1_map_density_scale1
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "densityscaleramp"         label   "Densityscale"         type    ramp_flt         default { "2" }         range   { 1! 10 }     }     parm {         name    "min"         label   "Min"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "max"         label   "Max"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "minscale"         label   "Minscale"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "maxscale"         label   "Maxscale"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "pscaleramp"         label   "Pscaleramp"         type    ramp_flt         default { "2" }         range   { 1! 10 }     }     parm {         name    "mapdensityramp"         label   "Mapdensityramp"         type    ramp_flt         default { "2" }         range   { 1! 10 }     }     parm {         name    "mapscaleramp"         label   "Mapscaleramp"         type    ramp_flt         default { "2" }         range   { 1! 10 }     } ' $_obj_geo1_map_density_scale1
opmultiparm $_obj_geo1_map_density_scale1 'densityscale#pos' '../densityscale2_#pos' 'densityscale#value' '../densityscale2_#value' 'densityscale#interp' '../densityscale2_#interp' 'pscaleramp#pos' '../pscaleramp#pos' 'pscaleramp#value' '../pscaleramp#value' 'pscaleramp#interp' '../pscaleramp#interp'
opparm $_obj_geo1_map_density_scale1  bindings ( 0 ) groupbindings ( 0 ) densityscaleramp ( 0 ) pscaleramp ( 0 ) mapdensityramp ( 3 ) mapscaleramp ( 2 )
chblockbegin
chadd -t 0 0 $_obj_geo1_map_density_scale1 densityscaleramp
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../densityscale2")' $_obj_geo1_map_density_scale1/densityscaleramp
chadd -t 0 0 $_obj_geo1_map_density_scale1 densityscaleramp1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../densityscale2_1pos")' $_obj_geo1_map_density_scale1/densityscaleramp1pos
chadd -t 0 0 $_obj_geo1_map_density_scale1 densityscaleramp1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../densityscale2_1value")' $_obj_geo1_map_density_scale1/densityscaleramp1value
chadd -t 0 0 $_obj_geo1_map_density_scale1 densityscaleramp1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../densityscale2_1interp")' $_obj_geo1_map_density_scale1/densityscaleramp1interp
chadd -t 0 0 $_obj_geo1_map_density_scale1 min
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapdensitymin")/100' $_obj_geo1_map_density_scale1/min
chadd -t 0 0 $_obj_geo1_map_density_scale1 max
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapdensitymax")/100' $_obj_geo1_map_density_scale1/max
chadd -t 0 0 $_obj_geo1_map_density_scale1 minscale
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapscalemin")/100' $_obj_geo1_map_density_scale1/minscale
chadd -t 0 0 $_obj_geo1_map_density_scale1 maxscale
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../mapscalemax")/100' $_obj_geo1_map_density_scale1/maxscale
chadd -t 0 0 $_obj_geo1_map_density_scale1 pscaleramp
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../pscaleramp")' $_obj_geo1_map_density_scale1/pscaleramp
chadd -t 0 0 $_obj_geo1_map_density_scale1 pscaleramp1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../pscaleramp1pos")' $_obj_geo1_map_density_scale1/pscaleramp1pos
chadd -t 0 0 $_obj_geo1_map_density_scale1 pscaleramp1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../pscaleramp1value")' $_obj_geo1_map_density_scale1/pscaleramp1value
chadd -t 0 0 $_obj_geo1_map_density_scale1 pscaleramp1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../pscaleramp1interp")' $_obj_geo1_map_density_scale1/pscaleramp1interp
chblockend
opparm $_obj_geo1_map_density_scale1 snippet ( '@mapdensity = chramp("mapdensityramp",@map);\n@density *= fit01(@mapdensity,ch("min"),ch("max"));\n@mapA = @density;\n\n\n@mapscale =chramp("mapscaleramp",@map);\n@pscale *= fit01(@mapdensity,ch("minscale"),ch("maxscale"));\n@mapB = @pscale;' ) densityscaleramp ( densityscaleramp ) densityscaleramp1pos ( densityscaleramp1pos ) densityscaleramp1value ( densityscaleramp1value ) densityscaleramp1interp ( densityscaleramp1interp ) min ( min ) max ( max ) minscale ( minscale ) maxscale ( maxscale ) pscaleramp ( pscaleramp ) pscaleramp1pos ( pscaleramp1pos ) pscaleramp1value ( pscaleramp1value ) pscaleramp1interp ( pscaleramp1interp ) mapdensityramp ( 3 ) mapdensityramp2pos ( 0.2031872570514679 ) mapdensityramp2value ( 1 ) mapscaleramp2pos ( 0.99601596593856812 ) mapscaleramp2value ( 1 ) mapdensityramp3pos ( 0.98406374454498291 ) mapdensityramp3value ( 1 )
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_geo1_map_density_scale1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b on $_obj_geo1_map_density_scale1
opexprlanguage -s hscript $_obj_geo1_map_density_scale1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_density_scale1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_density_scale1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_density_scale1
opcf $_obj_geo1_map_density_scale1

# Node $_obj_geo1_map_density_scale1_attribvop1 (Sop/attribvop)
set _obj_geo1_map_density_scale1_attribvop1 = `run("opadd -e -n -v attribvop attribvop1")`
oplocate -x `$arg2 + 1` -y `$arg3 + 4.7469999999999999` $_obj_geo1_map_density_scale1_attribvop1
opmultiparm $_obj_geo1_map_density_scale1_attribvop1 'bindname#' '../bindname#' 'bindparm#' '../bindparm#' 'bindgroupname#' '../bindgroupname#' 'bindgroupparm#' '../bindgroupparm#'
opparm $_obj_geo1_map_density_scale1_attribvop1  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 bindgroup
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chs("../group")' $_obj_geo1_map_density_scale1_attribvop1/bindgroup
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 bindgrouptype
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../grouptype")' $_obj_geo1_map_density_scale1_attribvop1/bindgrouptype
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 bindclass
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../class")' $_obj_geo1_map_density_scale1_attribvop1/bindclass
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 vex_numcount
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../vex_numcount")' $_obj_geo1_map_density_scale1_attribvop1/vex_numcount
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 vex_threadjobsize
chkey -t 0 -v 1024 -m 0 -a 0 -A 0 -T a  -F 'ch("../vex_threadjobsize")' $_obj_geo1_map_density_scale1_attribvop1/vex_threadjobsize
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 vex_cwdpath
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chsop("../vex_cwdpath")' $_obj_geo1_map_density_scale1_attribvop1/vex_cwdpath
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 vex_outputmask
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chs("../vex_outputmask")' $_obj_geo1_map_density_scale1_attribvop1/vex_outputmask
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 vex_precision
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chs("../vex_precision")' $_obj_geo1_map_density_scale1_attribvop1/vex_precision
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 autobind
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../autobind")' $_obj_geo1_map_density_scale1_attribvop1/autobind
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 bindings
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../bindings")' $_obj_geo1_map_density_scale1_attribvop1/bindings
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 groupautobind
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../groupautobind")' $_obj_geo1_map_density_scale1_attribvop1/groupautobind
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 groupbindings
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../groupbindings")' $_obj_geo1_map_density_scale1_attribvop1/groupbindings
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 vex_updatenmls
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../vex_updatenmls")' $_obj_geo1_map_density_scale1_attribvop1/vex_updatenmls
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 vex_matchattrib
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chs("../vex_matchattrib")' $_obj_geo1_map_density_scale1_attribvop1/vex_matchattrib
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 vex_inplace
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../vex_inplace")' $_obj_geo1_map_density_scale1_attribvop1/vex_inplace
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1 vex_selectiongroup
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chs("../vex_selectiongroup")' $_obj_geo1_map_density_scale1_attribvop1/vex_selectiongroup
chblockend
opparm -V 18.5.408 $_obj_geo1_map_density_scale1_attribvop1 bindgroup ( bindgroup ) bindgrouptype ( bindgrouptype ) bindclass ( bindclass ) vex_numcount ( vex_numcount ) vex_threadjobsize ( vex_threadjobsize ) stdswitcher ( 1 1 ) vex_cwdpath ( vex_cwdpath ) vex_outputmask ( vex_outputmask ) vex_precision ( vex_precision ) autobind ( autobind ) bindings ( bindings ) groupautobind ( groupautobind ) groupbindings ( groupbindings ) vex_updatenmls ( vex_updatenmls ) vex_matchattrib ( vex_matchattrib ) vex_inplace ( vex_inplace ) vex_selectiongroup ( vex_selectiongroup )
opcolor -c 0.80000001192092896 0.80000001192092896 0.80000001192092896 $_obj_geo1_map_density_scale1_attribvop1
opset -d on -r on -h on -f off -y off -t off -l off -s off -u on -F off -c off -e on -b off $_obj_geo1_map_density_scale1_attribvop1
opexprlanguage -s hscript $_obj_geo1_map_density_scale1_attribvop1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_density_scale1_attribvop1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_density_scale1_attribvop1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_density_scale1_attribvop1
opcf $_obj_geo1_map_density_scale1_attribvop1

# Node $_obj_geo1_map_density_scale1_attribvop1_snippet1 (Vop/snippet)
set _obj_geo1_map_density_scale1_attribvop1_snippet1 = `run("opadd -e -n -v snippet snippet1")`
oplocate -x `$arg2 + 3.88226` -y `$arg3 + 2.5998899999999998` $_obj_geo1_map_density_scale1_attribvop1_snippet1
opparm $_obj_geo1_map_density_scale1_attribvop1_snippet1  namenum ( 0 )
chblockbegin
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1_snippet1 code
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chs("../../snippet")' $_obj_geo1_map_density_scale1_attribvop1_snippet1/code
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1_snippet1 strict
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../../vex_strict")' $_obj_geo1_map_density_scale1_attribvop1_snippet1/strict
chadd -t 0 0 $_obj_geo1_map_density_scale1_attribvop1_snippet1 exportlist
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chs("../../exportlist")' $_obj_geo1_map_density_scale1_attribvop1_snippet1/exportlist
chblockend
opparm -V 18.5.408 $_obj_geo1_map_density_scale1_attribvop1_snippet1 code ( code ) strict ( strict ) exportlist ( exportlist )
opcolor -c 0.80000001192092896 0.80000001192092896 0.80000001192092896 $_obj_geo1_map_density_scale1_attribvop1_snippet1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F off -c off -e on -b off -L off -M off -H on -E off $_obj_geo1_map_density_scale1_attribvop1_snippet1
opexprlanguage -s hscript $_obj_geo1_map_density_scale1_attribvop1_snippet1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_density_scale1_attribvop1_snippet1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_density_scale1_attribvop1_snippet1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_density_scale1_attribvop1_snippet1
opcf ..
opcf ..
opcf $_obj_geo1_map_density_scale1
opcf $_obj_geo1_map_density_scale1_attribvop1
opcf ..
opcf ..
opset -p on $_obj_geo1_map_density_scale1
opcf $arg1

# Node $_obj_geo1_occlusion (Sop/subnet)
set _obj_geo1_occlusion = `run("opadd -e -n -v subnet occlusion")`
oplocate -x `$arg2 + 4.1025030000000005` -y `$arg3 + 66.888940000000005` $_obj_geo1_occlusion
opspareds '    parm {         name    "label1"         baseparm         label   "Input #1 Label"         invisible         export  all     }     parm {         name    "label2"         baseparm         label   "Input #2 Label"         invisible         export  all     }     parm {         name    "label3"         baseparm         label   "Input #3 Label"         invisible         export  all     }     parm {         name    "label4"         baseparm         label   "Input #4 Label"         invisible         export  all     }     parm {         name    "rays"         label   "Rays"         type    integer         default { "50" }         range   { 0 10 }         parmtag { "autoscope" "0000000000000000" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "bias"         label   "Bias"         type    float         default { "0.5" }         range   { 0 1 }         parmtag { "autoscope" "0000000000000000" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "remapramp"         label   "Remapramp"         type    ramp_flt         default { "3" }         range   { 1! 10 }         parmtag { "autoscope" "0000000000000000" }         parmtag { "rampfloatdefault" "1pos ( 0 ) 1value ( 0 ) 1interp ( linear ) 2pos ( 0.89771199226379395 ) 2value ( 0 ) 2interp ( linear ) 3pos ( 1 ) 3value ( 1 ) 3interp ( linear )" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "maxdist"         label   "Maxdist"         type    float         default { "2" }         range   { 0 1 }         parmtag { "autoscope" "0000000000000000" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "conewidth"         label   "Conewidth"         type    float         default { "90" }         range   { 0 1 }         parmtag { "autoscope" "0000000000000000" }         parmtag { "script_callback_language" "python" }     } ' $_obj_geo1_occlusion
opmultiparm $_obj_geo1_occlusion 'remapramp#pos' '../remapramp#pos' 'remapramp#value' '../remapramp#value' 'remapramp#interp' '../remapramp#interp'
opparm $_obj_geo1_occlusion  remapramp ( 0 )
chblockbegin
chadd -t 0 0 $_obj_geo1_occlusion rays
chkey -t 0 -v 50 -m 0 -a 0 -A 0 -T a  -F 'ch("../rays")' $_obj_geo1_occlusion/rays
chadd -t 0 0 $_obj_geo1_occlusion bias
chkey -t 0 -v 0.5 -m 0 -a 0 -A 0 -T a  -F 'ch("../bias")' $_obj_geo1_occlusion/bias
chadd -t 0 0 $_obj_geo1_occlusion remapramp
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../remapramp")' $_obj_geo1_occlusion/remapramp
chadd -t 0 0 $_obj_geo1_occlusion remapramp1pos
chkey -t 0 -v 0.312247633934021 -m 0 -a 0 -A 0 -T a  -F 'ch("../remapramp1pos")' $_obj_geo1_occlusion/remapramp1pos
chadd -t 0 0 $_obj_geo1_occlusion remapramp1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../remapramp1value")' $_obj_geo1_occlusion/remapramp1value
chadd -t 0 0 $_obj_geo1_occlusion remapramp1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../remapramp1interp")' $_obj_geo1_occlusion/remapramp1interp
chadd -t 0 0 $_obj_geo1_occlusion maxdist
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../maxdist")' $_obj_geo1_occlusion/maxdist
chadd -t 0 0 $_obj_geo1_occlusion conewidth
chkey -t 0 -v 120 -m 0 -a 0 -A 0 -T a  -F 'ch("../conewidth")' $_obj_geo1_occlusion/conewidth
chblockend
opparm -V 18.5.408 $_obj_geo1_occlusion rays ( rays ) bias ( bias ) remapramp ( remapramp ) remapramp1pos ( remapramp1pos ) remapramp1value ( remapramp1value ) remapramp1interp ( remapramp1interp ) maxdist ( maxdist ) conewidth ( conewidth )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_occlusion
opexprlanguage -s hscript $_obj_geo1_occlusion
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion
opcf $_obj_geo1_occlusion

# Node $_obj_geo1_occlusion_attribwrangle1 (Sop/attribwrangle)
set _obj_geo1_occlusion_attribwrangle1 = `run("opadd -e -n -v attribwrangle attribwrangle1")`
oplocate -x `$arg2 + -0.600993` -y `$arg3 + 2.5573199999999998` $_obj_geo1_occlusion_attribwrangle1
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "maxdist"         label   "Maxdist"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "conewidth"         label   "Conewidth"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "bias"         label   "Bias"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "rays"         label   "Rays"         type    integer         default { "0" }         range   { 0 10 }     }     parm {         name    "remapocclu"         label   "Remapocclu"         type    ramp_flt         default { "2" }         range   { 1! 10 }     } ' $_obj_geo1_occlusion_attribwrangle1
opmultiparm $_obj_geo1_occlusion_attribwrangle1 'remapramp#pos' '../remapramp#pos' 'remapramp#value' '../remapramp#value' 'remapramp#interp' '../remapramp#interp' 'remapocclu#pos' '../../remapocclu#pos' 'remapocclu#value' '../../remapocclu#value' 'remapocclu#interp' '../../remapocclu#interp'
opparm $_obj_geo1_occlusion_attribwrangle1  bindings ( 0 ) groupbindings ( 0 ) remapocclu ( 2 )
chblockbegin
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 maxdist
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../../maxdist")' $_obj_geo1_occlusion_attribwrangle1/maxdist
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 conewidth
chkey -t 0 -v 90 -m 0 -a 0 -A 0 -T a  -F 'ch("../../conewidth")' $_obj_geo1_occlusion_attribwrangle1/conewidth
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 bias
chkey -t 0 -v 0.5 -m 0 -a 0 -A 0 -T a  -F 'ch("../../bias")' $_obj_geo1_occlusion_attribwrangle1/bias
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 rays
chkey -t 0 -v 50 -m 0 -a 0 -A 0 -T a  -F 'ch("../../rays")' $_obj_geo1_occlusion_attribwrangle1/rays
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 remapocclu
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../../remapocclu")' $_obj_geo1_occlusion_attribwrangle1/remapocclu
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 remapocclu1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../../remapocclu1pos")' $_obj_geo1_occlusion_attribwrangle1/remapocclu1pos
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 remapocclu1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../../remapocclu1value")' $_obj_geo1_occlusion_attribwrangle1/remapocclu1value
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 remapocclu1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../../remapocclu1interp")' $_obj_geo1_occlusion_attribwrangle1/remapocclu1interp
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 remapocclu2pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../../remapocclu2pos")' $_obj_geo1_occlusion_attribwrangle1/remapocclu2pos
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 remapocclu2value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../../remapocclu2value")' $_obj_geo1_occlusion_attribwrangle1/remapocclu2value
chadd -t 0 0 $_obj_geo1_occlusion_attribwrangle1 remapocclu2interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../../remapocclu2interp")' $_obj_geo1_occlusion_attribwrangle1/remapocclu2interp
chblockend
opparm $_obj_geo1_occlusion_attribwrangle1 snippet ( '#include <voplib.h>\n\nvector hit, raydir;\nfloat u, v, conewidth;\nfloat occluded; \nint hitprim, hitprim_2;\nfloat tempOcc = 0;\n \nfloat maxdist = ch(\'maxdist\');\nconewidth = radians(ch(\'conewidth\'));\nint rays = chi(\'rays\');\nfloat bias = chf(\'bias\');\n\nfor (int i = 0; i<rays; i++ ) {\n\n    raydir = sample_direction_cone(v@N,conewidth,vector2(rand(i*234524)));\n    hitprim = intersect(0,@P+(v@N*0.001), raydir*maxdist, hit, u, v);\n    hitprim_2 = intersect(1,@P+(v@N*0.001), raydir*maxdist, hit, u, v);\n\n    if (hitprim!=-1 || hitprim_2!=-1) \n      tempOcc+=1;\n\n}\n\ntempOcc = clamp(vop_bias(1.0-(tempOcc / rays), bias), 0, 1);\nf@occlusion = chramp("remapocclu", tempOcc);' ) maxdist ( maxdist ) conewidth ( conewidth ) bias ( bias ) rays ( rays ) remapocclu ( remapocclu ) remapocclu1pos ( remapocclu1pos ) remapocclu1value ( remapocclu1value ) remapocclu1interp ( remapocclu1interp ) remapocclu2pos ( remapocclu2pos ) remapocclu2value ( remapocclu2value ) remapocclu2interp ( remapocclu2interp )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_occlusion_attribwrangle1
opexprlanguage -s hscript $_obj_geo1_occlusion_attribwrangle1
opuserdata -n '___Version___' -v '' $_obj_geo1_occlusion_attribwrangle1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_attribwrangle1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_attribwrangle1

# Node $_obj_geo1_occlusion_attribblur1 (Sop/attribblur)
set _obj_geo1_occlusion_attribblur1 = `run("opadd -e -n -v attribblur attribblur1")`
oplocate -x `$arg2 + -0.597993` -y `$arg3 + 1.2518400000000001` $_obj_geo1_occlusion_attribblur1
opparm -V 1.0 $_obj_geo1_occlusion_attribblur1 attributes ( occlusion ) method ( edgelength ) stepsize ( 0.224 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_occlusion_attribblur1
opexprlanguage -s hscript $_obj_geo1_occlusion_attribblur1
opuserdata -n '___Version___' -v '1.0' $_obj_geo1_occlusion_attribblur1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_attribblur1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_attribblur1

# Node $_obj_geo1_occlusion_attribwrangle2 (Sop/attribwrangle)
set _obj_geo1_occlusion_attribwrangle2 = `run("opadd -e -n -v attribwrangle attribwrangle2")`
oplocate -x `$arg2 + -0.39714899999999997` -y `$arg3 + 0.0074091699999999996` $_obj_geo1_occlusion_attribwrangle2
opparm $_obj_geo1_occlusion_attribwrangle2  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_occlusion_attribwrangle2 snippet ( '@Cd = @occlusion;\n\n' )
opset -d on -r on -h off -f off -y off -t on -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_occlusion_attribwrangle2
opexprlanguage -s hscript $_obj_geo1_occlusion_attribwrangle2
opuserdata -n '___Version___' -v '' $_obj_geo1_occlusion_attribwrangle2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_attribwrangle2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_attribwrangle2
opcf ..
opcf $_obj_geo1_occlusion

# Node $_obj_geo1_occlusion_normal1 (Sop/normal)
set _obj_geo1_occlusion_normal1 = `run("opadd -e -n -v normal normal1")`
oplocate -x `$arg2 + -0.600993` -y `$arg3 + 3.74858` $_obj_geo1_occlusion_normal1
opparm -V 18.5.408 $_obj_geo1_occlusion_normal1 cuspangle ( 180 ) method ( 2 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_occlusion_normal1
opexprlanguage -s hscript $_obj_geo1_occlusion_normal1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_occlusion_normal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_occlusion_normal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_occlusion_normal1
oporder -e normal1 attribwrangle1 attribblur1 attribwrangle2 
opcf ..
opset -p on $_obj_geo1_occlusion
opcf $arg1

# Node $_obj_geo1_switch_height (Sop/switch)
set _obj_geo1_switch_height = `run("opadd -e -n -v switch switch_height")`
oplocate -x `$arg2 + 0.27340300000000006` -y `$arg3 + 43.832599999999999` $_obj_geo1_switch_height
chblockbegin
chadd -t 0 0 $_obj_geo1_switch_height input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enableheight")' $_obj_geo1_switch_height/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch_height
opexprlanguage -s hscript $_obj_geo1_switch_height
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch_height
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch_height
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch_height
opset -p on $_obj_geo1_switch_height
opcf $arg1

# Node $_obj_geo1_object_control1 (Sop/attribvop)
set _obj_geo1_object_control1 = `run("opadd -e -n -v attribvop object_control1")`
oplocate -x `$arg2 + 5.6034030000000001` -y `$arg3 + 49.906599999999997` $_obj_geo1_object_control1
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "minobject"         label   "min %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "maxobject"         label   "max %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "objectremap"         label   "objectremap"         type    ramp_flt         default { "2" }         range   { 1! 10 }         parmtag { "parmvop" "1" }         parmtag { "rampbasis_var" "objectremap_the_basis_strings" }         parmtag { "rampbasisdefault" "linear" }         parmtag { "rampfloatdefault" "1pos ( 0 ) 1value ( 0 ) 1interp ( linear ) 2pos ( 1 ) 2value ( 1 ) 2interp ( linear )" }         parmtag { "rampkeys_var" "objectremap_the_key_positions" }         parmtag { "rampshowcontrolsdefault" "1" }         parmtag { "rampvalues_var" "objectremap_the_key_values" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switchmode"         label   "switch mode"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_object_control1
opmultiparm $_obj_geo1_object_control1 'attributepscale#pos' '../attributepscale#pos' 'attributepscale#value' '../attributepscale#value' 'attributepscale#interp' '../attributepscale#interp' 'densityattribtue#pos' '../densityattribtue#pos' 'densityattribtue#value' '../densityattribtue#value' 'densityattribtue#interp' '../densityattribtue#interp' 'densityobject#pos' '../densityobjectramp#pos' 'densityobject#value' '../densityobjectramp#value' 'densityobject#interp' '../densityobjectramp#interp' 'objectscale#pos' '../objectscaleramp#pos' 'objectscale#value' '../objectscaleramp#value' 'objectscale#interp' '../objectscaleramp#interp' 'objectIDramp#pos' '../objectIDramp#pos' 'objectIDramp#value' '../objectIDramp#value' 'objectIDramp#interp' '../objectIDramp#interp' 'objectremap#pos' '../objectremap#pos' 'objectremap#value' '../objectremap#value' 'objectremap#interp' '../objectremap#interp'
opparm $_obj_geo1_object_control1  bindings ( 0 ) groupbindings ( 0 ) objectremap ( 2 )
chblockbegin
chadd -t 0 0 $_obj_geo1_object_control1 minobject
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../minobject")/100' $_obj_geo1_object_control1/minobject
chadd -t 0 0 $_obj_geo1_object_control1 maxobject
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../maxobject")/100' $_obj_geo1_object_control1/maxobject
chadd -t 0 0 $_obj_geo1_object_control1 objectremap
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../objectremap")' $_obj_geo1_object_control1/objectremap
chadd -t 0 0 $_obj_geo1_object_control1 objectremap1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../objectremap1pos")' $_obj_geo1_object_control1/objectremap1pos
chadd -t 0 0 $_obj_geo1_object_control1 objectremap1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../objectremap1value")' $_obj_geo1_object_control1/objectremap1value
chadd -t 0 0 $_obj_geo1_object_control1 objectremap1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../objectremap1interp")' $_obj_geo1_object_control1/objectremap1interp
chadd -t 0 0 $_obj_geo1_object_control1 switchmode
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../objectmode")' $_obj_geo1_object_control1/switchmode
chadd -t 0 0 $_obj_geo1_object_control1 objectremap2pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../objectremap2pos")' $_obj_geo1_object_control1/objectremap2pos
chadd -t 0 0 $_obj_geo1_object_control1 objectremap2value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../objectremap2value")' $_obj_geo1_object_control1/objectremap2value
chadd -t 0 0 $_obj_geo1_object_control1 objectremap2interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../objectremap2interp")' $_obj_geo1_object_control1/objectremap2interp
chblockend
opparm -V 18.5.408 $_obj_geo1_object_control1 minobject ( minobject ) maxobject ( maxobject ) objectremap ( objectremap ) objectremap1pos ( objectremap1pos ) objectremap1value ( objectremap1value ) objectremap1interp ( objectremap1interp ) switchmode ( switchmode ) objectremap2pos ( objectremap2pos ) objectremap2value ( objectremap2value ) objectremap2interp ( objectremap2interp )
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_geo1_object_control1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_object_control1
opexprlanguage -s hscript $_obj_geo1_object_control1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1
opcf $_obj_geo1_object_control1

# Node $_obj_geo1_object_control1_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_object_control1_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 33.438899999999997` -y `$arg3 + 0.0985346` $_obj_geo1_object_control1_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_object_control1_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_object_control1_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_geometryvopoutput1

# Node $_obj_geo1_object_control1_bind2 (Vop/bind)
set _obj_geo1_object_control1_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 28.935600000000001` -y `$arg3 + -0.65146499999999996` $_obj_geo1_object_control1_bind2
opparm -V 18.5.408 $_obj_geo1_object_control1_bind2 parmname ( density ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_bind2
opexprlanguage -s hscript $_obj_geo1_object_control1_bind2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_bind2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_bind2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_bind2

# Node $_obj_geo1_object_control1_bind7 (Vop/bind)
set _obj_geo1_object_control1_bind7 = `run("opadd -e -n -v bind bind7")`
oplocate -x `$arg2 + 4.53592` -y `$arg3 + 0.534918` $_obj_geo1_object_control1_bind7
opparm -V 18.5.408 $_obj_geo1_object_control1_bind7 parmname ( object ) parmtype ( vector ) vectordef ( 1 1 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_bind7
opexprlanguage -s hscript $_obj_geo1_object_control1_bind7
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_bind7
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_bind7
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_bind7

# Node $_obj_geo1_object_control1_multiply3 (Vop/multiply)
set _obj_geo1_object_control1_multiply3 = `run("opadd -e -n -v multiply multiply3")`
oplocate -x `$arg2 + 22.713999999999999` -y `$arg3 + 5.1751699999999996` $_obj_geo1_object_control1_multiply3
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_multiply3
opexprlanguage -s hscript $_obj_geo1_object_control1_multiply3
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_multiply3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_multiply3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_multiply3

# Node $_obj_geo1_object_control1_fit5 (Vop/fit)
set _obj_geo1_object_control1_fit5 = `run("opadd -e -n -v fit fit5")`
oplocate -x `$arg2 + 17.805599999999998` -y `$arg3 + 2.18384` $_obj_geo1_object_control1_fit5
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_fit5
opexprlanguage -s hscript $_obj_geo1_object_control1_fit5
opuserdata -n '___Version___' -v '' $_obj_geo1_object_control1_fit5
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_fit5
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_fit5

# Node $_obj_geo1_object_control1_destmin2 (Vop/parameter)
set _obj_geo1_object_control1_destmin2 = `run("opadd -e -n -v parameter destmin2")`
oplocate -x `$arg2 + 15.5274` -y `$arg3 + -0.634629` $_obj_geo1_object_control1_destmin2
opparm -V 18.5.408 $_obj_geo1_object_control1_destmin2 parmname ( minobject ) parmlabel ( 'min %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_destmin2
opexprlanguage -s hscript $_obj_geo1_object_control1_destmin2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_destmin2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_destmin2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_destmin2

# Node $_obj_geo1_object_control1_destmax4 (Vop/parameter)
set _obj_geo1_object_control1_destmax4 = `run("opadd -e -n -v parameter destmax4")`
oplocate -x `$arg2 + 15.5274` -y `$arg3 + -2.3748100000000001` $_obj_geo1_object_control1_destmax4
opparm -V 18.5.408 $_obj_geo1_object_control1_destmax4 parmname ( maxobject ) parmlabel ( 'max %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_destmax4
opexprlanguage -s hscript $_obj_geo1_object_control1_destmax4
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_destmax4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_destmax4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_destmax4

# Node $_obj_geo1_object_control1_bind1 (Vop/bind)
set _obj_geo1_object_control1_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 9.9133800000000001` -y `$arg3 + 4.4640500000000003` $_obj_geo1_object_control1_bind1
opparm -V 18.5.408 $_obj_geo1_object_control1_bind1 parmname ( density ) exportcontext ( cvex )
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_bind1
opexprlanguage -s hscript $_obj_geo1_object_control1_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_bind1

# Node $_obj_geo1_object_control1_vectofloat1 (Vop/vectofloat)
set _obj_geo1_object_control1_vectofloat1 = `run("opadd -e -n -v vectofloat vectofloat1")`
oplocate -x `$arg2 + 8.4174299999999995` -y `$arg3 + 0.60991799999999996` $_obj_geo1_object_control1_vectofloat1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_vectofloat1
opexprlanguage -s hscript $_obj_geo1_object_control1_vectofloat1
opuserdata -n '___Version___' -v '' $_obj_geo1_object_control1_vectofloat1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_vectofloat1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_vectofloat1

# Node $_obj_geo1_object_control1_bind8 (Vop/bind)
set _obj_geo1_object_control1_bind8 = `run("opadd -e -n -v bind bind8")`
oplocate -x `$arg2 + 26.787600000000001` -y `$arg3 + 1.4433499999999999` $_obj_geo1_object_control1_bind8
opparm -V 18.5.408 $_obj_geo1_object_control1_bind8 parmname ( objectA ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_bind8
opexprlanguage -s hscript $_obj_geo1_object_control1_bind8
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_bind8
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_bind8
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_bind8

# Node $_obj_geo1_object_control1_ramp1 (Vop/rampparm)
set _obj_geo1_object_control1_ramp1 = `run("opadd -e -n -v rampparm ramp1")`
oplocate -x `$arg2 + 14.2494` -y `$arg3 + 2.51275` $_obj_geo1_object_control1_ramp1
opparm $_obj_geo1_object_control1_ramp1  rampcolordefault ( 2 ) rampfloatdefault ( 2 )
opparm -V 18.5.408 $_obj_geo1_object_control1_ramp1 parmname ( objectremap ) parmlabel ( objectremap ) ramptype ( flt ) rampcolordefault2pos ( 1 ) rampcolordefault2c ( 1 1 1 ) rampfloatdefault2pos ( 1 ) rampfloatdefault2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_ramp1
opexprlanguage -s hscript $_obj_geo1_object_control1_ramp1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_ramp1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_ramp1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_ramp1

# Node $_obj_geo1_object_control1_add1 (Vop/add)
set _obj_geo1_object_control1_add1 = `run("opadd -e -n -v add add1")`
oplocate -x `$arg2 + 21.2593` -y `$arg3 + -0.20146500000000001` $_obj_geo1_object_control1_add1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_add1
opexprlanguage -s hscript $_obj_geo1_object_control1_add1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_add1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_add1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_add1

# Node $_obj_geo1_object_control1_switch1 (Vop/switch)
set _obj_geo1_object_control1_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 25.299099999999999` -y `$arg3 + -0.20146500000000001` $_obj_geo1_object_control1_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_switch1
opexprlanguage -s hscript $_obj_geo1_object_control1_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_switch1

# Node $_obj_geo1_object_control1_parm1 (Vop/parameter)
set _obj_geo1_object_control1_parm1 = `run("opadd -e -n -v parameter parm1")`
oplocate -x `$arg2 + 22.655000000000001` -y `$arg3 + -4.37981` $_obj_geo1_object_control1_parm1
opparm -V 18.5.408 $_obj_geo1_object_control1_parm1 parmname ( switchmode ) parmlabel ( 'switch mode' ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_parm1
opexprlanguage -s hscript $_obj_geo1_object_control1_parm1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_parm1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_parm1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_parm1

# Node $_obj_geo1_object_control1_subtract1 (Vop/subtract)
set _obj_geo1_object_control1_subtract1 = `run("opadd -e -n -v subtract subtract1")`
oplocate -x `$arg2 + 20.390599999999999` -y `$arg3 + -2.3748100000000001` $_obj_geo1_object_control1_subtract1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_object_control1_subtract1
opexprlanguage -s hscript $_obj_geo1_object_control1_subtract1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_object_control1_subtract1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_control1_subtract1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_control1_subtract1
opcf ..
opcf $_obj_geo1_object_control1
oporder -e geometryvopoutput1 bind2 bind7 multiply3 fit5 destmin2 destmax4 bind1 vectofloat1 bind8 ramp1 add1 switch1 parm1 subtract1 
opcf ..
opset -p on $_obj_geo1_object_control1
opcf $arg1

# Node $_obj_geo1_object_density2 (Sop/attribwrangle)
set _obj_geo1_object_density2 = `run("opadd -e -n -v attribwrangle object_density2")`
oplocate -x `$arg2 + 29.300663` -y `$arg3 + 9.8354999999999961` $_obj_geo1_object_density2
opparm $_obj_geo1_object_density2  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_object_density2 snippet ( '@Cd = @curvatureA;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_object_density2
opexprlanguage -s hscript $_obj_geo1_object_density2
opuserdata -n '___Version___' -v '' $_obj_geo1_object_density2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_density2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_density2
opset -p on $_obj_geo1_object_density2
opcf $arg1

# Node $_obj_geo1_switch2 (Sop/switch)
set _obj_geo1_switch2 = `run("opadd -e -n -v switch switch2")`
oplocate -x `$arg2 + -1.2742` -y `$arg3 + 0.94149999999999068` $_obj_geo1_switch2
chblockbegin
chadd -t 0 0 $_obj_geo1_switch2 input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../visualizeCd")' $_obj_geo1_switch2/input
chblockend
opparm -V 18.5.408 $_obj_geo1_switch2 input ( input )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch2
opexprlanguage -s hscript $_obj_geo1_switch2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch2
opset -p on $_obj_geo1_switch2
opcf $arg1

# Node $_obj_geo1_switch_attribute2 (Sop/switch)
set _obj_geo1_switch_attribute2 = `run("opadd -e -n -v switch switch_attribute2")`
oplocate -x `$arg2 + -0.63600000000000001` -y `$arg3 + 57.877899999999997` $_obj_geo1_switch_attribute2
chblockbegin
chadd -t 0 0 $_obj_geo1_switch_attribute2 input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enableattribute2")' $_obj_geo1_switch_attribute2/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch_attribute2
opexprlanguage -s hscript $_obj_geo1_switch_attribute2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch_attribute2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch_attribute2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch_attribute2
opset -p on $_obj_geo1_switch_attribute2
opcf $arg1

# Node $_obj_geo1_switch_attribute1 (Sop/switch)
set _obj_geo1_switch_attribute1 = `run("opadd -e -n -v switch switch_attribute1")`
oplocate -x `$arg2 + -0.22549999999999992` -y `$arg3 + 67.993840000000006` $_obj_geo1_switch_attribute1
chblockbegin
chadd -t 0 0 $_obj_geo1_switch_attribute1 input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enableattribute1")' $_obj_geo1_switch_attribute1/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch_attribute1
opexprlanguage -s hscript $_obj_geo1_switch_attribute1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch_attribute1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch_attribute1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch_attribute1
opset -p on $_obj_geo1_switch_attribute1
opcf $arg1

# Node $_obj_geo1_pointvop1 (Sop/attribvop)
set _obj_geo1_pointvop1 = `run("opadd -e -n -v attribvop pointvop1")`
oplocate -x `$arg2 + 5.0387029999999999` -y `$arg3 + 52.308199999999999` $_obj_geo1_pointvop1
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "onlydistance"         label   "onlydistance"         type    toggle         default { "0" }         parmtag { "script_callback_language" "python" }     } ' $_obj_geo1_pointvop1
opparm $_obj_geo1_pointvop1  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 0 0 $_obj_geo1_pointvop1 onlydistance
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../onlydistance")' $_obj_geo1_pointvop1/onlydistance
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_pointvop1
opexprlanguage -s hscript $_obj_geo1_pointvop1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_pointvop1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop1
opcf $_obj_geo1_pointvop1

# Node $_obj_geo1_pointvop1_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_geo1_pointvop1_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + -0.93464100000000006` -y `$arg3 + 2.06033` $_obj_geo1_pointvop1_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop1_geometryvopglobal1
opexprlanguage -s hscript $_obj_geo1_pointvop1_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_geo1_pointvop1_geometryvopglobal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop1_geometryvopglobal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop1_geometryvopglobal1

# Node $_obj_geo1_pointvop1_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_pointvop1_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 14.0006` -y `$arg3 + 1.98272` $_obj_geo1_pointvop1_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop1_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_pointvop1_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_pointvop1_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop1_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop1_geometryvopoutput1

# Node $_obj_geo1_pointvop1_bind1 (Vop/bind)
set _obj_geo1_pointvop1_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + -0.44924900000000001` -y `$arg3 + 4.3669700000000002` $_obj_geo1_pointvop1_bind1
opparm -V 18.5.408 $_obj_geo1_pointvop1_bind1 parmname ( object ) parmtype ( vector ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop1_bind1
opexprlanguage -s hscript $_obj_geo1_pointvop1_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_pointvop1_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop1_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop1_bind1

# Node $_obj_geo1_pointvop1_max1 (Vop/max)
set _obj_geo1_pointvop1_max1 = `run("opadd -e -n -v max max1")`
oplocate -x `$arg2 + 5.5507499999999999` -y `$arg3 + 2.3905599999999998` $_obj_geo1_pointvop1_max1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop1_max1
opexprlanguage -s hscript $_obj_geo1_pointvop1_max1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_pointvop1_max1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop1_max1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop1_max1

# Node $_obj_geo1_pointvop1_vectofloat1 (Vop/vectofloat)
set _obj_geo1_pointvop1_vectofloat1 = `run("opadd -e -n -v vectofloat vectofloat1")`
oplocate -x `$arg2 + 1.6350899999999999` -y `$arg3 + 1.0002800000000001` $_obj_geo1_pointvop1_vectofloat1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop1_vectofloat1
opexprlanguage -s hscript $_obj_geo1_pointvop1_vectofloat1
opuserdata -n '___Version___' -v '' $_obj_geo1_pointvop1_vectofloat1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop1_vectofloat1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop1_vectofloat1

# Node $_obj_geo1_pointvop1_switch1 (Vop/switch)
set _obj_geo1_pointvop1_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 2.9919600000000002` -y `$arg3 + 4.2005600000000003` $_obj_geo1_pointvop1_switch1
chblockbegin
chadd -t 0 0 $_obj_geo1_pointvop1_switch1 switcher
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../onlydistance")' $_obj_geo1_pointvop1_switch1/switcher
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop1_switch1
opexprlanguage -s hscript $_obj_geo1_pointvop1_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_pointvop1_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop1_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop1_switch1

# Node $_obj_geo1_pointvop1_const1 (Vop/constant)
set _obj_geo1_pointvop1_const1 = `run("opadd -e -n -v constant const1")`
oplocate -x `$arg2 + 0.749533` -y `$arg3 + 3.07056` $_obj_geo1_pointvop1_const1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop1_const1
opexprlanguage -s hscript $_obj_geo1_pointvop1_const1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_pointvop1_const1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop1_const1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop1_const1

# Node $_obj_geo1_pointvop1_bind2 (Vop/bind)
set _obj_geo1_pointvop1_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 9.7071900000000007` -y `$arg3 + 1.86334` $_obj_geo1_pointvop1_bind2
opparm -V 18.5.408 $_obj_geo1_pointvop1_bind2 parmname ( object ) parmtype ( vector ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop1_bind2
opexprlanguage -s hscript $_obj_geo1_pointvop1_bind2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_pointvop1_bind2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop1_bind2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop1_bind2

# Node $_obj_geo1_pointvop1_floattovec1 (Vop/floattovec)
set _obj_geo1_pointvop1_floattovec1 = `run("opadd -e -n -v floattovec floattovec1")`
oplocate -x `$arg2 + 8.8600600000000007` -y `$arg3 + 0.24313199999999999` $_obj_geo1_pointvop1_floattovec1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_pointvop1_floattovec1
opexprlanguage -s hscript $_obj_geo1_pointvop1_floattovec1
opuserdata -n '___Version___' -v '' $_obj_geo1_pointvop1_floattovec1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_pointvop1_floattovec1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_pointvop1_floattovec1
opcf ..
opcf $_obj_geo1_pointvop1
oporder -e geometryvopglobal1 geometryvopoutput1 bind1 max1 vectofloat1 switch1 const1 bind2 floattovec1 
opcf ..
opset -p on $_obj_geo1_pointvop1
opcf $arg1

# Node $_obj_geo1_attribblur1 (Sop/attribblur)
set _obj_geo1_attribblur1 = `run("opadd -e -n -v attribblur attribblur1")`
oplocate -x `$arg2 + 5.3162029999999998` -y `$arg3 + 36.115000000000002` $_obj_geo1_attribblur1
chblockbegin
chadd -t 0 0 $_obj_geo1_attribblur1 iterations
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../iterations")' $_obj_geo1_attribblur1/iterations
chadd -t 0 0 $_obj_geo1_attribblur1 mode
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../mode")' $_obj_geo1_attribblur1/mode
chadd -t 0 0 $_obj_geo1_attribblur1 stepsize
chkey -t 0 -v 0.5 -m 0 -a 0 -A 0 -T a  -F 'ch("../stepsize")' $_obj_geo1_attribblur1/stepsize
chblockend
opparm -V 1.0 $_obj_geo1_attribblur1 attributes ( curvature ) iterations ( iterations ) mode ( mode ) stepsize ( stepsize )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_attribblur1
opexprlanguage -s hscript $_obj_geo1_attribblur1
opuserdata -n '___Version___' -v '1.0' $_obj_geo1_attribblur1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribblur1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribblur1
opset -p on $_obj_geo1_attribblur1
opcf $arg1

# Node $_obj_geo1_attribute1_control1 (Sop/attribvop)
set _obj_geo1_attribute1_control1 = `run("opadd -e -n -v attribvop attribute1_control1")`
oplocate -x `$arg2 + 4.715503` -y `$arg3 + 70.429640000000006` $_obj_geo1_attribute1_control1
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "attribute1remap"         label   "attribute remap"         type    ramp_flt         default { "2" }         range   { 1! 10 }         parmtag { "parmvop" "1" }         parmtag { "rampbasis_var" "attribute1remap_the_basis_strings" }         parmtag { "rampbasisdefault" "linear" }         parmtag { "rampfloatdefault" "1pos ( 0 ) 1value ( 0 ) 1interp ( linear ) 2pos ( 1 ) 2value ( 1 ) 2interp ( linear )" }         parmtag { "rampkeys_var" "attribute1remap_the_key_positions" }         parmtag { "rampshowcontrolsdefault" "1" }         parmtag { "rampvalues_var" "attribute1remap_the_key_values" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "attribute1min"         label   "min %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "attribute1max"         label   "max %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "attribtue"         label   "attribute"         type    string         default { "" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "switchmode"         label   "switch mode"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_attribute1_control1
opmultiparm $_obj_geo1_attribute1_control1 'attributepscale#pos' '../attributepscale#pos' 'attributepscale#value' '../attributepscale#value' 'attributepscale#interp' '../attributepscale#interp' 'densityattribtue#pos' '../densityattribtue#pos' 'densityattribtue#value' '../densityattribtue#value' 'densityattribtue#interp' '../densityattribtue#interp' 'attribute1IDramp#pos' '../attribute1IDramp#pos' 'attribute1IDramp#value' '../attribute1IDramp#value' 'attribute1IDramp#interp' '../attribute1IDramp#interp' 'attribute1remap#pos' '../attribute1remap#pos' 'attribute1remap#value' '../attribute1remap#value' 'attribute1remap#interp' '../attribute1remap#interp'
opparm $_obj_geo1_attribute1_control1  bindings ( 0 ) groupbindings ( 0 ) attribute1remap ( 2 )
chblockbegin
chadd -t 0 0 $_obj_geo1_attribute1_control1 attribute1remap
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute1remap")' $_obj_geo1_attribute1_control1/attribute1remap
chadd -t 0 0 $_obj_geo1_attribute1_control1 attribute1remap1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute1remap1pos")' $_obj_geo1_attribute1_control1/attribute1remap1pos
chadd -t 0 0 $_obj_geo1_attribute1_control1 attribute1remap1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute1remap1value")' $_obj_geo1_attribute1_control1/attribute1remap1value
chadd -t 0 0 $_obj_geo1_attribute1_control1 attribute1remap1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute1remap1interp")' $_obj_geo1_attribute1_control1/attribute1remap1interp
chadd -t 0 0 $_obj_geo1_attribute1_control1 attribute1min
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute1min")/100' $_obj_geo1_attribute1_control1/attribute1min
chadd -t 0 0 $_obj_geo1_attribute1_control1 attribute1max
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute1max")/100' $_obj_geo1_attribute1_control1/attribute1max
chadd -t 0 0 $_obj_geo1_attribute1_control1 switchmode
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute1mode")' $_obj_geo1_attribute1_control1/switchmode
chadd -t 0 0 $_obj_geo1_attribute1_control1 attribute1remap2pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute1remap2pos")' $_obj_geo1_attribute1_control1/attribute1remap2pos
chadd -t 0 0 $_obj_geo1_attribute1_control1 attribute1remap2value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute1remap2value")' $_obj_geo1_attribute1_control1/attribute1remap2value
chadd -t 0 0 $_obj_geo1_attribute1_control1 attribute1remap2interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../attribute1remap2interp")' $_obj_geo1_attribute1_control1/attribute1remap2interp
chblockend
opparm -V 18.5.408 $_obj_geo1_attribute1_control1 attribute1remap ( attribute1remap ) attribute1remap1pos ( attribute1remap1pos ) attribute1remap1value ( attribute1remap1value ) attribute1remap1interp ( attribute1remap1interp ) attribute1min ( attribute1min ) attribute1max ( attribute1max ) attribtue ( '`chs("../attribute1name")`' ) switchmode ( switchmode ) attribute1remap2pos ( attribute1remap2pos ) attribute1remap2value ( attribute1remap2value ) attribute1remap2interp ( attribute1remap2interp )
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_geo1_attribute1_control1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_attribute1_control1
opexprlanguage -s hscript $_obj_geo1_attribute1_control1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1
opcf $_obj_geo1_attribute1_control1

# Node $_obj_geo1_attribute1_control1_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_attribute1_control1_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 37.262300000000003` -y `$arg3 + 0.57428400000000002` $_obj_geo1_attribute1_control1_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute1_control1_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_geometryvopoutput1

# Node $_obj_geo1_attribute1_control1_bind2 (Vop/bind)
set _obj_geo1_attribute1_control1_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 32.503799999999998` -y `$arg3 + 0.57428400000000002` $_obj_geo1_attribute1_control1_bind2
opparm -V 18.5.408 $_obj_geo1_attribute1_control1_bind2 parmname ( density ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_bind2
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_bind2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_bind2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_bind2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_bind2

# Node $_obj_geo1_attribute1_control1_bind7 (Vop/bind)
set _obj_geo1_attribute1_control1_bind7 = `run("opadd -e -n -v bind bind7")`
oplocate -x `$arg2 + 4.4740399999999996` -y `$arg3 + -0.45509500000000003` $_obj_geo1_attribute1_control1_bind7
opparm -V 18.5.408 $_obj_geo1_attribute1_control1_bind7 parmname ( '`chs("../attribtue")`' ) vectordef ( 1 1 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_bind7
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_bind7
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_bind7
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_bind7
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_bind7

# Node $_obj_geo1_attribute1_control1_vectofloat2 (Vop/vectofloat)
set _obj_geo1_attribute1_control1_vectofloat2 = `run("opadd -e -n -v vectofloat vectofloat2")`
oplocate -x `$arg2 + 8.0678699999999992` -y `$arg3 + -0.080095` $_obj_geo1_attribute1_control1_vectofloat2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_vectofloat2
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_vectofloat2
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute1_control1_vectofloat2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_vectofloat2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_vectofloat2

# Node $_obj_geo1_attribute1_control1_ramp2 (Vop/rampparm)
set _obj_geo1_attribute1_control1_ramp2 = `run("opadd -e -n -v rampparm ramp2")`
oplocate -x `$arg2 + 14.993` -y `$arg3 + 2.7192400000000001` $_obj_geo1_attribute1_control1_ramp2
opparm $_obj_geo1_attribute1_control1_ramp2  rampcolordefault ( 2 ) rampfloatdefault ( 2 )
opparm -V 18.5.408 $_obj_geo1_attribute1_control1_ramp2 parmname ( attribute1remap ) parmlabel ( 'attribute remap' ) ramptype ( flt ) rampcolordefault2pos ( 1 ) rampcolordefault2c ( 1 1 1 ) rampfloatdefault2pos ( 1 ) rampfloatdefault2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_ramp2
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_ramp2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_ramp2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_ramp2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_ramp2

# Node $_obj_geo1_attribute1_control1_multiply3 (Vop/multiply)
set _obj_geo1_attribute1_control1_multiply3 = `run("opadd -e -n -v multiply multiply3")`
oplocate -x `$arg2 + 22.713999999999999` -y `$arg3 + 5.1751699999999996` $_obj_geo1_attribute1_control1_multiply3
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_multiply3
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_multiply3
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_multiply3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_multiply3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_multiply3

# Node $_obj_geo1_attribute1_control1_fit5 (Vop/fit)
set _obj_geo1_attribute1_control1_fit5 = `run("opadd -e -n -v fit fit5")`
oplocate -x `$arg2 + 17.805599999999998` -y `$arg3 + 2.18384` $_obj_geo1_attribute1_control1_fit5
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_fit5
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_fit5
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute1_control1_fit5
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_fit5
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_fit5

# Node $_obj_geo1_attribute1_control1_destmin2 (Vop/parameter)
set _obj_geo1_attribute1_control1_destmin2 = `run("opadd -e -n -v parameter destmin2")`
oplocate -x `$arg2 + 15.527799999999999` -y `$arg3 + -0.166161` $_obj_geo1_attribute1_control1_destmin2
opparm -V 18.5.408 $_obj_geo1_attribute1_control1_destmin2 parmname ( attribute1min ) parmlabel ( 'min %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_destmin2
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_destmin2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_destmin2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_destmin2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_destmin2

# Node $_obj_geo1_attribute1_control1_destmax4 (Vop/parameter)
set _obj_geo1_attribute1_control1_destmax4 = `run("opadd -e -n -v parameter destmax4")`
oplocate -x `$arg2 + 15.3329` -y `$arg3 + -1.93791` $_obj_geo1_attribute1_control1_destmax4
opparm -V 18.5.408 $_obj_geo1_attribute1_control1_destmax4 parmname ( attribute1max ) parmlabel ( 'max %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_destmax4
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_destmax4
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_destmax4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_destmax4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_destmax4

# Node $_obj_geo1_attribute1_control1_bind1 (Vop/bind)
set _obj_geo1_attribute1_control1_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 10.171200000000001` -y `$arg3 + 5.7273500000000004` $_obj_geo1_attribute1_control1_bind1
opparm -V 18.5.408 $_obj_geo1_attribute1_control1_bind1 parmname ( density ) exportcontext ( cvex )
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_bind1
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_bind1

# Node $_obj_geo1_attribute1_control1_bind4 (Vop/bind)
set _obj_geo1_attribute1_control1_bind4 = `run("opadd -e -n -v bind bind4")`
oplocate -x `$arg2 + 23.5806` -y `$arg3 + 1.73384` $_obj_geo1_attribute1_control1_bind4
opparm -V 18.5.408 $_obj_geo1_attribute1_control1_bind4 parmname ( attribute1A ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_bind4
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_bind4
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_bind4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_bind4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_bind4

# Node $_obj_geo1_attribute1_control1_add1 (Vop/add)
set _obj_geo1_attribute1_control1_add1 = `run("opadd -e -n -v add add1")`
oplocate -x `$arg2 + 23.990400000000001` -y `$arg3 + -0.016160999999999998` $_obj_geo1_attribute1_control1_add1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_add1
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_add1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_add1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_add1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_add1

# Node $_obj_geo1_attribute1_control1_switch1 (Vop/switch)
set _obj_geo1_attribute1_control1_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 29.2378` -y `$arg3 + 0.57428400000000002` $_obj_geo1_attribute1_control1_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_switch1
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_switch1

# Node $_obj_geo1_attribute1_control1_parm1 (Vop/parameter)
set _obj_geo1_attribute1_control1_parm1 = `run("opadd -e -n -v parameter parm1")`
oplocate -x `$arg2 + 26.593699999999998` -y `$arg3 + -3.60406` $_obj_geo1_attribute1_control1_parm1
opparm -V 18.5.408 $_obj_geo1_attribute1_control1_parm1 parmname ( switchmode ) parmlabel ( 'switch mode' ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_parm1
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_parm1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_parm1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_parm1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_parm1

# Node $_obj_geo1_attribute1_control1_subtract1 (Vop/subtract)
set _obj_geo1_attribute1_control1_subtract1 = `run("opadd -e -n -v subtract subtract1")`
oplocate -x `$arg2 + 23.774999999999999` -y `$arg3 + -1.65055` $_obj_geo1_attribute1_control1_subtract1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute1_control1_subtract1
opexprlanguage -s hscript $_obj_geo1_attribute1_control1_subtract1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute1_control1_subtract1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute1_control1_subtract1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute1_control1_subtract1
opcf ..
opcf $_obj_geo1_attribute1_control1
oporder -e geometryvopoutput1 bind2 bind7 vectofloat2 ramp2 multiply3 fit5 destmin2 destmax4 bind1 bind4 add1 switch1 parm1 subtract1 
opcf ..
opset -p on $_obj_geo1_attribute1_control1
opcf $arg1

# Node $_obj_geo1_attribcopy1 (Sop/attribcopy)
set _obj_geo1_attribcopy1 = `run("opadd -e -n -v attribcopy attribcopy1")`
oplocate -x `$arg2 + -2.925697` -y `$arg3 + 2.6235999999999962` $_obj_geo1_attribcopy1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_attribcopy1
opexprlanguage -s hscript $_obj_geo1_attribcopy1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribcopy1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribcopy1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribcopy1
opset -p on $_obj_geo1_attribcopy1
opcf $arg1

# Node $_obj_geo1_attribtransfer1 (Sop/attribtransfer)
set _obj_geo1_attribtransfer1 = `run("opadd -e -n -v attribtransfer attribtransfer1")`
oplocate -x `$arg2 + 5.1674030000000002` -y `$arg3 + 53.186199999999999` $_obj_geo1_attribtransfer1
chblockbegin
chadd -t 0 0 $_obj_geo1_attribtransfer1 thresholddist
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../thresholddist")' $_obj_geo1_attribtransfer1/thresholddist
chadd -t 0 0 $_obj_geo1_attribtransfer1 blendwidth
chkey -t 0 -v 50 -m 0 -a 0 -A 0 -T a  -F 'ch("../blendwidth")' $_obj_geo1_attribtransfer1/blendwidth
chblockend
opparm -V 18.5.408 $_obj_geo1_attribtransfer1 pointattriblist ( Cd ) thresholddist ( thresholddist ) blendwidth ( blendwidth )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_attribtransfer1
opexprlanguage -s hscript $_obj_geo1_attribtransfer1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribtransfer1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribtransfer1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribtransfer1
opset -p on $_obj_geo1_attribtransfer1
opcf $arg1

# Node $_obj_geo1_OUTPOUT (Sop/null)
set _obj_geo1_OUTPOUT = `run("opadd -e -n -v null OUTPOUT")`
oplocate -x `$arg2 + 0.0034000000000000696` -y `$arg3 + -1.12530000000001` $_obj_geo1_OUTPOUT
opset -d on -r on -h off -f off -y off -t on -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_OUTPOUT
opexprlanguage -s hscript $_obj_geo1_OUTPOUT
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_OUTPOUT
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_OUTPOUT
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_OUTPOUT
opset -p on $_obj_geo1_OUTPOUT
opcf $arg1

# Node $_obj_geo1_attribute_by_slope1 (Sop/attribvop)
set _obj_geo1_attribute_by_slope1 = `run("opadd -e -n -v attribvop attribute_by_slope1")`
oplocate -x `$arg2 + 2.3414030000000001` -y `$arg3 + 73.902739999999994` $_obj_geo1_attribute_by_slope1
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vex_inplace"         baseparm         label   "Compute Results In Place"         export  none     }     parm {         name    "vex_selectiongroup"         baseparm         label   "Output Selection Group"         export  none     }     parm {         name    "vex_precision"         baseparm         label   "VEX Precision"         export  none     }     parm {         name    "slopemin"         label   "slope min angle"         type    float         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "xn__slopemax_eia"         label   "slope max angle"         type    float         default { "90" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "minslope"         label   "min density "         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "maxslope"         label   "max density "         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "sloperemap"         label   "slope remap"         type    ramp_flt         default { "2" }         range   { 1! 10 }         parmtag { "parmvop" "1" }         parmtag { "rampbasis_var" "sloperemap_the_basis_strings" }         parmtag { "rampbasisdefault" "linear" }         parmtag { "rampfloatdefault" "1pos ( 0 ) 1value ( 0 ) 1interp ( linear ) 2pos ( 1 ) 2value ( 1 ) 2interp ( linear )" }         parmtag { "rampkeys_var" "sloperemap_the_key_positions" }         parmtag { "rampshowcontrolsdefault" "1" }         parmtag { "rampvalues_var" "sloperemap_the_key_values" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switchmode"         label   "switch mode"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_attribute_by_slope1
opmultiparm $_obj_geo1_attribute_by_slope1 'slopedensity#pos' '../slopedensityramp#pos' 'slopedensity#value' '../slopedensityramp#value' 'slopedensity#interp' '../slopedensityramp#interp' 'slopescale#pos' '../slopescaleramp#pos' 'slopescale#value' '../slopescaleramp#value' 'slopescale#interp' '../slopescaleramp#interp' 'slopeIDramp#pos' '../slopeIDramp#pos' 'slopeIDramp#value' '../slopeIDramp#value' 'slopeIDramp#interp' '../slopeIDramp#interp' 'sloperemap#pos' '../sloperemap#pos' 'sloperemap#value' '../sloperemap#value' 'sloperemap#interp' '../sloperemap#interp'
opparm $_obj_geo1_attribute_by_slope1  bindings ( 0 ) groupbindings ( 0 ) sloperemap ( 2 )
chblockbegin
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 slopemin
chkey -t 0 -v 40 -m 0 -a 0 -A 0 -T a  -F 'ch("../slopemin")' $_obj_geo1_attribute_by_slope1/slopemin
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 xn__slopemax_eia
chkey -t 0 -v 90 -m 0 -a 0 -A 0 -T a  -F 'ch("../xn__slopemax_eia")' $_obj_geo1_attribute_by_slope1/xn__slopemax_eia
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 minslope
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../minslope")/100' $_obj_geo1_attribute_by_slope1/minslope
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 maxslope
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../maxslope")/100' $_obj_geo1_attribute_by_slope1/maxslope
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 sloperemap
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../sloperemap")' $_obj_geo1_attribute_by_slope1/sloperemap
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 sloperemap1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../sloperemap1pos")' $_obj_geo1_attribute_by_slope1/sloperemap1pos
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 sloperemap1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../sloperemap1value")' $_obj_geo1_attribute_by_slope1/sloperemap1value
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 sloperemap1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../sloperemap1interp")' $_obj_geo1_attribute_by_slope1/sloperemap1interp
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 switchmode
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../slopemode")' $_obj_geo1_attribute_by_slope1/switchmode
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 sloperemap2pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../sloperemap2pos")' $_obj_geo1_attribute_by_slope1/sloperemap2pos
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 sloperemap2value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../sloperemap2value")' $_obj_geo1_attribute_by_slope1/sloperemap2value
chadd -t 0 0 $_obj_geo1_attribute_by_slope1 sloperemap2interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../sloperemap2interp")' $_obj_geo1_attribute_by_slope1/sloperemap2interp
chblockend
opparm -V 18.5.408 $_obj_geo1_attribute_by_slope1 slopemin ( slopemin ) xn__slopemax_eia ( xn__slopemax_eia ) minslope ( minslope ) maxslope ( maxslope ) sloperemap ( sloperemap ) sloperemap1pos ( sloperemap1pos ) sloperemap1value ( sloperemap1value ) sloperemap1interp ( sloperemap1interp ) switchmode ( switchmode ) sloperemap2pos ( sloperemap2pos ) sloperemap2value ( sloperemap2value ) sloperemap2interp ( sloperemap2interp )
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_geo1_attribute_by_slope1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_attribute_by_slope1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1
opcf $_obj_geo1_attribute_by_slope1

# Network Box $_obj_geo1_attribute_by_slope1___netbox1
set _obj_geo1_attribute_by_slope1___netbox1 = `run("nbadd -v __netbox1")`
nblocate -x `$arg2 + -8.30991` -y  `$arg3 + -0.67122` $_obj_geo1_attribute_by_slope1___netbox1
nbsize -w 15.539 -h 6.59632 $_obj_geo1_attribute_by_slope1___netbox1
nbset  -m off $_obj_geo1_attribute_by_slope1___netbox1
nbcolor -c 0.52 0.52 0.52 $_obj_geo1_attribute_by_slope1___netbox1

# Node $_obj_geo1_attribute_by_slope1_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_geo1_attribute_by_slope1_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + -12.7425` -y `$arg3 + 2.9497300000000002` $_obj_geo1_attribute_by_slope1_geometryvopglobal1
opcolor -c 0.80000001192092896 0.80000001192092896 0.80000001192092896 $_obj_geo1_attribute_by_slope1_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F off -c off -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_geometryvopglobal1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute_by_slope1_geometryvopglobal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_geometryvopglobal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_geometryvopglobal1

# Node $_obj_geo1_attribute_by_slope1_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_attribute_by_slope1_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 18.8612` -y `$arg3 + 1.4815700000000001` $_obj_geo1_attribute_by_slope1_geometryvopoutput1
opcolor -c 0.80000001192092896 0.80000001192092896 0.80000001192092896 $_obj_geo1_attribute_by_slope1_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c off -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute_by_slope1_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_geometryvopoutput1

# Node $_obj_geo1_attribute_by_slope1_dot1 (Vop/dot)
set _obj_geo1_attribute_by_slope1_dot1 = `run("opadd -e -n -v dot dot1")`
oplocate -x `$arg2 + -6.7406699999999997` -y `$arg3 + 1.6606099999999999` $_obj_geo1_attribute_by_slope1_dot1
opcolor -c 0.80000001192092896 0.80000001192092896 0.80000001192092896 $_obj_geo1_attribute_by_slope1_dot1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c off -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_dot1
nbop $_obj_geo1_attribute_by_slope1___netbox1 add $_obj_geo1_attribute_by_slope1_dot1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_dot1
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute_by_slope1_dot1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_dot1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_dot1

# Node $_obj_geo1_attribute_by_slope1_trig1 (Vop/trig)
set _obj_geo1_attribute_by_slope1_trig1 = `run("opadd -e -n -v trig trig1")`
oplocate -x `$arg2 + -4.2671900000000003` -y `$arg3 + 1.6874199999999999` $_obj_geo1_attribute_by_slope1_trig1
opparm $_obj_geo1_attribute_by_slope1_trig1 func ( vop_acos )
opcolor -c 0.80000001192092896 0.80000001192092896 0.80000001192092896 $_obj_geo1_attribute_by_slope1_trig1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c off -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_trig1
nbop $_obj_geo1_attribute_by_slope1___netbox1 add $_obj_geo1_attribute_by_slope1_trig1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_trig1
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute_by_slope1_trig1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_trig1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_trig1

# Node $_obj_geo1_attribute_by_slope1_fit4 (Vop/fit)
set _obj_geo1_attribute_by_slope1_fit4 = `run("opadd -e -n -v fit fit4")`
oplocate -x `$arg2 + -0.10027999999999999` -y `$arg3 + 1.8887799999999999` $_obj_geo1_attribute_by_slope1_fit4
opparm $_obj_geo1_attribute_by_slope1_fit4 srcmax ( 90 )
opcolor -c 0.80000001192092896 0.80000001192092896 0.80000001192092896 $_obj_geo1_attribute_by_slope1_fit4
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c off -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_fit4
nbop $_obj_geo1_attribute_by_slope1___netbox1 add $_obj_geo1_attribute_by_slope1_fit4
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_fit4
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute_by_slope1_fit4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_fit4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_fit4

# Node $_obj_geo1_attribute_by_slope1_radtodeg1 (Vop/radtodeg)
set _obj_geo1_attribute_by_slope1_radtodeg1 = `run("opadd -e -n -v radtodeg radtodeg1")`
oplocate -x `$arg2 + -2.21184` -y `$arg3 + 1.8887799999999999` $_obj_geo1_attribute_by_slope1_radtodeg1
opparm $_obj_geo1_attribute_by_slope1_radtodeg1 rad ( 1 ) rad_v ( 1 1 1 ) rad_p ( 1 1 1 ) rad_n ( 1 1 1 ) rad_c ( 1 1 1 ) rad_v4 ( 1 1 1 1 ) rad_uf ( 1 ) rad_uv ( 1 1 1 ) rad_up ( 1 1 1 ) rad_un ( 1 1 1 ) rad_uc ( 1 1 1 )
opcolor -c 0.80000001192092896 0.80000001192092896 0.80000001192092896 $_obj_geo1_attribute_by_slope1_radtodeg1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c off -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_radtodeg1
nbop $_obj_geo1_attribute_by_slope1___netbox1 add $_obj_geo1_attribute_by_slope1_radtodeg1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_radtodeg1
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute_by_slope1_radtodeg1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_radtodeg1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_radtodeg1

# Node $_obj_geo1_attribute_by_slope1_bind1 (Vop/bind)
set _obj_geo1_attribute_by_slope1_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 15.657400000000001` -y `$arg3 + -1.4330400000000001` $_obj_geo1_attribute_by_slope1_bind1
opparm -V 18.5.408 $_obj_geo1_attribute_by_slope1_bind1 parmname ( density ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opcolor -c 0.60000002384185791 0.60000002384185791 1 $_obj_geo1_attribute_by_slope1_bind1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_bind1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_bind1

# Node $_obj_geo1_attribute_by_slope1_srcmin (Vop/parameter)
set _obj_geo1_attribute_by_slope1_srcmin = `run("opadd -e -n -v parameter srcmin")`
oplocate -x `$arg2 + -3.65327` -y `$arg3 + -0.59999000000000002` $_obj_geo1_attribute_by_slope1_srcmin
opparm -V 18.5.408 $_obj_geo1_attribute_by_slope1_srcmin parmname ( slopemin ) parmlabel ( 'slope min angle' ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_srcmin
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_srcmin
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_srcmin
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_srcmin
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_srcmin

# Node $_obj_geo1_attribute_by_slope1_srcmax (Vop/parameter)
set _obj_geo1_attribute_by_slope1_srcmax = `run("opadd -e -n -v parameter srcmax")`
oplocate -x `$arg2 + -3.65327` -y `$arg3 + -2.5192100000000002` $_obj_geo1_attribute_by_slope1_srcmax
opparm -V 18.5.408 $_obj_geo1_attribute_by_slope1_srcmax parmname ( 'slope max' ) parmlabel ( 'slope max angle' ) floatdef ( 90 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_srcmax
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_srcmax
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_srcmax
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_srcmax
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_srcmax

# Node $_obj_geo1_attribute_by_slope1_fit5 (Vop/fit)
set _obj_geo1_attribute_by_slope1_fit5 = `run("opadd -e -n -v fit fit5")`
oplocate -x `$arg2 + 5.9290399999999996` -y `$arg3 + -1.25936` $_obj_geo1_attribute_by_slope1_fit5
opcolor -c 0.80000001192092896 0.80000001192092896 0.80000001192092896 $_obj_geo1_attribute_by_slope1_fit5
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c off -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_fit5
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_fit5
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute_by_slope1_fit5
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_fit5
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_fit5

# Node $_obj_geo1_attribute_by_slope1_destmin (Vop/parameter)
set _obj_geo1_attribute_by_slope1_destmin = `run("opadd -e -n -v parameter destmin")`
oplocate -x `$arg2 + 0.097178600000000004` -y `$arg3 + -1.13304` $_obj_geo1_attribute_by_slope1_destmin
opparm -V 18.5.408 $_obj_geo1_attribute_by_slope1_destmin parmname ( minslope ) parmlabel ( 'min density ' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_destmin
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_destmin
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_destmin
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_destmin
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_destmin

# Node $_obj_geo1_attribute_by_slope1_destmin1 (Vop/parameter)
set _obj_geo1_attribute_by_slope1_destmin1 = `run("opadd -e -n -v parameter destmin1")`
oplocate -x `$arg2 + 0.097178600000000004` -y `$arg3 + -2.8689499999999999` $_obj_geo1_attribute_by_slope1_destmin1
opparm -V 18.5.408 $_obj_geo1_attribute_by_slope1_destmin1 parmname ( maxslope ) parmlabel ( 'max density ' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_destmin1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_destmin1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_destmin1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_destmin1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_destmin1

# Node $_obj_geo1_attribute_by_slope1_bind3 (Vop/bind)
set _obj_geo1_attribute_by_slope1_bind3 = `run("opadd -e -n -v bind bind3")`
oplocate -x `$arg2 + 5.9290399999999996` -y `$arg3 + -3.1605500000000002` $_obj_geo1_attribute_by_slope1_bind3
opparm -V 18.5.408 $_obj_geo1_attribute_by_slope1_bind3 parmname ( density ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_bind3
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_bind3
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_bind3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_bind3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_bind3

# Node $_obj_geo1_attribute_by_slope1_multiply2 (Vop/multiply)
set _obj_geo1_attribute_by_slope1_multiply2 = `run("opadd -e -n -v multiply multiply2")`
oplocate -x `$arg2 + 9.0904500000000006` -y `$arg3 + -0.45304` $_obj_geo1_attribute_by_slope1_multiply2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_multiply2
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_multiply2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_multiply2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_multiply2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_multiply2

# Node $_obj_geo1_attribute_by_slope1_bind5 (Vop/bind)
set _obj_geo1_attribute_by_slope1_bind5 = `run("opadd -e -n -v bind bind5")`
oplocate -x `$arg2 + 8.0180000000000007` -y `$arg3 + 4.9953099999999999` $_obj_geo1_attribute_by_slope1_bind5
opparm -V 18.5.408 $_obj_geo1_attribute_by_slope1_bind5 parmname ( slopeA ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_bind5
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_bind5
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_bind5
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_bind5
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_bind5

# Node $_obj_geo1_attribute_by_slope1_ramp1 (Vop/rampparm)
set _obj_geo1_attribute_by_slope1_ramp1 = `run("opadd -e -n -v rampparm ramp1")`
oplocate -x `$arg2 + 2.8997199999999999` -y `$arg3 + 0.32064399999999998` $_obj_geo1_attribute_by_slope1_ramp1
opparm $_obj_geo1_attribute_by_slope1_ramp1  rampcolordefault ( 2 ) rampfloatdefault ( 2 )
opparm -V 18.5.408 $_obj_geo1_attribute_by_slope1_ramp1 parmname ( sloperemap ) parmlabel ( 'slope remap' ) ramptype ( flt ) rampcolordefault2pos ( 1 ) rampcolordefault2c ( 1 1 1 ) rampfloatdefault2pos ( 1 ) rampfloatdefault2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_ramp1
nbop $_obj_geo1_attribute_by_slope1___netbox1 add $_obj_geo1_attribute_by_slope1_ramp1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_ramp1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_ramp1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_ramp1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_ramp1

# Node $_obj_geo1_attribute_by_slope1_add1 (Vop/add)
set _obj_geo1_attribute_by_slope1_add1 = `run("opadd -e -n -v add add1")`
oplocate -x `$arg2 + 9.5066900000000008` -y `$arg3 + -2.5197400000000001` $_obj_geo1_attribute_by_slope1_add1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_add1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_add1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_add1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_add1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_add1

# Node $_obj_geo1_attribute_by_slope1_switch1 (Vop/switch)
set _obj_geo1_attribute_by_slope1_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 12.491` -y `$arg3 + -2.1444399999999999` $_obj_geo1_attribute_by_slope1_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_switch1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_switch1

# Node $_obj_geo1_attribute_by_slope1_mix1 (Vop/mix)
set _obj_geo1_attribute_by_slope1_mix1 = `run("opadd -e -n -v mix mix1")`
oplocate -x `$arg2 + 9.5066900000000008` -y `$arg3 + -3.9905499999999998` $_obj_geo1_attribute_by_slope1_mix1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_mix1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_mix1
opuserdata -n '___Version___' -v '' $_obj_geo1_attribute_by_slope1_mix1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_mix1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_mix1

# Node $_obj_geo1_attribute_by_slope1_parm1 (Vop/parameter)
set _obj_geo1_attribute_by_slope1_parm1 = `run("opadd -e -n -v parameter parm1")`
oplocate -x `$arg2 + 9.8468999999999998` -y `$arg3 + -6.3227799999999998` $_obj_geo1_attribute_by_slope1_parm1
opparm -V 18.5.408 $_obj_geo1_attribute_by_slope1_parm1 parmname ( switchmode ) parmlabel ( 'switch mode' ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_attribute_by_slope1_parm1
opexprlanguage -s hscript $_obj_geo1_attribute_by_slope1_parm1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribute_by_slope1_parm1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribute_by_slope1_parm1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribute_by_slope1_parm1

# Sticky Note __stickynote1
python -c 'hou.pwd().createStickyNote("__stickynote1")'
python -c 'hou.pwd().findStickyNote("__stickynote1").setColor(hou.Color((1, 0.969, 0.522)))'
python -c 'hou.pwd().findStickyNote("__stickynote1").setText("DOT PRODUCT  for slope ")'
python -c 'hou.pwd().findStickyNote("__stickynote1").setTextSize(1)'
python -c 'hou.pwd().findStickyNote("__stickynote1").setTextColor(hou.Color((0, 0, 0)))'
python -c 'hou.pwd().findStickyNote("__stickynote1").setDrawBackground(True)'
python -c 'hou.pwd().findStickyNote("__stickynote1").setPosition(hou.Vector2(-8.15991, 3.77717))'
python -c 'hou.pwd().findStickyNote("__stickynote1").setSize(hou.Vector2(15.0262, 1.77293))'
python -c 'hou.pwd().findStickyNote("__stickynote1").setMinimized(False)'
opcf ..
opcf $_obj_geo1_attribute_by_slope1
oporder -e geometryvopglobal1 geometryvopoutput1 dot1 trig1 fit4 radtodeg1 bind1 srcmin srcmax fit5 destmin destmin1 bind3 multiply2 bind5 ramp1 add1 switch1 mix1 parm1 
opcf ..
opset -p on $_obj_geo1_attribute_by_slope1
opcf $arg1

# Node $_obj_geo1_attribpromote1 (Sop/attribpromote)
set _obj_geo1_attribpromote1 = `run("opadd -e -n -v attribpromote attribpromote1")`
oplocate -x `$arg2 + 3.7274029999999994` -y `$arg3 + 37.1616` $_obj_geo1_attribpromote1
opparm -V 18.5.408 $_obj_geo1_attribpromote1 inname ( curvature ) inclass ( primitive ) method ( max )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_attribpromote1
opexprlanguage -s hscript $_obj_geo1_attribpromote1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribpromote1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribpromote1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribpromote1
opset -p on $_obj_geo1_attribpromote1
opcf $arg1

# Node $_obj_geo1_switch24 (Sop/switch)
set _obj_geo1_switch24 = `run("opadd -e -n -v switch switch24")`
oplocate -x `$arg2 + 7.6992030000000007` -y `$arg3 + 21.634100000000004` $_obj_geo1_switch24
chblockbegin
chadd -t 0 0 $_obj_geo1_switch24 input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../udim")' $_obj_geo1_switch24/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch24
opexprlanguage -s hscript $_obj_geo1_switch24
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch24
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch24
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch24
opset -p on $_obj_geo1_switch24
opcf $arg1

# Node $_obj_geo1_uvproject1 (Sop/uvproject)
set _obj_geo1_uvproject1 = `run("opadd -e -n -v uvproject uvproject1")`
oplocate -x `$arg2 + 4.2461029999999997` -y `$arg3 + 27.297499999999999` $_obj_geo1_uvproject1
opparm -V 18.5.408 $_obj_geo1_uvproject1 grouptype ( points ) t ( 0 55.369277954101563 0 ) r ( 90 0 0 ) s ( 1999.426513671875 1999.107666015625 192.052734375 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_uvproject1
opexprlanguage -s hscript $_obj_geo1_uvproject1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_uvproject1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_uvproject1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_uvproject1
opset -p on $_obj_geo1_uvproject1
opcf $arg1

# Node $_obj_geo1_switch_map (Sop/switch)
set _obj_geo1_switch_map = `run("opadd -e -n -v switch switch_map")`
oplocate -x `$arg2 + -0.2891999999999999` -y `$arg3 + 16.0839` $_obj_geo1_switch_map
chblockbegin
chadd -t 0 0 $_obj_geo1_switch_map input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enablemap")' $_obj_geo1_switch_map/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch_map
opexprlanguage -s hscript $_obj_geo1_switch_map
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch_map
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch_map
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch_map
opset -p on $_obj_geo1_switch_map
opcf $arg1

# Node $_obj_geo1_map (Sop/attribvop)
set _obj_geo1_map = `run("opadd -e -n -v attribvop map")`
oplocate -x `$arg2 + 4.2427030000000006` -y `$arg3 + 22.713100000000004` $_obj_geo1_map
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Usize"         label   "usize"         type    float         default { "1" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Vsize"         label   "vsize"         type    float         default { "1" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Voffset"         label   "Voffset"         type    float         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Uoffset"         label   "Uoffset"         type    float         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "remapmin"         label   "min input"         type    float         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "remapmax"         label   "max input"         type    float         default { "1" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switch_rgb"         label   "switch_rgb"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "cmapinput"         label   "Color Map"         type    image         default { "$HH/pic/Mandril.pic" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "st"         label   "st"         type    float         invisible         size    2         default { "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switchRGB"         label   "vizRGB"         type    toggle         default { "0" }         parmtag { "script_callback_language" "python" }     } ' $_obj_geo1_map
opparm $_obj_geo1_map  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 0 0 $_obj_geo1_map Usize
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../Usize")' $_obj_geo1_map/Usize
chadd -t 0 0 $_obj_geo1_map Vsize
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../Vsize")' $_obj_geo1_map/Vsize
chadd -t 0 0 $_obj_geo1_map Voffset
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../Voffset")' $_obj_geo1_map/Voffset
chadd -t 0 0 $_obj_geo1_map Uoffset
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../Uoffset")' $_obj_geo1_map/Uoffset
chadd -t 0 0 $_obj_geo1_map remapmin
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../remapmin")' $_obj_geo1_map/remapmin
chadd -t 0 0 $_obj_geo1_map remapmax
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../remapmax")' $_obj_geo1_map/remapmax
chadd -t 0 0 $_obj_geo1_map switch_rgb
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../rgbchannel")' $_obj_geo1_map/switch_rgb
chadd -t 0 0 $_obj_geo1_map cmapinput
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chs("../cmapinput")' $_obj_geo1_map/cmapinput
chadd -t 0 0 $_obj_geo1_map switchRGB
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../switchRGB")' $_obj_geo1_map/switchRGB
chblockend
opparm -V 18.5.408 $_obj_geo1_map Usize ( Usize ) Vsize ( Vsize ) Voffset ( Voffset ) Uoffset ( Uoffset ) remapmin ( remapmin ) remapmax ( remapmax ) switch_rgb ( switch_rgb ) cmapinput ( cmapinput ) switchRGB ( switchRGB )
opcolor -c 0.14499999582767487 0.66699999570846558 0.55699998140335083 $_obj_geo1_map
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_map
opexprlanguage -s hscript $_obj_geo1_map
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map
opcf $_obj_geo1_map

# Node $_obj_geo1_map_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_geo1_map_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + -6.0132599999999998` -y `$arg3 + 3.5672700000000002` $_obj_geo1_map_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_geometryvopglobal1
opexprlanguage -s hscript $_obj_geo1_map_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_geometryvopglobal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_geometryvopglobal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_geometryvopglobal1

# Node $_obj_geo1_map_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_map_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 26.603000000000002` -y `$arg3 + 2.0142500000000001` $_obj_geo1_map_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_map_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_geometryvopoutput1

# Node $_obj_geo1_map_vectofloat1 (Vop/vectofloat)
set _obj_geo1_map_vectofloat1 = `run("opadd -e -n -v vectofloat vectofloat1")`
oplocate -x `$arg2 + -3.1116100000000002` -y `$arg3 + 3.1261899999999998` $_obj_geo1_map_vectofloat1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_vectofloat1
opexprlanguage -s hscript $_obj_geo1_map_vectofloat1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_vectofloat1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_vectofloat1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_vectofloat1

# Node $_obj_geo1_map_multiply1 (Vop/multiply)
set _obj_geo1_map_multiply1 = `run("opadd -e -n -v multiply multiply1")`
oplocate -x `$arg2 + 1.7243999999999999` -y `$arg3 + 4.5616899999999996` $_obj_geo1_map_multiply1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_multiply1
opexprlanguage -s hscript $_obj_geo1_map_multiply1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_multiply1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_multiply1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_multiply1

# Node $_obj_geo1_map_parm1 (Vop/parameter)
set _obj_geo1_map_parm1 = `run("opadd -e -n -v parameter parm1")`
oplocate -x `$arg2 + -0.48977599999999999` -y `$arg3 + 0.56726799999999999` $_obj_geo1_map_parm1
opparm -V 18.5.408 $_obj_geo1_map_parm1 parmname ( Usize ) parmlabel ( usize ) floatdef ( 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_parm1
opexprlanguage -s hscript $_obj_geo1_map_parm1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_parm1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_parm1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_parm1

# Node $_obj_geo1_map_parm2 (Vop/parameter)
set _obj_geo1_map_parm2 = `run("opadd -e -n -v parameter parm2")`
oplocate -x `$arg2 + -0.124948` -y `$arg3 + -2.1724700000000001` $_obj_geo1_map_parm2
opparm -V 18.5.408 $_obj_geo1_map_parm2 parmname ( Vsize ) parmlabel ( vsize ) floatdef ( 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_parm2
opexprlanguage -s hscript $_obj_geo1_map_parm2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_parm2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_parm2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_parm2

# Node $_obj_geo1_map_multiply2 (Vop/multiply)
set _obj_geo1_map_multiply2 = `run("opadd -e -n -v multiply multiply2")`
oplocate -x `$arg2 + 2.2615099999999999` -y `$arg3 + 2.4623900000000001` $_obj_geo1_map_multiply2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_multiply2
opexprlanguage -s hscript $_obj_geo1_map_multiply2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_multiply2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_multiply2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_multiply2

# Node $_obj_geo1_map_add1 (Vop/add)
set _obj_geo1_map_add1 = `run("opadd -e -n -v add add1")`
oplocate -x `$arg2 + 5.1325099999999999` -y `$arg3 + 2.4623900000000001` $_obj_geo1_map_add1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_add1
opexprlanguage -s hscript $_obj_geo1_map_add1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_add1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_add1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_add1

# Node $_obj_geo1_map_parm3 (Vop/parameter)
set _obj_geo1_map_parm3 = `run("opadd -e -n -v parameter parm3")`
oplocate -x `$arg2 + 2.98929` -y `$arg3 + 0.56726799999999999` $_obj_geo1_map_parm3
opparm -V 18.5.408 $_obj_geo1_map_parm3 parmname ( Voffset ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_parm3
opexprlanguage -s hscript $_obj_geo1_map_parm3
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_parm3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_parm3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_parm3

# Node $_obj_geo1_map_add2 (Vop/add)
set _obj_geo1_map_add2 = `run("opadd -e -n -v add add2")`
oplocate -x `$arg2 + 5.1325099999999999` -y `$arg3 + 4.4116900000000001` $_obj_geo1_map_add2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_add2
opexprlanguage -s hscript $_obj_geo1_map_add2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_add2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_add2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_add2

# Node $_obj_geo1_map_parm4 (Vop/parameter)
set _obj_geo1_map_parm4 = `run("opadd -e -n -v parameter parm4")`
oplocate -x `$arg2 + 3.53057` -y `$arg3 + -2.0512899999999998` $_obj_geo1_map_parm4
opparm -V 18.5.408 $_obj_geo1_map_parm4 parmname ( Uoffset ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_parm4
opexprlanguage -s hscript $_obj_geo1_map_parm4
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_parm4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_parm4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_parm4

# Node $_obj_geo1_map_bind1 (Vop/bind)
set _obj_geo1_map_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 19.9635` -y `$arg3 + -1.19889` $_obj_geo1_map_bind1
opparm -V 18.5.408 $_obj_geo1_map_bind1 parmname ( map ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_bind1
opexprlanguage -s hscript $_obj_geo1_map_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_bind1

# Node $_obj_geo1_map_vectofloat2 (Vop/vectofloat)
set _obj_geo1_map_vectofloat2 = `run("opadd -e -n -v vectofloat vectofloat2")`
oplocate -x `$arg2 + 10.571899999999999` -y `$arg3 + 1.3826499999999999` $_obj_geo1_map_vectofloat2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_vectofloat2
opexprlanguage -s hscript $_obj_geo1_map_vectofloat2
opuserdata -n '___Version___' -v '' $_obj_geo1_map_vectofloat2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_vectofloat2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_vectofloat2

# Node $_obj_geo1_map_colormap1 (Vop/colormap)
set _obj_geo1_map_colormap1 = `run("opadd -e -n -v colormap colormap1")`
oplocate -x `$arg2 + 8.1346699999999998` -y `$arg3 + 3.4316900000000001` $_obj_geo1_map_colormap1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_colormap1
opexprlanguage -s hscript $_obj_geo1_map_colormap1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_colormap1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_colormap1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_colormap1

# Node $_obj_geo1_map_cmap (Vop/parameter)
set _obj_geo1_map_cmap = `run("opadd -e -n -v parameter cmap")`
oplocate -x `$arg2 + 6.3016500000000004` -y `$arg3 + 0.163826` $_obj_geo1_map_cmap
opparm -V 18.5.408 $_obj_geo1_map_cmap parmname ( cmapinput ) parmlabel ( 'Color Map' ) parmtype ( image ) imagedef ( '$HH/pic/Mandril.pic' ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_cmap
opexprlanguage -s hscript $_obj_geo1_map_cmap
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_cmap
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_cmap
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_cmap

# Node $_obj_geo1_map_fit1 (Vop/fit)
set _obj_geo1_map_fit1 = `run("opadd -e -n -v fit fit1")`
oplocate -x `$arg2 + 16.810700000000001` -y `$arg3 + -0.52339599999999997` $_obj_geo1_map_fit1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_fit1
opexprlanguage -s hscript $_obj_geo1_map_fit1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_fit1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_fit1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_fit1

# Node $_obj_geo1_map_srcmin (Vop/parameter)
set _obj_geo1_map_srcmin = `run("opadd -e -n -v parameter srcmin")`
oplocate -x `$arg2 + 11.593299999999999` -y `$arg3 + 1.1621300000000001` $_obj_geo1_map_srcmin
opparm -V 18.5.408 $_obj_geo1_map_srcmin parmname ( remapmin ) parmlabel ( 'min input' ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_map_srcmin
opexprlanguage -s hscript $_obj_geo1_map_srcmin
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_srcmin
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_srcmin
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_srcmin

# Node $_obj_geo1_map_srcmax (Vop/parameter)
set _obj_geo1_map_srcmax = `run("opadd -e -n -v parameter srcmax")`
oplocate -x `$arg2 + 11.693300000000001` -y `$arg3 + 0.96212600000000004` $_obj_geo1_map_srcmax
opparm -V 18.5.408 $_obj_geo1_map_srcmax parmname ( remapmax ) parmlabel ( 'max input' ) floatdef ( 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_map_srcmax
opexprlanguage -s hscript $_obj_geo1_map_srcmax
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_srcmax
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_srcmax
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_srcmax

# Node $_obj_geo1_map_vectofloat3 (Vop/vectofloat)
set _obj_geo1_map_vectofloat3 = `run("opadd -e -n -v vectofloat vectofloat3")`
oplocate -x `$arg2 + 10.571899999999999` -y `$arg3 + -0.82339600000000002` $_obj_geo1_map_vectofloat3
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_vectofloat3
opexprlanguage -s hscript $_obj_geo1_map_vectofloat3
opuserdata -n '___Version___' -v '' $_obj_geo1_map_vectofloat3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_vectofloat3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_vectofloat3

# Node $_obj_geo1_map_vectofloat4 (Vop/vectofloat)
set _obj_geo1_map_vectofloat4 = `run("opadd -e -n -v vectofloat vectofloat4")`
oplocate -x `$arg2 + 10.436` -y `$arg3 + -2.8240099999999999` $_obj_geo1_map_vectofloat4
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_vectofloat4
opexprlanguage -s hscript $_obj_geo1_map_vectofloat4
opuserdata -n '___Version___' -v '' $_obj_geo1_map_vectofloat4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_vectofloat4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_vectofloat4

# Node $_obj_geo1_map_switch1 (Vop/switch)
set _obj_geo1_map_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 13.758900000000001` -y `$arg3 + -0.52339599999999997` $_obj_geo1_map_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_switch1
opexprlanguage -s hscript $_obj_geo1_map_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_switch1

# Node $_obj_geo1_map_parm5 (Vop/parameter)
set _obj_geo1_map_parm5 = `run("opadd -e -n -v parameter parm5")`
oplocate -x `$arg2 + 11.1226` -y `$arg3 + -4.7082800000000002` $_obj_geo1_map_parm5
opparm -V 18.5.408 $_obj_geo1_map_parm5 parmname ( switch_rgb ) parmlabel ( switch_rgb ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_parm5
opexprlanguage -s hscript $_obj_geo1_map_parm5
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_parm5
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_parm5
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_parm5

# Node $_obj_geo1_map_uvcoords1 (Vop/uvcoords::2.0)
set _obj_geo1_map_uvcoords1 = `run("opadd -e -n -v uvcoords::2.0 uvcoords1")`
oplocate -x `$arg2 + 10.297800000000001` -y `$arg3 + 6.5899700000000001` $_obj_geo1_map_uvcoords1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_uvcoords1
opexprlanguage -s hscript $_obj_geo1_map_uvcoords1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_uvcoords1
opuserdata -n '___toolcount___' -v '71' $_obj_geo1_map_uvcoords1
opuserdata -n '___toolid___' -v 'tool_12' $_obj_geo1_map_uvcoords1

# Node $_obj_geo1_map_switch2 (Vop/switch)
set _obj_geo1_map_switch2 = `run("opadd -e -n -v switch switch2")`
oplocate -x `$arg2 + 23.9572` -y `$arg3 + 1.0705100000000001` $_obj_geo1_map_switch2
chblockbegin
chadd -t 0 0 $_obj_geo1_map_switch2 switcher
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../switchRGB")' $_obj_geo1_map_switch2/switcher
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_switch2
opexprlanguage -s hscript $_obj_geo1_map_switch2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_switch2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_switch2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_switch2

# Node $_obj_geo1_map_floattovec1 (Vop/floattovec)
set _obj_geo1_map_floattovec1 = `run("opadd -e -n -v floattovec floattovec1")`
oplocate -x `$arg2 + 22.162700000000001` -y `$arg3 + -0.60392699999999999` $_obj_geo1_map_floattovec1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_floattovec1
opexprlanguage -s hscript $_obj_geo1_map_floattovec1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_floattovec1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_floattovec1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_floattovec1
opcf ..
opcf $_obj_geo1_map
oporder -e geometryvopglobal1 geometryvopoutput1 vectofloat1 multiply1 parm1 parm2 multiply2 add1 parm3 add2 parm4 bind1 vectofloat2 colormap1 cmap fit1 srcmin srcmax vectofloat3 vectofloat4 switch1 parm5 uvcoords1 switch2 floattovec1 
opcf ..
opset -p on $_obj_geo1_map
opcf $arg1

# Node $_obj_geo1_map_1007 (Sop/attribvop)
set _obj_geo1_map_1007 = `run("opadd -e -n -v attribvop map_1007")`
oplocate -x `$arg2 + 8.8292030000000015` -y `$arg3 + 22.713100000000004` $_obj_geo1_map_1007
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "mapUDIM"         label   "mapUDIM"         type    string         default { "" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "udim"         label   "udim"         type    string         default { "" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "remapmin"         label   "min input"         type    float         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "remapmax"         label   "max input"         type    float         default { "1" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switch_rgb"         label   "switch_rgb"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "st"         label   "st"         type    float         invisible         size    2         default { "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switchRGB"         label   "vizRGB"         type    toggle         default { "0" }         parmtag { "script_callback_language" "python" }     } ' $_obj_geo1_map_1007
opparm $_obj_geo1_map_1007  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 0 0 $_obj_geo1_map_1007 remapmin
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../map/remapmin")' $_obj_geo1_map_1007/remapmin
chadd -t 0 0 $_obj_geo1_map_1007 remapmax
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../map/remapmax")' $_obj_geo1_map_1007/remapmax
chadd -t 0 0 $_obj_geo1_map_1007 switch_rgb
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../map/switch_rgb")' $_obj_geo1_map_1007/switch_rgb
chadd -t 0 0 $_obj_geo1_map_1007 switchRGB
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../map/switchRGB")' $_obj_geo1_map_1007/switchRGB
chblockend
opparm -V 18.5.408 $_obj_geo1_map_1007 mapUDIM ( '`chs("path")``chs("map")``chs("udim")``chs("extension")`' ) udim ( '<UDIM>' ) remapmin ( remapmin ) remapmax ( remapmax ) switch_rgb ( switch_rgb ) switchRGB ( switchRGB )
opcolor -c 0.14499999582767487 0.66699999570846558 0.55699998140335083 $_obj_geo1_map_1007
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_map_1007
opexprlanguage -s hscript $_obj_geo1_map_1007
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_1007
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007
opcf $_obj_geo1_map_1007

# Node $_obj_geo1_map_1007_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_geo1_map_1007_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + -6.0132599999999998` -y `$arg3 + 3.5672700000000002` $_obj_geo1_map_1007_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_geometryvopglobal1
opexprlanguage -s hscript $_obj_geo1_map_1007_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_geometryvopglobal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_geometryvopglobal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_geometryvopglobal1

# Node $_obj_geo1_map_1007_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_map_1007_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 40.252400000000002` -y `$arg3 + 1.0785899999999999` $_obj_geo1_map_1007_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_map_1007_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_geometryvopoutput1

# Node $_obj_geo1_map_1007_bind1 (Vop/bind)
set _obj_geo1_map_1007_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 34.252400000000002` -y `$arg3 + 0.18854399999999999` $_obj_geo1_map_1007_bind1
opparm -V 18.5.408 $_obj_geo1_map_1007_bind1 parmname ( map ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_bind1
opexprlanguage -s hscript $_obj_geo1_map_1007_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_1007_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_bind1

# Node $_obj_geo1_map_1007_vectofloat2 (Vop/vectofloat)
set _obj_geo1_map_1007_vectofloat2 = `run("opadd -e -n -v vectofloat vectofloat2")`
oplocate -x `$arg2 + 28.171700000000001` -y `$arg3 + -0.40587899999999999` $_obj_geo1_map_1007_vectofloat2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_vectofloat2
opexprlanguage -s hscript $_obj_geo1_map_1007_vectofloat2
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_vectofloat2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_vectofloat2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_vectofloat2

# Node $_obj_geo1_map_1007_fit1 (Vop/fit)
set _obj_geo1_map_1007_fit1 = `run("opadd -e -n -v fit fit1")`
oplocate -x `$arg2 + 31.029499999999999` -y `$arg3 + 0.92625199999999996` $_obj_geo1_map_1007_fit1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_fit1
opexprlanguage -s hscript $_obj_geo1_map_1007_fit1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_fit1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_fit1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_fit1

# Node $_obj_geo1_map_1007_srcmin (Vop/parameter)
set _obj_geo1_map_1007_srcmin = `run("opadd -e -n -v parameter srcmin")`
oplocate -x `$arg2 + 11.593299999999999` -y `$arg3 + 1.1621300000000001` $_obj_geo1_map_1007_srcmin
opparm -V 18.5.408 $_obj_geo1_map_1007_srcmin parmname ( remapmin ) parmlabel ( 'min input' ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_map_1007_srcmin
opexprlanguage -s hscript $_obj_geo1_map_1007_srcmin
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_1007_srcmin
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_srcmin
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_srcmin

# Node $_obj_geo1_map_1007_srcmax (Vop/parameter)
set _obj_geo1_map_1007_srcmax = `run("opadd -e -n -v parameter srcmax")`
oplocate -x `$arg2 + 11.693300000000001` -y `$arg3 + 0.96212600000000004` $_obj_geo1_map_1007_srcmax
opparm -V 18.5.408 $_obj_geo1_map_1007_srcmax parmname ( remapmax ) parmlabel ( 'max input' ) floatdef ( 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_map_1007_srcmax
opexprlanguage -s hscript $_obj_geo1_map_1007_srcmax
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_1007_srcmax
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_srcmax
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_srcmax

# Node $_obj_geo1_map_1007_vectofloat3 (Vop/vectofloat)
set _obj_geo1_map_1007_vectofloat3 = `run("opadd -e -n -v vectofloat vectofloat3")`
oplocate -x `$arg2 + 28.171700000000001` -y `$arg3 + -2.61192` $_obj_geo1_map_1007_vectofloat3
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_vectofloat3
opexprlanguage -s hscript $_obj_geo1_map_1007_vectofloat3
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_vectofloat3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_vectofloat3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_vectofloat3

# Node $_obj_geo1_map_1007_vectofloat4 (Vop/vectofloat)
set _obj_geo1_map_1007_vectofloat4 = `run("opadd -e -n -v vectofloat vectofloat4")`
oplocate -x `$arg2 + 28.035799999999998` -y `$arg3 + -4.6125400000000001` $_obj_geo1_map_1007_vectofloat4
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_vectofloat4
opexprlanguage -s hscript $_obj_geo1_map_1007_vectofloat4
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_vectofloat4
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_vectofloat4
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_vectofloat4

# Node $_obj_geo1_map_1007_switch1 (Vop/switch)
set _obj_geo1_map_1007_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 31.358699999999999` -y `$arg3 + -2.3119200000000002` $_obj_geo1_map_1007_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_switch1
opexprlanguage -s hscript $_obj_geo1_map_1007_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_1007_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_switch1

# Node $_obj_geo1_map_1007_parm5 (Vop/parameter)
set _obj_geo1_map_1007_parm5 = `run("opadd -e -n -v parameter parm5")`
oplocate -x `$arg2 + 24.361000000000001` -y `$arg3 + -6.49681` $_obj_geo1_map_1007_parm5
opparm -V 18.5.408 $_obj_geo1_map_1007_parm5 parmname ( switch_rgb ) parmlabel ( switch_rgb ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_parm5
opexprlanguage -s hscript $_obj_geo1_map_1007_parm5
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_1007_parm5
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_parm5
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_parm5

# Node $_obj_geo1_map_1007_texture1 (Vop/texture::2.0)
set _obj_geo1_map_1007_texture1 = `run("opadd -e -n -v texture::2.0 texture1")`
oplocate -x `$arg2 + 20.657800000000002` -y `$arg3 + 3.7586200000000001` $_obj_geo1_map_1007_texture1
opparm $_obj_geo1_map_1007_texture1 map ( '`chs("../mapUDIM")`' ) wrap ( decal )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_texture1
opexprlanguage -s hscript $_obj_geo1_map_1007_texture1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_texture1
opuserdata -n '___toolcount___' -v '32' $_obj_geo1_map_1007_texture1
opuserdata -n '___toolid___' -v 'tool_2' $_obj_geo1_map_1007_texture1

# Node $_obj_geo1_map_1007_inttovec1 (Vop/inttovec)
set _obj_geo1_map_1007_inttovec1 = `run("opadd -e -n -v inttovec inttovec1")`
oplocate -x `$arg2 + 17.264099999999999` -y `$arg3 + -0.33767000000000003` $_obj_geo1_map_1007_inttovec1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_inttovec1
opexprlanguage -s hscript $_obj_geo1_map_1007_inttovec1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_inttovec1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_inttovec1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_inttovec1

# Node $_obj_geo1_map_1007_bind2 (Vop/bind)
set _obj_geo1_map_1007_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 8.6028099999999998` -y `$arg3 + -0.33767000000000003` $_obj_geo1_map_1007_bind2
opparm -V 18.5.408 $_obj_geo1_map_1007_bind2 parmname ( uv ) parmtype ( vector ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_bind2
opexprlanguage -s hscript $_obj_geo1_map_1007_bind2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_1007_bind2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_bind2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_bind2

# Node $_obj_geo1_map_1007_vectofloat1 (Vop/vectofloat)
set _obj_geo1_map_1007_vectofloat1 = `run("opadd -e -n -v vectofloat vectofloat1")`
oplocate -x `$arg2 + 14.6028` -y `$arg3 + -0.33767000000000003` $_obj_geo1_map_1007_vectofloat1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_vectofloat1
opexprlanguage -s hscript $_obj_geo1_map_1007_vectofloat1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_vectofloat1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_vectofloat1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_vectofloat1

# Node $_obj_geo1_map_1007_floor1 (Vop/floor)
set _obj_geo1_map_1007_floor1 = `run("opadd -e -n -v floor floor1")`
oplocate -x `$arg2 + 11.5655` -y `$arg3 + -0.33767000000000003` $_obj_geo1_map_1007_floor1
opparm $_obj_geo1_map_1007_floor1 signature ( v )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_floor1
opexprlanguage -s hscript $_obj_geo1_map_1007_floor1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_floor1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_floor1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_floor1

# Node $_obj_geo1_map_1007_switch2 (Vop/switch)
set _obj_geo1_map_1007_switch2 = `run("opadd -e -n -v switch switch2")`
oplocate -x `$arg2 + 37.668900000000001` -y `$arg3 + 0.928593` $_obj_geo1_map_1007_switch2
chblockbegin
chadd -t 0 0 $_obj_geo1_map_1007_switch2 switcher
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../switchRGB")' $_obj_geo1_map_1007_switch2/switcher
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_switch2
opexprlanguage -s hscript $_obj_geo1_map_1007_switch2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_map_1007_switch2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_switch2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_switch2

# Node $_obj_geo1_map_1007_floattovec1 (Vop/floattovec)
set _obj_geo1_map_1007_floattovec1 = `run("opadd -e -n -v floattovec floattovec1")`
oplocate -x `$arg2 + 35.722799999999999` -y `$arg3 + -1.9138599999999999` $_obj_geo1_map_1007_floattovec1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_map_1007_floattovec1
opexprlanguage -s hscript $_obj_geo1_map_1007_floattovec1
opuserdata -n '___Version___' -v '' $_obj_geo1_map_1007_floattovec1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_map_1007_floattovec1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_map_1007_floattovec1
opcf ..
opcf $_obj_geo1_map_1007
oporder -e geometryvopglobal1 geometryvopoutput1 bind1 vectofloat2 fit1 srcmin srcmax vectofloat3 vectofloat4 switch1 parm5 texture1 inttovec1 bind2 vectofloat1 floor1 switch2 floattovec1 
opcf ..
opset -p on $_obj_geo1_map_1007
opcf $arg1

# Node $_obj_geo1_attribwrangle3 (Sop/attribwrangle)
set _obj_geo1_attribwrangle3 = `run("opadd -e -n -v attribwrangle attribwrangle3")`
oplocate -x `$arg2 + 8.3481030000000001` -y `$arg3 + 58.825099999999999` $_obj_geo1_attribwrangle3
opparm $_obj_geo1_attribwrangle3  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_attribwrangle3 snippet ( '@objval= 1;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_attribwrangle3
opexprlanguage -s hscript $_obj_geo1_attribwrangle3
opuserdata -n '___Version___' -v '' $_obj_geo1_attribwrangle3
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribwrangle3
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribwrangle3
opset -p on $_obj_geo1_attribwrangle3
opcf $arg1

# Node $_obj_geo1_switch_slope (Sop/switch)
set _obj_geo1_switch_slope = `run("opadd -e -n -v switch switch_slope")`
oplocate -x `$arg2 + -0.22549999999999992` -y `$arg3 + 71.339340000000007` $_obj_geo1_switch_slope
chblockbegin
chadd -t 0 0 $_obj_geo1_switch_slope input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enableslope")' $_obj_geo1_switch_slope/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch_slope
opexprlanguage -s hscript $_obj_geo1_switch_slope
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch_slope
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch_slope
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch_slope
opset -p on $_obj_geo1_switch_slope
opcf $arg1

# Node $_obj_geo1_null2 (Sop/null)
set _obj_geo1_null2 = `run("opadd -e -n -v null null2")`
oplocate -x `$arg2 + -3.123497` -y `$arg3 + 5.7834999999999894` $_obj_geo1_null2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_null2
opexprlanguage -s hscript $_obj_geo1_null2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_null2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_null2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_null2
opset -p on $_obj_geo1_null2
opcf $arg1

# Node $_obj_geo1_ID_viz1 (Sop/attribvop)
set _obj_geo1_ID_viz1 = `run("opadd -e -n -v attribvop ID_viz1")`
oplocate -x `$arg2 + 4.7488030000000006` -y `$arg3 + 12.416600000000003` $_obj_geo1_ID_viz1
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "IDviz"         label   "ID viz"         type    ramp_rgb         default { "2" }         range   { 1! 10 }         parmtag { "parmvop" "1" }         parmtag { "rampbasis_var" "IDviz_the_basis_strings" }         parmtag { "rampbasisdefault" "linear" }         parmtag { "rampcolordefault" "1pos ( 0 ) 1c ( 0 0 0 ) 1interp ( linear ) 2pos ( 1 ) 2c ( 1 1 1 ) 2interp ( linear )" }         parmtag { "rampcolortype" "rgb" }         parmtag { "rampkeys_var" "IDviz_the_key_positions" }         parmtag { "rampshowcontrolsdefault" "1" }         parmtag { "rampvalues_var" "IDviz_the_key_values" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_ID_viz1
opparm $_obj_geo1_ID_viz1  bindings ( 0 ) groupbindings ( 0 ) IDviz ( 3 )
opparm -V 18.5.408 $_obj_geo1_ID_viz1 IDviz ( 3 ) IDviz1c ( 1 0 0 ) IDviz2pos ( 0.5 ) IDviz2c ( 0 1 0 ) IDviz3pos ( 1 ) IDviz3c ( 0 0 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_ID_viz1
opexprlanguage -s hscript $_obj_geo1_ID_viz1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_ID_viz1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_ID_viz1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_ID_viz1
opcf $_obj_geo1_ID_viz1

# Node $_obj_geo1_ID_viz1_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_geo1_ID_viz1_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + 1.9057900000000001` -y `$arg3 + 1.97631` $_obj_geo1_ID_viz1_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_ID_viz1_geometryvopglobal1
opexprlanguage -s hscript $_obj_geo1_ID_viz1_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_geo1_ID_viz1_geometryvopglobal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_ID_viz1_geometryvopglobal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_ID_viz1_geometryvopglobal1

# Node $_obj_geo1_ID_viz1_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_ID_viz1_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 12.250400000000001` -y `$arg3 + 3.0445600000000002` $_obj_geo1_ID_viz1_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_ID_viz1_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_ID_viz1_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_ID_viz1_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_ID_viz1_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_ID_viz1_geometryvopoutput1

# Node $_obj_geo1_ID_viz1_ramp1 (Vop/rampparm)
set _obj_geo1_ID_viz1_ramp1 = `run("opadd -e -n -v rampparm ramp1")`
oplocate -x `$arg2 + 8.6045400000000001` -y `$arg3 + 2.6652999999999998` $_obj_geo1_ID_viz1_ramp1
opparm $_obj_geo1_ID_viz1_ramp1  rampcolordefault ( 2 ) rampfloatdefault ( 2 )
opparm -V 18.5.408 $_obj_geo1_ID_viz1_ramp1 parmname ( IDviz ) parmlabel ( 'ID viz' ) rampcolordefault2pos ( 1 ) rampcolordefault2c ( 1 1 1 ) rampfloatdefault2pos ( 1 ) rampfloatdefault2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_ID_viz1_ramp1
opexprlanguage -s hscript $_obj_geo1_ID_viz1_ramp1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_ID_viz1_ramp1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_ID_viz1_ramp1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_ID_viz1_ramp1

# Node $_obj_geo1_ID_viz1_bind1 (Vop/bind)
set _obj_geo1_ID_viz1_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 4.31365` -y `$arg3 + 3.2946499999999999` $_obj_geo1_ID_viz1_bind1
opparm -V 18.5.408 $_obj_geo1_ID_viz1_bind1 parmname ( ID ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_ID_viz1_bind1
opexprlanguage -s hscript $_obj_geo1_ID_viz1_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_ID_viz1_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_ID_viz1_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_ID_viz1_bind1
opcf ..
opcf $_obj_geo1_ID_viz1
oporder -e geometryvopglobal1 geometryvopoutput1 ramp1 bind1 
opcf ..
opset -p on $_obj_geo1_ID_viz1
opcf $arg1

# Node $_obj_geo1_switch10 (Sop/switch)
set _obj_geo1_switch10 = `run("opadd -e -n -v switch switch10")`
oplocate -x `$arg2 + -0.17849999999999999` -y `$arg3 + 5.1798999999999893` $_obj_geo1_switch10
chblockbegin
chadd -t 0 0 $_obj_geo1_switch10 input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../seeonly")' $_obj_geo1_switch10/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch10
opexprlanguage -s hscript $_obj_geo1_switch10
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch10
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch10
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch10
opset -p on $_obj_geo1_switch10
opcf $arg1

# Node $_obj_geo1_attribfromvolume1 (Sop/attribfromvolume)
set _obj_geo1_attribfromvolume1 = `run("opadd -e -n -v attribfromvolume attribfromvolume1")`
oplocate -x `$arg2 + 2.503603` -y `$arg3 + 55.818300000000001` $_obj_geo1_attribfromvolume1
opparm $_obj_geo1_attribfromvolume1  monoramp ( 2 ) vectorramp ( 2 )
opparm -V 18.5.408 $_obj_geo1_attribfromvolume1 name ( object ) monoramp2pos ( 1 ) monoramp2value ( 1 ) vectorramp2pos ( 1 ) vectorramp2c ( 1 1 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_attribfromvolume1
opexprlanguage -s hscript $_obj_geo1_attribfromvolume1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_attribfromvolume1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribfromvolume1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribfromvolume1
opset -p on $_obj_geo1_attribfromvolume1
opcf $arg1

# Node $_obj_geo1_attribwrangle1 (Sop/attribwrangle)
set _obj_geo1_attribwrangle1 = `run("opadd -e -n -v attribwrangle attribwrangle1")`
oplocate -x `$arg2 + -1.0471999999999999` -y `$arg3 + 4.2300999999999931` $_obj_geo1_attribwrangle1
opparm $_obj_geo1_attribwrangle1  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_attribwrangle1 snippet ( 'f@`chs("../attributename")` = @Cd;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_attribwrangle1
opexprlanguage -s hscript $_obj_geo1_attribwrangle1
opuserdata -n '___Version___' -v '' $_obj_geo1_attribwrangle1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_attribwrangle1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_attribwrangle1
opset -p on $_obj_geo1_attribwrangle1
opcf $arg1

# Node $_obj_geo1_measure1 (Sop/measure::2.0)
set _obj_geo1_measure1 = `run("opadd -e -n -v measure::2.0 measure1")`
oplocate -x `$arg2 + 3.7308029999999994` -y `$arg3 + 38.156399999999998` $_obj_geo1_measure1
opparm $_obj_geo1_measure1  colorramp ( 3 )
chblockbegin
chadd -t 0 0 $_obj_geo1_measure1 curvaturetype
chkey -t 0 -v 3 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvtype")' $_obj_geo1_measure1/curvaturetype
chblockend
opparm -V 18.5.408 $_obj_geo1_measure1 measure ( curvature ) curvaturetype ( curvaturetype ) attribname ( curvature ) totalattribname ( totalcurvature ) colorramp1c ( 0 0 1 ) colorramp2pos ( 0.5 ) colorramp2c ( 1 1 1 ) colorramp3pos ( 1 ) colorramp3c ( 1 0 0 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_measure1
opexprlanguage -s hscript $_obj_geo1_measure1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_measure1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_measure1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_measure1
opset -p on $_obj_geo1_measure1
opcf $arg1

# Node $_obj_geo1_subdivide1 (Sop/subdivide)
set _obj_geo1_subdivide1 = `run("opadd -e -n -v subdivide subdivide1")`
oplocate -x `$arg2 + 4.0726030000000009` -y `$arg3 + 23.973300000000002` $_obj_geo1_subdivide1
opparm -V 18.5.408 $_obj_geo1_subdivide1 iterations ( 8 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b on $_obj_geo1_subdivide1
opexprlanguage -s hscript $_obj_geo1_subdivide1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_subdivide1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_subdivide1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_subdivide1
opset -p on $_obj_geo1_subdivide1
opcf $arg1

# Node $_obj_geo1_switch_object (Sop/switch)
set _obj_geo1_switch_object = `run("opadd -e -n -v switch switch_object")`
oplocate -x `$arg2 + -0.061599999999999988` -y `$arg3 + 48.3339` $_obj_geo1_switch_object
chblockbegin
chadd -t 0 0 $_obj_geo1_switch_object input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enableobject")' $_obj_geo1_switch_object/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch_object
opexprlanguage -s hscript $_obj_geo1_switch_object
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch_object
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch_object
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch_object
opset -p on $_obj_geo1_switch_object
opcf $arg1

# Node $_obj_geo1_curvature_control (Sop/attribvop)
set _obj_geo1_curvature_control = `run("opadd -e -n -v attribvop curvature_control")`
oplocate -x `$arg2 + 4.2147030000000001` -y `$arg3 + 32.657600000000002` $_obj_geo1_curvature_control
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "curvaturemin"         label   "min %"         type    float         default { "0" }         range   { 0 100 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "curvaturemax"         label   "max %"         type    float         default { "100" }         range   { 0 100 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "curvatureremap"         label   "curvature remap"         type    ramp_flt         default { "2" }         range   { 1! 10 }         parmtag { "parmvop" "1" }         parmtag { "rampbasis_var" "curvatureremap_the_basis_strings" }         parmtag { "rampbasisdefault" "linear" }         parmtag { "rampfloatdefault" "1pos ( 0 ) 1value ( 0 ) 1interp ( linear ) 2pos ( 1 ) 2value ( 1 ) 2interp ( linear )" }         parmtag { "rampkeys_var" "curvatureremap_the_key_positions" }         parmtag { "rampshowcontrolsdefault" "1" }         parmtag { "rampvalues_var" "curvatureremap_the_key_values" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switchmode"         label   "switch mode"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_curvature_control
opmultiparm $_obj_geo1_curvature_control 'heightY#pos' '../heightdensityramp#pos' 'heightY#value' '../heightdensityramp#value' 'heightY#interp' '../heightdensityramp#interp' 'heightscaleY#pos' '../heightscaleramp#pos' 'heightscaleY#value' '../heightscaleramp#value' 'heightscaleY#interp' '../heightscaleramp#interp' 'heightdensityramp#pos' '../heightdensityramp#pos' 'heightdensityramp#value' '../heightdensityramp#value' 'heightdensityramp#interp' '../heightdensityramp#interp' 'heightscaleramp#pos' '../heightscaleramp#pos' 'heightscaleramp#value' '../heightscaleramp#value' 'heightscaleramp#interp' '../heightscaleramp#interp' 'heightIDramp#pos' '../heightIDramp#pos' 'heightIDramp#value' '../heightIDramp#value' 'heightIDramp#interp' '../heightIDramp#interp' 'occlusiondensityramp#pos' '../occlusiondensityramp#pos' 'occlusiondensityramp#value' '../occlusiondensityramp#value' 'occlusiondensityramp#interp' '../occlusiondensityramp#interp' 'occlusionscaleramp#pos' '../occlusionscaleramp#pos' 'occlusionscaleramp#value' '../occlusionscaleramp#value' 'occlusionscaleramp#interp' '../occlusionscaleramp#interp' 'occlusionIDramp#pos' '../occlusionIDramp#pos' 'occlusionIDramp#value' '../occlusionIDramp#value' 'occlusionIDramp#interp' '../occlusionIDramp#interp' 'curvaturedensityramp#pos' '../curvaturedensityramp#pos' 'curvaturedensityramp#value' '../curvaturedensityramp#value' 'curvaturedensityramp#interp' '../curvaturedensityramp#interp' 'curvaturescaleramp#pos' '../curvaturescaleramp#pos' 'curvaturescaleramp#value' '../curvaturescaleramp#value' 'curvaturescaleramp#interp' '../curvaturescaleramp#interp' 'curvatureIDramp#pos' '../curvatureIDramp#pos' 'curvatureIDramp#value' '../curvatureIDramp#value' 'curvatureIDramp#interp' '../curvatureIDramp#interp' 'curvatureremap#pos' '../curvatureremap#pos' 'curvatureremap#value' '../curvatureremap#value' 'curvatureremap#interp' '../curvatureremap#interp'
opparm $_obj_geo1_curvature_control  bindings ( 0 ) groupbindings ( 0 ) curvatureremap ( 2 )
chblockbegin
chadd -t 0 0 $_obj_geo1_curvature_control curvaturemin
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvaturemin")/100' $_obj_geo1_curvature_control/curvaturemin
chadd -t 0 0 $_obj_geo1_curvature_control curvaturemax
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvaturemax")/100' $_obj_geo1_curvature_control/curvaturemax
chadd -t 0 0 $_obj_geo1_curvature_control curvatureremap
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvatureremap")' $_obj_geo1_curvature_control/curvatureremap
chadd -t 0 0 $_obj_geo1_curvature_control curvatureremap1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvatureremap1pos")' $_obj_geo1_curvature_control/curvatureremap1pos
chadd -t 0 0 $_obj_geo1_curvature_control curvatureremap1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvatureremap1value")' $_obj_geo1_curvature_control/curvatureremap1value
chadd -t 0 0 $_obj_geo1_curvature_control curvatureremap1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvatureremap1interp")' $_obj_geo1_curvature_control/curvatureremap1interp
chadd -t 0 0 $_obj_geo1_curvature_control switchmode
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvaturemode")' $_obj_geo1_curvature_control/switchmode
chadd -t 0 0 $_obj_geo1_curvature_control curvatureremap2pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvatureremap2pos")' $_obj_geo1_curvature_control/curvatureremap2pos
chadd -t 0 0 $_obj_geo1_curvature_control curvatureremap2value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvatureremap2value")' $_obj_geo1_curvature_control/curvatureremap2value
chadd -t 0 0 $_obj_geo1_curvature_control curvatureremap2interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../curvatureremap2interp")' $_obj_geo1_curvature_control/curvatureremap2interp
chblockend
opparm -V 18.5.408 $_obj_geo1_curvature_control curvaturemin ( curvaturemin ) curvaturemax ( curvaturemax ) curvatureremap ( curvatureremap ) curvatureremap1pos ( curvatureremap1pos ) curvatureremap1value ( curvatureremap1value ) curvatureremap1interp ( curvatureremap1interp ) switchmode ( switchmode ) curvatureremap2pos ( curvatureremap2pos ) curvatureremap2value ( curvatureremap2value ) curvatureremap2interp ( curvatureremap2interp )
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_geo1_curvature_control
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_curvature_control
opexprlanguage -s hscript $_obj_geo1_curvature_control
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control
opcf $_obj_geo1_curvature_control

# Node $_obj_geo1_curvature_control_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_geo1_curvature_control_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + -3.4408699999999999` -y `$arg3 + -0.43231199999999997` $_obj_geo1_curvature_control_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_geometryvopglobal1
opexprlanguage -s hscript $_obj_geo1_curvature_control_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_geo1_curvature_control_geometryvopglobal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_geometryvopglobal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_geometryvopglobal1

# Node $_obj_geo1_curvature_control_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_curvature_control_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 24.994` -y `$arg3 + -1.7758799999999999` $_obj_geo1_curvature_control_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_curvature_control_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_curvature_control_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_geometryvopoutput1

# Node $_obj_geo1_curvature_control_bind1 (Vop/bind)
set _obj_geo1_curvature_control_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 20.6038` -y `$arg3 + -2.2258800000000001` $_obj_geo1_curvature_control_bind1
opparm -V 18.5.408 $_obj_geo1_curvature_control_bind1 parmname ( density ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_bind1
opexprlanguage -s hscript $_obj_geo1_curvature_control_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_bind1

# Node $_obj_geo1_curvature_control_bind2 (Vop/bind)
set _obj_geo1_curvature_control_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 5.0366900000000001` -y `$arg3 + 3.7838599999999998` $_obj_geo1_curvature_control_bind2
opparm -V 18.5.408 $_obj_geo1_curvature_control_bind2 parmname ( density ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_bind2
opexprlanguage -s hscript $_obj_geo1_curvature_control_bind2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_bind2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_bind2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_bind2

# Node $_obj_geo1_curvature_control_multiply1 (Vop/multiply)
set _obj_geo1_curvature_control_multiply1 = `run("opadd -e -n -v multiply multiply1")`
oplocate -x `$arg2 + 14.666399999999999` -y `$arg3 + 3.5192000000000001` $_obj_geo1_curvature_control_multiply1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_multiply1
opexprlanguage -s hscript $_obj_geo1_curvature_control_multiply1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_multiply1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_multiply1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_multiply1

# Node $_obj_geo1_curvature_control_fit2 (Vop/fit)
set _obj_geo1_curvature_control_fit2 = `run("opadd -e -n -v fit fit2")`
oplocate -x `$arg2 + 9.8352799999999991` -y `$arg3 + 1.3403` $_obj_geo1_curvature_control_fit2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_fit2
opexprlanguage -s hscript $_obj_geo1_curvature_control_fit2
opuserdata -n '___Version___' -v '' $_obj_geo1_curvature_control_fit2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_fit2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_fit2

# Node $_obj_geo1_curvature_control_destmin (Vop/parameter)
set _obj_geo1_curvature_control_destmin = `run("opadd -e -n -v parameter destmin")`
oplocate -x `$arg2 + 7.7417499999999997` -y `$arg3 + 2.59049` $_obj_geo1_curvature_control_destmin
opparm -V 18.5.408 $_obj_geo1_curvature_control_destmin parmname ( curvaturemin ) parmlabel ( 'min %' ) rangeflt ( 0 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_destmin
opexprlanguage -s hscript $_obj_geo1_curvature_control_destmin
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_destmin
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_destmin
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_destmin

# Node $_obj_geo1_curvature_control_destmax (Vop/parameter)
set _obj_geo1_curvature_control_destmax = `run("opadd -e -n -v parameter destmax")`
oplocate -x `$arg2 + 7.8667800000000003` -y `$arg3 + 0.89029499999999995` $_obj_geo1_curvature_control_destmax
opparm -V 18.5.408 $_obj_geo1_curvature_control_destmax parmname ( curvaturemax ) parmlabel ( 'max %' ) floatdef ( 100 ) rangeflt ( 0 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_destmax
opexprlanguage -s hscript $_obj_geo1_curvature_control_destmax
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_destmax
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_destmax
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_destmax

# Node $_obj_geo1_curvature_control_bind6 (Vop/bind)
set _obj_geo1_curvature_control_bind6 = `run("opadd -e -n -v bind bind6")`
oplocate -x `$arg2 + 19.347200000000001` -y `$arg3 + 0.23798` $_obj_geo1_curvature_control_bind6
opparm -V 18.5.408 $_obj_geo1_curvature_control_bind6 parmname ( curvatureA ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_bind6
opexprlanguage -s hscript $_obj_geo1_curvature_control_bind6
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_bind6
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_bind6
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_bind6

# Node $_obj_geo1_curvature_control_bind8 (Vop/bind)
set _obj_geo1_curvature_control_bind8 = `run("opadd -e -n -v bind bind8")`
oplocate -x `$arg2 + 2.3686699999999998` -y `$arg3 + 2.0604900000000002` $_obj_geo1_curvature_control_bind8
opparm -V 18.5.408 $_obj_geo1_curvature_control_bind8 parmname ( Cd ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_bind8
opexprlanguage -s hscript $_obj_geo1_curvature_control_bind8
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_bind8
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_bind8
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_bind8

# Node $_obj_geo1_curvature_control_ramp1 (Vop/rampparm)
set _obj_geo1_curvature_control_ramp1 = `run("opadd -e -n -v rampparm ramp1")`
oplocate -x `$arg2 + 7.4662699999999997` -y `$arg3 + -0.78976900000000005` $_obj_geo1_curvature_control_ramp1
opparm $_obj_geo1_curvature_control_ramp1  rampcolordefault ( 2 ) rampfloatdefault ( 2 )
opparm -V 18.5.408 $_obj_geo1_curvature_control_ramp1 parmname ( curvatureremap ) parmlabel ( 'curvature remap' ) ramptype ( flt ) rampcolordefault2pos ( 1 ) rampcolordefault2c ( 1 1 1 ) rampfloatdefault2pos ( 1 ) rampfloatdefault2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_ramp1
opexprlanguage -s hscript $_obj_geo1_curvature_control_ramp1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_ramp1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_ramp1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_ramp1

# Node $_obj_geo1_curvature_control_add1 (Vop/add)
set _obj_geo1_curvature_control_add1 = `run("opadd -e -n -v add add1")`
oplocate -x `$arg2 + 12.496499999999999` -y `$arg3 + -2.0758800000000002` $_obj_geo1_curvature_control_add1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_add1
opexprlanguage -s hscript $_obj_geo1_curvature_control_add1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_add1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_add1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_add1

# Node $_obj_geo1_curvature_control_switch1 (Vop/switch)
set _obj_geo1_curvature_control_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 17.103300000000001` -y `$arg3 + -1.7758799999999999` $_obj_geo1_curvature_control_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_switch1
opexprlanguage -s hscript $_obj_geo1_curvature_control_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_switch1

# Node $_obj_geo1_curvature_control_parm1 (Vop/parameter)
set _obj_geo1_curvature_control_parm1 = `run("opadd -e -n -v parameter parm1")`
oplocate -x `$arg2 + 14.459199999999999` -y `$arg3 + -5.9542299999999999` $_obj_geo1_curvature_control_parm1
opparm -V 18.5.408 $_obj_geo1_curvature_control_parm1 parmname ( switchmode ) parmlabel ( 'switch mode' ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_parm1
opexprlanguage -s hscript $_obj_geo1_curvature_control_parm1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_parm1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_parm1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_parm1

# Node $_obj_geo1_curvature_control_subtract1 (Vop/subtract)
set _obj_geo1_curvature_control_subtract1 = `run("opadd -e -n -v subtract subtract1")`
oplocate -x `$arg2 + 11.640499999999999` -y `$arg3 + -4.0007200000000003` $_obj_geo1_curvature_control_subtract1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_curvature_control_subtract1
opexprlanguage -s hscript $_obj_geo1_curvature_control_subtract1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_curvature_control_subtract1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_curvature_control_subtract1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_curvature_control_subtract1
opcf ..
opcf $_obj_geo1_curvature_control
oporder -e geometryvopglobal1 geometryvopoutput1 bind1 bind2 multiply1 fit2 destmin destmax bind6 bind8 ramp1 add1 switch1 parm1 subtract1 
opcf ..
opset -p on $_obj_geo1_curvature_control
opcf $arg1

# Node $_obj_geo1_noise_control1 (Sop/attribvop)
set _obj_geo1_noise_control1 = `run("opadd -e -n -v attribvop noise_control1")`
oplocate -x `$arg2 + 4.593202999999999` -y `$arg3 + 41.737400000000001` $_obj_geo1_noise_control1
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "noisemin"         label   "min %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "noisemax"         label   "max %"         type    float         default { "100" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "type"         label   "Noise Type"         type    string         default { "anoise" }         menu {             "pnoise"        "Perlin Noise"             "onoise"        "Original Perlin Noise"             "snoise"        "Sparse Convolution Noise"             "anoise"        "Alligator Noise"             "xnoise"        "Simplex Noise"             "correctnoise"  "Zero Centered Perlin Noise"         }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "freq"         label   "Frequency"         type    float         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "offset"         label   "Offset"         type    float         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "amp"         label   "Amplitude"         type    float         default { "1" }         range   { -1 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "rough"         label   "Roughness"         type    float         default { "0.5" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "atten"         label   "Attenuation"         type    float         default { "1" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "turb"         label   "Turbulence"         type    integer         default { "5" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "srcmin"         label   "Minimum Value In Source Range"         type    float         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "srcmax"         label   "Maximum Value In Source Range"         type    float         default { "1" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "visualize_noise"         label   "visualize noise"         type    toggle         default { "0" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "noiseremap"         label   "noise remap"         type    ramp_flt         default { "2" }         range   { 1! 10 }         parmtag { "parmvop" "1" }         parmtag { "rampbasis_var" "noiseremap_the_basis_strings" }         parmtag { "rampbasisdefault" "linear" }         parmtag { "rampfloatdefault" "1pos ( 0 ) 1value ( 0 ) 1interp ( linear ) 2pos ( 1 ) 2value ( 1 ) 2interp ( linear )" }         parmtag { "rampkeys_var" "noiseremap_the_key_positions" }         parmtag { "rampshowcontrolsdefault" "1" }         parmtag { "rampvalues_var" "noiseremap_the_key_values" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "switchmode"         label   "switch mode"         type    integer         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_geo1_noise_control1
opmultiparm $_obj_geo1_noise_control1 'noisedensity#pos' '../noisedensity#pos' 'noisedensity#value' '../noisedensity#value' 'noisedensity#interp' '../noisedensity#interp' 'noisescale#pos' '../noisescale#pos' 'noisescale#value' '../noisescale#value' 'noisescale#interp' '../noisescale#interp' 'heightY#pos' '../heightdensityramp#pos' 'heightY#value' '../heightdensityramp#value' 'heightY#interp' '../heightdensityramp#interp' 'heightscaleY#pos' '../heightscaleramp#pos' 'heightscaleY#value' '../heightscaleramp#value' 'heightscaleY#interp' '../heightscaleramp#interp' 'densitynoise#pos' '../densitynoiseramp#pos' 'densitynoise#value' '../densitynoiseramp#value' 'densitynoise#interp' '../densitynoiseramp#interp' 'scalenoise#pos' '../scalenoiseramp#pos' 'scalenoise#value' '../scalenoiseramp#value' 'scalenoise#interp' '../scalenoiseramp#interp' 'noiseIDramp#pos' '../noiseIDramp#pos' 'noiseIDramp#value' '../noiseIDramp#value' 'noiseIDramp#interp' '../noiseIDramp#interp' 'noiseremap#pos' '../noiseremap#pos' 'noiseremap#value' '../noiseremap#value' 'noiseremap#interp' '../noiseremap#interp'
opparm $_obj_geo1_noise_control1  bindings ( 0 ) groupbindings ( 0 ) noiseremap ( 2 )
chblockbegin
chadd -t 0 0 $_obj_geo1_noise_control1 noisemin
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../noisemin")/100' $_obj_geo1_noise_control1/noisemin
chadd -t 0 0 $_obj_geo1_noise_control1 noisemax
chkey -t 0 -v 100 -m 0 -a 0 -A 0 -T a  -F 'ch("../noisemax")/100' $_obj_geo1_noise_control1/noisemax
chadd -t 0 0 $_obj_geo1_noise_control1 type
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'chs("../type")' $_obj_geo1_noise_control1/type
chadd -t 0 0 $_obj_geo1_noise_control1 freq1
chkey -t 0 -v 0.01 -m 0 -a 0 -A 0 -T a  -F 'ch("../freq1")' $_obj_geo1_noise_control1/freq1
chadd -t 0 0 $_obj_geo1_noise_control1 freq2
chkey -t 0 -v 0.01 -m 0 -a 0 -A 0 -T a  -F 'ch("../freq2")' $_obj_geo1_noise_control1/freq2
chadd -t 0 0 $_obj_geo1_noise_control1 freq3
chkey -t 0 -v 0.01 -m 0 -a 0 -A 0 -T a  -F 'ch("../freq3")' $_obj_geo1_noise_control1/freq3
chadd -t 0 0 $_obj_geo1_noise_control1 offset1
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../offset1")' $_obj_geo1_noise_control1/offset1
chadd -t 0 0 $_obj_geo1_noise_control1 offset2
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../offset2")' $_obj_geo1_noise_control1/offset2
chadd -t 0 0 $_obj_geo1_noise_control1 offset3
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../offset3")' $_obj_geo1_noise_control1/offset3
chadd -t 0 0 $_obj_geo1_noise_control1 amp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../amp")' $_obj_geo1_noise_control1/amp
chadd -t 0 0 $_obj_geo1_noise_control1 rough
chkey -t 0 -v 0.5 -m 0 -a 0 -A 0 -T a  -F 'ch("../rough")' $_obj_geo1_noise_control1/rough
chadd -t 0 0 $_obj_geo1_noise_control1 turb
chkey -t 0 -v 7 -m 0 -a 0 -A 0 -T a  -F 'ch("../turb")' $_obj_geo1_noise_control1/turb
chadd -t 0 0 $_obj_geo1_noise_control1 srcmin
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../noisemininput")' $_obj_geo1_noise_control1/srcmin
chadd -t 0 0 $_obj_geo1_noise_control1 srcmax
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../noisemaxinput")' $_obj_geo1_noise_control1/srcmax
chadd -t 0 0 $_obj_geo1_noise_control1 noiseremap
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseremap")' $_obj_geo1_noise_control1/noiseremap
chadd -t 0 0 $_obj_geo1_noise_control1 noiseremap1pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseremap1pos")' $_obj_geo1_noise_control1/noiseremap1pos
chadd -t 0 0 $_obj_geo1_noise_control1 noiseremap1value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseremap1value")' $_obj_geo1_noise_control1/noiseremap1value
chadd -t 0 0 $_obj_geo1_noise_control1 noiseremap1interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseremap1interp")' $_obj_geo1_noise_control1/noiseremap1interp
chadd -t 0 0 $_obj_geo1_noise_control1 switchmode
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../noisemode")' $_obj_geo1_noise_control1/switchmode
chadd -t 0 0 $_obj_geo1_noise_control1 noiseremap2pos
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseremap2pos")' $_obj_geo1_noise_control1/noiseremap2pos
chadd -t 0 0 $_obj_geo1_noise_control1 noiseremap2value
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseremap2value")' $_obj_geo1_noise_control1/noiseremap2value
chadd -t 0 0 $_obj_geo1_noise_control1 noiseremap2interp
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseremap2interp")' $_obj_geo1_noise_control1/noiseremap2interp
chblockend
opparm -V 18.5.408 $_obj_geo1_noise_control1 noisemin ( noisemin ) noisemax ( noisemax ) type ( type ) freq ( freq1 freq2 freq3 ) offset ( offset1 offset2 offset3 ) amp ( amp ) rough ( rough ) turb ( turb ) srcmin ( srcmin ) srcmax ( srcmax ) noiseremap ( noiseremap ) noiseremap1pos ( noiseremap1pos ) noiseremap1value ( noiseremap1value ) noiseremap1interp ( noiseremap1interp ) switchmode ( switchmode ) noiseremap2pos ( noiseremap2pos ) noiseremap2value ( noiseremap2value ) noiseremap2interp ( noiseremap2interp )
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_geo1_noise_control1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_noise_control1
opexprlanguage -s hscript $_obj_geo1_noise_control1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1
opcf $_obj_geo1_noise_control1

# Node $_obj_geo1_noise_control1_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_geo1_noise_control1_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + 1.33613` -y `$arg3 + 0.57589800000000002` $_obj_geo1_noise_control1_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_geometryvopglobal1
opexprlanguage -s hscript $_obj_geo1_noise_control1_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_geo1_noise_control1_geometryvopglobal1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_geometryvopglobal1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_geometryvopglobal1

# Node $_obj_geo1_noise_control1_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_geo1_noise_control1_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 29.016500000000001` -y `$arg3 + 1.0061500000000001` $_obj_geo1_noise_control1_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_geometryvopoutput1
opexprlanguage -s hscript $_obj_geo1_noise_control1_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_geo1_noise_control1_geometryvopoutput1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_geometryvopoutput1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_geometryvopoutput1

# Node $_obj_geo1_noise_control1_bind1 (Vop/bind)
set _obj_geo1_noise_control1_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 24.666799999999999` -y `$arg3 + -0.048854000000000002` $_obj_geo1_noise_control1_bind1
opparm -V 18.5.408 $_obj_geo1_noise_control1_bind1 parmname ( density ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_bind1
opexprlanguage -s hscript $_obj_geo1_noise_control1_bind1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_bind1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_bind1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_bind1

# Node $_obj_geo1_noise_control1_bind2 (Vop/bind)
set _obj_geo1_noise_control1_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 7.9110800000000001` -y `$arg3 + 7.7066499999999998` $_obj_geo1_noise_control1_bind2
opparm -V 18.5.408 $_obj_geo1_noise_control1_bind2 parmname ( density ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_bind2
opexprlanguage -s hscript $_obj_geo1_noise_control1_bind2
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_bind2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_bind2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_bind2

# Node $_obj_geo1_noise_control1_multiply1 (Vop/multiply)
set _obj_geo1_noise_control1_multiply1 = `run("opadd -e -n -v multiply multiply1")`
oplocate -x `$arg2 + 18.060700000000001` -y `$arg3 + 7.3574200000000003` $_obj_geo1_noise_control1_multiply1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_multiply1
opexprlanguage -s hscript $_obj_geo1_noise_control1_multiply1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_multiply1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_multiply1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_multiply1

# Node $_obj_geo1_noise_control1_fit2 (Vop/fit)
set _obj_geo1_noise_control1_fit2 = `run("opadd -e -n -v fit fit2")`
oplocate -x `$arg2 + 13.1897` -y `$arg3 + 4.3671199999999999` $_obj_geo1_noise_control1_fit2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_fit2
opexprlanguage -s hscript $_obj_geo1_noise_control1_fit2
opuserdata -n '___Version___' -v '' $_obj_geo1_noise_control1_fit2
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_fit2
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_fit2

# Node $_obj_geo1_noise_control1_destmin (Vop/parameter)
set _obj_geo1_noise_control1_destmin = `run("opadd -e -n -v parameter destmin")`
oplocate -x `$arg2 + 7.6562400000000004` -y `$arg3 + 4.9700100000000003` $_obj_geo1_noise_control1_destmin
opparm -V 18.5.408 $_obj_geo1_noise_control1_destmin parmname ( noisemin ) parmlabel ( 'min %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_destmin
opexprlanguage -s hscript $_obj_geo1_noise_control1_destmin
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_destmin
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_destmin
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_destmin

# Node $_obj_geo1_noise_control1_destmax (Vop/parameter)
set _obj_geo1_noise_control1_destmax = `run("opadd -e -n -v parameter destmax")`
oplocate -x `$arg2 + 7.6562400000000004` -y `$arg3 + 2.73055` $_obj_geo1_noise_control1_destmax
opparm -V 18.5.408 $_obj_geo1_noise_control1_destmax parmname ( noisemax ) parmlabel ( 'max %' ) floatdef ( 100 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_destmax
opexprlanguage -s hscript $_obj_geo1_noise_control1_destmax
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_destmax
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_destmax
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_destmax

# Node $_obj_geo1_noise_control1_turbnoise1 (Vop/turbnoise)
set _obj_geo1_noise_control1_turbnoise1 = `run("opadd -e -n -v turbnoise turbnoise1")`
oplocate -x `$arg2 + 4.4779299999999997` -y `$arg3 + 1.24186` $_obj_geo1_noise_control1_turbnoise1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_turbnoise1
opexprlanguage -s hscript $_obj_geo1_noise_control1_turbnoise1
opuserdata -n '___Version___' -v '' $_obj_geo1_noise_control1_turbnoise1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_turbnoise1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_turbnoise1

# Node $_obj_geo1_noise_control1_type (Vop/parameter)
set _obj_geo1_noise_control1_type = `run("opadd -e -n -v parameter type")`
oplocate -x `$arg2 + 3.5918899999999998` -y `$arg3 + 2.86686` $_obj_geo1_noise_control1_type
opparm -V 18.5.408 $_obj_geo1_noise_control1_type parmname ( type ) parmlabel ( 'Noise Type' ) parmtype ( string ) stringdef ( anoise ) exportcontext ( cvex ) providemenu ( on ) menuchoices ( 'pnoise "Perlin Noise" onoise "Original Perlin Noise" snoise "Sparse Convolution Noise" anoise "Alligator Noise" xnoise "Simplex Noise" correctnoise "Zero Centered Perlin Noise" ' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_type
opexprlanguage -s hscript $_obj_geo1_noise_control1_type
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_type
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_type
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_type

# Node $_obj_geo1_noise_control1_freq (Vop/parameter)
set _obj_geo1_noise_control1_freq = `run("opadd -e -n -v parameter freq")`
oplocate -x `$arg2 + 3.79189` -y `$arg3 + 2.4668600000000001` $_obj_geo1_noise_control1_freq
opparm -V 18.5.408 $_obj_geo1_noise_control1_freq parmname ( freq ) parmlabel ( Frequency ) parmtype ( float3 ) float3def ( 1 1 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_freq
opexprlanguage -s hscript $_obj_geo1_noise_control1_freq
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_freq
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_freq
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_freq

# Node $_obj_geo1_noise_control1_offset (Vop/parameter)
set _obj_geo1_noise_control1_offset = `run("opadd -e -n -v parameter offset")`
oplocate -x `$arg2 + 3.8918900000000001` -y `$arg3 + 2.2668599999999999` $_obj_geo1_noise_control1_offset
opparm -V 18.5.408 $_obj_geo1_noise_control1_offset parmname ( offset ) parmlabel ( Offset ) parmtype ( float3 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_offset
opexprlanguage -s hscript $_obj_geo1_noise_control1_offset
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_offset
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_offset
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_offset

# Node $_obj_geo1_noise_control1_amp (Vop/parameter)
set _obj_geo1_noise_control1_amp = `run("opadd -e -n -v parameter amp")`
oplocate -x `$arg2 + 3.9918900000000002` -y `$arg3 + 2.0668600000000001` $_obj_geo1_noise_control1_amp
opparm -V 18.5.408 $_obj_geo1_noise_control1_amp parmname ( amp ) parmlabel ( Amplitude ) floatdef ( 1 ) rangeflt ( -1 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_amp
opexprlanguage -s hscript $_obj_geo1_noise_control1_amp
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_amp
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_amp
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_amp

# Node $_obj_geo1_noise_control1_rough (Vop/parameter)
set _obj_geo1_noise_control1_rough = `run("opadd -e -n -v parameter rough")`
oplocate -x `$arg2 + 4.0918900000000002` -y `$arg3 + 1.86686` $_obj_geo1_noise_control1_rough
opparm -V 18.5.408 $_obj_geo1_noise_control1_rough parmname ( rough ) parmlabel ( Roughness ) floatdef ( 0.5 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_rough
opexprlanguage -s hscript $_obj_geo1_noise_control1_rough
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_rough
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_rough
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_rough

# Node $_obj_geo1_noise_control1_atten (Vop/parameter)
set _obj_geo1_noise_control1_atten = `run("opadd -e -n -v parameter atten")`
oplocate -x `$arg2 + 4.1918899999999999` -y `$arg3 + 1.66686` $_obj_geo1_noise_control1_atten
opparm -V 18.5.408 $_obj_geo1_noise_control1_atten parmname ( atten ) parmlabel ( Attenuation ) floatdef ( 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_atten
opexprlanguage -s hscript $_obj_geo1_noise_control1_atten
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_atten
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_atten
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_atten

# Node $_obj_geo1_noise_control1_turb (Vop/parameter)
set _obj_geo1_noise_control1_turb = `run("opadd -e -n -v parameter turb")`
oplocate -x `$arg2 + 4.2918900000000004` -y `$arg3 + 1.4668600000000001` $_obj_geo1_noise_control1_turb
opparm -V 18.5.408 $_obj_geo1_noise_control1_turb parmname ( turb ) parmlabel ( Turbulence ) parmtype ( int ) intdef ( 5 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_turb
opexprlanguage -s hscript $_obj_geo1_noise_control1_turb
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_turb
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_turb
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_turb

# Node $_obj_geo1_noise_control1_fit1 (Vop/fit)
set _obj_geo1_noise_control1_fit1 = `run("opadd -e -n -v fit fit1")`
oplocate -x `$arg2 + 7.3398099999999999` -y `$arg3 + 0.401146` $_obj_geo1_noise_control1_fit1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_fit1
opexprlanguage -s hscript $_obj_geo1_noise_control1_fit1
opuserdata -n '___Version___' -v '' $_obj_geo1_noise_control1_fit1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_fit1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_fit1

# Node $_obj_geo1_noise_control1_srcmin (Vop/parameter)
set _obj_geo1_noise_control1_srcmin = `run("opadd -e -n -v parameter srcmin")`
oplocate -x `$arg2 + 6.5665199999999997` -y `$arg3 + 1.61686` $_obj_geo1_noise_control1_srcmin
opparm -V 18.5.408 $_obj_geo1_noise_control1_srcmin parmname ( srcmin ) parmlabel ( 'Minimum Value In Source Range' ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_srcmin
opexprlanguage -s hscript $_obj_geo1_noise_control1_srcmin
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_srcmin
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_srcmin
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_srcmin

# Node $_obj_geo1_noise_control1_srcmax (Vop/parameter)
set _obj_geo1_noise_control1_srcmax = `run("opadd -e -n -v parameter srcmax")`
oplocate -x `$arg2 + 6.6665200000000002` -y `$arg3 + 1.41686` $_obj_geo1_noise_control1_srcmax
opparm -V 18.5.408 $_obj_geo1_noise_control1_srcmax parmname ( srcmax ) parmlabel ( 'Maximum Value In Source Range' ) floatdef ( 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_srcmax
opexprlanguage -s hscript $_obj_geo1_noise_control1_srcmax
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_srcmax
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_srcmax
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_srcmax

# Node $_obj_geo1_noise_control1_bind6 (Vop/bind)
set _obj_geo1_noise_control1_bind6 = `run("opadd -e -n -v bind bind6")`
oplocate -x `$arg2 + 20.874199999999998` -y `$arg3 + 3.7290899999999998` $_obj_geo1_noise_control1_bind6
opparm -V 18.5.408 $_obj_geo1_noise_control1_bind6 parmname ( noiseA ) overridetype ( on ) useasparmdefiner ( on ) exportparm ( whenconnected ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_bind6
opexprlanguage -s hscript $_obj_geo1_noise_control1_bind6
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_bind6
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_bind6
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_bind6

# Node $_obj_geo1_noise_control1_ramp1 (Vop/rampparm)
set _obj_geo1_noise_control1_ramp1 = `run("opadd -e -n -v rampparm ramp1")`
oplocate -x `$arg2 + 10.3691` -y `$arg3 + 1.47753` $_obj_geo1_noise_control1_ramp1
opparm $_obj_geo1_noise_control1_ramp1  rampcolordefault ( 2 ) rampfloatdefault ( 2 )
opparm -V 18.5.408 $_obj_geo1_noise_control1_ramp1 parmname ( noiseremap ) parmlabel ( 'noise remap' ) ramptype ( flt ) rampcolordefault2pos ( 1 ) rampcolordefault2c ( 1 1 1 ) rampfloatdefault2pos ( 1 ) rampfloatdefault2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_ramp1
opexprlanguage -s hscript $_obj_geo1_noise_control1_ramp1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_ramp1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_ramp1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_ramp1

# Node $_obj_geo1_noise_control1_add1 (Vop/add)
set _obj_geo1_noise_control1_add1 = `run("opadd -e -n -v add add1")`
oplocate -x `$arg2 + 16.001999999999999` -y `$arg3 + -1.12371` $_obj_geo1_noise_control1_add1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_add1
opexprlanguage -s hscript $_obj_geo1_noise_control1_add1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_add1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_add1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_add1

# Node $_obj_geo1_noise_control1_switch1 (Vop/switch)
set _obj_geo1_noise_control1_switch1 = `run("opadd -e -n -v switch switch1")`
oplocate -x `$arg2 + 20.0702` -y `$arg3 + -1.31941` $_obj_geo1_noise_control1_switch1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_switch1
opexprlanguage -s hscript $_obj_geo1_noise_control1_switch1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_switch1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_switch1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_switch1

# Node $_obj_geo1_noise_control1_parm1 (Vop/parameter)
set _obj_geo1_noise_control1_parm1 = `run("opadd -e -n -v parameter parm1")`
oplocate -x `$arg2 + 17.426100000000002` -y `$arg3 + -5.4977499999999999` $_obj_geo1_noise_control1_parm1
opparm -V 18.5.408 $_obj_geo1_noise_control1_parm1 parmname ( switchmode ) parmlabel ( 'switch mode' ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_parm1
opexprlanguage -s hscript $_obj_geo1_noise_control1_parm1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_parm1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_parm1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_parm1

# Node $_obj_geo1_noise_control1_subtract1 (Vop/subtract)
set _obj_geo1_noise_control1_subtract1 = `run("opadd -e -n -v subtract subtract1")`
oplocate -x `$arg2 + 14.6074` -y `$arg3 + -3.5442399999999998` $_obj_geo1_noise_control1_subtract1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_geo1_noise_control1_subtract1
opexprlanguage -s hscript $_obj_geo1_noise_control1_subtract1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_noise_control1_subtract1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_noise_control1_subtract1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_noise_control1_subtract1
opcf ..
opcf $_obj_geo1_noise_control1
oporder -e geometryvopglobal1 geometryvopoutput1 bind1 bind2 multiply1 fit2 destmin destmax turbnoise1 type freq offset amp rough atten turb fit1 srcmin srcmax bind6 ramp1 add1 switch1 parm1 subtract1 
opcf ..
opset -p on $_obj_geo1_noise_control1
opcf $arg1

# Node $_obj_geo1_color4 (Sop/color)
set _obj_geo1_color4 = `run("opadd -e -n -v color color4")`
oplocate -x `$arg2 + 1.5010029999999999` -y `$arg3 + 56.818300000000001` $_obj_geo1_color4
opparm $_obj_geo1_color4  ramp ( 2 )
opparm $_obj_geo1_color4 color ( 0 0 0 ) ramp2pos ( 1 ) ramp2c ( 1 1 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b on $_obj_geo1_color4
opexprlanguage -s hscript $_obj_geo1_color4
opuserdata -n '___Version___' -v '' $_obj_geo1_color4
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_color4
opuserdata -n '___toolid___' -v 'sop_color' $_obj_geo1_color4
opset -p on $_obj_geo1_color4
opcf $arg1

# Node $_obj_geo1_object_density1 (Sop/attribwrangle)
set _obj_geo1_object_density1 = `run("opadd -e -n -v attribwrangle object_density1")`
oplocate -x `$arg2 + 19.304262999999999` -y `$arg3 + 11.407699999999998` $_obj_geo1_object_density1
opparm $_obj_geo1_object_density1  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_object_density1 snippet ( '@Cd = @occlusionA;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_object_density1
opexprlanguage -s hscript $_obj_geo1_object_density1
opuserdata -n '___Version___' -v '' $_obj_geo1_object_density1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_object_density1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_object_density1
opset -p on $_obj_geo1_object_density1
opcf $arg1

# Node $_obj_geo1_height_density (Sop/attribwrangle)
set _obj_geo1_height_density = `run("opadd -e -n -v attribwrangle height_density")`
oplocate -x `$arg2 + 9.204403000000001` -y `$arg3 + 9.039599999999993` $_obj_geo1_height_density
opparm $_obj_geo1_height_density  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_height_density snippet ( '@Cd = @heightA;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_height_density
opexprlanguage -s hscript $_obj_geo1_height_density
opuserdata -n '___Version___' -v '' $_obj_geo1_height_density
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_height_density
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_height_density
opset -p on $_obj_geo1_height_density
opcf $arg1

# Node $_obj_geo1_switch30 (Sop/switch)
set _obj_geo1_switch30 = `run("opadd -e -n -v switch switch30")`
oplocate -x `$arg2 + 0.27340300000000006` -y `$arg3 + 39.177` $_obj_geo1_switch30
chblockbegin
chadd -t 0 0 $_obj_geo1_switch30 input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../enablenoise")' $_obj_geo1_switch30/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_switch30
opexprlanguage -s hscript $_obj_geo1_switch30
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_switch30
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_switch30
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_switch30
opset -p on $_obj_geo1_switch30
opcf $arg1

# Node $_obj_geo1_uvtransform1 (Sop/uvtransform::2.0)
set _obj_geo1_uvtransform1 = `run("opadd -e -n -v uvtransform::2.0 uvtransform1")`
oplocate -x `$arg2 + 4.2461029999999997` -y `$arg3 + 24.973300000000002` $_obj_geo1_uvtransform1
chblockbegin
chadd -t 0 0 $_obj_geo1_uvtransform1 rz
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../rotateUV")' $_obj_geo1_uvtransform1/rz
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_uvtransform1
opexprlanguage -s hscript $_obj_geo1_uvtransform1
opuserdata -n '___Version___' -v '18.5.408' $_obj_geo1_uvtransform1
opuserdata -n '___toolcount___' -v '1' $_obj_geo1_uvtransform1
opuserdata -n '___toolid___' -v 'subnet' $_obj_geo1_uvtransform1
opset -p on $_obj_geo1_uvtransform1

opcf $arg1
opwire -n $_obj_geo1_switch2 -0 $_obj_geo1_attribdelete1
opcf $arg1
opwire -n $_obj_geo1_null1 -0 $_obj_geo1_init_default
opcf $arg1
opwire -n $_obj_geo1_isooffset1 -0 $_obj_geo1_color2
opcf $arg1
opwire -n $_obj_geo1_switch1 -0 $_obj_geo1_attribute1_density
opcf $arg1
opwire -n $_obj_geo1_switch1 -0 $_obj_geo1_slope_density
opcf $arg1
opwire -n $_obj_geo1_switch30 -0 $_obj_geo1_switch_noise
opwire -n $_obj_geo1_curvature_control -1 $_obj_geo1_switch_noise
opcf $arg1
opwire -n $_obj_geo1_switch_map -0 $_obj_geo1_pscale_viz
opcf $arg1
opwire -n $_obj_geo1_switch1 -0 $_obj_geo1_attribute2_density
opcf $arg1
opwire -n $_obj_geo1_switch1 -0 $_obj_geo1_map_density1
opcf $arg1
opwire -n -i 0 -0 $_obj_geo1_null1
opcf $arg1
opwire -n $_obj_geo1_density_viz -0 $_obj_geo1_switch1
opwire -n $_obj_geo1_pscale_viz -1 $_obj_geo1_switch1
opwire -n $_obj_geo1_ID_viz1 -2 $_obj_geo1_switch1
opcf $arg1
opwire -n $_obj_geo1_attribwrangle3 -0 $_obj_geo1_isooffset1
opcf $arg1
opwire -n $_obj_geo1_occlusion -0 $_obj_geo1_occlusion_control
opcf $_obj_geo1_occlusion_control
opwire -n $_obj_geo1_occlusion_control_bind1 -3 $_obj_geo1_occlusion_control_geometryvopoutput1
opwire -n $_obj_geo1_occlusion_control_switch1 -0 $_obj_geo1_occlusion_control_bind1
opwire -n $_obj_geo1_occlusion_control_bind2 -0 $_obj_geo1_occlusion_control_multiply1
opwire -n $_obj_geo1_occlusion_control_fit2 -1 $_obj_geo1_occlusion_control_multiply1
opwire -n $_obj_geo1_occlusion_control_bind8 -0 $_obj_geo1_occlusion_control_fit2
opwire -n $_obj_geo1_occlusion_control_destmin -3 $_obj_geo1_occlusion_control_fit2
opwire -n $_obj_geo1_occlusion_control_destmax -4 $_obj_geo1_occlusion_control_fit2
opwire -n $_obj_geo1_occlusion_control_fit2 -0 $_obj_geo1_occlusion_control_bind6
opwire -n $_obj_geo1_occlusion_control_parm1 -0 $_obj_geo1_occlusion_control_switch1
opwire -n $_obj_geo1_occlusion_control_multiply1 -1 $_obj_geo1_occlusion_control_switch1
opwire -n $_obj_geo1_occlusion_control_add1 -2 $_obj_geo1_occlusion_control_switch1
opwire -n $_obj_geo1_occlusion_control_subtract1 -3 $_obj_geo1_occlusion_control_switch1
opwire -n $_obj_geo1_occlusion_control_bind2 -0 $_obj_geo1_occlusion_control_add1
opwire -n $_obj_geo1_occlusion_control_fit2 -1 $_obj_geo1_occlusion_control_add1
opwire -n $_obj_geo1_occlusion_control_bind2 -0 $_obj_geo1_occlusion_control_subtract1
opwire -n $_obj_geo1_occlusion_control_fit2 -1 $_obj_geo1_occlusion_control_subtract1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_attribfromvolume1 -0 $_obj_geo1_color1
opcf $arg1
opwire -n $_obj_geo1_switch3 -0 $_obj_geo1_pointvop4
opcf $_obj_geo1_pointvop4
opwire -n $_obj_geo1_pointvop4_ramp1 -3 $_obj_geo1_pointvop4_geometryvopoutput1
opwire -n $_obj_geo1_pointvop4_bind1 -0 $_obj_geo1_pointvop4_ramp1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_switch1 -0 $_obj_geo1_object_density
opcf $arg1
opwire -n $_obj_geo1_switch1 -0 $_obj_geo1_noise_density
opcf $arg1
opwire -n $_obj_geo1_switch_map -0 $_obj_geo1_density_viz
opcf $arg1
opcf $arg1
opwire -n $_obj_geo1_attribwrangle3 -0 $_obj_geo1_color3
opcf $arg1
opwire -n $_obj_geo1_switch27 -0 $_obj_geo1_attribute1_control2
opcf $_obj_geo1_attribute1_control2
opwire -n $_obj_geo1_attribute1_control2_bind2 -3 $_obj_geo1_attribute1_control2_geometryvopoutput1
opwire -n $_obj_geo1_attribute1_control2_switch1 -0 $_obj_geo1_attribute1_control2_bind2
opwire -n $_obj_geo1_attribute1_control2_bind7 -0 $_obj_geo1_attribute1_control2_vectofloat2
opwire -n $_obj_geo1_attribute1_control2_vectofloat2 -0 $_obj_geo1_attribute1_control2_ramp2
opwire -n $_obj_geo1_attribute1_control2_bind1 -0 $_obj_geo1_attribute1_control2_multiply3
opwire -n $_obj_geo1_attribute1_control2_fit5 -1 $_obj_geo1_attribute1_control2_multiply3
opwire -n $_obj_geo1_attribute1_control2_ramp2 -0 $_obj_geo1_attribute1_control2_fit5
opwire -n $_obj_geo1_attribute1_control2_destmin2 -3 $_obj_geo1_attribute1_control2_fit5
opwire -n $_obj_geo1_attribute1_control2_destmax4 -4 $_obj_geo1_attribute1_control2_fit5
opwire -n $_obj_geo1_attribute1_control2_fit5 -0 $_obj_geo1_attribute1_control2_bind4
opwire -n $_obj_geo1_attribute1_control2_bind1 -0 $_obj_geo1_attribute1_control2_add1
opwire -n $_obj_geo1_attribute1_control2_fit5 -1 $_obj_geo1_attribute1_control2_add1
opwire -n $_obj_geo1_attribute1_control2_parm1 -0 $_obj_geo1_attribute1_control2_switch1
opwire -n $_obj_geo1_attribute1_control2_multiply3 -1 $_obj_geo1_attribute1_control2_switch1
opwire -n $_obj_geo1_attribute1_control2_add1 -2 $_obj_geo1_attribute1_control2_switch1
opwire -n $_obj_geo1_attribute1_control2_subtract1 -3 $_obj_geo1_attribute1_control2_switch1
opwire -n $_obj_geo1_attribute1_control2_bind1 -0 $_obj_geo1_attribute1_control2_subtract1
opwire -n $_obj_geo1_attribute1_control2_fit5 -1 $_obj_geo1_attribute1_control2_subtract1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_map_density_scale1 -0 $_obj_geo1_map_control
opcf $_obj_geo1_map_control
opwire -n $_obj_geo1_map_control_switch2 -3 $_obj_geo1_map_control_geometryvopoutput1
opwire -n $_obj_geo1_map_control_switch1 -0 $_obj_geo1_map_control_bind1
opwire -n $_obj_geo1_map_control_bind2 -0 $_obj_geo1_map_control_multiply1
opwire -n $_obj_geo1_map_control_fit2 -1 $_obj_geo1_map_control_multiply1
opwire -n $_obj_geo1_map_control_ramp1 -0 $_obj_geo1_map_control_fit2
opwire -n $_obj_geo1_map_control_parm1 -3 $_obj_geo1_map_control_fit2
opwire -n $_obj_geo1_map_control_parm2 -4 $_obj_geo1_map_control_fit2
opwire -n $_obj_geo1_map_control_fit2 -0 $_obj_geo1_map_control_bind8
opwire -n $_obj_geo1_map_control_floattovec1 -1 $_obj_geo1_map_control_switch2
opwire -n $_obj_geo1_map_control_bind13 -2 $_obj_geo1_map_control_switch2
opwire -n $_obj_geo1_map_control_bind1 -0 $_obj_geo1_map_control_floattovec1
opwire -n $_obj_geo1_map_control_bind1 -1 $_obj_geo1_map_control_floattovec1
opwire -n $_obj_geo1_map_control_bind1 -2 $_obj_geo1_map_control_floattovec1
opwire -n $_obj_geo1_map_control_bind7 -0 $_obj_geo1_map_control_ramp1
opwire -n $_obj_geo1_map_control_bind2 -0 $_obj_geo1_map_control_add1
opwire -n $_obj_geo1_map_control_fit2 -1 $_obj_geo1_map_control_add1
opwire -n $_obj_geo1_map_control_parm3 -0 $_obj_geo1_map_control_switch1
opwire -n $_obj_geo1_map_control_multiply1 -1 $_obj_geo1_map_control_switch1
opwire -n $_obj_geo1_map_control_add1 -2 $_obj_geo1_map_control_switch1
opwire -n $_obj_geo1_map_control_subtract1 -3 $_obj_geo1_map_control_switch1
opwire -n $_obj_geo1_map_control_bind2 -0 $_obj_geo1_map_control_subtract1
opwire -n $_obj_geo1_map_control_fit2 -1 $_obj_geo1_map_control_subtract1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_attribpromote1 -0 $_obj_geo1_switch3
opwire -n $_obj_geo1_attribblur1 -1 $_obj_geo1_switch3
opcf $arg1
opwire -n $_obj_geo1_switch_attribute1 -0 $_obj_geo1_switch27
opwire -n $_obj_geo1_occlusion_control -1 $_obj_geo1_switch27
opcf $arg1
opwire -n $_obj_geo1_uvproject1 -0 $_obj_geo1_switch9
opwire -n $_obj_geo1_switch_noise -1 $_obj_geo1_switch9
opcf $arg1
opwire -n $_obj_geo1_switch_object -0 $_obj_geo1_height_control1
opcf $_obj_geo1_height_control1
opwire -n $_obj_geo1_height_control1_bind1 -3 $_obj_geo1_height_control1_geometryvopoutput1
opwire -n $_obj_geo1_height_control1_relbbox1 -0 $_obj_geo1_height_control1_vectofloat1
opwire -n $_obj_geo1_height_control1_switch2 -0 $_obj_geo1_height_control1_bind1
opwire -n $_obj_geo1_height_control1_bind2 -0 $_obj_geo1_height_control1_multiply1
opwire -n $_obj_geo1_height_control1_fit2 -1 $_obj_geo1_height_control1_multiply1
opwire -n -o 1 $_obj_geo1_height_control1_vectofloat1 -0 $_obj_geo1_height_control1_fit1
opwire -n $_obj_geo1_height_control1_fit3 -0 $_obj_geo1_height_control1_fit2
opwire -n $_obj_geo1_height_control1_destmin -3 $_obj_geo1_height_control1_fit2
opwire -n $_obj_geo1_height_control1_destmax -4 $_obj_geo1_height_control1_fit2
opwire -n $_obj_geo1_height_control1_fit2 -0 $_obj_geo1_height_control1_bind6
opwire -n $_obj_geo1_height_control1_fit1 -0 $_obj_geo1_height_control1_ramp2
opwire -n $_obj_geo1_height_control1_ramp2 -0 $_obj_geo1_height_control1_fit3
opwire -n $_obj_geo1_height_control1_switch1 -1 $_obj_geo1_height_control1_fit3
opwire -n $_obj_geo1_height_control1_type -0 $_obj_geo1_height_control1_turbnoise1
opwire -n $_obj_geo1_height_control1_geometryvopglobal1 -1 $_obj_geo1_height_control1_turbnoise1
opwire -n $_obj_geo1_height_control1_freq -2 $_obj_geo1_height_control1_turbnoise1
opwire -n $_obj_geo1_height_control1_offset -3 $_obj_geo1_height_control1_turbnoise1
opwire -n $_obj_geo1_height_control1_amp -4 $_obj_geo1_height_control1_turbnoise1
opwire -n $_obj_geo1_height_control1_rough -5 $_obj_geo1_height_control1_turbnoise1
opwire -n $_obj_geo1_height_control1_atten -6 $_obj_geo1_height_control1_turbnoise1
opwire -n $_obj_geo1_height_control1_turb -7 $_obj_geo1_height_control1_turbnoise1
opwire -n $_obj_geo1_height_control1_turbnoise1 -0 $_obj_geo1_height_control1_fit4
opwire -n $_obj_geo1_height_control1_srcmin -1 $_obj_geo1_height_control1_fit4
opwire -n $_obj_geo1_height_control1_srcmax -2 $_obj_geo1_height_control1_fit4
opwire -n $_obj_geo1_height_control1_destmin1 -3 $_obj_geo1_height_control1_fit4
opwire -n $_obj_geo1_height_control1_destmax1 -4 $_obj_geo1_height_control1_fit4
opwire -n $_obj_geo1_height_control1_parm1 -0 $_obj_geo1_height_control1_switch1
opwire -n $_obj_geo1_height_control1_const1 -1 $_obj_geo1_height_control1_switch1
opwire -n $_obj_geo1_height_control1_fit4 -2 $_obj_geo1_height_control1_switch1
opwire -n $_obj_geo1_height_control1_bind2 -0 $_obj_geo1_height_control1_add1
opwire -n $_obj_geo1_height_control1_fit2 -1 $_obj_geo1_height_control1_add1
opwire -n $_obj_geo1_height_control1_parm2 -0 $_obj_geo1_height_control1_switch2
opwire -n $_obj_geo1_height_control1_multiply1 -1 $_obj_geo1_height_control1_switch2
opwire -n $_obj_geo1_height_control1_add1 -2 $_obj_geo1_height_control1_switch2
opwire -n $_obj_geo1_height_control1_subtract1 -3 $_obj_geo1_height_control1_switch2
opwire -n $_obj_geo1_height_control1_bind2 -0 $_obj_geo1_height_control1_subtract1
opwire -n $_obj_geo1_height_control1_fit2 -1 $_obj_geo1_height_control1_subtract1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_switch24 -0 $_obj_geo1_map_density_scale1
opcf $_obj_geo1_map_density_scale1
opwire -n -i 0 -0 $_obj_geo1_map_density_scale1_attribvop1
opwire -n -i 1 -1 $_obj_geo1_map_density_scale1_attribvop1
opwire -n -i 2 -2 $_obj_geo1_map_density_scale1_attribvop1
opwire -n -i 3 -3 $_obj_geo1_map_density_scale1_attribvop1
opcf $_obj_geo1_map_density_scale1_attribvop1
opcf ..
opcf ..
opcf $arg1
opwire -n $_obj_geo1_switch_attribute1 -0 $_obj_geo1_occlusion
opcf $_obj_geo1_occlusion
opwire -n -i 0 -0 $_obj_geo1_occlusion_normal1
opwire -n $_obj_geo1_occlusion_normal1 -0 $_obj_geo1_occlusion_attribwrangle1
opwire -n $_obj_geo1_occlusion_attribwrangle1 -0 $_obj_geo1_occlusion_attribblur1
opwire -n $_obj_geo1_occlusion_attribblur1 -0 $_obj_geo1_occlusion_attribwrangle2
opcf ..
opcf $arg1
opwire -n $_obj_geo1_switch_object -0 $_obj_geo1_switch_height
opwire -n $_obj_geo1_height_control1 -1 $_obj_geo1_switch_height
opcf $arg1
opwire -n $_obj_geo1_pointvop1 -0 $_obj_geo1_object_control1
opcf $_obj_geo1_object_control1
opwire -n $_obj_geo1_object_control1_bind2 -3 $_obj_geo1_object_control1_geometryvopoutput1
opwire -n $_obj_geo1_object_control1_switch1 -0 $_obj_geo1_object_control1_bind2
opwire -n $_obj_geo1_object_control1_bind1 -0 $_obj_geo1_object_control1_multiply3
opwire -n $_obj_geo1_object_control1_fit5 -1 $_obj_geo1_object_control1_multiply3
opwire -n $_obj_geo1_object_control1_ramp1 -0 $_obj_geo1_object_control1_fit5
opwire -n $_obj_geo1_object_control1_destmin2 -3 $_obj_geo1_object_control1_fit5
opwire -n $_obj_geo1_object_control1_destmax4 -4 $_obj_geo1_object_control1_fit5
opwire -n $_obj_geo1_object_control1_bind7 -0 $_obj_geo1_object_control1_vectofloat1
opwire -n $_obj_geo1_object_control1_fit5 -0 $_obj_geo1_object_control1_bind8
opwire -n -o 1 $_obj_geo1_object_control1_vectofloat1 -0 $_obj_geo1_object_control1_ramp1
opwire -n $_obj_geo1_object_control1_bind1 -0 $_obj_geo1_object_control1_add1
opwire -n $_obj_geo1_object_control1_fit5 -1 $_obj_geo1_object_control1_add1
opwire -n $_obj_geo1_object_control1_parm1 -0 $_obj_geo1_object_control1_switch1
opwire -n $_obj_geo1_object_control1_multiply3 -1 $_obj_geo1_object_control1_switch1
opwire -n $_obj_geo1_object_control1_add1 -2 $_obj_geo1_object_control1_switch1
opwire -n $_obj_geo1_object_control1_subtract1 -3 $_obj_geo1_object_control1_switch1
opwire -n $_obj_geo1_object_control1_bind1 -0 $_obj_geo1_object_control1_subtract1
opwire -n $_obj_geo1_object_control1_fit5 -1 $_obj_geo1_object_control1_subtract1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_switch1 -0 $_obj_geo1_object_density2
opcf $arg1
opwire -n $_obj_geo1_attribcopy1 -0 $_obj_geo1_switch2
opwire -n $_obj_geo1_attribwrangle1 -1 $_obj_geo1_switch2
opcf $arg1
opwire -n $_obj_geo1_switch27 -0 $_obj_geo1_switch_attribute2
opwire -n $_obj_geo1_attribute1_control2 -1 $_obj_geo1_switch_attribute2
opcf $arg1
opwire -n $_obj_geo1_switch_slope -0 $_obj_geo1_switch_attribute1
opwire -n $_obj_geo1_attribute1_control1 -1 $_obj_geo1_switch_attribute1
opcf $arg1
opwire -n $_obj_geo1_attribtransfer1 -0 $_obj_geo1_pointvop1
opcf $_obj_geo1_pointvop1
opwire -n $_obj_geo1_pointvop1_bind2 -3 $_obj_geo1_pointvop1_geometryvopoutput1
opwire -n $_obj_geo1_pointvop1_switch1 -0 $_obj_geo1_pointvop1_max1
opwire -n $_obj_geo1_pointvop1_vectofloat1 -1 $_obj_geo1_pointvop1_max1
opwire -n -o 6 $_obj_geo1_pointvop1_geometryvopglobal1 -0 $_obj_geo1_pointvop1_vectofloat1
opwire -n $_obj_geo1_pointvop1_bind1 -1 $_obj_geo1_pointvop1_switch1
opwire -n $_obj_geo1_pointvop1_const1 -2 $_obj_geo1_pointvop1_switch1
opwire -n $_obj_geo1_pointvop1_floattovec1 -0 $_obj_geo1_pointvop1_bind2
opwire -n $_obj_geo1_pointvop1_max1 -0 $_obj_geo1_pointvop1_floattovec1
opwire -n $_obj_geo1_pointvop1_max1 -1 $_obj_geo1_pointvop1_floattovec1
opwire -n $_obj_geo1_pointvop1_max1 -2 $_obj_geo1_pointvop1_floattovec1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_attribpromote1 -0 $_obj_geo1_attribblur1
opcf $arg1
opwire -n $_obj_geo1_switch_slope -0 $_obj_geo1_attribute1_control1
opcf $_obj_geo1_attribute1_control1
opwire -n $_obj_geo1_attribute1_control1_bind2 -3 $_obj_geo1_attribute1_control1_geometryvopoutput1
opwire -n $_obj_geo1_attribute1_control1_switch1 -0 $_obj_geo1_attribute1_control1_bind2
opwire -n $_obj_geo1_attribute1_control1_bind7 -0 $_obj_geo1_attribute1_control1_vectofloat2
opwire -n $_obj_geo1_attribute1_control1_vectofloat2 -0 $_obj_geo1_attribute1_control1_ramp2
opwire -n $_obj_geo1_attribute1_control1_bind1 -0 $_obj_geo1_attribute1_control1_multiply3
opwire -n $_obj_geo1_attribute1_control1_fit5 -1 $_obj_geo1_attribute1_control1_multiply3
opwire -n $_obj_geo1_attribute1_control1_ramp2 -0 $_obj_geo1_attribute1_control1_fit5
opwire -n $_obj_geo1_attribute1_control1_destmin2 -3 $_obj_geo1_attribute1_control1_fit5
opwire -n $_obj_geo1_attribute1_control1_destmax4 -4 $_obj_geo1_attribute1_control1_fit5
opwire -n $_obj_geo1_attribute1_control1_fit5 -0 $_obj_geo1_attribute1_control1_bind4
opwire -n $_obj_geo1_attribute1_control1_bind1 -0 $_obj_geo1_attribute1_control1_add1
opwire -n $_obj_geo1_attribute1_control1_fit5 -1 $_obj_geo1_attribute1_control1_add1
opwire -n $_obj_geo1_attribute1_control1_parm1 -0 $_obj_geo1_attribute1_control1_switch1
opwire -n $_obj_geo1_attribute1_control1_multiply3 -1 $_obj_geo1_attribute1_control1_switch1
opwire -n $_obj_geo1_attribute1_control1_add1 -2 $_obj_geo1_attribute1_control1_switch1
opwire -n $_obj_geo1_attribute1_control1_subtract1 -3 $_obj_geo1_attribute1_control1_switch1
opwire -n $_obj_geo1_attribute1_control1_bind1 -0 $_obj_geo1_attribute1_control1_subtract1
opwire -n $_obj_geo1_attribute1_control1_fit5 -1 $_obj_geo1_attribute1_control1_subtract1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_attribwrangle1 -0 $_obj_geo1_attribcopy1
opwire -n $_obj_geo1_null2 -1 $_obj_geo1_attribcopy1
opcf $arg1
opwire -n $_obj_geo1_color1 -0 $_obj_geo1_attribtransfer1
opwire -n $_obj_geo1_color3 -1 $_obj_geo1_attribtransfer1
opcf $arg1
opwire -n $_obj_geo1_attribdelete1 -0 $_obj_geo1_OUTPOUT
opcf $arg1
opwire -n $_obj_geo1_init_default -0 $_obj_geo1_attribute_by_slope1
opcf $_obj_geo1_attribute_by_slope1
opwire -n $_obj_geo1_attribute_by_slope1_bind1 -3 $_obj_geo1_attribute_by_slope1_geometryvopoutput1
opwire -n -o 8 $_obj_geo1_attribute_by_slope1_geometryvopglobal1 -0 $_obj_geo1_attribute_by_slope1_dot1
opwire -n $_obj_geo1_attribute_by_slope1_dot1 -0 $_obj_geo1_attribute_by_slope1_trig1
opwire -n $_obj_geo1_attribute_by_slope1_radtodeg1 -0 $_obj_geo1_attribute_by_slope1_fit4
opwire -n $_obj_geo1_attribute_by_slope1_srcmin -1 $_obj_geo1_attribute_by_slope1_fit4
opwire -n $_obj_geo1_attribute_by_slope1_srcmax -2 $_obj_geo1_attribute_by_slope1_fit4
opwire -n $_obj_geo1_attribute_by_slope1_trig1 -0 $_obj_geo1_attribute_by_slope1_radtodeg1
opwire -n $_obj_geo1_attribute_by_slope1_switch1 -0 $_obj_geo1_attribute_by_slope1_bind1
opwire -n $_obj_geo1_attribute_by_slope1_ramp1 -0 $_obj_geo1_attribute_by_slope1_fit5
opwire -n $_obj_geo1_attribute_by_slope1_destmin -3 $_obj_geo1_attribute_by_slope1_fit5
opwire -n $_obj_geo1_attribute_by_slope1_destmin1 -4 $_obj_geo1_attribute_by_slope1_fit5
opwire -n $_obj_geo1_attribute_by_slope1_fit5 -0 $_obj_geo1_attribute_by_slope1_multiply2
opwire -n $_obj_geo1_attribute_by_slope1_bind3 -1 $_obj_geo1_attribute_by_slope1_multiply2
opwire -n $_obj_geo1_attribute_by_slope1_fit5 -0 $_obj_geo1_attribute_by_slope1_bind5
opwire -n $_obj_geo1_attribute_by_slope1_fit4 -0 $_obj_geo1_attribute_by_slope1_ramp1
opwire -n $_obj_geo1_attribute_by_slope1_bind3 -0 $_obj_geo1_attribute_by_slope1_add1
opwire -n $_obj_geo1_attribute_by_slope1_fit5 -1 $_obj_geo1_attribute_by_slope1_add1
opwire -n $_obj_geo1_attribute_by_slope1_parm1 -0 $_obj_geo1_attribute_by_slope1_switch1
opwire -n $_obj_geo1_attribute_by_slope1_multiply2 -1 $_obj_geo1_attribute_by_slope1_switch1
opwire -n $_obj_geo1_attribute_by_slope1_add1 -2 $_obj_geo1_attribute_by_slope1_switch1
opwire -n $_obj_geo1_attribute_by_slope1_mix1 -3 $_obj_geo1_attribute_by_slope1_switch1
opwire -n $_obj_geo1_attribute_by_slope1_bind3 -0 $_obj_geo1_attribute_by_slope1_mix1
opwire -n $_obj_geo1_attribute_by_slope1_fit5 -2 $_obj_geo1_attribute_by_slope1_mix1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_measure1 -0 $_obj_geo1_attribpromote1
opcf $arg1
opwire -n $_obj_geo1_map -0 $_obj_geo1_switch24
opwire -n $_obj_geo1_map_1007 -1 $_obj_geo1_switch24
opcf $arg1
opwire -n $_obj_geo1_switch_noise -0 $_obj_geo1_uvproject1
opcf $arg1
opwire -n $_obj_geo1_switch_noise -0 $_obj_geo1_switch_map
opwire -n $_obj_geo1_map_control -1 $_obj_geo1_switch_map
opcf $arg1
opwire -n $_obj_geo1_subdivide1 -0 $_obj_geo1_map
opcf $_obj_geo1_map
opwire -n $_obj_geo1_map_switch2 -3 $_obj_geo1_map_geometryvopoutput1
opwire -n -o 7 $_obj_geo1_map_geometryvopglobal1 -0 $_obj_geo1_map_vectofloat1
opwire -n $_obj_geo1_map_vectofloat1 -0 $_obj_geo1_map_multiply1
opwire -n $_obj_geo1_map_parm1 -1 $_obj_geo1_map_multiply1
opwire -n -o 1 $_obj_geo1_map_vectofloat1 -0 $_obj_geo1_map_multiply2
opwire -n $_obj_geo1_map_parm2 -1 $_obj_geo1_map_multiply2
opwire -n $_obj_geo1_map_multiply2 -0 $_obj_geo1_map_add1
opwire -n $_obj_geo1_map_parm3 -1 $_obj_geo1_map_add1
opwire -n $_obj_geo1_map_multiply1 -0 $_obj_geo1_map_add2
opwire -n $_obj_geo1_map_parm4 -1 $_obj_geo1_map_add2
opwire -n $_obj_geo1_map_fit1 -0 $_obj_geo1_map_bind1
opwire -n $_obj_geo1_map_colormap1 -0 $_obj_geo1_map_vectofloat2
opwire -n $_obj_geo1_map_cmap -0 $_obj_geo1_map_colormap1
opwire -n $_obj_geo1_map_add2 -1 $_obj_geo1_map_colormap1
opwire -n $_obj_geo1_map_add1 -2 $_obj_geo1_map_colormap1
opwire -n $_obj_geo1_map_switch1 -0 $_obj_geo1_map_fit1
opwire -n $_obj_geo1_map_srcmin -1 $_obj_geo1_map_fit1
opwire -n $_obj_geo1_map_srcmax -2 $_obj_geo1_map_fit1
opwire -n $_obj_geo1_map_colormap1 -0 $_obj_geo1_map_vectofloat3
opwire -n $_obj_geo1_map_colormap1 -0 $_obj_geo1_map_vectofloat4
opwire -n $_obj_geo1_map_parm5 -0 $_obj_geo1_map_switch1
opwire -n $_obj_geo1_map_vectofloat2 -1 $_obj_geo1_map_switch1
opwire -n -o 1 $_obj_geo1_map_vectofloat3 -2 $_obj_geo1_map_switch1
opwire -n -o 2 $_obj_geo1_map_vectofloat4 -3 $_obj_geo1_map_switch1
opwire -n $_obj_geo1_map_floattovec1 -1 $_obj_geo1_map_switch2
opwire -n $_obj_geo1_map_colormap1 -2 $_obj_geo1_map_switch2
opwire -n $_obj_geo1_map_bind1 -0 $_obj_geo1_map_floattovec1
opwire -n $_obj_geo1_map_bind1 -1 $_obj_geo1_map_floattovec1
opwire -n $_obj_geo1_map_bind1 -2 $_obj_geo1_map_floattovec1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_subdivide1 -0 $_obj_geo1_map_1007
opcf $_obj_geo1_map_1007
opwire -n $_obj_geo1_map_1007_switch2 -3 $_obj_geo1_map_1007_geometryvopoutput1
opwire -n $_obj_geo1_map_1007_fit1 -0 $_obj_geo1_map_1007_bind1
opwire -n $_obj_geo1_map_1007_texture1 -0 $_obj_geo1_map_1007_vectofloat2
opwire -n $_obj_geo1_map_1007_switch1 -0 $_obj_geo1_map_1007_fit1
opwire -n $_obj_geo1_map_1007_srcmin -1 $_obj_geo1_map_1007_fit1
opwire -n $_obj_geo1_map_1007_srcmax -2 $_obj_geo1_map_1007_fit1
opwire -n $_obj_geo1_map_1007_texture1 -0 $_obj_geo1_map_1007_vectofloat3
opwire -n $_obj_geo1_map_1007_texture1 -0 $_obj_geo1_map_1007_vectofloat4
opwire -n $_obj_geo1_map_1007_parm5 -0 $_obj_geo1_map_1007_switch1
opwire -n $_obj_geo1_map_1007_vectofloat2 -1 $_obj_geo1_map_1007_switch1
opwire -n -o 1 $_obj_geo1_map_1007_vectofloat3 -2 $_obj_geo1_map_1007_switch1
opwire -n -o 2 $_obj_geo1_map_1007_vectofloat4 -3 $_obj_geo1_map_1007_switch1
opwire -n $_obj_geo1_map_1007_inttovec1 -1 $_obj_geo1_map_1007_texture1
opwire -n $_obj_geo1_map_1007_vectofloat1 -0 $_obj_geo1_map_1007_inttovec1
opwire -n -o 1 $_obj_geo1_map_1007_vectofloat1 -1 $_obj_geo1_map_1007_inttovec1
opwire -n $_obj_geo1_map_1007_floor1 -0 $_obj_geo1_map_1007_vectofloat1
opwire -n $_obj_geo1_map_1007_bind2 -0 $_obj_geo1_map_1007_floor1
opwire -n $_obj_geo1_map_1007_floattovec1 -1 $_obj_geo1_map_1007_switch2
opwire -n $_obj_geo1_map_1007_texture1 -2 $_obj_geo1_map_1007_switch2
opwire -n $_obj_geo1_map_1007_bind1 -0 $_obj_geo1_map_1007_floattovec1
opwire -n $_obj_geo1_map_1007_bind1 -1 $_obj_geo1_map_1007_floattovec1
opwire -n $_obj_geo1_map_1007_bind1 -2 $_obj_geo1_map_1007_floattovec1
opcf ..
opcf $arg1
opwire -n -i 1 -0 $_obj_geo1_attribwrangle3
opcf $arg1
opwire -n $_obj_geo1_init_default -0 $_obj_geo1_switch_slope
opwire -n $_obj_geo1_attribute_by_slope1 -1 $_obj_geo1_switch_slope
opcf $arg1
opwire -n $_obj_geo1_null1 -0 $_obj_geo1_null2
opcf $arg1
opwire -n $_obj_geo1_switch_map -0 $_obj_geo1_ID_viz1
opcf $_obj_geo1_ID_viz1
opwire -n $_obj_geo1_ID_viz1_ramp1 -3 $_obj_geo1_ID_viz1_geometryvopoutput1
opwire -n $_obj_geo1_ID_viz1_bind1 -0 $_obj_geo1_ID_viz1_ramp1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_switch1 -0 $_obj_geo1_switch10
opwire -n $_obj_geo1_height_density -1 $_obj_geo1_switch10
opwire -n $_obj_geo1_object_density1 -2 $_obj_geo1_switch10
opwire -n $_obj_geo1_slope_density -3 $_obj_geo1_switch10
opwire -n $_obj_geo1_attribute1_density -4 $_obj_geo1_switch10
opwire -n $_obj_geo1_attribute2_density -5 $_obj_geo1_switch10
opwire -n $_obj_geo1_object_density -6 $_obj_geo1_switch10
opwire -n $_obj_geo1_noise_density -7 $_obj_geo1_switch10
opwire -n $_obj_geo1_object_density2 -8 $_obj_geo1_switch10
opwire -n $_obj_geo1_map_density1 -9 $_obj_geo1_switch10
opcf $arg1
opwire -n $_obj_geo1_color4 -0 $_obj_geo1_attribfromvolume1
opwire -n $_obj_geo1_color2 -1 $_obj_geo1_attribfromvolume1
opcf $arg1
opwire -n $_obj_geo1_switch10 -0 $_obj_geo1_attribwrangle1
opcf $arg1
opwire -n $_obj_geo1_switch30 -0 $_obj_geo1_measure1
opcf $arg1
opwire -n $_obj_geo1_uvtransform1 -0 $_obj_geo1_subdivide1
opcf $arg1
opwire -n $_obj_geo1_switch_attribute2 -0 $_obj_geo1_switch_object
opwire -n $_obj_geo1_object_control1 -1 $_obj_geo1_switch_object
opcf $arg1
opwire -n $_obj_geo1_pointvop4 -0 $_obj_geo1_curvature_control
opcf $_obj_geo1_curvature_control
opwire -n $_obj_geo1_curvature_control_bind1 -3 $_obj_geo1_curvature_control_geometryvopoutput1
opwire -n $_obj_geo1_curvature_control_switch1 -0 $_obj_geo1_curvature_control_bind1
opwire -n $_obj_geo1_curvature_control_bind2 -0 $_obj_geo1_curvature_control_multiply1
opwire -n $_obj_geo1_curvature_control_fit2 -1 $_obj_geo1_curvature_control_multiply1
opwire -n $_obj_geo1_curvature_control_ramp1 -0 $_obj_geo1_curvature_control_fit2
opwire -n $_obj_geo1_curvature_control_destmin -3 $_obj_geo1_curvature_control_fit2
opwire -n $_obj_geo1_curvature_control_destmax -4 $_obj_geo1_curvature_control_fit2
opwire -n $_obj_geo1_curvature_control_fit2 -0 $_obj_geo1_curvature_control_bind6
opwire -n $_obj_geo1_curvature_control_bind8 -0 $_obj_geo1_curvature_control_ramp1
opwire -n $_obj_geo1_curvature_control_bind2 -0 $_obj_geo1_curvature_control_add1
opwire -n $_obj_geo1_curvature_control_fit2 -1 $_obj_geo1_curvature_control_add1
opwire -n $_obj_geo1_curvature_control_parm1 -0 $_obj_geo1_curvature_control_switch1
opwire -n $_obj_geo1_curvature_control_multiply1 -1 $_obj_geo1_curvature_control_switch1
opwire -n $_obj_geo1_curvature_control_add1 -2 $_obj_geo1_curvature_control_switch1
opwire -n $_obj_geo1_curvature_control_subtract1 -3 $_obj_geo1_curvature_control_switch1
opwire -n $_obj_geo1_curvature_control_bind2 -0 $_obj_geo1_curvature_control_subtract1
opwire -n $_obj_geo1_curvature_control_fit2 -1 $_obj_geo1_curvature_control_subtract1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_switch_height -0 $_obj_geo1_noise_control1
opcf $_obj_geo1_noise_control1
opwire -n $_obj_geo1_noise_control1_bind1 -3 $_obj_geo1_noise_control1_geometryvopoutput1
opwire -n $_obj_geo1_noise_control1_switch1 -0 $_obj_geo1_noise_control1_bind1
opwire -n $_obj_geo1_noise_control1_bind2 -0 $_obj_geo1_noise_control1_multiply1
opwire -n $_obj_geo1_noise_control1_fit2 -1 $_obj_geo1_noise_control1_multiply1
opwire -n $_obj_geo1_noise_control1_ramp1 -0 $_obj_geo1_noise_control1_fit2
opwire -n $_obj_geo1_noise_control1_destmin -3 $_obj_geo1_noise_control1_fit2
opwire -n $_obj_geo1_noise_control1_destmax -4 $_obj_geo1_noise_control1_fit2
opwire -n $_obj_geo1_noise_control1_type -0 $_obj_geo1_noise_control1_turbnoise1
opwire -n $_obj_geo1_noise_control1_geometryvopglobal1 -1 $_obj_geo1_noise_control1_turbnoise1
opwire -n $_obj_geo1_noise_control1_freq -2 $_obj_geo1_noise_control1_turbnoise1
opwire -n $_obj_geo1_noise_control1_offset -3 $_obj_geo1_noise_control1_turbnoise1
opwire -n $_obj_geo1_noise_control1_amp -4 $_obj_geo1_noise_control1_turbnoise1
opwire -n $_obj_geo1_noise_control1_rough -5 $_obj_geo1_noise_control1_turbnoise1
opwire -n $_obj_geo1_noise_control1_atten -6 $_obj_geo1_noise_control1_turbnoise1
opwire -n $_obj_geo1_noise_control1_turb -7 $_obj_geo1_noise_control1_turbnoise1
opwire -n $_obj_geo1_noise_control1_turbnoise1 -0 $_obj_geo1_noise_control1_fit1
opwire -n $_obj_geo1_noise_control1_srcmin -1 $_obj_geo1_noise_control1_fit1
opwire -n $_obj_geo1_noise_control1_srcmax -2 $_obj_geo1_noise_control1_fit1
opwire -n $_obj_geo1_noise_control1_fit2 -0 $_obj_geo1_noise_control1_bind6
opwire -n $_obj_geo1_noise_control1_fit1 -0 $_obj_geo1_noise_control1_ramp1
opwire -n $_obj_geo1_noise_control1_bind2 -0 $_obj_geo1_noise_control1_add1
opwire -n $_obj_geo1_noise_control1_fit2 -1 $_obj_geo1_noise_control1_add1
opwire -n $_obj_geo1_noise_control1_parm1 -0 $_obj_geo1_noise_control1_switch1
opwire -n $_obj_geo1_noise_control1_multiply1 -1 $_obj_geo1_noise_control1_switch1
opwire -n $_obj_geo1_noise_control1_add1 -2 $_obj_geo1_noise_control1_switch1
opwire -n $_obj_geo1_noise_control1_subtract1 -3 $_obj_geo1_noise_control1_switch1
opwire -n $_obj_geo1_noise_control1_bind2 -0 $_obj_geo1_noise_control1_subtract1
opwire -n $_obj_geo1_noise_control1_fit2 -1 $_obj_geo1_noise_control1_subtract1
opcf ..
opcf $arg1
opwire -n $_obj_geo1_switch_attribute2 -0 $_obj_geo1_color4
opcf $arg1
opwire -n $_obj_geo1_switch1 -0 $_obj_geo1_object_density1
opcf $arg1
opwire -n $_obj_geo1_switch1 -0 $_obj_geo1_height_density
opcf $arg1
opwire -n $_obj_geo1_switch_height -0 $_obj_geo1_switch30
opwire -n $_obj_geo1_noise_control1 -1 $_obj_geo1_switch30
opcf $arg1
opwire -n $_obj_geo1_switch9 -0 $_obj_geo1_uvtransform1

set oidx = 0
if ($argc >= 9 && "$arg9" != "") then
    set oidx = $arg9
endif

if ($argc >= 5 && "$arg4" != "") then
    set output = $_obj_geo1_uvtransform1
    opwire -n $output -$arg5 $arg4
endif
if ($argc >= 6 && "$arg6" != "") then
    set input = $_obj_geo1_attribdelete1
    if ($arg8) then
        opwire -n -i $arg6 -0 $input
    else
        opwire -n -o $oidx $arg6 -0 $input
    endif
endif
opcf $saved_path
'''
hou.hscript(h_preamble + h_extra_args + h_cmd)

