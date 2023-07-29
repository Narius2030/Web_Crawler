import crawling_data as crd
import pymssql

#Create a connection with Postgres database
connection = pymssql.connect(
    server="DESKTOP-BEALJ3H\SQLEXPRESS",
    database="master",
)

#Properties of table
table_name = 'NBmovies'
fields = [
    ('movie_id', 'integer primary key'),
    ('VietNam_name', 'varchar(100)'),
    ('English_name', 'varchar(100)'),
    ('Status', 'char(50)'),
    ('Link', 'varchar(100)')
]

movie_info = crd.crawl_data('https://motchill2.net/phim-le')
crd.create_table(connection, table_name, fields)
crd.insert_data(connection, movie_info, table_name, fields)
crd.export_to_csv(fields, movie_info)
    