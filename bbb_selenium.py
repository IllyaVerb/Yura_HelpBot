import requests as req
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re, time

import classes.Student_In_Meeting as sim

  
# Виноград
#go_in_meet("https://bbb.comsys.kpi.ua/b/x2g-dqc-6fg", "Undef", [("Доброго дня", False)])

# Жабін
#go_in_meet("https://bbb.comsys.kpi.ua/b/val-3gt-q6j", "Undef", [("Доброго дня", False)])

# Клименко
#go_in_meet("https://bbb.comsys.kpi.ua/b/iry-ped-qe9", "Баланюк", [("Доброго дня", False)])

stud = sim.Student_In_Meeting()
stud.go_in_meeting("https://bbb.comsys.kpi.ua/b/iry-ped-qe9", "Найкращий студент", [("Доброго дня", False),
                                                                                      ("До побачення", False)])
time.sleep(10)

stud.exit_meeting()
