#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from www.orm import *
from www.model import *
import sys

# 创建异步事件的句柄
loop = asyncio.get_event_loop()

# 创建实例
async def test():
    await create_pool(loop=loop,host='172.16.2.97', port=3306, user='wangsong', password='wangsong', db='test')

    # 添加用户信息
    user1 = User_test( name='tony', passwd='123', email='wangsong@zhimabang.com', image='test.png')
    user2 = User_test( name='tony', passwd='123', email='wangsong@zhimabang.com', image='test.png' )
    await user1.save()
    await user2.save()
    print (User_test.save)



    # 返回表全部结果
    # r = await User.findAll(User)
    # print(1, r)

    # 返回指定条件结果
    # r = await User.findAll(User, where='name=\'Mike\'')
    # print(1, r)

    # 返回主键值查找结果  find("主键值")
    # r = await User.find("2")
    # print(3, r)

    #update，remove未调试
    #r = await User.update(name='Abl2n', id='10')

    # 暂时不完善，只是移除一个刚创建的对象
    # await user1.remove()

    await destory_pool()

loop.run_until_complete(test())
loop.close()
if loop.is_closed():
    sys.exit(0)
