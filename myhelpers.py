__author__ = 'abykov'

def getCurrentDateforFileName():
    import time
    return (time.strftime("%y%m%d"))

def getCurrentDateTimeForFileName():
    import time
    return (time.strftime("%y%m%d%H%M"))

def getCurrentDateTimeWithSecForFileName():
    import time
    return (time.strftime("%y%m%d%H%M%S"))

def getNewFilePathWithDateNoSpaces(full_file_name):
    import os

    fn_noExt = getFileNameWithNoExtentionAndPath(full_file_name)
    #os.path.splitext(os.path.basename(ffn))[0]
    fn_noExt_NoSpaces = fn_noExt.replace(' ', '')
    fExt = os.path.splitext(full_file_name)[1]
    fDir = os.path.dirname(full_file_name)

    return fDir + '\\' +fn_noExt_NoSpaces + '_' +getCurrentDateTimeWithSecForFileName() + fExt

def getFileNameWithNoExtentionAndPath(fn):
    import os
    return os.path.splitext(os.path.basename(fn))[0]

def addNewField (ds, field_type_text, field_name, field_length, field_precision = None, field_alias = None, field_scale = None, field_is_nullable = None, field_is_required = None, toOverwrite = False):
    import arcpy
    if fieldExist(ds, field_name):
        if toOverwrite:
            arcpy.DeleteField_management(ds, [field_name])

    #print ds, field_name, field_type_text, field_length
    #arcpy.AddField_management(ds, field_name, field_type_text, "", "", field_length)
    arcpy.AddField_management(ds, field_name, field_type_text, field_precision, field_scale, field_length, field_alias, field_is_nullable, field_is_required)

def fieldExist(ds, field_name):
    import arcpy
    field_list = arcpy.ListFields(ds, field_name)

    field_count = len(field_list)

    if (field_count == 1):
        return True
    else:
        return False

def deleteField (ds, keep_fields = None, delete_fields = None):
    import arcpy
    fields = arcpy.ListFields(ds)
    if keep_fields is not None:
        dropFields = [x.name for x in fields if x.name not in keep_fields]
        arcpy.DeleteField_management(ds, dropFields)
    else:
        dropFields = [x.name for x in fields if x.name in delete_fields]
        arcpy.DeleteField_management(ds, dropFields)

def renameField(ds, field_name, new_field_name):
    import arcpy

    fields = arcpy.ListFields(ds)
    for field in fields:
        if field.name == field_name:
            field_type_text = str(field.type)
            field_length = field.length
            field_precision = field.precision
            field_scale = field.scale
            field_alias = field.aliasName
            field_is_nullable = field.isNullable
            field_is_required = field.required

    #adding a copy of field we are going to delete
    #addNewField(ds, field_type_text, new_field_name, field_length, None, None, True)
    addNewField(
        ds
        , field_type_text
        , new_field_name
        , field_length

        , field_precision
        , field_alias
        , field_scale
        , field_is_nullable
        , field_is_required
        #, field_domain
        , True
    )

    #copy data from old field
    arcpy.CalculateField_management(ds, new_field_name, "!"+field_name+"!", "PYTHON_9.3")

    #delete old field
    deleteField(ds, None, [field_name])