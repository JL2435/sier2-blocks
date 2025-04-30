from sier2 import Info

def blocks() -> list[Info]:
    return [
        Info('sier2_blocks.blocks.io:LoadDataFrame', 'Load a dataframe from a file'),
        Info('sier2_blocks.blocks.io:SaveDataFrame', 'Save a dataframe'),
        
        Info('sier2_blocks.blocks.view:SimpleTable', 'Display a simple table'),
        Info('sier2_blocks.blocks.view:SimpleTableSelect', 'Display a simple table and pass selections on'),

        Info('sier2_blocks.blocks.holoviews:HvPoints', 'A Holoviews Points chart'),
        Info('sier2_blocks.blocks.holoviews:HvPointsSelect', 'A Holoviews Points chart that passes on selections'),
        Info('sier2_blocks.blocks.holoviews:HvHist', 'A Holoviews Histogram chart'),

        Info('sier2_blocks.blocks.test_data:StaticDataFrame', 'Static test dataframe'),
        Info('sier2_blocks.blocks.test_data:FakerData', 'Generate realistic fake data of various types'),
    ]

def dags() -> list[Info]:
    return [
        Info('sier2_blocks.dags.examples:table_view', 'Load a dataframe from file and display in a panel table'),
        Info('sier2_blocks.dags.examples:static_view', 'Load a static dataframe and display in a panel table'),
        Info('sier2_blocks.dags.examples:save_csv', 'Load and export a dataframe'),
        Info('sier2_blocks.dags.examples:hv_points', 'Load and plot a dataframe as points'),
        Info('sier2_blocks.dags.examples:hv_hist', 'Load a dataframe and plot a histogram'),
        Info('sier2_blocks.dags.examples:faker_view', 'Load and display fake data'),
    ]
