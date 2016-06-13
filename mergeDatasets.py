__author__ = 'abykov'
def mergeDatasets(ds1, ds2, resDS, intDS):
    import arcpy
    import myhelpers

    arcpy.env.overwriteOutput = True

    #add new field fromDS
    #create fromDS name based on file name
    #

    fn1_noExt = myhelpers.getFileNameWithNoExtentionAndPath(ds1)
    fn2_noExt = myhelpers.getFileNameWithNoExtentionAndPath(ds2)

    myhelpers.addNewField(ds1, 'TEXT', 'fromDS', 50, '', '', True)
    myhelpers.addNewField(ds2, 'TEXT', 'fromDS', 50, '', '', True)

    ds1_layer = 'ds1_layer'
    arcpy.MakeFeatureLayer_management(ds1, ds1_layer)
    ds2_layer = 'ds2_layer'
    arcpy.MakeFeatureLayer_management(ds2, ds2_layer)

    arcpy.CalculateField_management(ds1_layer, 'fromDS', '"'+fn1_noExt+'"', "PYTHON_9.3")
    arcpy.CalculateField_management(ds2_layer, 'fromDS', '"'+fn2_noExt+'"', "PYTHON_9.3")

    ds1_fieldsList = arcpy.ListFields(ds1)
    ds1_fieldsListLen = len(ds1_fieldsList)
    #ds2_fieldsList = arcpy.ListFields(ds2)

    #print ds1_fieldsListLen

    arcpy.Union_analysis([ds1, ds2], intDS, "ALL")

    intDS_fieldsList = arcpy.ListFields(intDS)
    #print len(intDS_fieldsList)

    intDS_layer = 'intDS_layer'
    arcpy.MakeFeatureLayer_management(intDS, intDS_layer)

    query_text = intDS_fieldsList[ds1_fieldsListLen+1].baseName + " <> -1"
    print query_text

    arcpy.SelectLayerByAttribute_management(intDS_layer, "NEW_SELECTION", query_text)
    arcpy.CopyFeatures_management(intDS_layer, resDS)

    keep_fields = []
    myhelpers.deleteField(resDS, keep_fields, None)

mergeDatasets(r'C:\abykov\shared\projects\15_PythonTest\exclude\ds1.shp'
              , r'C:\abykov\shared\projects\15_PythonTest\exclude\ds2.shp'
              , r'C:\abykov\shared\projects\15_PythonTest\exclude\dsRes.shp'
              , r'C:\abykov\shared\projects\15_PythonTest\exclude\dsInt.shp')