import math
import numpy as np


def combination(count):
  return int(math.factorial(count)/(math.factorial(2)*math.factorial(count-2)))

class Kulka:
  def __init__(self, m,r,v ):
    if type(m)!= float:
      raise Exception("Masa ma byc floatem!\n")

    if type(r)!= np.ndarray and type(r)!= list:
      raise Exception("Masa ma byc floatem!\n")

    if type(v)!= np.ndarray and type(v)!= list:
      raise Exception("Polozenie musi byc wektorem!")
    if m <= 0:
      raise Exception("Masa mniejsza od 0!")

    self.m = m
    self.r = np.array(r, dtype=np.float32)
    self.v = np.array(v, dtype=np.float32)
    self.R = np.array(np.sqrt(m), dtype=np.float32)
    self.E = 0.5 * m * np.linalg.norm(self.v)**2

  def __str__(self):
    napis = f"Predkosc: {self.v}\nMasa: {self.m}\nPolozenie: {self.r}\n"
    return napis

def check_colission(kulki):

    count = len(kulki)
    collisions = []
    pary = []

    for first in range(count):
        for second in range(first+1, count):
            pary.append((first, second))

            dx = kulki[second].r[0] - kulki[first].r[0]
            dy = kulki[second].r[1] - kulki[first].r[1]
            distance_sq = dx**2 + dy**2
            
            R1 = kulki[second].R
            R2 = kulki[first].R
            
            if distance_sq <= (R1+R2)**2:
                collisions.append(True)
            else:
                collisions.append(False)

    return collisions, pary

def check_wall(kulki,a):
  count = len(kulki)
  collisions_x = []
  collisions_y = []

  for idx in range(count):
    rx = kulki[idx].r[0]
    ry = kulki[idx].r[1]
    R = kulki[idx].R
    if rx <= R or rx >= a - R:
      collisions_x.append(True)
    else:
      collisions_x.append(False)

    if ry<= R or ry >= a-R:
      collisions_y.append(True)
    else:
      collisions_y.append(False)
  return collisions_x, collisions_y

def move_kulki(kulki, dt,a):

  count = len(kulki)

  for i in range(count):
      kulki[i].r += kulki[i].v * dt

  kulki_col, pary = check_colission(kulki)
  wall_x, wall_y = check_wall(kulki,a)
  if count > 1:
      for i in range(combination(count)):
          if kulki_col[i]:
              first = pary[i][0]
              second = pary[i][1]

              dx = kulki[second].r[0] - kulki[first].r[0]
              dy = kulki[second].r[1] - kulki[first].r[1]
              D = np.sqrt(dx**2 + dy**2)

              if D == 0:
                  dx, dy = 1, 0
                  D = 1

              nx = dx / D
              ny = dy / D

              v_rel = (kulki[first].v[0] - kulki[second].v[0]) * nx + \
                      (kulki[first].v[1] - kulki[second].v[1]) * ny
              m1 = kulki[first].m
              m2 = kulki[second].m

              v1n_final = kulki[first].v[0] - (2*m2/(m1+m2)) * v_rel * nx
              v1t_final = kulki[first].v[1] - (2*m2/(m1+m2)) * v_rel * ny

              v2n_final = kulki[second].v[0] + (2*m1/(m1+m2)) * v_rel * nx
              v2t_final = kulki[second].v[1] + (2*m1/(m1+m2)) * v_rel * ny

              kulki[first].v[0] = v1n_final
              kulki[first].v[1] = v1t_final
              kulki[second].v[0] = v2n_final
              kulki[second].v[1] = v2t_final
              R1 = kulki[first].R
              R2 = kulki[second].R
              overlap = R1+R2 - D #dt moze byc zbyt duze lub na poczatku nachodza na siebie:
              if overlap > 0:
                  separation = overlap / 2 + 0.001
                  kulki[first].r[0] -= separation * nx
                  kulki[first].r[1] -= separation * ny
                  kulki[second].r[0] += separation * nx
                  kulki[second].r[1] += separation * ny

              kulki[first].E = 0.5 * m1 * np.linalg.norm(kulki[first].v)**2
              kulki[second].E = 0.5 * m2 * np.linalg.norm(kulki[second].v)**2

  for i in range(count):
      if wall_x[i]:
          kulki[i].v[0] = -kulki[i].v[0]
          R = kulki[i].R
          if kulki[i].r[0] < R:
              kulki[i].r[0] = R
          else:
              kulki[i].r[0] = a - R

      if wall_y[i]:
          R = kulki[i].R
          kulki[i].v[1] = -kulki[i].v[1]

          if kulki[i].r[1] < R:
              kulki[i].r[1] = R
          else:
              kulki[i].r[1] = a - R


      kulki[i].E = 0.5 * kulki[i].m * np.linalg.norm(kulki[i].v)**2

  return kulki


def main(a, dt):
  count = int(input("Podaj ile kulek: "))
  random = bool(int(input("Parametry generowane losowe (0 lub 1): ")))
  kulki = []
  used_r = []
  max_attempts = 100
  bool_tab = []
  T = int(input("Podaj czas animacji w sekundach: "))

  for idx in range(count):
    if random == False:
      vx = float(input(f"\nPodaj predkosc pozioma kulki numer: {idx+1}: "))
      vy = float(input(f"Podaj predkosc pionowa kulki numer: {idx+1}: "))
      m = float(input("Podaj mase kulki: "))
      rx = float(input(f"Podaj wektor x: "))
      ry = float(input("Podaj wektor y: "))
      v = [vx,vy]
      r = [rx,ry]
      R = np.sqrt(m)

      if (rx >= a-R or ry >= a-R) or (rx <= R or ry <= R):
        raise Exception("Kulka poza sciana!")
      if m <= 0:
        raise Exception("Masa musi byc dodatnia!")

    else:
      print("\n")
      m = np.random.uniform(low=0.1, high=2)
      R = np.sqrt(m)
      v = np.random.uniform(low=-3, high=3, size=2)
      r = np.random.uniform(low=R, high=a-R, size=2)

    for j in range(max_attempts):
      for num,old_r in enumerate(used_r):
        if (old_r[0] - r[0])>R and (old_r[1] - r[1])>R:
          bool_tab.append(True)
        else:
          r = np.random.uniform(low=R, high=a-R, size=2)
          bool_tab = []

    if np.array(bool_tab).all() == True:
      used_r.append(r)
      kulki.append(Kulka(m,r,v))

  return kulki, T