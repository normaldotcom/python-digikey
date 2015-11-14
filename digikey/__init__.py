# -*- coding: utf-8 -*-
from __future__ import division
import code

from bs4 import BeautifulSoup
from bs4 import Comment



# EMZ TODO: need to handle the mu symbol properly

def parse_number(s):
    print("Parsing number " + str(s.encode('utf-8')))
    s = s.strip()
    if ' ' in s: # deal with '2000V (2kV)'
        s = s[:s.index(' ')]
    units = [u'F', u'V', u'VAC', u'H']
    for unit in units:
        if s.endswith(unit):
            s = s[:s.index(unit)]
            break

    multipliers = {u'k': 1e3, u'M': 1e6, u'G': 1e9, u'µ': 1e-6, u'u': 1e-6, u'm': 1e-3, u'p': 1e-12, u'n': 1e-9, u'K': 1e3}
    mult = 1
    while s[-1] in multipliers:
        mult *= multipliers[s[-1]]
        s = s[:-1]
    if s == '-': return None
    if s == '*': return None
    return float(s) * mult

def parse_tolerance(s):
    print("Parsing tolerance " + str(s))
    def parse_percentage(s):
        s = s.strip()
        assert s[-1] == u'%'
        return float(s[:-1])/100
    
    s = s.strip()
    
    #print (s,)
    
    if s == u'Jumper':
        print (1, 1)
        return (1, 1)
    elif s.startswith(u'\xb1'):
        x = parse_percentage(s[1:])
        print (1-x, 1+x)
        return (1-x, 1+x)
    elif u',' in s:
        left, right = s.split(u',')
        x = (1+parse_percentage(left), 1+parse_percentage(right))
        print(tuple(sorted(x)))
        return tuple(sorted(x))
    else:
        print(repr(s))
        return None

def within_tolerance(desired, tolerance_percent, actual):
	if desired == 0:
		return actual == desired
	else:
		return abs(actual - desired)/desired <= tolerance_percent/100

class FilteringPage(object):
    def __init__(self, r):
        form = r.html.find('form', dict(name='attform'))
        table = form.table
        params = [th.string for th in table.tr.findAll('th')]
        print(params)

        #selects = [td.select for td in table.tr.findNextSibling().findAll('td', recursive=False)]
        tablecells = table.tr.findNextSibling().findAll('select', recursive=True)
        selects = {}
        ctr = 0
#        for cell in tablecells:
#            selects[ctr] = cell.findAll('option') 
#            ctr = ctr + 1
        selects = tablecells

#        vars = globals()
#        vars.update(locals())
#        shell=code.InteractiveConsole(vars)
#        shell.interact()
 
        assert len(selects) == len(params)
        
        self.params = params
        self.selects = selects
        
        results = r.html.find('table', dict(id='productTable'))
        self.first_part_number = results.tbody.tr.find('td', {'class': 'digikey-partnumber'}).a.string

    def produce_filter_options(self, name, func):
        i = self.params.index(name)
        selected = self.selects[i]

        print(selected['name'])

        res = [(selected['name'], option['value'])
           for option in selected.findAll('option', recursive=True)
            if func(' '.join(x for x in option if not isinstance(x, Comment)))]
        if not res:
            assert False, 'filter matched nothing'
        return res
