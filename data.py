import json
data ={}
data = {}
data['conseiller'] = []
data['conseiller'].append({
    'mle': '0001',
    'login': 'ag0001Scott',
    'date_debut': '2012-11-10',
    'date_fin' : None
})
data['conseiller'].append({
    'mle': '0002',
    'login': 'ag0002Larry',
    'date_debut': '2011-09-15',
    'date_fin' : None
})
data['conseiller'].append({
    'mle': '0003',
    'login': 'ag0003Tim',
    'date_debut': '2010-03-22',
    'date_fin' : None
})

with open('Agent.txt', 'w') as outfile:
    json.dump(data, outfile)
