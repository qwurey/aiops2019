# -*- coding:utf-8 -*-
'''
Created on 2017.11.28
Updated on 2018.05.15

@author: Qiao Wei
'''


import os
import datetime
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
import capacity.color as color
import random


def pre_rows(path):
    row_list = []
    with open(path) as f:
        content = f.readlines()
    for i in range(len(content) - 1):
        row_list.append(int(content[i]))
    print(min(row_list))
    print(max(row_list))


def print_customize(l):
    for i in l:
        print(i)
    return


def pre_index(path):
    ans = os.listdir(path)
    print(len(ans))
    set_i = set()
    set_e = set()
    set_c = set()
    set_p = set()
    set_l = set()
    for i in range(len(ans)):
        with open(path + ans[i]) as f:
            content = f.readlines()
            for j in range(len(content)):
                s = content[j].split(',')
                set_i.add(s[0])
                set_e.add(s[1])
                set_c.add(s[2])
                set_p.add(s[3])
                set_l.add(s[4])
    print(len(set_i))
    print(len(set_e))
    print(len(set_c))
    print(len(set_p))
    print(len(set_l))
    list_i = list(set_i)
    list_i.sort()
    list_e = list(set_e)
    list_e.sort()
    list_c = list(set_c)
    list_c.sort()
    list_p = list(set_p)
    list_p.sort()
    list_l = list(set_l)
    list_l.sort()
    print_customize(list_i)
    print_customize(list_e)
    print_customize(list_c)
    print_customize(list_p)
    print_customize(list_l)
    pass


def timestamp2str(time_num):
    timestamp = float(time_num/1000)
    time_array = time.localtime(timestamp)
    other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return other_style_time


def date_compare(item1, item2):
    t1 = time.mktime(time.strptime(item1, '%Y-%m-%d'))
    t2 = time.mktime(time.strptime(item2, '%Y-%m-%d'))
    print(t1, t2)
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    else:
        return 0


def filename2timestamp(filename):
    s = filename.split('.')
    tstr = timestamp2str(int(s[0]))
    return tstr


def pre_time(path):
    ans = os.listdir(path)
    date_time_dict = dict()
    for i in range(len(ans)):
        s = ans[i].split('.')
        # print(s[0])
        tstr = timestamp2str(int(s[0]))
        # print(tstr)
        ttstr = tstr.split(' ')
        if ttstr[0] in date_time_dict:
            date_time_dict.get(ttstr[0]).append(ttstr[1])
        else:
            date_time_dict[ttstr[0]] = list()
    print(date_time_dict)
    for key in date_time_dict.keys():
        print(key + ':' + str(len(date_time_dict[key])))

    # keys = date_time_dict.keys()
    # print(keys)
    # q = sorted(keys, date_compare)
    # print(keys)
    pass


def cal_element(path):
    ans = os.listdir(path)
    ans.sort()
    '''
        I：140
        E：13
        C：9
        P：36
        L：5
    '''
    layer = 5
    I = 150  # max label of i is: i148
    E = 13
    C = 9
    P = 36
    L = 5
    kpi = []

    # 读取每个时点的数据文件
    for t in range(0, len(ans)):

        print('layer5 ELEMENT START!')
        # 初始化B_iecpl
        B_iecpl = {}
        for i in range(I + 1):
            elist = {}
            for e in range(E + 1):
                clist = {}
                for c in range(C + 1):
                    plist = {}
                    for p in range(P + 1):
                        llist = {}
                        for l in range(L + 1):
                            llist[l] = 0
                        plist[p] = llist
                    clist[c] = plist
                elist[e] = clist
            B_iecpl[i] = elist

        with open(path + ans[t]) as f:
            print('正在读取第' + str(t) + '个文件:' + ans[t] + ', 时间节点为:' + filename2timestamp(ans[t]))
            lines = f.readlines()
            for j in lines:
                try:
                    content = j.split(',')
                    if content[0] != 'unknown':
                        i_number = int(content[0][1:])
                    else:
                        i_number = 0
                    if content[1] != 'unknown':
                        e_number = int(content[1][1:])
                    else:
                        e_number = 0
                    if content[2] != 'unknown':
                        c_number = int(content[2][1:])
                    else:
                        c_number = 0
                    if content[3] != 'unknown':
                        p_number = int(content[3][1:])
                    else:
                        p_number = 0
                    if content[4] != 'unknown':
                        l_number = int(content[4][1:])
                    else:
                        l_number = 0
                    B_iecpl[i_number][e_number][c_number][p_number][l_number] += int(content[-1])
                except Exception as e:
                    print('except:' + str(e) + ',content=' + j)
            # print(j.strip())
            # print('i=' + str(i_number) + ',e=' + str(e_number) + ',c=' + str(c_number)
            #       + ',p=' + str(p_number) + ',l=' + str(l_number)
            #       + ', leaf=' + str(B_iecpl[i_number][e_number][c_number][p_number][l_number]) + '\n')
            print('layer5 ELEMENT START!')

        # 根据每个时点的数据文件计算该时点的KPI
        print('初始化B_iecpl完毕，开始计算该时点的KPI')
        temp = 0
        for i in range(I):
            for e in range(E):
                for c in range(C):
                    for p in range(P):
                        for l in range(L):
                            temp += B_iecpl[i][e][c][p][l]
        kpi.append(temp)
        print('该时刻KPI值为:' + str(temp))

        # 计算一个时点的节点数
        # 140*13*9*36*5 = 2948400
        null_number = 0
        value_number = 0
        for i in range(I):
            for e in range(E):
                for c in range(C):
                    for p in range(P):
                        for l in range(L):
                            if B_iecpl[i][e][c][p][l] == 0:
                                null_number += 1
                            else:
                                value_number += 1
                                # print(B_iecpl[i][e][c][p][l])

        print('缺少值的叶子节点的个数为:' + str(null_number))
        print('有值的叶子节点值的个数为:' + str(value_number))
        print('叶子节点值的总个数为:' + str(null_number + value_number))
        print()

        # 计算所有层的、所有cuboid
        layer1_count = 5
        layer2_count = 10
        layer3_count = 10
        layer4_count = 5
        layer5_count = 1
        layers_count_list = [layer1_count, layer2_count, layer3_count, layer4_count, layer5_count]
        # layer4
        # B4_iecp = []
        # B4_iecl = []
        # B4_iepl = []
        # B4_icpl = []
        # B4_ecpl = []

        print('layer4 ELEMENT START!')
        # 初始化 B4_iecp
        B4_iecp = {}
        for i in range(I + 1):
            elist = {}
            for e in range(E + 1):
                clist = {}
                for c in range(C + 1):
                    plist = {}
                    for p in range(P + 1):
                        plist[p] = 0
                    clist[c] = plist
                elist[e] = clist
            B4_iecp[i] = elist
        # 赋值 B4_iecp
        for i in range(I):
            for e in range(E):
                for c in range(C):
                    for p in range(P):
                        for l in range(L):
                            B4_iecp[i][e][c][p] += B_iecpl[i][e][c][p][l]

        # 初始化 B4_iecl
        B4_iecl = {}
        for i in range(I + 1):
            elist = {}
            for e in range(E + 1):
                clist = {}
                for c in range(C + 1):
                    llist = {}
                    for l in range(L + 1):
                        llist[l] = 0
                    clist[c] = llist
                elist[e] = clist
            B4_iecl[i] = elist
        # 赋值 B4_iecl
        for i in range(I):
            for e in range(E):
                for c in range(C):
                    for l in range(L):
                        for p in range(P):
                            B4_iecl[i][e][c][l] += B_iecpl[i][e][c][p][l]
        # 初始化 B4_iepl
        B4_iepl = {}
        for i in range(I + 1):
            elist = {}
            for e in range(E + 1):
                plist = {}
                for p in range(P + 1):
                    llist = {}
                    for l in range(L + 1):
                        llist[l] = 0
                    plist[p] = llist
                elist[e] = plist
            B4_iepl[i] = elist
        # 赋值 B4_iepl
        for i in range(I):
            for e in range(E):
                for p in range(P):
                    for l in range(L):
                        for c in range(C):
                            B4_iepl[i][e][p][l] += B_iecpl[i][e][c][p][l]
        # 初始化 B4_icpl
        B4_icpl = {}
        for i in range(I + 1):
            clist = {}
            for c in range(C + 1):
                plist = {}
                for p in range(P + 1):
                    llist = {}
                    for l in range(L + 1):
                        llist[l] = 0
                    plist[p] = llist
                clist[c] = plist
            B4_icpl[i] = clist
        # 赋值 B4_icpl
        for i in range(I):
            for c in range(C):
                for p in range(P):
                    for l in range(L):
                        for e in range(E):
                            B4_icpl[i][c][p][l] += B_iecpl[i][e][c][p][l]
        # 初始化 B4_ecpl
        B4_ecpl = {}
        for e in range(E + 1):
            clist = {}
            for c in range(C + 1):
                plist = {}
                for p in range(P + 1):
                    llist = {}
                    for l in range(L + 1):
                        llist[l] = 0
                    plist[p] = llist
                clist[c] = plist
            B4_ecpl[e] = clist
        # 赋值 B4_ecpl
        for e in range(E):
            for c in range(C):
                for p in range(P):
                    for l in range(L):
                        for i in range(I):
                            B4_ecpl[e][c][p][l] += B_iecpl[i][e][c][p][l]
        print('layer4 ELEMENT OVER!')
        pass

        print('layer3 ELEMENT START!')
        # layer3： iecpl
        # B3_iec = []
        # 初始化 B4_iecp
        B3_iec = {}
        for i in range(I + 1):
            elist = {}
            for e in range(E + 1):
                clist = {}
                for c in range(C + 1):
                    clist[c] = 0
                elist[e] = clist
            B3_iec[i] = elist
        # 赋值 B3_iec
        for i in range(I):
            for e in range(E):
                for c in range(C):
                    for p in range(P):
                        B3_iec[i][e][c] += B4_iecp[i][e][c][p]

        # B3_iep = []
        # B3_iel = []
        # B3_icp = []
        # B3_icl = []
        # B3_ipl = []
        # B3_ecp = []
        # B3_ecl = []
        # B3_epl = []
        # B3_cpl = []

        print('layer3 ELEMENT OVER!')

        print('layer2 ELEMENT START!')

        print('layer2 ELEMENT OVER!')

        print('layer1 ELEMENT START!')

        print('layer1 ELEMENT OVER!')

        break

    # 输出全部时点的KPI
    # print('共有' + str(len(kpi)) + '个KPI时点数据')
    # print(kpi)
    # for i in range(len(ans)):
    #     print(kpi[i])
    pass




def kpi(path):
    with open(path) as f:
        content = f.readlines()
        print(content[0])
        kpis = content[0].split(',')
        print(str(len(kpis)))

    x = list(range(0, 4032))
    fig1 = plt.figure()
    plt.plot(x, kpis, '-')
    plt.title('Total KPIS')
    plt.xlabel('time')
    plt.ylabel('kpi')
    plt.show()
    pass


def kpi_mean_std(path):
    with open(path) as f:
        content = f.readlines()
        print(content[0])
        kpis = content[0].split(',')
        print(str(len(kpis)))

    minute_kpi = []
    for i in range(0, 288):
        target_minute = list()
        minute_kpi.append(target_minute)
    for i in range(0, len(kpis)):
        minute_kpi[i % 288].append(float(kpis[i]))
        # print(i)
        # print(i % 288)
    minute_mean = []
    minute_std = []
    for i in range(0, 288):
        # print(len(minute_kpi[i]))
        minute_mean.append(np.mean(np.array(minute_kpi[i])))
        minute_std.append(np.std(np.array(minute_kpi[i])))
    for i in range(0, 288):
        print(str(i) + ',' + str(minute_mean[i]) + ',' + str(minute_std[i]))
    minute_upper = []
    minute_down = []
    c = 2.0
    for i in range(0, 288):
        minute_down.append(minute_mean[i] - c * minute_std[i])
        minute_upper.append(minute_mean[i] + c * minute_std[i])
    # show with graph
    # x = list(range(0, 288))
    # plt.figure(num=3, figsize=(8, 5))
    # a, = plt.plot(x, minute_mean, color='red', label='minute mean')
    # b, = plt.plot(x, minute_upper, color='blue', label='minute upper')
    # c, = plt.plot(x, minute_down, color='green', label='minute down')
    # plt.legend(handles=[a, b, c])
    # plt.xlabel('minute index')
    # plt.ylabel('minute kpi')
    # plt.title('kpi minute', loc='left')
    # plt.show()
    return minute_mean, minute_std, minute_upper, minute_down


def print_lines(y, title, dates):
    for i in range(len(y)):
        xi = np.linspace(0, 287, 288)
        y_target_date = y[i]
        yi = np.array(y_target_date)
        plt.title(title)
        color_id = random.randint(0, 139)
        color_names = list(color.cnames.values())
        color_name = color_names[color_id]
        plt.plot(xi, yi, color=color_name, label=dates[i])
    plt.legend()
    plt.xlabel('minute')
    plt.ylabel('kpi')
    plt.show()


def kpi_days_show(path, minute_mean, minute_std, minute_upper, minute_down):
    with open(path) as f:
        content = f.readlines()
        print(content[0])
        kpis = content[0].split(',')
        print(str(len(kpis)))
    y = []
    for i in range(0, 14):
        yi = kpis[i * 288 : (i+1) * 288]
        y.append(yi)
    # y.append(minute_mean)
    # y.append(minute_std)
    # y.append(minute_upper)
    # y.append(minute_down)
    # dates = ['2018-09-01', '2018-09-02', '2018-09-03', '2018-09-04', '2018-09-05'
    #          , '2018-09-06', '2018-09-07', '2018-09-08', '2018-09-09', '2018-09-10'
    #          , '2018-09-11', '2018-09-12', '2018-09-13', '2018-09-14'
    #          , 'kpi mean', 'kpi std', 'kpi minute upper', 'kpi minute down']
    dates = ['2018-09-01', '2018-09-02', '2018-09-03', '2018-09-04', '2018-09-05'
        , '2018-09-06', '2018-09-07', '2018-09-08', '2018-09-09', '2018-09-10'
        , '2018-09-11', '2018-09-12', '2018-09-13', '2018-09-14']
    xi = np.linspace(0, 287, 288)
    plt.plot(xi, minute_mean, color='black', label='kpi mean')
    plt.plot(xi, minute_std, color='red', label='kpi std')
    plt.plot(xi, minute_upper, color='red', label='kpi minute upper')
    plt.plot(xi, minute_down, color='red', label='kpi minute down')
    print_lines(y, 'minute kpi', dates)
    pass


if __name__ == '__main__':

    log_file_flag = 0  # 1: open , 0: close
    # log_file_flag = 1  # 1: open , 0: close
    log_file_location = '/Users/urey/Assignment/aiops/kpi.data'

    if log_file_flag == 1:
        log_file = open(log_file_location, 'w')
        sys.stdout = log_file

    start = datetime.datetime.now()

    # path = '/Users/urey/Assignment/aiops/rows.data'
    # pre_rows(path)

    # pre_index(path)

    # path = '/Users/urey/Assignment/aiops/2019AIOps_data/'
    # pre_time(path)

    path = '/Users/urey/Assignment/aiops/2019AIOps_data/'
    cal_element(path)

    # path = '/Users/urey/Assignment/aiops/kpi_list.data'
    # kpi(path)

    # path = '/Users/urey/Assignment/aiops/kpi_list.data'
    # minute_mean, minute_std, minute_upper, minute_down = kpi_mean_std(path)
    # kpi_days_show(path, minute_mean, minute_std, minute_upper, minute_down)

    end = datetime.datetime.now()
    print('耗时:' + str(end - start))

    if log_file_flag == 1:
        log_file.close()



