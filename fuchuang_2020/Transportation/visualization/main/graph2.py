# coding:utf-8
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from collections import Counter
from shortestpass import ReadFile
from shortestpass import Station
import math

class Vertex():

    def __init__(self, name):
        self.name = name
        self.connected_vertex = {}

    def __str__(self):
        return str(self.name)  +  str([(vertex.name,str(self.connected_vertex[vertex])) for vertex in self.connected_vertex.keys()])

    def appendNeighbor(self, neighbor, weight=1):
        self.connected_vertex[neighbor] = weight

    def deleteNeighbor(self, neighbor):
        del self.connected_vertex[neighbor]

    def getNeighbors(self):
        return self.connected_vertex.keys()

    def getWeight(self, neighbor):
        return self.connected_vertex[neighbor]
    
    def getName(self):
        return self.name

class Graph():

    def __init__(self):
        self.ver_list = {}
        self.num_vertex = 0
    
    def addVertex(self, name):
        new_vertex = Vertex(name)
        self.ver_list[name] = new_vertex
        self.num_vertex += 1
        return new_vertex

    def getVertex(self, name):
        if name in self.ver_list:
            return self.ver_list[name]
        else:
            return None

    def addEdge(self, init, target, weight=1):
        if init not in self.ver_list:
            self.addVertex(init)
        if target not in self.ver_list:
            self.addVertex(target)
        self.ver_list[init].appendNeighbor(self.ver_list[target], weight)

    def deleteEdge(self, vertex1, vertex2):
        self.ver_list[vertex1].deleteNeighbor(self.ver_list[vertex2])

    def getVertices(self):
        return self.ver_list.keys()

    def __contains__(self, name):
        return name in self.ver_list

    def __iter__(self):
        return iter(self.ver_list.values())

class Dfs():

    def __init__(self):
        self.createGraph()
        # new_dict = {}
        # 1. 得到 结点间的路径
        # for sta_list in self.sta:
        #     new_dict[(sta_list[0], sta_list[-1])] = sta_list[1:-1:1]
        #     new_dict[(sta_list[-1], sta_list[0])] = sta_list[-2:0:-1]
        # print(new_dict)
        self.stationinfo_dict = {'Sta1': ['1号线', '0'],'Sta159': ['1号线', '0'],'Sta108': ['1号线', '0'],'Sta83': ['1号线', '0'],'Sta107': ['1号线', '0'],'Sta154': ['1号线', '0'],'Sta150': ['1号线', '0'],'Sta64': ['1号线', '0'],'Sta89': ['1号线', '1'],'Sta80': ['1号线', '0'],'Sta97': ['1号线', '0'],'Sta110': ['1号线', '0'],'Sta106': ['1号线', '0'],'Sta34': ['1号线', '0'],'Sta128': ['1号线', '0'],'Sta74': ['1号线', '0'],'Sta149': ['1号线', '0'],'Sta49': ['1号线', '0'],'Sta65': ['1号线', '0'],'Sta9': ['2号线', '0'],'Sta163': ['2号线', '0'],'Sta53': ['2号线', '0'],'Sta78': ['2号线', '0'],'Sta79': ['2号线', '0'],'Sta18': ['2号线', '0'],'Sta123': ['2号线', '0'],'Sta127': ['2号线', '1'],'Sta81': ['2号线', '0'],'Sta27': ['2号线', '0'],'Sta48': ['2号线', '0'],'Sta151': ['2号线', '0'],'Sta68': ['2号线', '0'],'Sta52': ['2号线', '0'],'Sta76': ['2号线', '0'],'Sta57': ['2号线', '0'],'Sta71': ['2号线', '0'],'Sta139': ['2号线', '0'],'Sta24': ['2号线', '0'],'Sta105': ['2号线', '0'],'Sta51': ['2号线', '0'],'Sta143': ['3号线', '0'],'Sta156': ['3号线', '0'],'Sta61': ['3号线', '0'],'Sta50': ['3号线', '0'],'Sta119': ['3号线', '0'],'Sta66': ['3号线', '0'],'Sta12': ['3号线', '0'],'Sta161': ['3号线', '0'],'Sta21': ['3号线', '0'],'Sta133': ['3号线', '0'],'Sta22': ['3号线', '0'],'Sta138': ['3号线', '0'],'Sta41': ['3号线', '1'],'Sta30': ['3号线', '0'],'Sta67': ['3号线', '0'],'Sta144': ['3号线', '0'],'Sta29': ['3号线', '0'],'Sta126': ['3号线', '0'],'Sta40': ['3号线', '0'],'Sta131': ['3号线', '0'],'Sta39': ['3号线', '0'],'Sta100': ['3号线', '0'],'Sta167': ['3号线', '0'],'Sta113': ['3号线', '0'],'Sta141': ['3号线', '0'],'Sta142': ['3号线', '0'],'Sta158': ['3号线', '0'],'Sta44': ['3号线', '0'],'Sta117': ['3号线', '0'],'Sta147': ['3号线', '0'],'Sta42': ['3号线', '0'],'Sta35': ['3号线', '0'],'Sta109': ['3号线', '0'],'Sta33': ['3号线', '0'],'Sta112': ['3号线', '0'],'Sta153': ['3号线', '0'],'Sta125': ['3号线', '0'],'Sta121': ['3号线', '0'],'Sta11': ['3号线', '0'],'Sta134': ['10号线', '1'],'Sta59': ['4号线', '0'],'Sta19': ['4号线', '0'],'Sta62': ['4号线', '0'],'Sta165': ['4号线', '0'],'Sta58': ['4号线', '0'],'Sta38': ['4号线', '0'],'Sta43': ['5号线', '0'],'Sta10': ['5号线', '0'],'Sta96': ['5号线', '0'],'Sta132': ['5号 线', '0'],'Sta37': ['5号线', '0'],'Sta16': ['5号线', '0'],'Sta69': ['5号线', '0'],'Sta54': ['5号线', '0'],'Sta120': ['11号线', '0'],'Sta130': ['11号线', '0'],'Sta146': ['11号线', '0'],'Sta25': ['11号线', '0'],'Sta3': ['11号线', '1'],'Sta46': ['11号线', '0'],'Sta86': ['11号线', '0'],'Sta15': ['11号线', '1'],'Sta162': ['11号线', '0'],'Sta118': ['11号线', '0'],'Sta20': ['11号线', '0'],'Sta55': ['11号线', '0'],'Sta70': ['11号线', '0'],'Sta13': ['11号线', '0'],'Sta140': ['11号线', '1'],'Sta77': ['11号线', '0'],'Sta122': ['11号线', '0'],'Sta36': ['11号线', '0'],'Sta166': ['11号线', '0'],'Sta99': ['11号线', '0'],'Sta124': ['11号线', '0'],'Sta28': ['11号线', '0'],'Sta82': ['11号线', '0'],'Sta164': ['11号线', '0'],'Sta152': ['11号线', '0'],'Sta45': ['11号线', '0'],'Sta75': ['10号线', '1'],'Sta136': ['12号线', '0'],'Sta137': ['12号线', '0'],'Sta101': ['12号线', '0'],'Sta17': ['12号线', '0'],'Sta26': ['12号线', '0'],'Sta90': ['12号线', '1'],'Sta95': ['12号线', '0'],'Sta93': ['12号线', '0'],'Sta92': ['12号线', '0'],'Sta32': ['12号线', '0'],'Sta91': ['12号线', '0'],'Sta157': ['10号线', '0'],'Sta168': ['10号线', '0'],'Sta85': ['10号线', '0'],'Sta2': ['10号线', '0'],'Sta4': ['10号线', '0'],'Sta103': ['10号线', '0'],'Sta145': ['10号线', '0'],'Sta88': ['10号线', '0'],'Sta94': ['10号线', '0'],'Sta160': ['10号线', '0'],'Sta7': ['10号线', '0'],'Sta6': ['10号线', '0'],'Sta8': ['10号线', '0'],'Sta102': ['10号线', '0'],'Sta31': ['12号线', '0'],'Sta72': ['12号线', '0'],'Sta116': ['12号线', '0'],'Sta129': ['2号线', '0'],'Sta47': ['2号线', '1'],'Sta60': ['12号线', '0'],'Sta148': ['12号线', '0'],'Sta73': ['12号线', '0'],'Sta23': ['11号线', '1'],'Sta56': ['11号线', '1'],'Sta115': ['11号线', '1'],'Sta63': ['11号线', '1'],'Sta114': ['10号线', '1'],'Sta135': ['10号线', '1'],'Sta87': ['10号线', '1'],'Sta84': ['4号线', '0'],'Sta111': ['11号线', '0']}

        self.passes37 = {('Sta24', 'Sta127'): ['Sta51', 'Sta105', 'Sta139', 'Sta71', 'Sta57', 'Sta76', 'Sta52', 'Sta68', 'Sta151', 'Sta48', 'Sta27', 'Sta81'], ('Sta127', 'Sta24'): ['Sta81', 'Sta27', 'Sta48', 'Sta151', 'Sta68', 'Sta52', 'Sta76', 'Sta57', 'Sta71', 'Sta139', 'Sta105', 'Sta51'], ('Sta73', 'Sta127'): ['Sta148', 'Sta60'], ('Sta127', 'Sta73'): ['Sta60', 'Sta148'], ('Sta127', 'Sta47'): ['Sta123'], ('Sta47', 'Sta127'): ['Sta123'], ('Sta1', 'Sta47'): ['Sta159'], ('Sta47', 'Sta1'): ['Sta159'], ('Sta47', 'Sta89'): ['Sta108', 'Sta83', 'Sta107', 'Sta154', 'Sta150', 'Sta64'], ('Sta89', 'Sta47'): ['Sta64', 'Sta150', 'Sta154', 'Sta107', 'Sta83', 'Sta108'], ('Sta127', 'Sta41'): ['Sta91'], ('Sta41', 'Sta127'): ['Sta91'], ('Sta89', 'Sta65'): ['Sta80', 'Sta97', 'Sta110', 'Sta106', 'Sta34', 'Sta128', 'Sta74', 'Sta149', 'Sta49'], ('Sta65', 'Sta89'): ['Sta49', 'Sta149', 'Sta74', 'Sta128', 'Sta34', 'Sta106', 'Sta110', 'Sta97', 'Sta80'], ('Sta136', 'Sta89'): [], ('Sta89', 'Sta136'): [], ('Sta89', 'Sta23'): ['Sta137', 'Sta101', 'Sta31', 'Sta17'], ('Sta23', 'Sta89'): ['Sta17', 'Sta31', 'Sta101', 'Sta137'], ('Sta23', 'Sta140'): ['Sta20', 'Sta55', 'Sta70', 'Sta13'], ('Sta140', 'Sta23'): ['Sta13', 'Sta70', 'Sta55', 'Sta20'], ('Sta140', 'Sta77'): ['Sta99', 'Sta166', 'Sta124', 'Sta28', 'Sta36', 'Sta122'], ('Sta77', 'Sta140'): ['Sta122', 'Sta36', 'Sta28', 'Sta124', 'Sta166', 'Sta99'], ('Sta140', 'Sta75'): ['Sta111', 'Sta82', 'Sta164', 'Sta152'], ('Sta75', 'Sta140'): ['Sta152', 'Sta164', 'Sta82', 'Sta111'], ('Sta75', 'Sta102'): [], ('Sta102', 'Sta75'): [], ('Sta75', 'Sta45'): [], ('Sta45', 'Sta75'): [], ('Sta75', 'Sta87'): ['Sta8', 'Sta6', 'Sta7', 'Sta160', 'Sta94'], ('Sta87', 'Sta75'): ['Sta94', 'Sta160', 'Sta7', 'Sta6', 'Sta8'], ('Sta11', 'Sta87'): ['Sta121', 'Sta125', 'Sta153', 'Sta112', 'Sta33', 'Sta109'], ('Sta87', 'Sta11'): ['Sta109', 'Sta33', 'Sta112', 'Sta153', 'Sta125', 'Sta121'], ('Sta58', 'Sta90'): ['Sta38', 'Sta165', 'Sta62', 'Sta19', 'Sta59', 'Sta84'], ('Sta90', 'Sta58'): ['Sta84', 'Sta59', 'Sta19', 'Sta62', 'Sta165', 'Sta38'], ('Sta23', 'Sta90'): ['Sta26'], ('Sta90', 'Sta23'): ['Sta26'], ('Sta43', 'Sta56'): ['Sta10', 'Sta96', 'Sta132', 'Sta37', 'Sta16', 'Sta69', 'Sta54'], ('Sta56', 'Sta43'): ['Sta54', 'Sta69', 'Sta16', 'Sta37', 'Sta132', 'Sta96', 'Sta10'], ('Sta90', 'Sta134'): [], ('Sta134', 'Sta90'): [], ('Sta87', 'Sta134'): ['Sta88', 'Sta145', 'Sta103', 'Sta4', 'Sta2', 'Sta85'], ('Sta134', 'Sta87'): ['Sta85', 'Sta2', 'Sta4', 'Sta103', 'Sta145', 'Sta88'], ('Sta87', 'Sta135'): ['Sta35', 'Sta42', 'Sta147', 'Sta117', 'Sta44', 'Sta158', 'Sta142', 'Sta141', 'Sta113', 'Sta167'], ('Sta135', 'Sta87'): ['Sta167', 'Sta113', 'Sta141', 'Sta142', 'Sta158', 'Sta44', 'Sta117', 'Sta147', 'Sta42', 'Sta35'], ('Sta56', 'Sta115'): ['Sta118'], ('Sta115', 'Sta56'): ['Sta118'], ('Sta115', 'Sta41'): ['Sta126', 'Sta29', 'Sta144', 'Sta67', 'Sta30'], ('Sta41', 'Sta115'): ['Sta30', 'Sta67', 'Sta144', 'Sta29', 'Sta126'], ('Sta143', 'Sta41'): ['Sta156', 'Sta61', 'Sta50', 'Sta119', 'Sta66', 'Sta12', 'Sta161', 'Sta21', 'Sta133', 'Sta22', 'Sta138'], ('Sta41', 'Sta143'): ['Sta138', 'Sta22', 'Sta133', 'Sta21', 'Sta161', 'Sta12', 'Sta66', 'Sta119', 'Sta50', 'Sta61', 'Sta156'], ('Sta120', 'Sta63'): ['Sta130', 'Sta146', 'Sta25'], ('Sta63', 'Sta120'): ['Sta25', 'Sta146', 'Sta130'], ('Sta47', 'Sta63'): ['Sta18', 'Sta79', 'Sta53', 'Sta163', 'Sta9', 'Sta129'], ('Sta63', 'Sta47'): ['Sta129', 'Sta9', 'Sta163', 'Sta53', 'Sta79', 'Sta18'], ('Sta41', 'Sta3'): ['Sta32', 'Sta116', 'Sta92'], ('Sta3', 'Sta41'): ['Sta92', 'Sta116', 'Sta32'], ('Sta3', 'Sta15'): ['Sta46', 'Sta86'], ('Sta15', 'Sta3'): ['Sta86', 'Sta46'], ('Sta157', 'Sta114'): [], ('Sta114', 'Sta157'): [], ('Sta115', 'Sta114'): ['Sta162'], ('Sta114', 'Sta115'): ['Sta162'], ('Sta115', 'Sta135'): ['Sta40', 'Sta131', 'Sta39', 'Sta100'], ('Sta135', 'Sta115'): ['Sta100', 'Sta39', 'Sta131', 'Sta40'], ('Sta114', 'Sta135'): ['Sta168'], ('Sta135', 'Sta114'): ['Sta168'], ('Sta135', 'Sta134'): [], ('Sta134', 'Sta135'): [], ('Sta15', 'Sta134'): ['Sta95'], ('Sta134', 'Sta15'): ['Sta95'], ('Sta56', 'Sta23'): [], ('Sta23', 'Sta56'): [], ('Sta63', 'Sta3'): [], ('Sta3', 'Sta63'): [], ('Sta15', 'Sta114'): [], ('Sta114', 'Sta15'): []}

        self.between_line = {('Sta65', 'Sta49'): '1号线', ('Sta49', 'Sta65'): '1号线', ('Sta49', 'Sta149'): '1号线', ('Sta149', 'Sta49'): '1号线', ('Sta149', 'Sta74'): '1号线', ('Sta74', 'Sta149'): '1号线', ('Sta74', 'Sta128'): '1号线', ('Sta128', 'Sta74'): '1号线', ('Sta128', 'Sta34'): '1号线', ('Sta34', 'Sta128'): '1号线', ('Sta34', 'Sta106'): '1号线', ('Sta106', 'Sta34'): '1号线', ('Sta106', 'Sta110'): '1号线', ('Sta110', 'Sta106'): '1号线', ('Sta110', 'Sta97'): '1号线', ('Sta97', 'Sta110'): '1号线', ('Sta97', 'Sta80'): '1号线', ('Sta80', 'Sta97'): '1号线', ('Sta80', 'Sta89'): '1号线', ('Sta89', 'Sta80'): '1号线', ('Sta89', 'Sta137'): '12号线', ('Sta137', 'Sta89'): '12号线', ('Sta89', 'Sta64'): '1号线', ('Sta64', 'Sta89'): '1号线', ('Sta64', 'Sta150'): '1号线', ('Sta150', 'Sta64'): '1号线', ('Sta150', 'Sta154'): '1号线', ('Sta154', 'Sta150'): '1号线', ('Sta154', 'Sta107'): '1号线', ('Sta107', 'Sta154'): '1号线', ('Sta107', 'Sta83'): '1号线', ('Sta83', 'Sta107'): '1号线', ('Sta83', 'Sta108'): '1号线', ('Sta108', 'Sta83'): '1号线', ('Sta108', 'Sta47'): '1号线', ('Sta47', 'Sta108'): '1号线', ('Sta159', 'Sta1'): '1号线', ('Sta1', 'Sta159'): '1号线', ('Sta129', 'Sta9'): '2号线', ('Sta9', 'Sta129'): '2号线', ('Sta9', 'Sta163'): '2号线', ('Sta163', 'Sta9'): '2号线', ('Sta163', 'Sta53'): '2号线', ('Sta53', 'Sta163'): '2号线', ('Sta53', 'Sta79'): '2号线', ('Sta79', 'Sta53'): '2号线', ('Sta79', 'Sta18'): '2号线', ('Sta18', 'Sta79'): '2号线', ('Sta18', 'Sta47'): '2号线', ('Sta47', 'Sta18'): '2号线', ('Sta47', 'Sta159'): '1号线', ('Sta159', 'Sta47'): '1号线', ('Sta47', 'Sta123'): '2号线', ('Sta123', 'Sta47'): '2号线', ('Sta123', 'Sta127'): '2号线', ('Sta127', 'Sta123'): '2号线', ('Sta127', 'Sta60'): '12号线', ('Sta60', 'Sta127'): '12号线', ('Sta127', 'Sta81'): '2号线', ('Sta81', 'Sta127'): '2号线', ('Sta81', 'Sta27'): '2号线', ('Sta27', 'Sta81'): '2号线', ('Sta27', 'Sta48'): '2号线', ('Sta48', 'Sta27'): '2号线', ('Sta48', 'Sta151'): '2号线', ('Sta151', 'Sta48'): '2号线', ('Sta151', 'Sta68'): '2号线', ('Sta68', 'Sta151'): '2号线', ('Sta68', 'Sta52'): '2号线', ('Sta52', 'Sta68'): '2号线', ('Sta52', 'Sta76'): '2号线', ('Sta76', 'Sta52'): '2号线', ('Sta76', 'Sta57'): '2号线', ('Sta57', 'Sta76'): '2号线', ('Sta57', 'Sta71'): '2号线', ('Sta71', 'Sta57'): '2号线', ('Sta71', 'Sta139'): '2号线', ('Sta139', 'Sta71'): '2号线', ('Sta139', 'Sta105'): '2号线', ('Sta105', 'Sta139'): '2号线', ('Sta105', 'Sta51'): '2号线', ('Sta51', 'Sta105'): '2号线', ('Sta51', 'Sta24'): '2号线', ('Sta24', 'Sta51'): '2号线', ('Sta143', 'Sta156'): '3号线', ('Sta156', 'Sta143'): '3号线', ('Sta156', 'Sta61'): '3号线', ('Sta61', 'Sta156'): '3号线', ('Sta61', 'Sta50'): '3号线', ('Sta50', 'Sta61'): '3号线', ('Sta50', 'Sta119'): '3号线', ('Sta119', 'Sta50'): '3号线', ('Sta119', 'Sta66'): '3号线', ('Sta66', 'Sta119'): '3号线', ('Sta66', 'Sta12'): '3号线', ('Sta12', 'Sta66'): '3号线', ('Sta12', 'Sta161'): '3号线', ('Sta161', 'Sta12'): '3号线', ('Sta161', 'Sta21'): '3号线', ('Sta21', 'Sta161'): '3号线', ('Sta21', 'Sta133'): '3号线', ('Sta133', 'Sta21'): '3号线', ('Sta133', 'Sta22'): '3号线', ('Sta22', 'Sta133'): '3号线', ('Sta22', 'Sta138'): '3号线', ('Sta138', 'Sta22'): '3号线', ('Sta138', 'Sta41'): '3号线', ('Sta41', 'Sta138'): '3号线', ('Sta41', 'Sta91'): '12号线', ('Sta91', 'Sta41'): '12号线', ('Sta41', 'Sta30'): '3号线', ('Sta30', 'Sta41'): '3号线', ('Sta30', 'Sta67'): '3号线', ('Sta67', 'Sta30'): '3号线', ('Sta67', 'Sta144'): '3号线', ('Sta144', 'Sta67'): '3号线', ('Sta144', 'Sta29'): '3号线', ('Sta29', 'Sta144'): '3号线', ('Sta29', 'Sta126'): '3号线', ('Sta126', 'Sta29'): '3号线', ('Sta126', 'Sta115'): '3号线', ('Sta115', 'Sta126'): '3号 线', ('Sta40', 'Sta131'): '3号线', ('Sta131', 'Sta40'): '3号线', ('Sta131', 'Sta39'): '3号线', ('Sta39', 'Sta131'): '3号线', ('Sta39', 'Sta100'): '3号线', ('Sta100', 'Sta39'): '3号线', ('Sta100', 'Sta135'): '3号线', ('Sta135', 'Sta100'): '3号线', ('Sta167', 'Sta113'): '3号线', ('Sta113', 'Sta167'): '3号线', ('Sta113', 'Sta141'): '3号线', ('Sta141', 'Sta113'): '3号线', ('Sta141', 'Sta142'): '3号线', ('Sta142', 'Sta141'): '3号线', ('Sta142', 'Sta158'): '3号线', ('Sta158', 'Sta142'): '3号线', ('Sta158', 'Sta44'): '3号线', ('Sta44', 'Sta158'): '3号线', ('Sta44', 'Sta117'): '3号线', ('Sta117', 'Sta44'): '3号线', ('Sta117', 'Sta147'): '3号线', ('Sta147', 'Sta117'): '3号线', ('Sta147', 'Sta42'): '3号线', ('Sta42', 'Sta147'): '3号线', ('Sta42', 'Sta35'): '3号线', ('Sta35', 'Sta42'): '3号线', ('Sta35', 'Sta87'): '3号线', ('Sta87', 'Sta35'): '3号线', ('Sta109', 'Sta33'): '3号线', ('Sta33', 'Sta109'): '3号线', ('Sta33', 'Sta112'): '3号线', ('Sta112', 'Sta33'): '3号线', ('Sta112', 'Sta153'): '3号线', ('Sta153', 'Sta112'): '3号线', ('Sta153', 'Sta125'): '3号线', ('Sta125', 'Sta153'): '3号线', ('Sta125', 'Sta121'): '3号线', ('Sta121', 'Sta125'): '3号线', ('Sta121', 'Sta11'): '3号线', ('Sta11', 'Sta121'): '3号线', ('Sta157', 'Sta114'): '10号线', ('Sta114', 'Sta157'): '10号线', ('Sta114', 'Sta15'): '11号线', ('Sta15', 'Sta114'): '11号线', ('Sta114', 'Sta168'): '10号线', ('Sta168', 'Sta114'): '10号线', ('Sta168', 'Sta135'): '10号线', ('Sta135', 'Sta168'): '10号线', ('Sta135', 'Sta167'): '3号线', ('Sta167', 'Sta135'): '3号线', ('Sta135', 'Sta134'): '10号线', ('Sta134', 'Sta135'): '10号线', ('Sta134', 'Sta95'): '12号线', ('Sta95', 'Sta134'): '12号线', ('Sta134', 'Sta85'): '10号线', ('Sta85', 'Sta134'): '10号线', ('Sta85', 'Sta2'): '10号线', ('Sta2', 'Sta85'): '10号线', ('Sta2', 'Sta4'): '10号线', ('Sta4', 'Sta2'): '10号线', ('Sta4', 'Sta103'): '10号线', ('Sta103', 'Sta4'): '10号线', ('Sta103', 'Sta145'): '10号线', ('Sta145', 'Sta103'): '10号线', ('Sta145', 'Sta88'): '10号线', ('Sta88', 'Sta145'): '10号线', ('Sta88', 'Sta87'): '10号线', ('Sta87', 'Sta88'): '10号线', ('Sta87', 'Sta109'): '3号线', ('Sta109', 'Sta87'): '3号线', ('Sta87', 'Sta94'): '10号线', ('Sta94', 'Sta87'): '10号线', ('Sta94', 'Sta160'): '10号线', ('Sta160', 'Sta94'): '10号线', ('Sta160', 'Sta7'): '10号线', ('Sta7', 'Sta160'): '10号线', ('Sta7', 'Sta6'): '10号线', ('Sta6', 'Sta7'): '10号线', ('Sta6', 'Sta8'): '10号线', ('Sta8', 'Sta6'): '10号线', ('Sta8', 'Sta75'): '10号线', ('Sta75', 'Sta8'): '10号线', ('Sta75', 'Sta152'): '11号线', ('Sta152', 'Sta75'): '11号线', ('Sta75', 'Sta102'): '10号线', ('Sta102', 'Sta75'): '10号线', ('Sta84', 'Sta90'): '4号线', ('Sta90', 'Sta84'): '4号线', ('Sta84', 'Sta59'): '4号线', ('Sta59', 'Sta84'): '4号线', ('Sta59', 'Sta19'): '4号线', ('Sta19', 'Sta59'): '4号线', ('Sta19', 'Sta62'): '4号线', ('Sta62', 'Sta19'): '4号线', ('Sta62', 'Sta165'): '4号线', ('Sta165', 'Sta62'): '4号线', ('Sta165', 'Sta38'): '4号线', ('Sta38', 'Sta165'): '4号线', ('Sta38', 'Sta58'): '4号线', ('Sta58', 'Sta38'): '4号线', ('Sta43', 'Sta10'): '5号线', ('Sta10', 'Sta43'): '5号线', ('Sta10', 'Sta96'): '5号线', ('Sta96', 'Sta10'): '5号线', ('Sta96', 'Sta132'): '5号线', ('Sta132', 'Sta96'): '5号线', ('Sta132', 'Sta37'): '5号线', ('Sta37', 'Sta132'): '5号线', ('Sta37', 'Sta16'): '5号线', ('Sta16', 'Sta37'): '5号线', ('Sta16', 'Sta69'): '5号线', ('Sta69', 'Sta16'): '5号线', ('Sta69', 'Sta54'): '5号线', ('Sta54', 'Sta69'): '5号线', ('Sta77', 'Sta122'): '11号线', ('Sta122', 'Sta77'): '11号线', ('Sta122', 'Sta36'): '11号线', ('Sta36', 'Sta122'): '11号线', ('Sta36', 'Sta28'): '11号线', ('Sta28', 'Sta36'): '11号线', ('Sta28', 'Sta124'): '11号线', ('Sta124', 'Sta28'): '11号线', ('Sta124', 'Sta166'): '11号线', ('Sta166', 'Sta124'): '11号线', ('Sta166', 'Sta99'): '11号线', ('Sta99', 'Sta166'): '11号线', ('Sta99', 'Sta140'): '11号线', ('Sta140', 'Sta99'): '11号线', ('Sta45', 'Sta75'): '11号线', ('Sta75', 'Sta45'): '11号线', ('Sta152', 'Sta164'): '11号线', ('Sta164', 'Sta152'): '11号线', ('Sta164', 'Sta82'): '11号线', ('Sta82', 'Sta164'): '11号线', ('Sta82', 'Sta111'): '11号线', ('Sta111', 'Sta82'): '11号线', ('Sta111', 'Sta140'): '11号线', ('Sta140', 'Sta111'): '11号线', ('Sta140', 'Sta13'): '11号线', ('Sta13', 'Sta140'): '11号线', ('Sta13', 'Sta70'): '11号线', ('Sta70', 'Sta13'): '11号线', ('Sta70', 'Sta55'): '11号线', ('Sta55', 'Sta70'): '11号线', ('Sta55', 'Sta20'): '11号线', ('Sta20', 'Sta55'): '11号线', ('Sta20', 'Sta23'): '11号线', ('Sta23', 'Sta20'): '11号线', ('Sta23', 'Sta26'): '12号线', ('Sta26', 'Sta23'): '12号线', ('Sta23', 'Sta56'): '11号线', ('Sta56', 'Sta23'): '11号线', ('Sta56', 'Sta54'): '5号线', ('Sta54', 'Sta56'): '5号线', ('Sta56', 'Sta118'): '11号线', ('Sta118', 'Sta56'): '11号线', ('Sta118', 'Sta115'): '11号线', ('Sta115', 'Sta118'): '11号线', ('Sta115', 'Sta40'): '3号线', ('Sta40', 'Sta115'): '3号线', ('Sta115', 'Sta162'): '11号线', ('Sta162', 'Sta115'): '11号线', ('Sta162', 'Sta114'): '11号线', ('Sta114', 'Sta162'): '11号线', ('Sta15', 'Sta72'): '12号线', ('Sta72', 'Sta15'): '12号线', ('Sta15', 'Sta86'): '11号线', ('Sta86', 'Sta15'): '11号线', ('Sta86', 'Sta46'): '11号线', ('Sta46', 'Sta86'): '11号线', ('Sta46', 'Sta3'): '11号线', ('Sta3', 'Sta46'): '11号线', ('Sta3', 'Sta92'): '12号线', ('Sta92', 'Sta3'): '12号线', ('Sta3', 'Sta63'): '11号线', ('Sta63', 'Sta3'): '11号线', ('Sta63', 'Sta129'): '2号线', ('Sta129', 'Sta63'): '2号线', ('Sta63', 'Sta25'): '11号线', ('Sta25', 'Sta63'): '11号线', ('Sta25', 'Sta146'): '11号线', ('Sta146', 'Sta25'): '11号线', ('Sta146', 'Sta130'): '11号线', ('Sta130', 'Sta146'): '11号线', ('Sta130', 'Sta120'): '11号线', ('Sta120', 'Sta130'): '11号线', ('Sta136', 'Sta137'): '12号线', ('Sta137', 'Sta136'): '12号线', ('Sta137', 'Sta101'): '12号线', ('Sta101', 'Sta137'): '12号线', ('Sta101', 'Sta31'): '12号线', ('Sta31', 'Sta101'): '12号线', ('Sta31', 'Sta17'): '12号线', ('Sta17', 'Sta31'): '12号线', ('Sta17', 'Sta23'): '12号线', ('Sta23', 'Sta17'): '12号线', ('Sta26', 'Sta90'): '12号线', ('Sta90', 'Sta26'): '12号线', ('Sta90', 'Sta134'): '12号线', ('Sta134', 'Sta90'): '12号线', ('Sta95', 'Sta15'): '12号线', ('Sta15', 'Sta95'): '12号线', ('Sta72', 'Sta93'): '12号线', ('Sta93', 'Sta72'): '12号线', ('Sta93', 'Sta3'): '12号线', ('Sta3', 'Sta93'): '12号线', ('Sta92', 'Sta116'): '12号线', ('Sta116', 'Sta92'): '12号线', ('Sta116', 'Sta32'): '12号线', ('Sta32', 'Sta116'): '12号线', ('Sta32', 'Sta41'): '12号线', ('Sta41', 'Sta32'): '12号线', ('Sta91', 'Sta127'): '12号线', ('Sta127', 'Sta91'): '12号线', ('Sta60', 'Sta148'): '12号线', ('Sta148', 'Sta60'): '12号线', ('Sta148', 'Sta73'): '12号线', ('Sta73', 'Sta148'): '12号线'}

    def createGraph(self):
        g = Graph()
        sta = []
        self.write(sta)
        temp_set = set()
        for part_pass in sta:
            temp_set.add(part_pass[0])
            temp_set.add(part_pass[-1])
        for temp_sta in temp_set:
            g.addVertex(temp_sta) 
        for part_pass in sta:
            g.addEdge(part_pass[0], part_pass[-1], len(part_pass)-1)
            g.addEdge(part_pass[-1], part_pass[0], len(part_pass)-1)
          
        self.sta = sta
        self.g = g

    def write(self,sta):
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        i = []
        j = []
        k = []
        l = []
        m = []
        n = []
        o = []
        p = []
        q = []
        r = []
        s = []
        t = []
        u = []
        v = []
        w = []
        x = []
        y = []
        z = []
        a1 = []
        a2 = []
        a3 = []
        a4 = []
        a5 = []
        a6 = []
        a7 = []
        a8 = []
        a9 = []
        a10 = []
        a11 = []
        a12 = []
        a13 = []
        
        a.append("Sta24")
        a.append("Sta51")
        a.append("Sta105")
        a.append("Sta139")
        a.append("Sta71")
        a.append("Sta57")
        a.append("Sta76")
        a.append("Sta52")
        a.append("Sta68")
        a.append("Sta151")
        a.append("Sta48")
        a.append("Sta27")
        a.append("Sta81")
        a.append("Sta127")
        b.append("Sta73")
        b.append("Sta148")
        b.append("Sta60")
        b.append("Sta127")
        c.append("Sta127")
        c.append("Sta123")
        c.append("Sta47")
        d.append("Sta1")
        d.append("Sta159")
        d.append("Sta47")
        e.append("Sta47")
        e.append("Sta108")
        e.append("Sta83")
        e.append("Sta107")
        e.append("Sta154")
        e.append("Sta150")
        e.append("Sta64")
        e.append("Sta89")
        f.append("Sta127")
        f.append("Sta91")
        f.append("Sta41")
        g.append("Sta89")
        g.append("Sta80")
        g.append("Sta97")
        g.append("Sta110")
        g.append("Sta106")
        g.append("Sta34")
        g.append("Sta128")
        g.append("Sta74")
        g.append("Sta149")
        g.append("Sta49")
        g.append("Sta65")
        h.append("Sta136")
        h.append("Sta89")
        i.append("Sta89")
        i.append("Sta137")
        i.append("Sta101")
        i.append("Sta31")
        i.append("Sta17")
        i.append("Sta23")
        j.append("Sta23")
        j.append("Sta20")
        j.append("Sta55")
        j.append("Sta70")
        j.append("Sta13")
        j.append("Sta140")
        k.append("Sta140")
        k.append("Sta99")
        k.append("Sta166")
        k.append("Sta124")
        k.append("Sta28")
        k.append("Sta36")
        k.append("Sta122")
        k.append("Sta77")
        l.append("Sta140")
        l.append("Sta111")
        l.append("Sta82")
        l.append("Sta164")
        l.append("Sta152")
        l.append("Sta75")
        m.append("Sta75")
        m.append("Sta102")
        n.append("Sta75")
        n.append("Sta45")
        o.append("Sta75")
        o.append("Sta8")
        o.append("Sta6")
        o.append("Sta7")
        o.append("Sta160")
        o.append("Sta94")
        o.append("Sta87")
        p.append("Sta11")
        p.append("Sta121")
        p.append("Sta125")
        p.append("Sta153")
        p.append("Sta112")
        p.append("Sta33")
        p.append("Sta109")
        p.append("Sta87")
        q.append("Sta58")
        q.append("Sta38")
        q.append("Sta165")
        q.append("Sta62")
        q.append("Sta19")
        q.append("Sta59")
        q.append("Sta84")
        q.append("Sta90")
        r.append("Sta23")
        r.append("Sta26")
        r.append("Sta90")
        s.append("Sta43")
        s.append("Sta10")
        s.append("Sta96")
        s.append("Sta132")
        s.append("Sta37")
        s.append("Sta16")
        s.append("Sta69")
        s.append("Sta54")
        s.append("Sta56")
        t.append("Sta90")
        t.append("Sta134")
        u.append("Sta87")
        u.append("Sta88")
        u.append("Sta145")
        u.append("Sta103")
        u.append("Sta4")
        u.append("Sta2")
        u.append("Sta85")
        u.append("Sta134")
        v.append("Sta87")
        v.append("Sta35")
        v.append("Sta42")
        v.append("Sta147")
        v.append("Sta117")
        v.append("Sta44")
        v.append("Sta158")
        v.append("Sta142")
        v.append("Sta141")
        v.append("Sta113")
        v.append("Sta167")
        v.append("Sta135")
        w.append("Sta56")
        w.append("Sta118")
        w.append("Sta115")
        x.append("Sta115")
        x.append("Sta126")
        x.append("Sta29")
        x.append("Sta144")
        x.append("Sta67")
        x.append("Sta30")
        x.append("Sta41")
        y.append("Sta143")
        y.append("Sta156")
        y.append("Sta61")
        y.append("Sta50")
        y.append("Sta119")
        y.append("Sta66")
        y.append("Sta12")
        y.append("Sta161")
        y.append("Sta21")
        y.append("Sta133")
        y.append("Sta22")
        y.append("Sta138")
        y.append("Sta41")
        z.append("Sta120")
        z.append("Sta130")
        z.append("Sta146")
        z.append("Sta25")
        z.append("Sta63")
        a1.append("Sta47")
        a1.append("Sta18")
        a1.append("Sta79")
        a1.append("Sta53")
        a1.append("Sta163")
        a1.append("Sta9")
        a1.append("Sta129")
        a1.append("Sta63")
        a2.append("Sta41")
        a2.append("Sta32")
        a2.append("Sta116")
        a2.append("Sta92")
        a2.append("Sta3")
        a3.append("Sta3")
        a3.append("Sta93")
        a3.append("Sta72")
        a3.append("Sta15")
        a4.append("Sta3")
        a4.append("Sta46")
        a4.append("Sta86")
        a4.append("Sta15")
        a5.append("Sta157")
        a5.append("Sta114")
        a6.append("Sta115")
        a6.append("Sta162")
        a6.append("Sta114")
        a7.append("Sta115")
        a7.append("Sta40")
        a7.append("Sta131")
        a7.append("Sta39")
        a7.append("Sta100")
        a7.append("Sta135")
        a8.append("Sta114")
        a8.append("Sta168")
        a8.append("Sta135")
        a9.append("Sta135")
        a9.append("Sta134")
        a10.append("Sta15")
        a10.append("Sta95")
        a10.append("Sta134")
        a11.append("Sta56")
        a11.append("Sta23")
        a12.append("Sta63")
        a12.append("Sta3")
        a13.append("Sta15")
        a13.append("Sta114")
        sta.extend([a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z])
        sta.append(a1)
        sta.append(a2)
        sta.append(a3)
        sta.append(a4)
        sta.append(a5)
        sta.append(a6)
        sta.append(a7)
        sta.append(a8)
        sta.append(a9)
        sta.append(a10)
        sta.append(a11)
        sta.append(a12)
        sta.append(a13)

    def dfs(self, s, s2, g, sta):
        result_list = []
        stack, seen, big_list = [s,], [], []
        for i in range(len(g.getVertex(s).getNeighbors())+1):
            seen.append(s)
        while len(stack):
            vertex = stack.pop()
            big_list.append(vertex)
            nodes = list(set(g.getVertex(vertex).getNeighbors()))
            names = [ver.getName() for ver in nodes]
            if s2 in names:
                result_list.append([list(big_list),])
                # yield(big_list)
                while True:
                    if len(big_list)>1:
                        pop2 = big_list.pop()
                    try:
                        if seen[-1] == seen[-2]:
                            pop1 = seen.pop()
                            if seen[-2] == seen[-1]:
                                break
                            else:
                                pop1 = seen.pop()
                                continue
                        pop1 = seen.pop()
                    except:
                        break

                continue
            flag = 0
            for neighbor in names:
                if neighbor not in seen:
                    flag += 1
                    stack.append(neighbor)
            for i in range(flag):
                seen.append(vertex)
            if flag>1:
                seen.append(vertex)
            elif flag==0:

                while True:
                    if len(big_list)>1:
                        pop2 = big_list.pop()
                    if seen[-1] == seen[-2]:
                        pop1 = seen.pop()
                        if seen[-2] == seen[-1]:
                            break
                        else:
                            pop1 = seen.pop()
                            continue
                    pop1 = seen.pop()
        
        result_list.sort(key = self.returnLength)
        return result_list

    def returnLength(self, a):
        return len(a)

    def getPassInfo(self, s, s2):

        #初始化
        sta = self.sta
        g = self.g
        
        if g.getVertex(s) == None:
            g.addVertex(s)
            for sta_list in sta:
                if s in sta_list:
                    index_of_s = sta_list.index(s)
                    if s2 in sta_list and g.getVertex(s2) == None:
                        index_of_s2 = sta_list.index(s2)
                        if index_of_s < index_of_s2:
                            return [sta_list[index_of_s: index_of_s2+1: 1], index_of_s2-index_of_s,[],0 [self.stationinfo_dict[s][0]] , 1.0]
                        else: 
                            return [sta_list[index_of_s: index_of_s2-1: -1], index_of_s-index_of_s2,[],0 [self.stationinfo_dict[s][0]] , 1.0]
                    g.addEdge(sta_list[0], s, index_of_s)
                    g.addEdge(s, sta_list[0], index_of_s)
                    g.addEdge(s, sta_list[-1], len(sta_list)-index_of_s)
                    g.addEdge(sta_list[-1], s, len(sta_list)-index_of_s)
                    g.deleteEdge(sta_list[0], sta_list[-1])
                    g.deleteEdge(sta_list[-1], sta_list[0])
                    self.passes37[(s, sta_list[0])] = sta_list[index_of_s-1:0:-1]
                    self.passes37[(s, sta_list[-1])] = sta_list[index_of_s+1:-1:1]
                    break
        
        if g.getVertex(s2) == None:
            g.addVertex(s2)
            for sta_list in sta:
                if s2 in sta_list:
                    index_of_s2 = sta_list.index(s2)
                    g.addEdge(sta_list[0], s2, index_of_s2)
                    g.addEdge(s2, sta_list[0], index_of_s2)
                    g.addEdge(s2, sta_list[-1], len(sta_list)-index_of_s2)
                    g.addEdge(sta_list[-1], s2, len(sta_list)-index_of_s2)
                    g.deleteEdge(sta_list[0], sta_list[-1])
                    g.deleteEdge(sta_list[-1], sta_list[0])
                    self.passes37[(sta_list[0], s2)] = sta_list[1:index_of_s2:1]
                    self.passes37[(sta_list[-1], s2)] = sta_list[-2:index_of_s2:-1]
                    break 
        df = pd.DataFrame(self.dfs(s,s2,g,sta))
        df[[0, 1]] = df.apply(self.getTotalPass,axis=1, args=(s2,), result_type="expand" )
        df = df.sort_values(by=1, ascending=True).head(8)
        df[[2,3,4]] = df.apply(self.getTranfer, axis=1, args=(s2,), result_type="expand")
        df = df.sort_values(by=[3, 1], ascending=True).head(3)
        # 5.计算各路线权重
        min_stations = df[1].min()
        min_transfer = df[3].min()
        df[5] = ( 0 + ( -0.75 * (df[1])/min_stations ) + (-1.33 * (df[3]-min_transfer)) ).apply(np.exp)
        # 6. 计算权重比例
        maxest = df[5].sum()
        df[5] = df[5]/maxest
        return np.array(df).tolist()

    def takeWeight1(self,iterable):
        return iterable[1]

    def takeWeight3(self,iterable):
        return iterable[3]
    
    def getTotalPass(self, small_list, s2):
        small_list = small_list[0]
        small_list.append(s2)
        # 3. 完整路线
        new_list = []
        for j in range(len(small_list)-1):
            new_list.append(small_list[j])
            new_list.extend(self.passes37[(small_list[j], small_list[j+1])])
        new_list.append(s2)
        return new_list, len(new_list)
    
    def getTranfer(self, small_list, s2):
        small_list = small_list[0]
        # 4. 换乘数量
        oldline = self.between_line[(small_list[0], small_list[1])]
        oldsta = small_list[0]
        passed_line = [oldline]
        passes_sta = []
        for k in range(len(small_list)-1):
            line = self.between_line[(small_list[k], small_list[k+1])]
            sta = small_list[k]
            if line != oldline:
                passed_line.append(line)
                passes_sta.append((oldsta, sta))
                if k==len(small_list)-2:
                    passes_sta.append((sta, s2))
                oldsta = sta
            oldline = line
        return (passes_sta, len(passed_line)-1, passed_line)
            

class DB():

    def __init__(self, DB):
        DB_USER = 'maker0'
        DB_PASS = 'Maker0000'
        DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
        DB_PORT = 3306
        DATABASE = DB
        self.connect_info = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)  #1
        # 查询语句，选出testexcel表中的所有数据
        # sql = """select * from trips"""
        # read_sql_query的两个参数: sql语句， 数据库连接
        # df = pd.read_sql_query(sql,con=self.connect_info)
        # 输出testexcel表的查询结果
        print('连接成功')
    
    def excute(self, sql="""select * from trips"""):
        df = pd.read_sql_query(sql,con=self.connect_info)
        print('筛选完毕')
        return(df)

    # def getPassRate(self, s1, s2):

class UseDB():

    @staticmethod
    def getPassRate(s1,s2):
        conn = DB('library1')
        df = conn.excute(f"SELECT * FROM trips WHERE 进站名称={s1} and 出站名称={s2}")
        df['time'] = (df['出站时间'] - df['进站时间']).dt.total_seconds()
        print(np.array(df['time']))
        np_df = np.array(df['time']).reshape(-1,1)
        result_list = Sklearn().kmean(np_df, 2)
        print(result_list)
        result_dict = list(Counter(result_list).values())
        result_rate = []
        for item in result_dict:
            result_rate.append(item/(result_dict[0] + result_dict[1]))
        return result_rate
        
class Sklearn():
  
    def __init__(self):
        pass
        # X = np.array([[1, 2], [1, 4], [1, 0],[10, 2], [10, 4], [10, 0]])
        # kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
        # print(kmeans.labels_)
        # a = kmeans.predict([[0, 0], [12, 3]])
        # print(kmeans.cluster_centers_)

    @staticmethod
    def kmean(self, x, n):
        kmeans = KMeans(n_clusters=n, random_state=0).fit(x)
        return(kmeans.labels_)



def main():
    # db = DB('library_flow')
    # cursor = db.connect_info.cursor()
    print('Hello')
    # rf_txt = ReadFile()
    # rf_txt.readTxt()
    # b = UseDB.getPassRate('Sta77','Sta115')
    a = Dfs()
    print(a.getPassInfo('Sta17','Sta72'))
    # print()


if __name__ == '__main__':
    main()

