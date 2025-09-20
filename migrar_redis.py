import numpy as np
import time
import matplotlib.pyplot as plt
import faiss

# Configurações gerais
dim = 1536                        # dimensão da embedding
nb_values = [1000, 10000, 100000] # diferentes tamanhos da base
nq = 100                          # nº de queries
k = 3                             # top-k para recall

# Intervalos de parâmetros HNSW
M_values = [16, 32]
efConstruction_values = [200, 400]
efSearch_values = [64, 200]

results = []

for nb in nb_values:
    print(f"\n=== Base com {nb} vetores ===")

    # Gera base aleatória normalizada
    xb = np.random.random((nb, dim)).astype('float32')
    xb = xb / np.linalg.norm(xb, axis=1, keepdims=True)

    # Queries
    xq = np.random.random((nq, dim)).astype('float32')
    xq = xq / np.linalg.norm(xq, axis=1, keepdims=True)

    # ----- FLAT (exato) -----
    index_flat = faiss.IndexFlatIP(dim)
    index_flat.add(xb)

    start = time.time()
    D_flat, I_flat = index_flat.search(xq, k)
    flat_time = (time.time() - start) / nq

    # ----- Testes com HNSW -----
    for m in M_values:
        for efC in efConstruction_values:
            for efS in efSearch_values:
                
                index_hnsw = faiss.IndexHNSWFlat(dim, m)
                index_hnsw.hnsw.efConstruction = efC
                index_hnsw.hnsw.efSearch = efS
                index_hnsw.add(xb)

                start = time.time()
                D_hnsw, I_hnsw = index_hnsw.search(xq, k)
                hnsw_time = (time.time() - start) / nq

                # Recall@k
                recall = np.mean([
                    len(set(I_flat[i]) & set(I_hnsw[i])) / k
                    for i in range(nq)
                ])

                print(f"M={m}, efC={efC}, efS={efS} | FLAT: {flat_time:.6f}s | HNSW: {hnsw_time:.6f}s | Recall={recall:.3f}")
                results.append((nb, m, efC, efS, flat_time, hnsw_time, recall))

# ----- Resultados consolidados -----
import pandas as pd
results_df = pd.DataFrame(results, columns=["Base", "M", "efConstruction", "efSearch", "Tempo_FLAT", "Tempo_HNSW", "Recall"])

print("\n=== RESULTADOS FINAIS ===")
print(results_df)

# Exibir gráficos médios por base
plt.figure(figsize=(12,5))

for nb in nb_values:
    subset = results_df[results_df["Base"] == nb]
    plt.plot(subset["Recall"], subset["Tempo_HNSW"], 'o-', label=f"Base {nb} vetores")

plt.xlabel("Recall@3")
plt.ylabel("Tempo médio por consulta (s)")
plt.title("Trade-off Recall vs Tempo (HNSW)")
plt.legend()
plt.show()
