import requests
from bs4 import BeautifulSoup
import csv

def crawl_data(str_link):
    url = str_link
    f = requests.get(url, headers={})
    # print(f.content)
    soup = BeautifulSoup(f.content, "lxml")
    movies = soup.find_all("article", {'class': 'item movies'})

    #Lấy script của nhiều trang
    transcpt_pagination = soup.find("div", {"class": "pagination"})
    transcpt_links = transcpt_pagination.find_all('a', {"class": "inactive"})
    
    #Lấy tát cả thông tin phim của từng trang
    resul_movies = []
    for transcpt_link in transcpt_links:
        url = transcpt_link['href']
        f = requests.get(url, headers={})
    
        for movie in movies:
            movie_item = {}
            #Get data of each Tag element
            movie_status = movie.find('div', {'class':'trangthai'}).text
            movie_footer = movie.find('div', {'class':'data'})
            movie_link = movie_footer.find('a')['href']
            movie_vnname = movie_footer.find('a').text
            movie_enname = movie_footer.find('span').text
            #Add to list result_movies
            movie_item['movie VNname'] = movie_vnname
            movie_item['movie ENname'] = movie_enname
            movie_item['movie status'] = movie_status
            movie_item['movie link'] = movie_link
            resul_movies.append(movie_item)
    
    # print(resul_movies)
    return resul_movies

#-----Load data into database-----#

def create_table(conn, table_name, fields):
    """Create a table in database

    Args:
        conn (stirng): connection string of database
        table_name (string): name of the table
        fields (list): list of the fields(columns)
    """    
    cursor = conn.cursor()
    attrs_table = ', '.join([f"{field[0]} {field[1]}" for field in fields])
    
    #Crreate table in database
    sqlStr = f"""
        create table if not exists {table_name} (
            {attrs_table}
        );
    """
    #Excute the sql command
    cursor.execute(sqlStr)
    conn.commit()

import cleaning_data as cd

def insert_data(conn, data_info, table_name, fields):
    """Insert data into to table on database

    Args:
        conn (string): connection string
        data_info (list): list of movie items
        table_name (string): name of the table
        fields (list): list of fields of a table
    """    
    cursor = conn.cursor()  
    #String of the fields
    fields_table = ', '.join([f"{field[0]}" for field in fields])
    data_lst = []
    
    #Cleaning data
    data_info = cd.data_processing(data_info)
    
    #Wrap data into a string
    for idx, item in enumerate(data_info):
        item_lst = [f"'{item[key]}'" for key in item]
        data_lst.append(f'({idx}' + ", " + f"{','.join(item_lst)})")
    
    data_insert = ', '.join(data_lst)

    # Insert data into table
    sqlStr = f"""insert into {table_name}({fields_table}) values{data_insert}"""
    
    #Excute sql command
    try:
        cursor.execute(sqlStr)
        conn.commit()
    except Exception as ex:
        print(str(ex))
    
    conn.close()
    
def export_to_csv(fields, data_info):
    """Exporting to a csv file

    Args:
        fields (list): list of fields of a table
        data_info (list): list of movie items
    """    
    headers = [f"{field[0]}" for field in fields]
    # print(data_info)
    values = [[f"{items[item]}" for item in items] for items in data_info]
    
    with open('../movies.csv', 'w', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(values)
    