import pandas as pd
import networkx as nx
from tqdm import tqdm

# 데이터 불러오기
df = pd.read_csv("/data1/project/eunyi/tbi/drug_gene/cid_name/1.drug_totalnp_subacute.csv")

# Convert 'gene_list' to a Python list if it's in string format
df['gene_list'] = df['gene_list'].apply(lambda x: eval(x) if isinstance(x, str) else x)

# Create an edge list for the graph using drug-gene pairs
edges = []
for _, row in df.iterrows():
    drug = row['drug_name']
    genes = row['gene_list']
    for gene in genes:
        edges.append((drug, gene))

# Initialize a Networkx graph
G = nx.Graph()
G.add_edges_from(edges)

# Calculate Closeness Centrality with tqdm progress bar
closeness_centrality = {}
for node in tqdm(G.nodes, desc="Calculating Closeness Centrality", unit="node"):
    closeness_centrality[node] = nx.closeness_centrality(G, u=node)

# Convert to DataFrame
closeness_df = pd.DataFrame({
    "Drug_name": list(closeness_centrality.keys()),
    "Closeness Centrality": list(closeness_centrality.values())
})

# Display the DataFrame
print(closeness_df)

# Sort by Closeness Centrality
closeness_df_sorted = closeness_df.sort_values(by="Closeness Centrality", ascending=False).reset_index(drop=True)

# Display the sorted DataFrame
print(closeness_df_sorted)

# Save to CSV
closeness_df_sorted.to_csv("/data1/project/eunyi/tbi/drug_gene/cid_name/1.centrality_closeness.csv", index=False)