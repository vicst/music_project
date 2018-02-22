import os
import random


with open("mail.txt", "w") as mail:
    for nr in range(10):
        mail.write("".join(random.choices("uirhgievdiufbvgfdnv", k = 8))+"@cnc.ro \n")