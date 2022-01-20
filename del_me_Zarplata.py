# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 10:50:50 2021

@author: manager
"""
from math import sqrt


def converter(row: str):
    return list(map(float, row.split()))


def delta(par, step):
    return (par[1]-par[0]) / step


REALIZ = '525197 966995 669516 1216821 1082414 872851 966624 1038901 1053446 920501 1027812 984514 1476105 995015 1608580 1571390'
realiz = converter(REALIZ)

ZAKAZ = '183 155 169 215 312 128 189 207 288 142 154 190 343 140 259 243'
zakaz = converter(ZAKAZ)

ZP = '15387 23743 15246 26416 27002 22267 19810 27390 29996 19466 22444 28272 40496 23617 36516 31816'
zp = converter(ZP)

percent_realiz = (0, 0.007)
porog = (50, 200)
za_zakaz_over_porog = (10, 200)
stavka = (14000, 18000)

steps = 30

percents = [percent_realiz[0] + i*delta(percent_realiz, steps) for i in range(steps)]
porogs = [porog[0] + i*delta(porog, steps) for i in range(steps)]
za_zakaz = [za_zakaz_over_porog[0] + i*delta(za_zakaz_over_porog, steps) for i in range(steps)]
stavky = [stavka[0] + i*delta(stavka, steps) for i in range(steps)]

optimal_set = dict.fromkeys(["p%", 'porog', 'za_zakaz', 'stavka', 'min'])
value = 150000
for p in percents:
    for porog_ in porogs:
        for zz in za_zakaz:
            for stavka_ in stavky:
                sum_delta2 = 0
                for i in range(len(zp)):
                    sum_delta2 += (p*realiz[i] + zz*(zakaz[i]-porog_) + stavka_ - zp[i])**2

                if value > sqrt(sum_delta2):
                    value = sqrt(sum_delta2)
                    optimal_set["p%"] = p
                    optimal_set['porog'] = porog_
                    optimal_set['za_zakaz'] = zz
                    optimal_set['stavka'] = stavka_
                    optimal_set['min'] = sqrt(sum_delta2)

print(optimal_set)
