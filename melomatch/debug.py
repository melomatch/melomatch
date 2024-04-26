import logging
import uuid

from coloreflection import Color
from django.db import connection

logging.basicConfig(level=logging.INFO)
C = Color()


def print_queries(queries):
    tag = uuid.uuid4()
    logging.info("[%s] SQL PROFILER", tag)
    total_time = 0.0
    total_queries = 0
    for counter, query in enumerate(queries, start=1):
        nice_sql = query["sql"].replace('"', "").replace(",", ", ")
        sql = C.FG.red(f"[{query["time"]}] ") + nice_sql
        total_time = total_time + float(query["time"])

        # if counter <= 20:
        logging.info("[%s] %s\n", tag, sql)
        total_queries = counter

    total = f"[{tag}] {C.FG.green(f"[TOTAL TIME: {total_time} seconds, QUERIES: {total_queries}]")}"
    logging.info(total)


class SqlPrintingMiddleware:
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed.  This is only useful for debugging.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if len(connection.queries) > 0:
            print_queries(connection.queries)
        return response
