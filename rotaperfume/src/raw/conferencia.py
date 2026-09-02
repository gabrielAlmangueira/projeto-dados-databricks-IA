# Databricks notebook source
"""Conferência de chegada dos arquivos raw no Volume do Unity Catalog."""

from datetime import datetime, timezone

EXPECTED_FILES = {
    "erp": ("produtos.csv", "pedidos.csv", "itens_pedido.csv", "pagamentos.csv", "estoque.csv"),
    "crm": ("clientes.csv", "vendedores.csv", "carteira.csv", "oportunidades.csv", "visitas.csv"),
}


def _file_metrics(dbutils, spark, path: str) -> tuple[int, int]:
    parent, filename = path.rsplit("/", 1)
    matches = [item for item in dbutils.fs.ls(parent) if item.name == filename]
    if not matches:
        raise FileNotFoundError(path)
    lines = spark.read.text(path).count() - 1
    return matches[0].size, lines


def collect_arrivals(dbutils, spark, catalog: str) -> list[dict]:
    arrivals = []
    for system, filenames in EXPECTED_FILES.items():
        for filename in filenames:
            path = f"/Volumes/{catalog}/bronze/raw/{system}/{filename}"
            size, lines = _file_metrics(dbutils, spark, path)
            if lines <= 0:
                raise ValueError(f"Arquivo vazio: {path}")
            arrivals.append({
                "sistema": system,
                "arquivo": filename,
                "bytes": size,
                "linhas": lines,
                "conferido_em": datetime.now(timezone.utc),
            })
    return arrivals


def save_arrivals(spark, catalog: str, arrivals: list[dict]) -> None:
    table = f"{catalog}.bronze._raw_arquivos"
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {table} (
          sistema STRING, arquivo STRING, bytes BIGINT,
          linhas BIGINT, conferido_em TIMESTAMP
        ) COMMENT 'Controle dos arquivos raw conferidos na chegada ao Volume'
    """)
    spark.createDataFrame(arrivals).write.mode("append").saveAsTable(table)


def main(dbutils, spark) -> None:
    catalog = dbutils.widgets.get("catalog")
    arrivals = collect_arrivals(dbutils, spark, catalog)
    save_arrivals(spark, catalog, arrivals)
    print("sistema | arquivo | bytes | linhas")
    for item in arrivals:
        print(f"{item['sistema']} | {item['arquivo']} | {item['bytes']} | {item['linhas']}")


dbutils_runtime = globals().get("dbutils")
spark_runtime = globals().get("spark")
if dbutils_runtime is not None and spark_runtime is not None:
    main(dbutils_runtime, spark_runtime)
