from sier2 import Info

def blocks() -> list[Info]:
    return [
        Info('sier2_blocks.blocks.LoadDataFrame', 'Load a dataframe from a file'),
        Info('sier2_blocks.blocks.SaveDataFrame', 'Save a dataframe'),
        
        Info('sier2_blocks.blocks.SimpleTable', 'Display a simple table'),
        Info('sier2_blocks.blocks.SimpleTableSelect', 'Display a simple table and pass selections on'),

        Info('sier2_blocks.blocks.HvPoints', 'A Holoviews Points chart'),
        Info('sier2_blocks.blocks.HvPointsSelect', 'A Holoviews Points chart that passes on selections'),
        Info('sier2_blocks.blocks.HvHist', 'A Holoviews Histogram chart'),

        Info('sier2_blocks.blocks.StaticDataFrame', 'Static test dataframe'),
        Info('sier2_blocks.blocks.FakerData', 'Generate realistic fake data of various types'),

        Info('sier2_blocks.blocks.geo.ReadGeoPoints', 'Spatialize a data frame'),
        Info('sier2_blocks.blocks.geo.GeoPoints', 'Geoviews Points chart'),
        Info('sier2_blocks.blocks.geo.GeoPointsSelect', 'Geoviews Points chart that passes on selections'),
        
        Info('sier2_blocks.blocks.datamap.RunUMAP', 'Run data through UMAP to reduce dimensionality.'),
        Info('sier2_blocks.blocks.datamap.ThisNotThat', 'Show a ThisNotThat interactive plot.'),
    ]

def dags() -> list[Info]:
    return [
        Info('sier2_blocks.dags._dags.table_view', 'Load a dataframe from file and display in a panel table'),
        Info('sier2_blocks.dags._dags.static_view', 'Load a static dataframe and display in a panel table'),
        Info('sier2_blocks.dags._dags.save_csv', 'Load and export a dataframe'),
        Info('sier2_blocks.dags._dags.hv_points', 'Load and plot a dataframe as points'),
        Info('sier2_blocks.dags._dags.hv_hist', 'Load a dataframe and plot a histogram'),
        Info('sier2_blocks.dags._dags.faker_view', 'Load and display fake data'),

        # geo
        Info('sier2_blocks.dags.geo.geo_points', 'Load and plot a dataframe as geo points'),
        
        # datamap
        Info('sier2_blocks.dags.datamap.datamap', 'Load a dataframe and make a datamap'),
    ]
