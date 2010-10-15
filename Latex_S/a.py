from GChartWrapper import Pie
from GChartWrapper import Pie3D

p=Pie3D( [1,2,3,4] ).label('A','B','C','D').color('00dd00')
p.save('a.png')

p=Pie([5,10,15]).title('Hello Pie').color('red','lime').label('hello', 'world','Hello World')
p.save('b.png')