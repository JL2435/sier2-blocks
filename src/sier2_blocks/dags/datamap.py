from sier2 import Connection
from sier2.panel import PanelDag

from ..blocks._io import LoadDataFrame
from ..blocks.datamap import RunUMAP, ThisNotThat

def datamap():
    """Load a dataframe and make a datamap using UMAP and thisnotthat."""
    ldf = LoadDataFrame(name='Load DataFrame')
    umap = RunUMAP(name='UMAP')
    tnt = ThisNotThat(name='TNT')

    DOC = '''# UMAP Test

    Testing
    '''

    dag = PanelDag(doc=DOC, title='UMAP')
    dag.connect(ldf, umap, Connection('out_df', 'in_arr'))
    dag.connect(umap, tnt, Connection('out_arr', 'in_map_data'))
    dag.connect(ldf, tnt, Connection('out_df', 'in_df'))

    return dag