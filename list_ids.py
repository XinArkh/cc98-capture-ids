from wash_ids import wash_ids


ids_rst = wash_ids()

rec_list = []
rec_str = ''
for i, enum in enumerate(ids_rst):
    if (i+1) % 10 == 0 or (i+1) == len(ids_rst):
        rec_str += enum
        rec_list.append(rec_str)
        rec_str = ''
    else:
        rec_str += enum + ' '

for i, enum in enumerate(rec_list):
    print(i+1)
    print(enum, '\n')
