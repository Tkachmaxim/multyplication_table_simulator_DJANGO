import collections
import pandas

It=collections.namedtuple('It',['name','job','data'])
new_data=pandas.DataFrame(data={'members':['Artem Tkach', 'Yehor Tkach', 'Oksana Yereshenko'], 'age':[7,4,37]})
print(new_data['members'].map(lambda p:p.split()[0].upper()))


def some_f(data):
    if isinstance(data,int):
        return It(name='Max', job='Megacom', data='12.15')
    else:
        return It(name='Nothing', job='Nothing', data='Nothing')




