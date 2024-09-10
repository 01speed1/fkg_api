import os
import psycopg

DATABASE_URL = os.getenv('DATABASE_URL')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
TESTING = os.getenv('TESTING', 'False').lower() in ('true', '1', 't')

async def init_connection():
  print("Connecting to Postgres database...")
  conn = await psycopg.AsyncConnection.connect(
      host=DB_HOST,
      port=DB_PORT,
      user=DB_USER,
      password=DB_PASSWORD,
      dbname=DB_NAME
  )
  return conn

async def fetch(query, values):
  async with await init_connection() as conn:
    async with conn.cursor() as cur:
      await cur.execute(query, values)
      result = await cur.fetchall()
      return result

async def fetch_one(query, values):
  async with await init_connection() as conn:
    async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
      await cur.execute(query, values)
      result = await cur.fetchone()
      return result


async def execute(query, values):
  async with await init_connection() as conn:
    async with conn.cursor() as cur:
      await cur.execute(query, values)
      await conn.commit()

async def insert(table, values):
  columns = ', '.join(values.keys())
  placeholders = ', '.join(f'%({key})s' for key in values.keys())
  query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *'
  
  async with await init_connection() as conn:
    async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
      await cur.execute(query, values)
      result = await cur.fetchone()
      await conn.commit()
      return result
