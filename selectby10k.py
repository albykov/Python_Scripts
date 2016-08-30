import arcpy
fc = r'N:\Projects\151003 Lethbridge Ecological Inventory\05- Data\o2Data\Intermediate\iPADMap_160502\model2\model2_4s.shp'

arcpy.MakeFeatureLayer_management(fc, "lyr")
i = 0
fr = 0
to = fr*i + 10000
while to < 70000:
    #arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", ' "FID" >= ' + str(0) + 'AND FID < ' + str(10000))
    #arcpy.CopyFeatures_management("lyr", r'N:\Projects\151003 Lethbridge Ecological Inventory\05- Data\o2Data\Intermediate\iPADMap_160502\modelDice2\modelOrig250_'+str(i))
    print fr
    print to
    print '---'

    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", ' "FID" >= ' + str(fr) + 'AND FID < ' + str(to))
    arcpy.CopyFeatures_management("lyr", r'N:\Projects\151003 Lethbridge Ecological Inventory\05- Data\o2Data\Intermediate\iPADMap_160502\model2\model2_4sb\model2_4s_'+str(to))

    i = i + 1
    fr = i*10000
    to = fr + 10000

    if 1<>1:
        break

# Write the selected features to a new featureclass
