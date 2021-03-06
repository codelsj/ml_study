#!/usr/bin/env python
 
'''
File: demo_show.py
Author: foglsj@126.com
Date: 2018/04/02 18:54:54
'''
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1, 1, 50)
y1 = 2 * x + 1
y2 = 2 ** x + 1


plt.figure(num=3, figsize=(8, 5))
l1, = plt.plot(x, y1, label='aaa')
l2, = plt.plot(x, y2,
        color='red',
        linewidth=1.0,
        linestyle='-.',
        label='bbbb'
        )
plt.xlabel('I X')
plt.ylabel('I Y')

plt.xlim((-1,2))
plt.ylim((1,3))


new_ticks = np.linspace(-1, 2, 5)
plt.xticks(new_ticks)
plt.yticks([-2, -1.8, -1, 1.22, 3], ['$really\ bad$', r'$bad$', r'$normal$', r'$good$', r'$readly\ good$'])

#ax = plt.gca()
#ax.spines['right'].set_color('none')
#ax.spines['top'].set_color('none')

#ax.xaxis.set_ticks_position('bottom')
#ax.yaxis.set_ticks_position('left')


#ax.spines['bottom'].set_position(('data', 0))
#ax.spines['left'].set_position(('data', 0))

#plt.legend(handles=[l1, l2],  labels=['aaa', 'bbb'], loc='best')
plt.legend(handles=[l1, l2], 
                   labels = ['aaa', 'bbb'], 
                              loc = 'best'
                                        )


plt.show()
