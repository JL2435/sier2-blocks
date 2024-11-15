from ..blocks._io import LoadDataFrame
from ..blocks._holoviews import HvPoints
from ..blocks._view import SimpleTable, SimpleTable2

from sier2 import Connection
from sier2.panel import PanelDag

DOC = '''# Points chart

Load a dataframe from a file and display a Points chart.
'''

def hv_points_dag():
    """Load a dataframe from a file and display a Points chart."""

    ldf = LoadDataFrame(name='Load DataFrame')
    hp = HvPoints(name='Plot Points')

    DOC = '''# Points chart
    
    Load a dataframe from a file and display a Points chart.
    '''

    dag = PanelDag(doc=DOC, site='Chart', title='Points')
    dag.connect(ldf, hp,
        Connection('out_df', 'in_df'),
        Connection('out_kdims', 'in_kdims'),
        Connection('out_vdims', 'in_vdims'),
        Connection('out_opts', 'in_opts')
    )

    return dag

def table_view_dag():
    """Load a dataframe from file and display in a panel table."""

    ldf = LoadDataFrame(name='Load DataFrame')
    st = SimpleTable(name='View Table')
    sel_st = SimpleTable2(name='Selection')

    DOC = '''# Table viewer

    Load a dataframe from a file and display the data as a table.
    '''

    dag = PanelDag(doc=DOC, title='Table')
    dag.connect(ldf, st, Connection('out_df', 'in_df'))
    dag.connect(st, sel_st, Connection('out_df', 'in_df'))

    return dag
    

