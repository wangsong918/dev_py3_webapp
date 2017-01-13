#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging,aiomysql

# 输出SQL信息
def log(sql, args=()):
    logging.info('SQL: %s' % sql)

# 创建数据库连接池
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

# 查询数据库操作
async def select(sql, args, size=None):
    log(sql, args)
    # global __pool  # 重复定义？
    async with __pool.get() as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            res = await cur.fetchmany(size)
        else:
            res = await cur.fetchall()    # 返回结果集
            await cur.close()
        logging.info('rows returned: %s' % len(res))
        return res

# 增删改操作
async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount   # 返回结果数
            await cur.close()
        except BaseException as e:
            raise
        return affected
