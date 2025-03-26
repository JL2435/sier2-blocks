from ..blocks._io import LoadDataFrame, SaveDataFrame
from ..blocks._view import SimpleTable, SimpleTableSelect
from ..blocks._holoviews import HvPoints, HvPointsSelect, HvHist
from ..blocks._test_data import StaticDataFrame, FakerData

from sier2 import Connection
from sier2.panel import PanelDag


def hv_points():
    """Load a dataframe from a file and display a Points chart."""

    ldf = LoadDataFrame(name='Load DataFrame')
    hps = HvPointsSelect(name='Plot Points')
    st = SimpleTable(name='View Selection')

    DOC = '''# Points chart
    
    Load a dataframe from a file and display a Points chart.
    '''

    dag = PanelDag(doc=DOC, site='Chart', title='Points')
    dag.connect(ldf, hps,
        Connection('out_df', 'in_df'),
    )
    dag.connect(hps, st,
        Connection('out_df', 'in_df'),
    )

    return dag

def hv_hist():
    """Load a dataframe from a file and display a Histogram."""

    ldf = LoadDataFrame(name='Load DataFrame')
    hh = HvHist(name='Plot Histogram')

    DOC = '''# Points chart
    
    Load a dataframe from a file and display a Points chart.
    '''

    dag = PanelDag(doc=DOC, site='Chart', title='Histogram')
    dag.connect(ldf, hh,
        Connection('out_df', 'in_df'),
    )

    return dag

def table_view():
    """Load a dataframe from file and display in a panel table."""

    ldf = LoadDataFrame(name='Load DataFrame')
    st = SimpleTableSelect(name='View Table')
    sel_st = SimpleTable(name='Selection')

    DOC = '''# Table viewer

    Load a dataframe from a file and display the data as a table.
    '''

    dag = PanelDag(doc=DOC, title='Table')
    dag.connect(ldf, st, Connection('out_df', 'in_df'))
    dag.connect(st, sel_st, Connection('out_df', 'in_df'))

    return dag

def faker_view():
    """Load and display fake data."""

    fdf = FakerData(name='Fake Data')
    st = SimpleTable(name='Display')

    DOC = '''# Faker example

    Load and display fake data.
    '''

    dag = PanelDag(doc=DOC, title='Faker')
    dag.connect(fdf, st, Connection('out_data', 'in_df'))

    return dag

def static_view():
    """Load a static example dataframe and display in a table."""

    sdf = StaticDataFrame(name='Load DataFrame')
    st = SimpleTableSelect(name='View Table')
    sel_st = SimpleTable(name='Selection')

    DOC = '''# Static table viewer

    Load a static example dataframe and display the data as a table.
    '''

    dag = PanelDag(doc=DOC, title='Table')
    dag.connect(sdf, st, Connection('out_df', 'in_df'))
    dag.connect(st, sel_st, Connection('out_df', 'in_df'))

    return dag

def save_csv():
    """Load a dataframe from file and download."""
    sdf = StaticDataFrame(name='Load DataFrame')
    st = SimpleTableSelect(name='View Table')
    edf = SaveDataFrame(name='Export')

    DOC = '''# Table viewer

    Load a dataframe from file and download.
    '''

    dag = PanelDag(doc=DOC, title='Table')
    dag.connect(sdf, st, Connection('out_df', 'in_df'))
    dag.connect(st, edf, Connection('out_df', 'in_df'))

    return dag