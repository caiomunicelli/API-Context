
import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import numpy as np
import time

# Configurações
ORIGEM = {
    "host": "redis-11232.c251.east-us-mz.azure.redns.redis-cloud.com",
    "port": 11232,
    "password": "SqmeXnAz5MUR3wAqzdb2YFs8rfz5ih1a",
    "db": 0
}
DESTINO = {
    "host": "redis-17429.c262.us-east-1-3.ec2.redns.redis-cloud.com",
    "port": 17429,
    "password": "5hKERvlGvMpvycRoZWjRPCDVOrpT5ysT",
    "db": 0
}

INDEX_NAME = "document_index"
EMBEDDING_DIM = 1536  # ajuste conforme seu caso


def print_all_indexes(redis_client, nome):
    try:
        # FT._LIST retorna todos os índices
        indexes = redis_client.execute_command('FT._LIST')
        if not indexes:
            print(f"[{nome}] Nenhum índice encontrado.")
        for idx in indexes:
            idx_name = idx.decode() if isinstance(idx, bytes) else str(idx)
            try:
                info = redis_client.ft(idx_name).info()
                algorithm = info.get('algorithm', 'N/A')
                print(f"[{nome}] Índice: {idx_name} | Tipo de indexação: {algorithm}")
            except Exception as e:
                print(f"[{nome}] Índice: {idx_name} | Não foi possível obter o tipo de indexação: {e}")
    except Exception as e:
        print(f"[{nome}] Não foi possível listar índices: {e}")
    count = 0
    for _ in redis_client.scan_iter("doc:*"):
        count += 1
    print(f"[{nome}] Quantidade de registros: {count}")

from redis.commands.search.query import Query


def knn_query(redis_client, nome, query_vector, top_n=3):
    print(f"\n[{nome}] Executando consulta KNN...")
    try:
        start_time = time.time()
        base_query = (Query(f"*=>[KNN {top_n} @embedding $vec AS score]")
                      .sort_by("score")
                      .return_fields("content", "score")
                      .paging(0, top_n)
                      .dialect(2))
        query_params = {"vec": query_vector.tobytes()}
        res = redis_client.ft(INDEX_NAME).search(base_query, query_params)
        elapsed = time.time() - start_time
        print(f"[{nome}] Tempo de resposta: {elapsed:.4f} segundos. Top {top_n} resultados:")
        for doc in res.docs:
            print(f"  - Score: {doc.score}")
    except Exception as e:
        print(f"[{nome}] Erro na consulta KNN: {e}")

if __name__ == "__main__":
    r1 = redis.Redis(**ORIGEM)
    r2 = redis.Redis(**DESTINO)

    print_all_indexes(r1, "ORIGEM")
    print_all_indexes(r2, "DESTINO")

    # Gerar um único vetor de consulta e usar nos dois bancos
    query_vector = np.random.rand(EMBEDDING_DIM).astype(np.float32)
    knn_query(r1, "ORIGEM", query_vector)
    knn_query(r2, "DESTINO", query_vector)