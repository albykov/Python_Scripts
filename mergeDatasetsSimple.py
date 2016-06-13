__author__ = 'abykov'

def mergeDS(ds1, ds2, fields2keep_ds1 = {}, fields2match_ds2 = {}):
    import myhelpers
    #WORK WITH DS1
    #RENAME FIELDS ACCORDING SCHEMA
    for key in fields2keep_ds1.keys():
        print key
        myhelpers.renameField(ds1, fields2keep_ds1[key], key)


    #ADD FROMDS FIELD AND FILL IT

    #WORK WITH DS2
    #ADD FROMDS FIELD AND FILL IT
    #RENAME FIELDS

    #MERGE DATASETS

import fileLocations

#PARKLAND
fields_schema_ds1 = {}
fields_schema_ds1['NAME'] = 'ADDRESS'
fields_schema_ds1['CLASS'] = 'CLASS'
fields_schema_ds1['TYPE'] = 'TYPE'
fields_schema_ds1['OWNERSHIP'] = 'OWNERSHIP2'

#VACANTCITYLAND
fields_schema_ds2 = {}
fields_schema_ds2['NAME'] = 'NAME'
fields_schema_ds2['OWNERSHIP'] = 'OWNER'
#fields_schema_ds1['CLASS'] = 'CLASS'
#fields_schema_ds1['TYPE'] = 'TYPE'


mergeDS(fileLocations.edm_fc1, fileLocations.edm_fc2, fields_schema_ds1, fields_schema_ds2)
