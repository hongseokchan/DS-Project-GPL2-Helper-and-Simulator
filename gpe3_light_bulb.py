from __future__ import division, print_function
from visual import *
from visual.graph import *
import wx
import math
import subprocess

def start_simulation(evt):
    global light_bulb_temperature, light_bulb_IV, bulb,bulbcone, light,lamp
    L = 0.037
    e = 0.35
    sigma = 5.67 * 10 ** -8
    c0 = 2.5795 * 10 ** 6
    R0 = 17.26
    rho0 = 5.51 * 10 ** -8
    alpha = 4.5 * 10 ** -3
    beta = 0.0004
    T0 = 300
    V0 = input_voltage
    freq = input_frequency

    def V(t):
        return V0 * math.sin(2 * math.pi * freq * t)

    def f(t, T):
        return (V(t) ** 2 / (alpha * rho0 * (T - T0) + rho0) - e * sigma * (
                    4 * math.pi * R0 / rho0) ** 0.5 * L ** 1.5 * (T ** 4 - T0 ** 4)) / (
                           beta * c0 * (T - T0) + c0) / L ** 2

    def R_from_T(T):
        return R0 * (1 + alpha * (T - T0))

    t0 = 0
    y0 = T0

    h = 1 / freq * 0.0002
    t_max = 100
    n = int(t_max / h)

    t = t0
    y = y0

    t_list = []
    y_list = []
    R_list = []
    I_list = []
    V_list = []

    t_list.append(t0)
    y_list.append(y0)
    R_list.append(R_from_T(y0))
    V_list.append(V(t0))
    I_list.append(V(t0) / (R_from_T(y0)))

    while True:
        rate(300)
        light_bulb_temperature.plot(pos=(t, y))
        light_bulb_IV.plot(pos = (V(t)/(R_from_T(y)), V(t)))

        k = (V(t) / (R_from_T(y))) * V(t) * 1.6
        print(k)

        k1 = f(t, y)
        k2 = f(t + h / 2, y + h * k1 / 2)
        k3 = f(t + h / 2, y + h * k2 / 2)
        k4 = f(t + h, y + h * k3)
        y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t + h

        brightyellow = (0.92 * k, 0.92 * k, 0.22 * k)
        bulb.color = brightyellow
        bulb.opacity = k * 0.7 + 0.2
        bulbcone.color = brightyellow
        light.color = (k,k,0)
        lamp.color = light.color

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
g1 = gdisplay(window=w, x = window.dwidth, y=disp.height + 50, width=(L), height=Hgraph,xtitle='t(s)', ytitle = 'Temperature(K)')

light_bulb_temperature = gcurve(display = g1.display, color = color.blue)

g2 = gdisplay(window=w, x = L+ 2 *window.dwidth ,y=disp.height + 50, width=(L), height=Hgraph,xtitle='Voltage(V)', ytitle = 'Current(A)' )
light_bulb_IV = gcurve(display = g2.display,color = color.red)

# Place buttons, radio buttons, a scrolling text object, and a slider
# in the right half of the window. Positions and sizes are given in
# terms of pixels, and pos(0,0) is the upper left corner of the window.
p = w.panel  # Refers to the full region of the window in which to place widgets

wx.StaticText(p, pos=(d, 4), size=(L - 2 * d, d), label='Simulated video',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

wx.StaticText(p, pos=(d + 20, disp.height+26), size=(L - 2 * d, d), label='Temperature versus time',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

wx.StaticText(p, pos=(d + L + 20, disp.height+26), size=(L - 2 * d, d), label='I-V characteristic ciurve for lightbulb',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

default_padding = 100

start_simul = wx.Button(p, label='Start Simulation', pos=(L * 1.35, L * 0.4+default_padding))
start_simul.Bind(wx.EVT_BUTTON, start_simulation)

input_voltage = 3
input_frequency = 0.1


def input_voltage_text_change(evt):  # called on slider events
    global input_voltage, input_voltage_text, input_voltage_slider
    value = input_voltage_slider.GetValue()
    input_voltage = value
    input_voltage_text.SetLabel(str(value))

input_voltage_slider = wx.Slider(p, pos=(1.0 * L, 0.1 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=10)
input_voltage_slider.Bind(wx.EVT_SCROLL,  input_voltage_text_change)
wx.StaticText(p, pos=(1.0 * L, 0.05 * L+default_padding), label='Input AC Voltage (V)')
input_voltage_text = wx.StaticText(p, pos=(1.7 * L, 0.05 * L+default_padding), label='0')

input_voltage_slider.SetValue(input_voltage)
input_voltage_text.SetLabel(str(input_voltage))

def input_frequency_text_change(evt):  # called on slider events
    global input_frequency, input_frequency_slider, input_frequency_text
    value = input_frequency_slider.GetValue()
    input_frequency = value/10
    input_frequency_text.SetLabel(str(value/10))

input_frequency_slider = wx.Slider(p, pos=(1.0 * L, 0.25 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=1000)
input_frequency_slider.Bind(wx.EVT_SCROLL, input_frequency_text_change)
wx.StaticText(p, pos=(1.0 * L, 0.2 * L+default_padding), label='Input AC frequency (Hz)')
input_frequency_text = wx.StaticText(p, pos=(1.7 * L, 0.2 * L+default_padding), label='0')

input_frequency_slider.SetValue(input_frequency * 10)
input_frequency_text.SetLabel(str(input_frequency))


#simulation geometry

bulb= sphere(pos = vector(0, 4, 0), radius = 4)
bulbcone= cone(pos = (0,1,0), axis = (0,-10,0), radius = sqrt(7))
bulbroot = cylinder(pos = vector(0, -0.5, 0), axis = (0, -3, 0), radius = 2.2)
bulbrootball = sphere(pos = vector(0, -3, 0), radius = 2.2)
table = box(pos = (0,-7,4), length = 25, height = 4, width = 12)
filamentroot = cylinder(pos = vector(0,1,0), axis = (0,1.3,0), radius = 0.5)
filamentroot1 = cylinder(pos = vector(1.0/3, -0.5, sqrt(3)/3), axis = (0,1.5,0), radius = 0.1)
filamentroot2 = cylinder(pos = vector(-1.0/3, -0.5, sqrt(3)/3), axis = (0,1.5,0), radius = 0.1)
filamentroot3 = cylinder(pos = vector(0, -0.5, -2/3), axis = (0,1.5,0), radius = 0.1,  thickness = 0.1/30)

rootstring = helix(pos = (0,-0.5,0), axis = (0,-3,0), radius = sqrt(7)-0.4, coils = 8, color = (0.129, 0.263, 0.396))

filament1 = curve(pos = [(1.0/3, 0.3, sqrt(3)/3),(2,3.8,0)], radius = 0.08, color = color.black, material = materials.shiny)
filament2 = curve(pos = [(-1.0/3, 0.3, sqrt(3)/3),(-2,3.8,0)], radius = 0.08, color = color.black, material = materials. shiny)
filament3 = curve(pos = [(-0.2,2,0), (-0.8, 3.8, 0)], radius = 0.08, color = color.black, material = materials.shiny)
filament3 = curve(pos = [(0.2,2,0), (0.8, 3.8, 0)], radius = 0.08, color = color.black, material = materials.shiny)
filament5 = helix(pos = (-2,3.8,0), axis = (4,0,0), color = color.black, radius = 0.3, coils = 80)

electriccurrent1 = curve(pos = [(7,-5,7),(1,-5,7)], radius = 0.08, color = color.blue)
electriccurrent2 = curve(pos = [(7,-5,7),(7,-3,0)], radius = 0.08, color = color.blue)
electriccurrent2 = curve(pos = [(0,-3,0),(7,-3,0)], radius = 0.08, color = color.blue)
electriccurrent4 = curve(pos = [(-7,-5,7),(-1,-5,7)], radius = 0.08, color = color.red)
electriccurrent5 = curve(pos = [(-7,-5,7),(-7,-3,0)], radius = 0.08, color = color.red)
electriccurrent6 = curve(pos = [(0,-3,0),(-7,-3,0)], radius = 0.08, color = color.red)
accurrent = cylinder(pos = (0,-4.8,7), radius = 1, color = color.black, axis = (0,-1,0), material = materials. plastic, spec = 0.1)
t = arange(-1,1,0.001)
ac = curve(x = t, y = -4.8, z = 7-0.5*sin(math.pi*t), radius = 0.1, color = color.white)

#color

ac.color = color.white
bulbcone.opacity = 0.7
bulbroot.color = (0.5, 0.5, 0.5)
bulbcone.material = materials.rough
bulbroot.material = materials.rough
bulbrootball.color = (0.129, 0.263, 0.396)
table.color = (0.396, 0.263, 0.129)

k = 0.1
brightyellow = (0.92*k,0.92*k,0.22*k)
bulb.color = brightyellow
bulb.opacity = k*0.7+0.2
bulbcone.color = brightyellow
light = sphere(pos = (0,3.8,0), radius = 0.8, color=(k,k,0), material=materials.emissive)
lamp = local_light(pos = light.pos, color = light.color)

def setleft(evt):
    global subprocess
    subprocess.Popen(["lightbub.pdf"], shell=True)

m = w.menubar # Refers to the menubar, which can have several menus

menu = wx.Menu()
item = menu.Append(-1, 'Open Document', 'Make box rotate to the left')
w.win.Bind(wx.EVT_MENU, setleft, item)
m.Append(menu, 'Options')