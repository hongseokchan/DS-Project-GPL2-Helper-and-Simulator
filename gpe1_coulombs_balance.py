from __future__ import division, print_function
from visual import *
from visual.graph import *
import wx
import subprocess
import visual

def start_simulation(evt):
    global lball, rball, rhorpole, rverpole, rplate, lhorpole, triangleplate, lplate, lverpole1,lverpole2,lverpoleball,ltopplate
    global angle_ball, max_angle
    q = initial_voltage * 0.01/9/10**9
    k = 9 * 10 ** 9
    lball.visible = False
    rball.visible = False
    rhorpole.visible = False
    rverpole.visible = False
    rplate.visible = False
    lhorpole.visible = False
    triangleplate.visible = False
    lplate.visible = False
    lverpole1.visible = False
    lverpole2.visible = False
    lverpoleball.visible = False
    ltopplate.visible = False

    # 0<=t<=5
    t = 10
    i = 0
    # balls
    lball = sphere(pos=(0, 5, 0), color=color.green, radius=1)
    rball = sphere(pos=(12.0, 5, 0), color=color.green, radius=1)

    rhorpole = cylinder(pos=(12.0, 5, 0), axis=(4, 0, 0), radius=0.2, color=(0.976, 0.878, 0.776),
                        material=materials.wood)
    rverpole = cylinder(pos=(16.0, 5.4, 0), axis=(0, -5.4, 0), radius=0.3, color=(0.965, 0.80, 0.635),
                        material=materials.wood)

    if 12 < final_distance * 1.5:
        rball.visible = False
        rhorpole.visible = False
        rverpole.visible = False
        rball = sphere(pos=(final_distance * 1.5, 5, 0), color=color.green, radius=1)

        # rightpiece
        rhorpole = cylinder(pos=(final_distance * 1.5, 5, 0), axis=(4, 0, 0), radius=0.2, color=(0.976, 0.878, 0.776),
                            material=materials.wood)
        rverpole = cylinder(pos=(final_distance * 1.5 + 4, 5.4, 0), axis=(0, -5.4, 0), radius=0.3, color=(0.965, 0.80, 0.635),
                            material=materials.wood)
    rplate = box(pos=(19.0, 0.4, 0), length=30, width=3, height=0.8, color=(0.965, 0.80, 0.635),
                 material=materials.wood)

    # leftpiece
    lhorpole = cylinder(pos=(0, 5, 0), axis=(0, 0, -5), radius=0.2, color=(0.5, 0.5, 0.5), material=materials.shiny)

    tri = shapes.triangle(length=3, rotate=i)
    triangleplate = extrusion(pos=paths.line(start=(0, 4.8, -6), end=(0, 5.2, -6)), shape=tri, color=(0.5, 0.5, 0.5))
    lplate = box(pos=(0, 0.4, -5), length=8, width=13, height=0.8, color=(0.976, 0.878, 0.776), material=materials.wood)
    lverpole1 = cylinder(pos=(-2, 0, -10), axis=(0, 10, 0), radius=0.3, color=(0.5, 0.5, 0.5), material=materials.shiny)
    lverpole2 = cylinder(pos=(2, 0, -10), axis=(0, 10, 0), radius=0.3, color=(0.5, 0.5, 0.5), material=materials.shiny)
    ltopplate = box(pos=(0, 10, -6), length=5, width=8, height=0.4, color=(0.976, 0.878, 0.776),
                    material=materials.wood)
    lverpoleball = cylinder(pos=(0, 4.8, -6), axis=(0, 5.2, 0), radius=0.1)
    triangleplate.material = materials.shiny

    lhorpole.rotate(axis=(0, 1, 0), origin=(0, 5, -6), angle=-i)
    lball.rotate(axis=(0, 1, 0), origin=(0, 5, -6), angle=-i)

    h = 0.001

    i_dot = 0

    r = 0.2
    I = 0.01 * r ** 2
    kappa = 0.006
    flag = 1
    b = 0.005
    F_const = 0
    time = 0
    while rball.pos.x * 0.1 >= final_distance * 0.1:
        rate(1000)
        F = k * q ** 2 / ((rball.pos.x - lball.pos.x) * 0.1)** 2 * 1 - kappa * i - b * i_dot
        if abs(F) < abs(F_const) / 100:
            break
        if flag == 1:
            rhorpole.pos.x -= 1 * h
            rball.pos.x -= 1 * h
            rverpole.pos.x -= 1 * h

        if rball.pos.x * 0.1 <= final_distance * 0.1:
            rhorpole.pos.x += 1 * h
            rball.pos.x += 1 * h
            rverpole.pos.x += 1 * h
            flag = 0
            F_const = F
            print(F_const)

        i_dot += F * r / I * h * 100
        i += i_dot * h
        time += h
        #print(q)
        #print(i_dot)
        print('F:',F)

        tri.visible = False
        triangleplate.visible = False

        tri = shapes.triangle(length=3, rotate=i)
        triangleplate = extrusion(pos=paths.line(start=(0, 4.8, -6), end=(0, 5.2, -6)), shape=tri,color=(0.5, 0.5, 0.5))
        lhorpole.rotate(axis=(0, 1, 0), origin=(0, 5, -6), angle=-i)
        lball.rotate(axis=(0, 1, 0), origin=(0, 5, -6), angle=-i)

        q -= q * lose_charge_rate * 0.1 * h

        print(time,i)

        angle_ball.plot(pos=(time,i))
    max_angle.plot(pos=(final_distance,i))






L = 400
Hgraph = 300
# Create a window. Note that w.win is the wxPython "Frame" (the window).
# window.dwidth and window.dheight are the extra width and height of the window
# compared to the display region inside the window. If there is a menu bar,
# there is an additional height taken up, of amount window.menuheight.
# The default style is wx.DEFAULT_FRAME_STYLE; the style specified here
# does not enable resizing, minimizing, or full-sreening of the window.
w = window(width = 2 * (L + window.dwidth), height = L + window.dheight + window.menuheight + Hgraph,
           menus=True, title='Widgets',
           style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

# Place a 3D display widget in the left half of the window.
d = 20
disp = display(window=w, x=d, y=d, width=L - 2 * d, height=L - 2 * d, forward=-vector(0, 1, 2))
g1 = gdisplay(window=w, x = window.dwidth, y=disp.height + 50, width=(L), height=Hgraph,xtitle='x(m)', ytitle = 'B(T)')

angle_ball = gcurve(display = g1.display, color = color.blue)

g2 = gdisplay(window=w, x = L+ 2 *window.dwidth ,y=disp.height + 50, width=(L), height=Hgraph,xtitle='x(m)', ytitle = 'B(T)' )

max_angle = gcurve(display = g2.display,color = color.red)

#some geometrical constants
final_distance = 2
initial_voltage= 6000
lose_charge_rate = 0

# Place buttons, radio buttons, a scrolling text object, and a slider
# in the right half of the window. Positions and sizes are given in
# terms of pixels, and pos(0,0) is the upper left corner of the window.
p = w.panel  # Refers to the full region of the window in which to place widgets

wx.StaticText(p, pos=(d, 4), size=(L - 2 * d, d), label='Simulated video',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

wx.StaticText(p, pos=(d + 20, disp.height+26), size=(L - 2 * d, d), label='Rotation angle(rad) vs time(s)',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

wx.StaticText(p, pos=(d + L + 20, disp.height+26), size=(L - 2 * d, d), label='Maximum angle(rad) vs distance(m)',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

default_padding = 50

start_simul = wx.Button(p, label='Start Simulation', pos=(L * 1.35, L * 0.65))
start_simul.Bind(wx.EVT_BUTTON, start_simulation)

def final_distance_text_change(evt):  # called on slider events
    global final_distance, final_distance_slider, final_distance_text
    value = final_distance_slider.GetValue()
    final_distance = final_distance_slider.GetValue()
    final_distance_text.SetLabel(str(value))

final_distance_slider = wx.Slider(p, pos=(1.0 * L, 0.1 * L+default_padding), size=(0.9 * L, 20), minValue= 2, maxValue=20)
final_distance_slider.Bind(wx.EVT_SCROLL,  final_distance_text_change)
wx.StaticText(p, pos=(1.0 * L, 0.05 * L+default_padding), label='Final_distance between two charged sphere(cm)')
final_distance_text = wx.StaticText(p, pos=(1.7 * L, 0.05 * L+default_padding), label='0')

final_distance_slider.SetValue(final_distance)
final_distance_text.SetLabel(str(final_distance))

def initial_voltage_text_change(evt):  # called on slider events
    global initial_voltage, initial_voltage_slider, initial_voltage_text
    value = initial_voltage_slider.GetValue()
    initial_voltage = initial_voltage_slider.GetValue() * 100
    initial_voltage_text.SetLabel(str(value * 100))

initial_voltage_slider = wx.Slider(p, pos=(1.0 * L, 0.25 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=100)
initial_voltage_slider.Bind(wx.EVT_SCROLL, initial_voltage_text_change)
wx.StaticText(p, pos=(1.0 * L, 0.2 * L+default_padding), label='charge voltage')
initial_voltage_text = wx.StaticText(p, pos=(1.7 * L, 0.2 * L+default_padding), label='0')

initial_voltage_slider.SetValue(initial_voltage / 100)
initial_voltage_text.SetLabel(str(initial_voltage))

def lose_charge_rate_text_change(evt):  # called on slider events
    global lose_charge_rate,lose_charge_rate_text,lose_charge_rate_slider
    value = lose_charge_rate_slider.GetValue()
    lose_charge_rate = lose_charge_rate_slider.GetValue() * 0.01
    lose_charge_rate_text.SetLabel(str(value * 0.01))

lose_charge_rate_slider = wx.Slider(p, pos=(1.0 * L, 0.4 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=100)
lose_charge_rate_slider.Bind(wx.EVT_SCROLL, lose_charge_rate_text_change)
wx.StaticText(p, pos=(1.0 * L, 0.35 * L+default_padding), label='Charge Losing rate')
lose_charge_rate_text = wx.StaticText(p, pos=(1.7 * L, 0.35 * L+default_padding), label='0')

lose_charge_rate_slider.SetValue(lose_charge_rate * 100)
lose_charge_rate_text.SetLabel(str(lose_charge_rate))

# 0<=t<=5
t=0
#balls
lball  = sphere(pos = (0,5,0),color = color.green, radius = 1)
rball = sphere(pos = (2.0+t,5,0), color = color.green, radius = 1)

#rightpiece
rhorpole = cylinder(pos = (1.9+t,5,0), axis = (4,0,0), radius = 0.2, color= (0.976, 0.878, 0.776), material = materials.wood)
rverpole = cylinder(pos = (5.9+t,5.4,0), axis = (0,-5.4,0), radius = 0.3, color = (0.965, 0.80, 0.635), material = materials.wood)
rplate = box(pos = (11.5,0.4,0), length = 15, width = 3, height = 0.8, color = (0.965, 0.80, 0.635), material = materials.wood)

#leftpiece
lhorpole = cylinder(pos = (0,5,0), axis = (0,0,-5), radius = 0.2, color = (0.5,0.5,0.5),material = materials.shiny)
i=0
tri = shapes.triangle(length = 3, rotate=i)
triangleplate = extrusion(pos = paths.line(start = (0,4.8,-6),end = (0,5.2,-6)), shape = tri, color = (0.5,0.5,0.5))
lplate = box(pos = (0,0.4,-5), length = 8, width = 13, height = 0.8,  color= (0.976, 0.878, 0.776), material = materials.wood)
lverpole1 = cylinder(pos = (-2,0,-10), axis = (0,10,0),radius = 0.3,color = (0.5,0.5,0.5), material = materials.shiny)
lverpole2 = cylinder(pos = (2,0,-10),axis = (0,10,0), radius = 0.3, color = (0.5,0.5,0.5), material = materials.shiny)
ltopplate = box(pos = (0,10,-6), length = 5, width = 8, height = 0.4,  color= (0.976, 0.878, 0.776), material = materials.wood)
lverpoleball = cylinder(pos = (0,4.8,-6), axis = (0,5.2,0), radius = 0.1)
triangleplate.material = materials.shiny

lhorpole.rotate(axis = (0,1,0), origin = (0,5,-6),angle = -i)
lball.rotate(axis = (0,1,0), origin = (0,5,-6),angle = -i)


def setleft(evt):
    global subprocess
    subprocess.Popen(["coulomb.pdf"], shell=True)

m = w.menubar # Refers to the menubar, which can have several menus

menu = wx.Menu()
item = menu.Append(-1, 'Open Document', 'Make box rotate to the left')
w.win.Bind(wx.EVT_MENU, setleft, item)
m.Append(menu, 'Options')