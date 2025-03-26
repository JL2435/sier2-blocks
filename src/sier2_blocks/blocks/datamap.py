from sier2 import Block
import param

import panel as pn
import numpy as np
import pandas as pd

from umap import UMAP
from thisnotthat import BokehPlotPane


class RunUMAP(Block):
    """Run data through UMAP to reduce dimensionality."""
    
    in_arr = param.ClassSelector(
        doc='A pandas dataframe or numpy array containing high dimensional data',
        class_=(pd.DataFrame, np.array),
    )
    in_columns = param.ListSelector(
        doc='Columns to pass to UMAP (if in_arr is a dataframe).'
    )
    in_random_state = param.Number(doc='UMAP random seed', default=42)
    in_n_components = param.Integer(doc='UMAP dimensions', default=2)
    in_min_dist = param.Number(doc='UMAP min_distance', default=0.1)
    in_n_neighbors = param.Integer(doc='UMAP n_neighbors', default=15)
    in_metric = param.Selector(doc='UMAP metric', default='euclidean', objects=[
        'euclidean',
        'manhattan',
        'chebyshev',
        'minkowski',
        'canberra',
        'braycurtis',
        'mahalanobis',
        'wminkowski',
        'seuclidean',
        'cosine',
        'correlation',
        'haversine',
        'hamming',
        'jaccard',
        'dice',
        'russelrao',
        'kulsinski',
        'll_dirichlet',
        'hellinger',
        'rogerstanimoto',
        'sokalmichener',
        'sokalsneath',
        'yule',
    ])
    in_output_format = param.Selector(
        doc='Output format (pd.DataFrame/np.array)',
        objects=['numpy', 'pandas'],
        default='numpy'
    )
    
    out_arr = param.Parameter(
        doc='Output array',
        # class_=(pd.DataFrame, np.array),
    )
    out_reducer = param.Parameter(doc='UMAP reducer')

    def __init__(self, *args, block_pause_execution=True, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, continue_label='Run UMAP', **kwargs)

    def __panel__(self):
        return pn.Param(
            self,
            parameters=[
                'in_columns', 
                'in_random_state', 
                'in_n_components', 
                'in_min_dist', 
                'in_n_neighbors', 
                'in_metric', 
                'in_output_format',
            ]
        )
        
    def prepare(self):
        if isinstance(self.in_arr, pd.DataFrame):
            self.param['in_columns'].objects = self.in_arr.columns
            self.in_columns = [c for c in self.in_arr.columns if self.in_arr[c].dtype.kind in 'iuf']
        elif isinstance(self.in_arr, np.array):
            pass
        else:
            raise NotImplementedError

    def execute(self):
        reducer = UMAP(
            n_neighbors=self.in_n_neighbors,
            min_dist=self.in_min_dist,
            n_components=self.in_n_components,
            metric=self.in_metric,
            random_state=self.in_random_state
        )
        
        if self.in_columns:
            embedding = reducer.fit_transform(self.in_arr[self.in_columns])
        else:
            embedding = reducer.fit_transform(self.in_arr)
            
        self.out_reducer = reducer
        
        if self.in_output_format == 'numpy':
            self.out_arr = embedding

        elif self.in_output_format == 'pandas':
            self.out_arr = pd.DataFrame({
                f'umap_ax_{i}': embedding[:,i] for i in range(embedding.shape[1])
            })
        else:
            raise NotImplementedError
        
class ThisNotThat(Block):
    """ This Not That datamap viewer

    Use ThisNotThat to make an interactive viewer of a datamap.
    """
    
    in_df = param.DataFrame(doc='Input dataframe containing labels and hover text')
    in_map_data = param.Array(doc='Input map data')
    in_label_col = param.Selector(doc='Input label column')
    in_hover_col = param.Selector(doc='Input hover text column')

    def __init__(self, *args, block_pause_execution=True, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, continue_label='Make TnT Plot', **kwargs)
        
        self.plot = pn.pane.Placeholder(sizing_mode='stretch_width')

    def prepare(self):
        self.param['in_label_col'].objects = self.in_df.columns
        self.param['in_hover_col'].objects = self.in_df.columns
        
    def execute(self):
        if None not in (self.in_label_col, self.in_hover_col):
            self.plot.update(BokehPlotPane(
                self.in_map_data,
                labels=self.in_df[self.in_label_col].astype(str),
                hover_text=self.in_df[self.in_hover_col].astype(str),
                sizing_mode='stretch_width',
            ))

    def __panel__(self):
        return pn.Row(
            pn.Param(
                self,
                parameters=['in_label_col', 'in_hover_col'],
            ),
            self.plot,
            sizing_mode='stretch_width',
        )


