import xlrd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

def main():
    drawPicture_agebar(getDataList())

def getDataList():

    book_users = xlrd.open_workbook('dataFolder/users.xlsx')
    sheet_users = book_users.sheets()[0]
    col_datalist_users_age = sheet_users.col_values(2,start_rowx=1,end_rowx=None)
    col_datalist_users_gender = sheet_users.col_values(3,start_rowx=1,end_rowx=None)
    agedata_dict_man = {'all':0, '0-18':0, '18-25':0, '25-30':0, '30-35':0, '35-40':0, '40-45':0, '45-50':0, '50-55':0, '55-':0 }
    agedata_dict_woman = {'all':0, '0-18':0, '18-25':0, '25-30':0, '30-35':0, '35-40':0, '40-45':0, '45-50':0, '50-55':0, '55-':0 }
    for age, gender in zip(col_datalist_users_age,col_datalist_users_gender):
        age = int(2020-age)
        if gender==0:
            agedata_dict_man['all'] += 1
            if age<18:agedata_dict_man['0-18'] += 1
            elif age<25 and age>=18 : agedata_dict_man['18-25'] += 1
            elif age<30 and age>=25 : agedata_dict_man['25-30'] += 1
            elif age<35 and age>=30 : agedata_dict_man['30-35'] += 1
            elif age<40 and age>=35 : agedata_dict_man['35-40'] += 1
            elif age<45 and age>=40 : agedata_dict_man['40-45'] += 1
            elif age<50 and age>=45 : agedata_dict_man['45-50'] += 1
            elif age<55 and age>=50 : agedata_dict_man['50-55'] += 1
            elif age<200 and age>=55 : agedata_dict_man['55-'] += 1
            else: continue
        if gender==1:
            agedata_dict_woman['all'] += 1
            if age<18:agedata_dict_woman['0-18'] += 1
            elif age<25 and age>=18 : agedata_dict_woman['18-25'] += 1
            elif age<30 and age>=25 : agedata_dict_woman['25-30'] += 1
            elif age<35 and age>=30 : agedata_dict_woman['30-35'] += 1
            elif age<40 and age>=35 : agedata_dict_woman['35-40'] += 1
            elif age<45 and age>=40 : agedata_dict_woman['40-45'] += 1
            elif age<50 and age>=45 : agedata_dict_woman['45-50'] += 1
            elif age<55 and age>=50 : agedata_dict_woman['50-55'] += 1
            elif age<200 and age>=55 : agedata_dict_woman['55-'] += 1
            else: continue
    agedata_list = [agedata_dict_man, agedata_dict_woman]
    return agedata_list

def drawPicture_agebar(agedata_list):
    plt.rcParams['font.sans-serif']=['SimHei'] # 解决乱码

    X = agedata_list[0].keys()
    Y1 = agedata_list[0].values()
    Y2 = agedata_list[1].values()
    Y = []
    for y1, y2 in zip(Y1,Y2):
        Y.append(y1+y2)
    plt.figure()
   
    x=np.arange(4)+0.3  # 并列柱状图的关键，代表x轴位置
    width=0.3
    x=np.arange(len(X))  # 并列柱状图的关键，代表x轴位置

    plt.bar(x-0.3,Y,width,label='全部',color='g')
    plt.bar(X,Y1,width,label='男',color='b')
    plt.bar(x+0.3,Y2,width,label='女', color='r')

    plt.legend()
    plt.title('年龄结构分析')
    plt.xlabel('年龄')
    plt.ylabel('总人数')

    for x1, x2, y,y1,y2 in zip(x, X, Y, Y1, Y2):
        plt.text(x1-0.3, y, f'{y}', ha='center', va='bottom')
        plt.text(x2, y1, f'{y1}', ha='center', va='bottom')
        plt.text(x1+0.3, y2, f'{y2}', ha='center', va='bottom')


    plt.show()
if __name__ == '__main__':
    main()  