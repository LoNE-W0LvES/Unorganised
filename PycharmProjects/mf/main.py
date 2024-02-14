# import pandas as pd
#
# data = pd.read_csv('data.csv')
#
# data.dropna(inplace=True)
#
# data = pd.get_dummies(data, columns=['WindGustDir', 'WindDir9am', 'WindDir3pm', 'RainToday', 'RainTomorrow'])
#
# data = data.apply(pd.to_numeric, errors='coerce')
#
# X = data.drop(columns=['RainTomorrow_Yes'])
# y = data['RainTomorrow_Yes']
#
# data.to_csv('d.csv')
# print(data)

gg = open('d2.csv', 'r').read().replace("True", "1").replace("False", "0")
open('d3.csv', 'w').write(gg)