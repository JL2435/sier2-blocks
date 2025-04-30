import param
import pandas as pd
import panel as pn
from sier2 import Block

class SimpleTable(Block):
    """ Simple Table Viewer

    Make a tabulator to display an input table.
    """

    in_df = param.DataFrame(doc='Input pandas dataframe')
    out_df = param.DataFrame(doc='Output pandas dataframe', default=pd.DataFrame())

    def execute(self):
        self.out_df = self.in_df

    def __panel__(self):
        return pn.Param(
            self,
            parameters=['out_df'],
            widgets={'out_df': {'type': pn.widgets.Tabulator, 'page_size':20, 'pagination':'local', 'name':'DataFrame'}}
        )

class SimpleTableSelect(Block):
    """ Simple Table Selection

    Make a tabulator to display an input table.
    Pass on selections as an output.
    """

    in_df = param.DataFrame(doc='Input pandas dataframe')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    def __init__(self, *args, block_pause_execution=True, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, continue_label='Continue With Selection', **kwargs)
        self.tabulator = pn.widgets.Tabulator(pd.DataFrame(), name='DataFrame', page_size=20, pagination='local')

    # def prepare(self):
    #     if self.in_df is not None:
    #         self.tabulator.value = self.in_df
    #     else:
    #         self.tabulator.value = pd.DataFrame()

    def execute(self):
        self.out_df = self.tabulator.selected_dataframe

    def __panel__(self):
        return self.tabulator