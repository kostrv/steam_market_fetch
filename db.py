import aiomysql

async def create_pool(host: str, username: str, password: str, db: str) -> aiomysql.Pool:
    pool = None
    
    url = f'{username}:{password}@{host}/{db}'
    print(f'Connecting to MySQL Database [URL] {url}')
    
    try:
        pool = await aiomysql.create_pool(
            host=host,
            user=username,
            password=password,
            db=db,
            minsize=1,
            maxsize=10
        )
        print(f'[INFO] Connection pool to MySQL DB successful [URL] {username}:{password}@{host}/{db}')
    except Exception as e:
        print(f'[ERROR] Failed to create connection pool to MySQL DB: {e}')
        raise
    
    return pool

async def save_to_db(pool: aiomysql.Pool, data: dict) -> None:
    query = '''
    INSERT INTO parsed_data (title, total_month_sales, avg_week_sales, avg_day_sales, median_price)
    VALUES (%s, %s, %s, %s, %s) '''
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query, (
                data['title'],
                data['total_month_sales'],
                data['avg_week_sales'],
                data['avg_day_sales'],
                data['median_price']
            ))
            await conn.commit()

# async def execute_query(connection, query):
#     async with connection.cursor() as cursor:
#         try:
#             await cursor.execute(query)
#             result = await cursor.fetchall()
#             return result
#         except Exception as e:
#             print(f'The error '{e}' occurred')
#             return None

    # connection = await create_connection('localhost', 'username', 'password', 'mydatabase')

    # if connection:
    #     select_query = 'SELECT * FROM parsed_data'
    #     results = await execute_query(connection, select_query)

    #     if results:
    #         for row in results:
    #             print(row)

    #     connection.close()
