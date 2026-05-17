import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import umap

# Choose the year
year = '2026'

data = pd.read_csv(f'data/extracted_data/extracted_papers_flattened_{year}.csv')

# Preprocess
data = data[data['Name'].notna()]
names = data['Name'].values

# Encode text into embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(names, show_progress_bar=True)

# Reduce to 2D with UMAP
reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=10, min_dist=0.05)
embeddings_2d = reducer.fit_transform(embeddings)


data = data.reset_index(drop=True)
names = data[['Author_1','Author_2','Author_3','Author_4','Author_5']].values
data['authors'] = ''
for i,name in enumerate(names):
  names = name[~pd.isnull(name)]
  data.at[i, 'authors'] = ', '.join(names)
data = data.dropna(how='all', axis=0)

plot_df = pd.DataFrame({
    'x': embeddings_2d[:, 0],
    'y': embeddings_2d[:, 1],
    'year': year,
    'topic': data['Name'],
    'category': data['Category'],
    'authors': data['authors']
})

plot_df.to_csv(f'data/embeddings/embeddings_{year}.csv')
