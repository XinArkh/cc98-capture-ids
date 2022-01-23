import re


MYCC98ID = 'xxx'


def wash_ids():
    with open('./ids.txt', 'r', encoding='utf-8') as f:
        ids = f.read()

    ids = re.sub('\n', '', ids)     # 去除字符串中的回车
    ids = re.split(',', ids)[:-1]   # 根据逗号分隔字符串元素，并去除最后一个空元素

    # 创建负面集合并添加元素
    neg_set = set()
    neg_set.add(MYCC98ID)           # 自己的98id
    for one_id in ids:              # 匿名用户
        if one_id.startswith('匿名'):
            neg_set.add(one_id)

    ids_set = set(ids)              # 将所有id转换为集合，这一步顺便可以去除重复元素
    ids_rst = ids_set - neg_set     # 通过集合减运算得到所有需要进一步处理的元素

    return ids_rst


if __name__ == '__main__':
    ids_rst = wash_ids()
    print(ids_rst, '\n元素数量：', len(ids_rst))
