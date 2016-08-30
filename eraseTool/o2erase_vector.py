import o2erase
import arcpy
import misc
import sys

# inputs
# in_feature
in_feature = arcpy.GetParameterAsText(0)
print in_feature
if_feature = r'N:\Projects\151003 Lethbridge Ecological Inventory\05- Data\Eco_Inventory.gdb\Wetlands_151111'

# clip_feature
clip_feature = arcpy.GetParameterAsText(1)
if  clip_feature == '#':
#    clip_feature = r'C:\abykov\shared\projects\151003 Lethbridge Ecological Inventory\wetlands\ArcPro\Map.gdb\dig1b'
    sys.exit("Feature class to erase from was not specified")

res_path = arcpy.GetParameterAsText(2)
if res_path == '#':
#    res_path = r'C:\abykov\shared\projects\151003 Lethbridge Ecological Inventory\wetlands\testerase.shp'
     sys.exit("Result feature class was not specified")

print '----2'
print 'in_feature:' + in_feature
print 'clip_feature:' + clip_feature
print 'res_path:' + res_path
o2erase.o2erase_vector(in_feature, clip_feature, res_path)

mxd = arcpy.mapping.MapDocument("CURRENT")
dataFrame = arcpy.mapping.ListDataFrames(mxd, "*")[0]
addLayer = arcpy.mapping.Layer(res_path)
arcpy.mapping.AddLayer(dataFrame, addLayer)
