import shapefile as shp


def ParseShapefile(filename):
    """
    Extract GPS points from a shapefile.

    Args;
      (String) filename: the address of a shapefile.
    Return:
      (list) shapePoint: a list of GPS point in the given shapefile.
    """

    # Read the shapefile and get its shape records.
    ctr = shp.Reader(filename)
    ShapeRecords = ctr.iterShapeRecords()

    # For storing GPS data of roads.
    shapePoint = []

    # Extract GPS data of major roads that are the types of 
    # 'trunk' and 'primary'.
    for sr in ShapeRecords:
        if sr.record[0] in ['trunk', 'primary']:
            shapePoint.append([])
            for point in sr.shape.points:
                shapePoint[-1].append((point[1], point[0]))


    return shapePoint


#ParseShapefile("/Users/Jason/GitHub/RoadSeftey/RoadSafety/Data/shapefile/delhi_highway/delhi_highway.shp")
