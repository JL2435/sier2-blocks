from sier2 import Info

def blocks() -> list[Info]:
    return [
        Info('sier2_blocks.blocks:LoadDataFrame', 'Load a dataframe from a file'),
        Info('sier2_blocks.blocks:SaveDataFrame', 'Save a dataframe'),
        
        Info('sier2_blocks.blocks:SimpleTable', 'Display a simple table'),
        Info('sier2_blocks.blocks:SimpleTableSelect', 'Display a simple table and pass selections on'),

        Info('sier2_blocks.blocks:HvPoints', 'A Holoviews Points chart'),
        Info('sier2_blocks.blocks:HvPointsSelect', 'A Holoviews Points chart that passes on selections'),
        Info('sier2_blocks.blocks:HvHist', 'A Holoviews Histogram chart'),

        Info('sier2_blocks.blocks:StaticDataFrame', 'Static test dataframe'),
        Info('sier2_blocks.blocks:FakerData', 'Generate realistic fake data of various types'),
    ]

def dags() -> list[Info]:
    return [
        Info('sier2_blocks.dags:table_view', 'Load a dataframe from file and display in a panel table'),
        Info('sier2_blocks.dags:static_view', 'Load a static dataframe and display in a panel table'),
        Info('sier2_blocks.dags:save_csv', 'Load and export a dataframe'),
        Info('sier2_blocks.dags:hv_points', 'Load and plot a dataframe as points'),
        Info('sier2_blocks.dags:hv_hist', 'Load a dataframe and plot a histogram'),
        Info('sier2_blocks.dags:faker_view', 'Load and display fake data'),
    ]
