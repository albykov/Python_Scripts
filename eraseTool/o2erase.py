# todo: work with raster?
# todo: option to leave only in_feature fields
# todo: check extension for analysis
# todo: add to tools
import arcpy


# print to console or to tool messages
def printout(msg):
    import arcpy
    print msg
    arcpy.AddMessage(msg)

def o2eraseRasterFromRaster(raster_to_delete_from, raster_to_be_deleted, result_path):
    import arcpy
    from arcpy.sa import *

    s = Raster(raster_to_delete_from)
    g = Raster(raster_to_be_deleted)

    result = SetNull(~IsNull(g), s)
    result.save(result_path)

def o2erase_vector(in_feature, clip_feature, res_path = None):
    print '----'
    print 'in_feature:' + in_feature
    print 'clip_feature:' + clip_feature
    print 'res_path:' + res_path
    import arcpy
    import os
    import misc
    arcpy.env.overwriteOutput = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    intP = "in_memory" + "\\" + "myMemoryFeature"
    #intP = arcpy.env.scratchFolder + "\\" + "myMemoryFeature.shp"

    # result
    # todo: default is next to script folder
    if res_path is None:
        # res_path = basedir + "\\erase_result.shp"
        res_path = misc.newFileName(basedir, 'erased_vector.shp')

    printout('-----Starting erase features-----')
    printout('in_feature: ' + in_feature)
    printout('clip_feature: ' + clip_feature)
    printout('res_path: ' + res_path)

    arcpy.Union_analysis(
        in_features=[in_feature, clip_feature]
        ,out_feature_class=intP
        ,join_attributes="ALL"
        ,cluster_tolerance="#"
        ,gaps="GAPS")

    in_feature_fields = []
    for f in arcpy.ListFields(in_feature):
        in_feature_fields.append(f.name)

    clip_feature_fields = []
    for f in arcpy.ListFields(clip_feature):
        clip_feature_fields.append(f.name)

    int_feature_fields = []
    for f in arcpy.ListFields(intP):
        int_feature_fields.append(f.name)

    fieldList2Show = ''
    new_fields = []

    for fname in int_feature_fields:
        if fname in in_feature_fields:
            fieldList2Show += fname + ' ' + fname + ' VISIBLE;'
        else:
            fieldList2Show += fname + ' ' + fname + ' HIDDEN;'
            new_fields.append(fname)

    fieldList2Show = fieldList2Show[:-1]

    definitionQuery = arcpy.AddFieldDelimiters('int_layer', new_fields[0])
    definitionQuery += ' >= 0 and ' + arcpy.AddFieldDelimiters('int_layer', new_fields[1]) + ' < 0'

    arcpy.MakeFeatureLayer_management(
        intP
        , 'int_layer'
        , definitionQuery
        , "#"
        , fieldList2Show
    )

    arcpy.CopyFeatures_management('int_layer', res_path, "#", "0", "0", "0")

    arcpy.Delete_management("in_memory")

    printout('-----Erase features COMPLETED!-----')


# o2erase(in_feature, clip_feature)

def o2erase_raster_by_raster(in_raster, clip_raster, res_path = None):
    import arcpy
    import os
    import misc
    arcpy.env.overwriteOutput = True
    basedir = os.path.abspath(os.path.dirname(__file__))

    int_path = "in_memory"

    # result
    # todo: default is next to script folder
    if res_path is None:
        res_path = misc.newFileName(basedir, 'erased_raster.tif')

    printout('-----Starting erase raster-----')
    printout('in_raster: ' + in_raster)
    printout('clip_raster: ' + clip_raster)
    printout('res_path: ' + res_path)

    # todo: create Null raster
    null_in_vector = int_path + '/null_in_vector'
    o2rasterBoundary(in_raster, null_in_vector)

    null_clip_vector = int_path + '/null_clip_vector'
    o2rasterBoundary(clip_raster, null_clip_vector)

    erased_vector = int_path + '\erased_vector'
    o2erase_vector(null_in_vector, null_clip_vector, erased_vector)

    arcpy.Clip_management(in_raster=in_raster
                          , rectangle='#'
                          , out_raster=res_path
                          , in_template_dataset=erased_vector
                          , nodata_value="-3.402823e+038"
                          , clipping_geometry="ClippingGeometry"
                          , maintain_clipping_extent="NO_MAINTAIN_EXTENT")

    arcpy.Delete_management("in_memory")

    printout('-----Erase features COMPLETED!-----')


def o2rasterBoundary(in_raster, res_vector = None):
    import misc

    if misc.checkLicenses(['Spatial']):

        import arcpy
        import os

        arcpy.env.overwriteOutput = True
        basedir = os.path.abspath(os.path.dirname(__file__))

        int_path = "in_memory"
        null_raster = int_path + '/raster_n1'


        # result
        # todo: default is next to script folder
        if res_vector is None:
            res_path = misc.newFileName(basedir, 'null_vector.shp')

        # in order to make rastercalc we need raster layer
        raster_layer = arcpy.mapping.Layer(in_raster)

        # making 0 valued raster
        printout('Int("'+raster_layer.longName+'"*0))')
        arcpy.gp.RasterCalculator_sa('Int("'+raster_layer.longName+'"*0))', null_raster)

        # conversion to vector
        arcpy.RasterToPolygon_conversion(in_raster=null_raster
                                         ,out_polygon_features=res_vector
                                         ,simplify="SIMPLIFY"
                                         ,raster_field="Value")

        # arcpy.Delete_management("in_memory")
        return res_vector

# dem1 = r'C:\Users\abykov\Documents\ArcGIS\Default.gdb\dem_17m_gb_lpass_Clip'
# dem2 = r'C:\abykov\prjs_data\p01_suncor_140606\vis_2045\v5\o4_180\res\1b_10m'
# o2erase_raster_by_raster(dem1, dem2)