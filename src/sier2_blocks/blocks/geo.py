from sier2 import Block
from sier2_blocks_config import config
import param

import panel as pn
import numpy as np

import geopandas as gpd
import geoviews as gv
import holoviews as hv
import geoviews.tile_sources as gvts

gv.extension('bokeh', inline=True)

BASEMAP_URL = config()['basemap_url']

def guess_lon_col(cols):
    """
    Given a list of columns, guess what is an acceptable longitude column name.
    """
    guess = [c for c in cols if 'lon' in c.lower()]
    if guess:
        return guess[0]

    guess = [c for c in cols if 'x' in c.lower()]
    if guess:
        return guess[0]

    return cols[0]

def guess_lat_col(cols):
    """
    Given a list of columns, guess what is an acceptable latitude column name.
    """
    guess = [c for c in cols if 'lat' in c.lower()]
    if guess:
        return guess[0]

    guess = [c for c in cols if 'y' in c.lower()]
    if guess:
        return guess[0]

    # Assume we also didn't find a longitude, so default to the second column to avoid clashes.
    #
    return cols[1]

class ReadGeoPoints(Block):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')
    in_lat_col = param.ObjectSelector(doc='Latitude column name')
    in_lon_col = param.ObjectSelector(doc='Longitude column name')
    out_gdf = param.DataFrame(doc='Output pandas dataframe')

    def __init__(self, *args, block_pause_execution=True, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, **kwargs)

    def prepare(self):
        coordinate_cols = [c for c in self.in_df.columns if self.in_df[c].dtype.kind in 'iuf']
        self.param['in_lat_col'].objects = coordinate_cols
        self.param['in_lon_col'].objects = coordinate_cols

        self.in_lat_col = guess_lat_col(coordinate_cols)
        self.in_lon_col = guess_lon_col(coordinate_cols)
        
    def execute(self):
        geometry = gpd.points_from_xy(self.in_df[self.in_lon_col], self.in_df[self.in_lat_col])
        self.out_gdf = gpd.GeoDataFrame(self.in_df, geometry=geometry)

    def __panel__(self):
        # return self.hv_pane
        return pn.Param(
            self,
            parameters=[
                'in_lat_col',
                'in_lon_col',
            ]
        )

class GeoPoints(Block):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_gdf = param.DataFrame(doc='A geo pandas dataframe containing a location column')
    out_gdf = param.DataFrame(doc='Output geo pandas dataframe')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if BASEMAP_URL is not None:
            self.map = gv.WMTS(BASEMAP_URL).opts(active_tools=['wheel_zoom'])
        else:
            self.map = gvts.CartoMidnight().opts(active_tools=['wheel_zoom'])

        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width', min_height=600)#'scale_both')
        self.hv_pane.object=self._produce_plot
    
    @param.depends('in_gdf')
    def _produce_plot(self):
        if self.in_gdf is not None:
            plot = self.map * gv.Points(self.in_gdf)
        else:
            plot = self.map

        return plot

    def execute(self):
        self.out_gdf = self.in_gdf

    def __panel__(self):
        return self.hv_pane

class GeoPointsSelect(Block):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_gdf = param.DataFrame(doc='A geo pandas dataframe containing a location column')
    out_gdf = param.DataFrame(doc='Output geo pandas dataframe')

    def __init__(self, *args, block_pause_execution=True, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, **kwargs)

        if BASEMAP_URL is not None:
            self.map = gv.WMTS(BASEMAP_URL).opts(
                tools=['box_select', 'lasso_select'],
                active_tools=['wheel_zoom'],
            )
        else:
            self.map = gvts.CartoMidnight().opts(
                tools=['box_select', 'lasso_select'],
                active_tools=['wheel_zoom'],
            )

        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width', min_height=600)#'scale_both')
        self.selection = hv.streams.Selection1D()
        self.hv_pane.object = self._produce_plot
    
    @param.depends('in_gdf')
    def _produce_plot(self):
        if self.in_gdf is not None:
            plot = self.map * gv.Points(self.in_gdf)
        else:
            plot = self.map

        self.selection.source = plot
        return plot

    def execute(self):
        print(self.selection.index)
        self.out_gdf = self.in_gdf.loc[self.selection.index]

    def __panel__(self):
        return self.hv_pane