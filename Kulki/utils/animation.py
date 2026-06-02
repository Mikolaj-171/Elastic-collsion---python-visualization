import matplotlib.pyplot as plt
from kulka import move_kulki

def init(ax, kulki):
  global circles
  circles = []
  
  for patch in ax.patches[:]:
    patch.remove()
    
  for k in kulki:
    c = plt.Circle(k.r, k.R, facecolor='b', edgecolor = 'black',linewidth=0.7, alpha=0.8)
    circles.append(c)
    ax.add_patch(c)
    
  return circles

def update(frame, circles, kulki, dt, a):
  move_kulki(kulki, dt,a)
  for c, k in zip(circles, kulki):
      c.center = k.r
  return circles