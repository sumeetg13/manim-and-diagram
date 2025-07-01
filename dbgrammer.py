from diagrams import Diagram, Cluster
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.database import SQL

with Diagram("Simple Database Diagram", show=True, direction="LR"):

    db = PostgreSQL("Main DB")

    with Cluster("Tables"):
        user_table = SQL("User")
        orders_table = SQL("Orders")
        product_table = SQL("Product")

    db >> user_table
    db >> orders_table
    db >> product_table
    orders_table >> user_table
    orders_table >> product_table
