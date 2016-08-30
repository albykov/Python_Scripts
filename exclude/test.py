# s = r'D:\TEMP\CCTemp.gdb\CC_1_2_resS'
# res = r'C:\Users\abykov\Documents\ArcGIS\Default.gdb\rastercalc2'
#
# # Import the arcpy site package
# import arcpy, numpy
#
# # Your input floating point raster
# #raster = r'C:\temp\floating_point_raster.tif'
#
# # Convert the raster to a numpy array
# sarray = arcpy.RasterToNumPyArray(s, nodata_to_value = 0)
# rarray = arcpy.RasterToNumPyArray(res, nodata_to_value = 0)
# # Sum the array
# print sarray.sum()
# print rarray.sum()

import arcpy, numpy as np, cs_arc.py
arcpy.CheckOutExtension("Spatial")
tiles = r'D:\TEMP\test15m\db.gdb\new_fishNet_3x3'
tiles_layer = 'tiles_layer'
arcpy.MakeFeatureLayer_management(tiles, tiles_layer)

arcpy.SelectLayerByAttribute_management(
                tiles_layer,
                'NEW_SELECTION',
                '"OID" IN (1)')

with arcpy.da.SearchCursor(tiles_layer, ['OID@', 'SHAPE@']) as cursor:
    for row in cursor:
        print row[0], row[1].extent
        proc_ext = row[1].extent
f_r = r'D:\TEMP\test15m\db.gdb\testfrictionPlus05m_n'


arcpy.env.overwriteOutput = True
arcpy.env.extent = proc_ext

clipped_f_r = arcpy.gp.ExtractByMask_sa(f_r, tiles_layer, r'D:\TEMP\test15m\cl.tif')

r = arcpy.Raster(clipped_f_r)

s_np = np.ones((r.height,1))
print s_np.sum()
g_np = np.ones((r.height,1))



#
#lowerLeft = arcpy.Point(r.extent.XMin, r.extent.YMin)
# s_r = arcpy.NumPyArrayToRaster(s_np, lowerLeft, r.meanCellHeight)
# #s_r.save(r'd:\s.tif')
#
# lowerRight = arcpy.Point(r.extent.XMax, r.extent.YMin)
# g_r = arcpy.NumPyArrayToRaster(g_np, lowerRight, r.meanCellHeight)
#g_r.save(r'd:\g.tif')

# #n = arcpy.RasterToNumPyArray(r)
#
# #print numpy.ndarray.size(n)
# #print arcpy.RasterToNumPyArray(r)[:5, :5]
#
# lowerLeft = arcpy.Point(r.extent.XMin, r.extent.YMin)
# print 'x'
# x = arcpy.RasterToNumPyArray(r, arcpy.Point(r.extent.XMin, r.extent.YMin), r.width, 1)
# print 'y'
# y = arcpy.RasterToNumPyArray(r, arcpy.Point(r.extent.XMin, r.extent.YMin), 1, r.height)
# xr = arcpy.NumPyArrayToRaster(x, lowerLeft, r.meanCellHeight)
# yr = arcpy.NumPyArrayToRaster(y, lowerLeft, r.meanCellWidth)
# xr.save(r'd:\1.tif')

arcpy.CheckInExtension("Spatial")
