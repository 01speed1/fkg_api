import os
import asyncio
import psycopg

from app.db.config import settings

print(settings.database_url)

async def init_connection():
  conn = await psycopg.AsyncConnection.connect(
      host="postgres_db",
      port=5432,
      user="postgres",
      password="password",
      dbname="postgres"
  )
  return conn

async def close_connection(conn):
  await conn.close()

async def fetch(conn, query, values):
  async with conn.cursor() as cur:
    await cur.execute(query, values)
    result = await cur.fetchall()
    return result

async def execute(conn, query, values):
  async with conn.cursor() as cur:
    await cur.execute(query, values)
    await conn.commit()
