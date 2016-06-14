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
        myhelpers.renameField(ds2, fields2match_ds2[key], key)
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

import fileLocations

#PARKLAND
fields_schema_ds1 = {}
fields_schema_ds1['NAME'] = 'ADDRESS'
fields_schema_ds1['OWNERSHIP'] = 'OWNERSHIP2'
fields_schema_ds1['CLASS'] = 'CLASS'
fields_schema_ds1['TYPE'] = 'TYPE'
#fields_schema_ds1['MAINTAINER'] = ''

#VACANTCITYLAND
fields_schema_ds2 = {}
fields_schema_ds2['NAME'] = 'NAME'
fields_schema_ds2['OWNERSHIP'] = 'OWNER'
fields_schema_ds2['MAINTAINER'] = 'MAINTAINER'
#fields_schema_ds2['CLASS'] = ''
#fields_schema_ds2['TYPE'] = ''

result = mergeDS(fileLocations.edm_parkland, fileLocations.edm_vacantcityland, fields_schema_ds1, fields_schema_ds2)

#TURF
fields_schema_ds3 = {}
#fields_schema_ds3['NAME'] = ''
fields_schema_ds3['OWNERSHIP'] = 'OWNER'
fields_schema_ds3['MAINTAINER'] = 'MAINTAINER'
fields_schema_ds3['CLASS'] = 'SERVICE_LE'
fields_schema_ds3['TYPE'] = 'TYPE'
result = mergeDS(result, fileLocations.edm_turf, {}, fields_schema_ds3)

#NATURAL
fields_schema_ds4 = {}
fields_schema_ds4['NAME'] = 'ADDRESS'
fields_schema_ds4['OWNERSHIP'] = 'OWNER'
fields_schema_ds4['MAINTAINER'] = 'MAINTAINER'
#fields_schema_ds4['CLASS'] = ''
fields_schema_ds4['TYPE'] = 'TYPE'
result = mergeDS(result, fileLocations.edm_naturalareas, {}, fields_schema_ds4)