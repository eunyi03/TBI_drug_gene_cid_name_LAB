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

# Calculate Betweenness Centrality with tqdm progress bar
betweenness_centrality = {}
for node in tqdm(G.nodes, desc="Calculating Betweenness Centrality", unit="node"):
    # 각 노드에 대해 개별적으로 betweenness 중심성을 계산하는 방법
    betweenness_centrality[node] = nx.betweenness_centrality(G, normalized=True).get(node, 0)

# Convert to DataFrame
betweenness_df = pd.DataFrame({
    "Drug_name": list(betweenness_centrality.keys()),
    "Betweenness Centrality": list(betweenness_centrality.values())
})

# Sort by Betweenness Centrality
betweenness_df_sorted = betweenness_df.sort_values(by="Betweenness Centrality", ascending=False).reset_index(drop=True)

# Display the sorted DataFrame
print(betweenness_df_sorted)

# Save to CSV
betweenness_df_sorted.to_csv("/data1/project/eunyi/tbi/drug_gene/cid_name/1.centrality_betweenness.csv", index=False)