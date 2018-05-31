# -*- coding: cp1252 -*-
import selection as s

def mise_a_jour_budget(cc,
                       championnat,
                       prime_championnat,
                       coupe,
                       prime_coupe):
    budget_old = cc.budget
    ms = cc.masse_salariale
    revenus = cc.revenus

    if budget_old < 0:
        cc.avertissement += 1
    else:
        cc.avertissement = max(0, cc.avertissement - 1)

    cc.budget = budget_old - ms + revenus + championnat + prime_championnat + \
                coupe + prime_coupe

    print cc.nom, u': budget et avertissement mis à jour'

"""
Sauvegarde temporaire des budgets avant maj
"""
with open('temp_budgets.txt', 'w') as f:
    for nom in s.noms_clubs():
        cc = s.charger(nom, 'c')
        print cc.nom, cc.budget
        f.write(cc.nom+' '+str(cc.budget)+'\n')

"""
maj
"""
for nom in s.noms_clubs():
    print nom
    cc = s.charger(nom, 'c')

    championnat = int(raw_input(nom+' championnat ? '))
    prime_championnat  = int(raw_input(nom+' prime championnat ? '))
    coupe = int(raw_input(nom+' coupe ? '))
    prime_coupe = int(raw_input(nom+' prime coupe ? '))

    mise_a_jour_budget(cc,
                       championnat,
                       prime_championnat,
                       coupe,
                       prime_coupe)

    cc.sauvegarder()
