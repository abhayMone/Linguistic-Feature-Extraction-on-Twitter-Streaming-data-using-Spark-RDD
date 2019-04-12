import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import  style
import os
path= os.environ['HOME']
style.use('seaborn-deep')
file = path+'/example.txt'
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def animate(i):
    graph_data = open(file,'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    zs = []
    es = []
    bs = []
    cs = []
    for line in lines:
        if len(line) > 0:
            x, y, z, e, b, c = line.split(',')
            #print(zs)
            #print(xs)
            #print(ys)
            xs.append(int(x))
            ys.append(int(y))
            zs.append(int(z))
            es.append(int(e))
            bs.append(int(b))
            cs.append(int(c))
    ax1.clear()
    ax1.plot(xs,ys, label="Negative")
    ax1.set_xlabel('time(s)')
    ax1.set_ylabel('values(percentage)')
    ax1.set_title('Linguistic Features percentages from Live Twitter data')
    ax1.plot(xs,zs, label="Neutral")
    #ax1.legend([a,b],['Negative','Postitive'])
    ax1.plot(xs,es, label="Positive")
    ax1.plot(xs,bs, label="Vulgarity")
    ax1.plot(xs,cs, label="Opinion")
    ax1.legend(loc ='best')

    #ax1.set_yticks([0,5,10,15,20])
    #ax1.set_yticklabels(['0','5','10','15','20'])



ani = anim.FuncAnimation(fig, animate, interval= 100)
plt.show()