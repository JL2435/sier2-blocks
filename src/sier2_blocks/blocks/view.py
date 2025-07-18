import param
import pandas as pd
import panel as pn
from sier2 import Block


class SimpleTable(Block):
    """ Simple Table Viewer

    Make a tabulator to display an input table.
    """
    
    pn.extension('tabulator')
    
    in_df = param.DataFrame(doc='Input pandas dataframe')
    in_tabulator_kwargs = param.Dict(doc='Keyword arguments passed to the tabulator display', default=dict())
    
    out_df = param.DataFrame(doc='Output pandas dataframe', default=pd.DataFrame())

    def execute(self):
        self.out_df = self.in_df

    def __panel__(self):
        # Build a dictionary of arguments for the tabulator.
        # These defaults will be overriden by in_tabulator_kwargs.
        #
        display_dict = {
            'type': pn.widgets.Tabulator, 
            'page_size':20, 
            'pagination':'local', 
            'name':'DataFrame',
        }
        display_dict.update(self.in_tabulator_kwargs)
        return pn.Param(
            self,
            parameters=['out_df'],
            widgets={'out_df': display_dict}
        )

class SimpleTableSelect(Block):
    """ Simple Table Selection

    Make a tabulator to display an input table.
    Pass on selections as an output.
    """
    
    pn.extension('tabulator')
    
    in_df = param.DataFrame(doc='Input pandas dataframe')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    def __init__(self, *args, block_pause_execution=True, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, continue_label='Continue With Selection', **kwargs)
        self.tabulator = pn.widgets.Tabulator(pd.DataFrame(), name='DataFrame', page_size=20, pagination='local')

    def prepare(self):
        if self.in_df is not None:
            self.tabulator.value = self.in_df
        else:
            self.tabulator.value = pd.DataFrame()

    def execute(self):
        self.out_df = self.tabulator.selected_dataframe

    def __panel__(self):
        return self.tabulator

class PerspectiveTable(Block):
    """Perspective Table Viewer

    Display a table in an interactive viewer.
    If block_pause_execution is set, then the table will be editable and pass on the edited version.
    """
    
    pn.extension('perspective')
    
    in_df = param.DataFrame(doc='Input pandas dataframe')
    in_columns_config = param.Dict(doc='Config to pass to Perspective, a dictionary of {column:config}')
    
    out_df = param.DataFrame(doc='Output pandas dataframe', default=pd.DataFrame())

    def __init__(self, *args, block_pause_execution=False, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, **kwargs)

        self.editable = block_pause_execution

        # We don't want to build the perspective until after we have the data,
        # otherwise it won't have any columns loaded in.
        # Instead we have an empty row that we put the perspective into.
        #
        self._perspective = pn.Row()
        self.perspective = pn.Row()
        
    def prepare(self):
        print('Preparing')
        self._perspective.clear()

        self.perspective = pn.pane.Perspective(
            self.in_df, 
            # theme='pro-dark', 
            sizing_mode='stretch_both', 
            min_height=720, 
            columns_config=self.in_columns_config,
            editable=self.editable,
        )
        
        self._perspective.append(self.perspective)

    def execute(self):
        self.out_df = self.perspective.object
        
    def __panel__(self):
        return self._perspective

class MultiPerspectiveTable(Block):
    """View tables
    Takes a dictionary of {name: dataframe} and displays them each in a tab containing a Perspective view."""
    
    in_data = param.Dict(doc='Tables to view')
    table_tabs = pn.Tabs(sizing_mode='stretch_width', closable=True)
    
    def execute(self):
        
        for name, data in self.in_data.items():
            if name not in self.table_tabs._names:
                
                # get columns with more than 10% rows populated
                if not data.empty:
                    col_summary = data.describe(include='all').T[['count']]
                    select_columns = list(col_summary[col_summary['count'] >= (0.1 * col_summary['count'].max())].index)
                    
                    # pn.pane.Perspective does not support data structures or booleans so we have to remove everything from any list, dicts, sets, tuple's and boolean objects and put as a string
                    # 
                    data = data.map(lambda x: str(x) if isinstance(x, (list, tuple, set, dict, bool)) else x)
                    data_view = pn.pane.Perspective(
                        data,
                        sizing_mode='stretch_width', 
                        min_height=600, 
                        columns=select_columns,
                    )
                    self.table_tabs.append((name, data_view))
        
    def __panel__(self):
        return self.table_tabs
