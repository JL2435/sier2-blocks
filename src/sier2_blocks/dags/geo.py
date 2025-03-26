from sier2 import Connection
from sier2.panel import PanelDag

from ..blocks._test_data import StaticDataFrame
from ..blocks._view import SimpleTable
from ..blocks.geo import ReadGeoPoints, GeoPoints, GeoPointsSelect

def geo_points():
    sdf = StaticDataFrame(name='Load DataFrame', block_pause_execution=True)
    rgp = ReadGeoPoints(name='Spatialize DataFrame')
    gps = GeoPointsSelect(name='Plot Points')
    gp = GeoPoints(name='View Selection')
    st = SimpleTable(name='View Table')

    DOC = '''# Geo points chart
    
    Load an example dataframe and display a Geo points chart, allowing for a subset to be plotted.
    '''

    dag = PanelDag(doc=DOC, site='Chart', title='Geo Points')
    dag.connect(sdf, rgp,
        Connection('out_df', 'in_df'),
    )
    dag.connect(rgp, gps,
        Connection('out_gdf', 'in_gdf'),
    )
    dag.connect(gps, gp,
        Connection('out_gdf', 'in_gdf'),
    )
    dag.connect(gps, st,
        Connection('out_gdf', 'in_df'),
    )

    return dag