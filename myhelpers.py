__author__ = 'abykov'


def clipRasterByPolygon(raster_path, polygon_path, output_path = None):
    polygon_extent = arcpy.Describe(polygon_path).extent
    clip_extent = "%f %f %f %f" % (
        polygon_extent.XMin,
        polygon_extent.YMin,
        polygon_extent.XMax,
        polygon_extent.YMax
    )
    #print clip_extent

    if output_path is None:
        f_dir = os.path.dirname(full_file_name)
        fn_noExt = fExt = os.path.splitext(full_file_name)[0]
        f_ext = os.path.splitext(full_file_name)[1]
        output_path = f_dir + '\\' + fn_noExt + '1.' + f_ext

    arcpy.Clip_management(
        raster_path
        , clip_extent
        , output_path
        , polygon_path
        , "-9999"
        , "ClippingGeometry"
        , "MAINTAIN_EXTENT"
    )
    return output_path

def getSquareBuffer (feature_class_path, buffer_size_in_m, output_path = None):
    import arcpy, os
    arcpy.env.overwriteOutput = True
    fc_desc = arcpy.Describe(feature_class_path)
    arcpy.env.outputCoordinateSystem = fc_desc.spatialReference

    fc = output_path
    arcpy.CreateFeatureclass_management(
        os.path.dirname(output_path),
        os.path.basename(output_path),
        "POLYLINE")
    cursor = arcpy.da.InsertCursor(fc, ["SHAPE@"])
    array = arcpy.Array(
        [
            arcpy.Point(fc_desc.extent.XMin - buffer_size_in_m, fc_desc.extent.YMin - buffer_size_in_m),
            arcpy.Point(fc_desc.extent.XMin - buffer_size_in_m, fc_desc.extent.YMax + buffer_size_in_m),
            arcpy.Point(fc_desc.extent.XMax + buffer_size_in_m, fc_desc.extent.YMax + buffer_size_in_m),
            arcpy.Point(fc_desc.extent.XMax + buffer_size_in_m, fc_desc.extent.YMin - buffer_size_in_m),
            arcpy.Point(fc_desc.extent.XMin - buffer_size_in_m, fc_desc.extent.YMin - buffer_size_in_m)
        ]
    )
    polyline = arcpy.Polyline(array)
    cursor.insertRow([polyline])
    del cursor
    return output_path

def getAvgLengthForAllShapes(feature_class_path):
    with arcpy.da.SearchCursor(feature_class_path, 'SHAPE@') as rows:
        length_sum = 0
        rows_num = 0
        for row in rows:
            length_sum += row[0].getLength('PLANAR', 'METERS')
            rows_num += 1
            #print rows_num, length_sum
        result = length_sum//rows_num
        print 'average = ', result
        return result

def getCurrentDateforFileName():
    import time
    return (time.strftime("%y%m%d"))

def getCurrentDateTimeForFileName():
    import time
    return (time.strftime("%y%m%d%H%M"))

def getCurrentDateTimeWithSecForFileName():
    import time
    return (time.strftime("%y%m%d%H%M%S"))

def getNewFilePathWithDateNoSpaces(full_file_name, def_folder = None):
    import os


    if def_folder is not None:
        fDir = def_folder
    else:
        fDir = os.path.dirname(full_file_name)
    fn_noExt = getFileNameWithNoExtentionAndPath(full_file_name)
    #os.path.splitext(os.path.basename(ffn))[0]
    fn_noExt_NoSpaces = fn_noExt.replace(' ', '')
    fExt = os.path.splitext(full_file_name)[1]
    #fDir = os.path.dirname(full_file_name)

    return fDir + '\\' +fn_noExt_NoSpaces + '_' +getCurrentDateTimeWithSecForFileName() + fExt

def getNewFilePathWithDateNoSpacesWithFixes(full_file_name, prefix = None, postfix = None):
    import os
    pref = ''
    postf = ''
    if prefix is not None:
        pref = prefix
    if postfix is not None:
        postf = prefix
    fn_noExt = getFileNameWithNoExtentionAndPath(full_file_name)
    #os.path.splitext(os.path.basename(ffn))[0]
    fn_noExt_NoSpaces = fn_noExt.replace(' ', '')
    fExt = os.path.splitext(full_file_name)[1]
    fDir = os.path.dirname(full_file_name)
    return fDir + '\\' + pref +fn_noExt_NoSpaces + postf +'_' +getCurrentDateTimeWithSecForFileName() + fExt

def o2eraseRasterFromRaster(raster_to_delete_from, raster_to_be_deleted, result_path):
    import arcpy
    from arcpy.sa import *

    s =Raster(raster_to_delete_from)
    g =Raster(raster_to_be_deleted)

    result = SetNull(~IsNull(g), s)
    result.save(result_path)

def checkGDB(gdb_path, create_if_doesnt_exists = False):
    import os
    if not arcpy.Exists(gdb_path):
        result = False
        if create_if_doesnt_exists:
            arcpy.CreateFileGDB_management(
                os.path.dirname(gdb_path),
                os.path.splitext(os.path.basename(gdb_path))[0]
                )
    else:
        result = True
    return result

def getRasterSide(raster_path, side, output_raster_path = None):
    raster = arcpy.Raster(raster_path)
    arcpy.env.overwriteOutput = True
    arcpy.env.outputCoordinateSystem = raster.spatialReference
    import os

    if side in ['south', 'bottom']:
        lowerLeft = arcpy.Point(raster.extent.XMin, raster.extent.YMin)
        numpy_raster = arcpy.RasterToNumPyArray(raster, lowerLeft, raster.width, 1)
        raster_from_numpy = arcpy.NumPyArrayToRaster(numpy_raster, lowerLeft, raster.meanCellHeight)
    elif side in ['north', 'top']:
            lowerLeft = arcpy.Point(
                raster.extent.XMin,
                raster.extent.YMax - raster.meanCellHeight
            )
            numpy_raster = arcpy.RasterToNumPyArray(raster, lowerLeft, raster.width, 1)
            raster_from_numpy = arcpy.NumPyArrayToRaster(numpy_raster, lowerLeft, raster.meanCellHeight)
    elif side in ['east', 'right']:
        lowerLeft = arcpy.Point(
            raster.extent.XMax - raster.meanCellWidth,
            raster.extent.YMin
        )
        numpy_raster = arcpy.RasterToNumPyArray(raster, lowerLeft, 1, raster.height)
        raster_from_numpy = arcpy.NumPyArrayToRaster(numpy_raster, lowerLeft, raster.meanCellHeight)
    elif side in ['west', 'left']:
        lowerLeft = arcpy.Point(
            raster.extent.XMin,
            raster.extent.YMin
        )
        numpy_raster = arcpy.RasterToNumPyArray(raster, lowerLeft, 1, raster.height)
        raster_from_numpy = arcpy.NumPyArrayToRaster(numpy_raster, lowerLeft, raster.meanCellHeight)

    else:
        print 'ERROR in GetRasterSide'
        return None

    if output_raster_path is None:
        f_dir = os.path.dirname(raster_path)
        fn_noExt = os.path.splitext(os.path.basename(raster_path))[0]
        fn_Ext = os.path.splitext(os.path.basename(raster_path))[1]
        output_raster_path = f_dir+'//'+fn_noExt+'_'+side+fn_Ext
    raster_from_numpy.save(output_raster_path)
    return output_raster_path

def getFileNameWithNoExtentionAndPath(fn):
    import os
    return os.path.splitext(os.path.basename(fn))[0]

def addNewField (ds, field_type_text, field_name, field_length, field_precision = None, field_alias = None, field_scale = None, field_is_nullable = None, field_is_required = None, toOverwrite = False):
    #print 'add'
    import arcpy
    if fieldExist(ds, field_name):
        if toOverwrite:
            arcpy.DeleteField_management(ds, [field_name])

    #print ds, field_name, field_type_text, field_length
    #arcpy.AddField_management(ds, field_name, field_type_text, "", "", field_length)
    arcpy.AddField_management(ds, field_name, field_type_text, field_precision, field_scale, field_length, field_alias, field_is_nullable, field_is_required)

def fieldExist(ds, field_name):
    #print 'fex'
    import arcpy
    field_list = arcpy.ListFields(ds, field_name)

    field_count = len(field_list)

    if (field_count == 1):
        return True
    else:
        return False

def deleteField (ds, keep_fields = None, delete_fields = None):
    #print 'del'
    import arcpy, sys
    fields = arcpy.ListFields(ds)

    if keep_fields is not None:

        if 'FID' not in keep_fields:
            keep_fields.append('FID')

        if 'Shape' not in keep_fields:
            keep_fields.append('Shape')

        dropFields = [x.name for x in fields if x.name not in keep_fields]

        print 'drop fields', dropFields

        if len(dropFields) > 0:
            arcpy.DeleteField_management(ds, dropFields)
        else:
            print 'Nothing to delete'
        #except:
            #print sys.exc_info()[0]
    else:
        keep_fields = []

        if 'FID' not in keep_fields:
            keep_fields.append('FID')

        if 'Shape' not in keep_fields:
            keep_fields.append('Shape')

        dropFields = [x.name for x in fields if x.name in delete_fields]
        print 'drop fields2', dropFields

        if len(dropFields) > 0:
            arcpy.DeleteField_management(ds, dropFields)
        else:
            print 'Nothing to delete'

def renameField(ds, field_name, new_field_name):
    is_found = False
    if field_name <> new_field_name:
        #print 'ren'
        import arcpy
        fields = arcpy.ListFields(ds)
        is_found = False
        for field in fields:
            if field.name == field_name:
                is_found = True
                field_type_text = str(field.type)
                field_length = field.length
                field_precision = field.precision
                field_scale = field.scale
                field_alias = field.aliasName
                field_is_nullable = field.isNullable
                field_is_required = field.required


        #adding a copy of field we are going to delete
        #addNewField(ds, field_type_text, new_field_name, field_length, None, None, True)
        if is_found:
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
    return is_found

def createNewFolder(folder_name, overwrite = False):
    import os
    if not overwrite:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)