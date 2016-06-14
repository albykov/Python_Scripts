__author__ = 'abykov'

def mergeDS(ds1, ds2, fields2keep_ds1 = {}, fields2match_ds2 = {}):
    import myhelpers, arcpy
    #todo: work with a copies of files
    #todo: add default values if doesnt exist

    #WORK WITH DS1
    #RENAME FIELDS ACCORDING SCHEMA

    if len(fields2keep_ds1) > 0:
        keep_fields = []
        for key in fields2keep_ds1.keys():
            myhelpers.renameField(ds1, fields2keep_ds1[key], key)
            keep_fields.append(key)

        keep_fields.append('FROMDS')

        #delete rest of the fields
        #print 'keep field for parkland', keep_fields
        myhelpers.deleteField(ds1, keep_fields, None)

        #ADD FROMDS FIELD AND FILL IT
        #wont do that since this ds1 should already have fromDS
        #myhelpers.addNewField(ds1, 'TEXT', 'FROMDS', '50', None, None, None, None, None, True)
        #arcpy.CalculateField_management(ds1, 'FROMDS', "PARKLAND", "PYTHON_9.3")

    #WORK WITH DS2
    #ADD FROMDS FIELD AND FILL IT
    myhelpers.addNewField(ds2, 'TEXT', 'FROMDS', '50', None, None, None, None, None, True)
    fromds = myhelpers.getFileNameWithNoExtentionAndPath(ds2)
    arcpy.CalculateField_management(ds2, 'FROMDS', "'"+fromds+"'", "PYTHON_9.3")
    #RENAME FIELDS
    keep_fields = []
    for key in fields2match_ds2.keys():
        #if field from values is found it will be renamed
        if myhelpers.renameField(ds2, fields2match_ds2[key], key):
            pass
        #if field is not found, creating field from key with Unknown value
        #else:
            #if field with key name exists, drop it and put Unknown
            #if myhelpers.fieldExist(ds2, key):


        keep_fields.append(key)

    keep_fields.append('FROMDS')

    #delete rest of the fields
    #print 'keep field for vacantland', keep_fields
    myhelpers.deleteField(ds2, keep_fields, None)

    #MERGE DATASETS
    result = myhelpers.getNewFilePathWithDateNoSpaces(ds1)
    #result = res
    arcpy.Merge_management(
        inputs="'"+ds1+"';'"+ds2+"'"
        , output = myhelpers.getNewFilePathWithDateNoSpaces(ds1)
        , field_mappings="")
    return result