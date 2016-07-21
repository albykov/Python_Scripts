__author__ = 'abykov'

def mergeDS(ds1, ds2, dsresult = None, fields2keep_ds1 = {}, fields2match_ds2 = {}, is_overlapping = False):
    import myhelpers, arcpy

    #printing datasets and function
    print 'Merging on ' + myhelpers.getFileNameWithNoExtentionAndPath(ds1) + ' and ' + myhelpers.getFileNameWithNoExtentionAndPath(ds2)

    #todo: add default values if doesnt exist

    #making a copy
    ds1copy = myhelpers.getNewFilePathWithDateNoSpaces(ds1)
    arcpy.Copy_management(ds1, ds1copy)

    #WORK WITH DS1
    #RENAME FIELDS ACCORDING SCHEMA

    if len(fields2keep_ds1) > 0:
        keep_fields = []
        for key in fields2keep_ds1.keys():
            myhelpers.renameField(ds1, fields2keep_ds1[key], key)
            keep_fields.append(key)


        keep_fields.append('FROMDS')

        #delete rest of the fields
        myhelpers.deleteField(ds1copy, keep_fields, None)

        #ADD FROMDS FIELD AND FILL IT
        #wont do that since this ds1 should already have fromDS
        #myhelpers.addNewField(ds1, 'TEXT', 'FROMDS', '50', None, None, None, None, None, True)
        #arcpy.CalculateField_management(ds1, 'FROMDS', "PARKLAND", "PYTHON_9.3")

    #WORK WITH DS2
    #ADD FROMDS FIELD AND FILL IT

    #making a copy
    ds2copy = myhelpers.getNewFilePathWithDateNoSpaces(ds2)
    arcpy.Copy_management(ds2, ds2copy)

    myhelpers.addNewField(ds2copy, 'TEXT', 'FROMDS', '50', None, None, None, None, None, True)
    fromds = myhelpers.getFileNameWithNoExtentionAndPath(ds2)
    arcpy.CalculateField_management(ds2copy, 'FROMDS', "'"+fromds+"'", "PYTHON_9.3")
    #RENAME FIELDS
    keep_fields = []
    for key in fields2match_ds2.keys():
        #if field from values is found it will be renamed
        if myhelpers.renameField(ds2copy, fields2match_ds2[key], key):
            pass
        #if field is not found, creating field from key with Unknown value

        keep_fields.append(key)

    keep_fields.append('FROMDS')

    #delete rest of the fields
    myhelpers.deleteField(ds2copy, keep_fields, None)

    result = dsresult
    #MERGE DATASETS
    if dsresult is None:
        result = myhelpers.getNewFilePathWithDateNoSpacesWithFixes(ds1, 'm_' + myhelpers.getFileNameWithNoExtentionAndPath(ds2))
    else:
        result = dsresult


    if is_overlapping:
        #merge onooverlapping

        ds1copy2 = myhelpers.getNewFilePathWithDateNoSpaces(ds1copy)

        arcpy.Erase_analysis(
            in_features=ds1copy
            , erase_features=ds2copy
            , out_feature_class=ds1copy2
            , cluster_tolerance="")

        arcpy.Merge_management(
            inputs="'"+ds1copy2+"';'"+ds2copy+"'"
            , output=result
            #myhelpers.getNewFilePathWithDateNoSpacesWithFixes(ds1, 'm_' + myhelpers.getFileNameWithNoExtentionAndPath(ds2))
            , field_mappings="")
    else:
        #merge overlaping features
        arcpy.Merge_management(
            inputs="'"+ds1copy+"';'"+ds2copy+"'"
            , output=result
            #myhelpers.getNewFilePathWithDateNoSpacesWithFixes(ds1, 'm_' + myhelpers.getFileNameWithNoExtentionAndPath(ds2))
            , field_mappings="")

    print 'Merging is Done... ' + result
    return result