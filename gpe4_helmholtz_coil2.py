from __future__ import division, print_function
from visual import *
from visual.graph import *
import wx
import subprocess
import visual

def start_simulation(evt):
    global straight1, ring1, straight2, ring2, rail, probe_tip, probe_body, car_body, car_wheel1, car_wheel2, car_wheel3, car_wheel4
    global coil_radius_width, coil_radius, simulation_speed,simulation_scale, circ1,circ2, dist_coil, rail_y, probe_y, num_coil, current, coil_width, parallel_magnetic, perpendicular_magnetic
    global g1,g2, Bx,By, xrange
    global w
    '''
    #deleting the graph
    g1.visible = 0
    g2.visible = 0

    g1 = gdisplay(window=w, x=window.dwidth, y=disp.height + 50, width=(L), height=Hgraph, xtitle='x(m)', ytitle='B(T)')
    parallel_magnetic = gcurve(display=g1.display, color=color.blue)
    g2 = gdisplay(window=w, x=L + 2 * window.dwidth, y=disp.height + 50, width=(L), height=Hgraph, xtitle='x(m)',ytitle='B(T)')
    perpendicular_magnetic = gcurve(display=g2.display, color=color.red)
    '''

    ring1.visible = False
    ring2.visible = False
    rail.visible = False
    probe_tip.visible=False
    probe_body.visible=False
    car_body.visible=False
    car_wheel1.visible=False
    car_wheel2.visible = False
    car_wheel3.visible = False
    car_wheel4.visible = False

    circ1 = shapes.circle(pos=(0, 0), radius=coil_radius + coil_radius_width / 2)
    circ2 = shapes.circle(pos=(0, 0), radius=coil_radius - coil_radius_width / 2)

    straight1 = [(-(dist_coil / 2 - coil_width / 2), 0, 0), (-(dist_coil / 2 + coil_width / 2), 0, 0)]
    ring1 = extrusion(pos=straight1, shape=circ1 - circ2, color=color.red)

    straight2 = [(dist_coil / 2 - coil_width / 2, 0, 0), (dist_coil / 2 + coil_width / 2, 0, 0)]
    ring2 = extrusion(pos=straight2, shape=circ1 - circ2, color=color.blue)

    # Making rail
    rail = box(pos=(0, rail_y, 0), length=dist_coil * 8, height=1, width=10)

    # Making car
    car_center = -dist_coil * 3 - 10
    probe_tip = box(pos=(car_center + 10, probe_y, 0), length=10, height=1, width=1.5, color=color.red)
    probe_body = box(pos=(car_center, probe_y, 0), length=10, height=1, width=5, color=color.red)
    car_body = box(pos=(car_center, probe_y - 1.5, 0), length=14, height=2, width=7, color=color.green)
    car_wheel1 = cylinder(pos=(car_center - 5, probe_y - 1.5, -4), axis=(0, 0, 0.5), radius=1.5, color=color.green)
    car_wheel2 = cylinder(pos=(car_center + 5, probe_y - 1.5, -4), axis=(0, 0, 0.5), radius=1.5, color=color.green)
    car_wheel3 = cylinder(pos=(car_center - 5, probe_y - 1.5, 4), axis=(0, 0, -0.5), radius=1.5, color=color.green)
    car_wheel4 = cylinder(pos=(car_center + 5, probe_y - 1.5, 4), axis=(0, 0, -0.5), radius=1.5, color=color.green)


    while probe_tip.pos.x < dist_coil * 3:
        rate(30)
        probe_tip.pos.x += simulation_speed
        probe_body.pos.x += simulation_speed
        car_body.pos.x += simulation_speed
        car_wheel1.pos.x += simulation_speed
        car_wheel2.pos.x += simulation_speed
        car_wheel3.pos.x += simulation_speed
        car_wheel4.pos.x += simulation_speed
        parallel_magnetic.plot(pos=(probe_tip.pos.x*simulation_scale, Bx(dist_coil * simulation_scale/2+probe_tip.pos.x*simulation_scale,probe_tip.pos.y*simulation_scale) + Bx(-dist_coil* simulation_scale/2 + probe_tip.pos.x*simulation_scale,probe_tip.pos.y*simulation_scale)))
        perpendicular_magnetic.plot(pos=(probe_tip.pos.x*simulation_scale, By(dist_coil* simulation_scale/2+probe_tip.pos.x*simulation_scale,probe_tip.pos.y*simulation_scale) + By(-dist_coil* simulation_scale/2 + probe_tip.pos.x*simulation_scale,probe_tip.pos.y*simulation_scale)))

arrow_list = []


def draw_vec_field(evt):
    global straight1, ring1, straight2, ring2, rail, probe_tip, probe_body, car_body, car_wheel1, car_wheel2, car_wheel3, car_wheel4, xrange

    ring1.visible = False
    ring2.visible = False
    rail.visible = False
    probe_tip.visible = False
    probe_body.visible = False
    car_body.visible = False
    car_wheel1.visible = False
    car_wheel2.visible = False
    car_wheel3.visible = False
    car_wheel4.visible = False

    circ1 = shapes.circle(pos=(0, 0), radius=coil_radius + coil_radius_width / 2)
    circ2 = shapes.circle(pos=(0, 0), radius=coil_radius - coil_radius_width / 2)

    straight1 = [(-(dist_coil / 2 - coil_width / 2), 0, 0), (-(dist_coil / 2 + coil_width / 2), 0, 0)]
    ring1 = extrusion(pos=straight1, shape=circ1 - circ2, color=color.red)

    straight2 = [(dist_coil / 2 - coil_width / 2, 0, 0), (dist_coil / 2 + coil_width / 2, 0, 0)]
    ring2 = extrusion(pos=straight2, shape=circ1 - circ2, color=color.blue)

    # Making rail
    rail = box(pos=(0, rail_y, 0), length=dist_coil * 8, height=1, width=10)

    # Making car
    car_center = -dist_coil * 3 - 10
    probe_tip = box(pos=(car_center + 10, probe_y, 0), length=10, height=1, width=1.5, color=color.red)
    probe_body = box(pos=(car_center, probe_y, 0), length=10, height=1, width=5, color=color.red)
    car_body = box(pos=(car_center, probe_y - 1.5, 0), length=14, height=2, width=7, color=color.green)
    car_wheel1 = cylinder(pos=(car_center - 5, probe_y - 1.5, -4), axis=(0, 0, 0.5), radius=1.5, color=color.green)
    car_wheel2 = cylinder(pos=(car_center + 5, probe_y - 1.5, -4), axis=(0, 0, 0.5), radius=1.5, color=color.green)
    car_wheel3 = cylinder(pos=(car_center - 5, probe_y - 1.5, 4), axis=(0, 0, -0.5), radius=1.5, color=color.green)
    car_wheel4 = cylinder(pos=(car_center + 5, probe_y - 1.5, 4), axis=(0, 0, -0.5), radius=1.5, color=color.green)

    delta_x = 1
    delta_y = 1
    x = xrange(-dist_coil * 2,dist_coil * 2,3)
    y = xrange(-coil_radius * 2,coil_radius * 2,3)
    print(1)
    for i in range(len(x)):
        for j in range(len(y)):
            if (x[i] != dist_coil/2 and x[i] != -dist_coil/2) or (y[j] != coil_radius and y[j] != -coil_radius):
                x_pos = x[i] * simulation_scale
                y_pos = y[j] * simulation_scale
                Bx_pos=Bx(dist_coil * simulation_scale/2+x_pos,y_pos) + Bx(-dist_coil* simulation_scale/2 + x_pos,y_pos)
                By_pos = By(dist_coil * simulation_scale/2+x_pos,y_pos) + By(-dist_coil * simulation_scale/2+x_pos,y_pos)
                B = (Bx_pos ** 2 + By_pos ** 2) ** 0.5 / 3
                Bx_norm = Bx_pos/B
                By_norm = By_pos/B
                pointer = arrow(pos = (x_pos/simulation_scale,y_pos/simulation_scale,0), axis=(Bx_norm,By_norm,0),shaftwidth = 0.5)
                arrow_list.append(pointer)

def delete_vec_field(evt):
    global arrow_list
    for i in range(len(arrow_list)):
        arrow_list[i].visible = False
    arrow_list = []

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


#physical variables
dist_coil = 20
coil_radius = 15
probe_y = 0

simulation_speed = 0.4
rail_y = probe_y - 3.5
num_coil = 500
current = 0.1

parallel_magnetic = gcurve(display = g1.display, color = color.blue)

g2 = gdisplay(window=w, x = L+ 2 *window.dwidth ,y=disp.height + 50, width=(L), height=Hgraph,xtitle='x(m)', ytitle = 'B(T)' )
perpendicular_magnetic = gcurve(display = g2.display,color = color.red)

#some geometrical constants
coil_width = 2
coil_radius_width = 2
simulation_scale = 0.01


# Place buttons, radio buttons, a scrolling text object, and a slider
# in the right half of the window. Positions and sizes are given in
# terms of pixels, and pos(0,0) is the upper left corner of the window.
p = w.panel  # Refers to the full region of the window in which to place widgets

wx.StaticText(p, pos=(d, 4), size=(L - 2 * d, d), label='Simulated video',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

wx.StaticText(p, pos=(d + 20, disp.height+26), size=(L - 2 * d, d), label='Magnetic field parallel to the axis',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

wx.StaticText(p, pos=(d + L + 20, disp.height+26), size=(L - 2 * d, d), label='Magnetic field perpendicular to the axis',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

default_padding = 30

start_simul = wx.Button(p, label='Start Simulation', pos=(L * 1.35, L * 0.65+default_padding))
start_simul.Bind(wx.EVT_BUTTON, start_simulation)

draw_vector_field = wx.Button(p, label='Draw Magnetic field vector', pos=(L * 1.05, L * 0.75+default_padding))
draw_vector_field.Bind(wx.EVT_BUTTON, draw_vec_field)

delete_vector_field = wx.Button(p, label='Delete Magnetic field vector', pos=(L * 1.5, L * 0.75+default_padding))
delete_vector_field.Bind(wx.EVT_BUTTON, delete_vec_field)

def num_coils_text_change(evt):  # called on slider events
    global num_coil, num_coils_slider, num_coils_text
    value = num_coils_slider.GetValue()
    num_coil = num_coils_slider.GetValue()
    num_coils_text.SetLabel(str(value))

num_coils_slider = wx.Slider(p, pos=(1.0 * L, 0.1 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=500)
num_coils_slider.Bind(wx.EVT_SCROLL,  num_coils_text_change)
wx.StaticText(p, pos=(1.0 * L, 0.05 * L+default_padding), label='Number of Coils')
num_coils_text = wx.StaticText(p, pos=(1.7 * L, 0.05 * L+default_padding), label='0')

num_coils_slider.SetValue(num_coil)
num_coils_text.SetLabel(str(num_coil))

def dist_coil_text_change(evt):  # called on slider events
    global dist_coil, dist_coil_slider,dist_coil_text
    value = dist_coil_slider.GetValue()
    dist_coil = dist_coil_slider.GetValue() * 0.1
    dist_coil_text.SetLabel(str(value))

dist_coil_slider = wx.Slider(p, pos=(1.0 * L, 0.25 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=400)
dist_coil_slider.Bind(wx.EVT_SCROLL, dist_coil_text_change)
wx.StaticText(p, pos=(1.0 * L, 0.2 * L+default_padding), label='Distance between Coils (mm)')
dist_coil_text = wx.StaticText(p, pos=(1.7 * L, 0.2 * L+default_padding), label='0')

dist_coil_slider.SetValue(dist_coil * 10)
dist_coil_text.SetLabel(str(dist_coil * 10))

def coil_radius_text_change(evt):  # called on slider events
    global coil_radius, coil_radius_text,coil_radius_slider
    value = coil_radius_slider.GetValue()
    coil_radius = coil_radius_slider.GetValue() * 0.1
    coil_radius_text.SetLabel(str(value))

coil_radius_slider = wx.Slider(p, pos=(1.0 * L, 0.4 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=200)
coil_radius_slider.Bind(wx.EVT_SCROLL, coil_radius_text_change)
wx.StaticText(p, pos=(1.0 * L, 0.35 * L+default_padding), label='Radius of Coils (mm)')
coil_radius_text = wx.StaticText(p, pos=(1.7 * L, 0.35 * L+default_padding), label='0')

coil_radius_slider.SetValue(coil_radius * 10)
coil_radius_text.SetLabel(str(coil_radius * 10))

def probe_y_pos_text_change(evt):  # called on slider events
    global probe_y, rail_y, probe_y_pos_slider,probe_y_pos_text
    probe_y = probe_y_pos_slider.GetValue() * 0.1
    rail_y = probe_y - 3.5
    value = probe_y_pos_slider.GetValue()
    probe_y_pos_text.SetLabel(str(value))

probe_y_pos_slider = wx.Slider(p, pos=(1.0 * L, 0.55 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=200)
probe_y_pos_slider.Bind(wx.EVT_SCROLL, probe_y_pos_text_change)
wx.StaticText(p, pos=(1.0 * L, 0.5 * L+default_padding), label='Probe y Position (mm)')
probe_y_pos_text = wx.StaticText(p, pos=(1.7 * L, 0.5 * L+default_padding), label='0')

probe_y_pos_slider.SetValue(probe_y * 10)
probe_y_pos_text.SetLabel(str(probe_y * 10))

#physcs simulation

def xrange(start,end,step,exclude = -1):
    print(exclude)
    if exclude == -1:
        tmp  = start
        L = []
        while tmp <= end:
            L.append(tmp)
            tmp += step
    else:
        tmp = start
        L = []
        while tmp <= end:
            if tmp != exclude and tmp != - exclude:
                L.append(tmp)
            tmp += step
    return L

def Bx(x,y):
    global dBx
    r = coil_radius * simulation_scale
    N = num_coil
    I = current
    mu0 = 4 * math.pi * 10 ** -7
    d = dist_coil * simulation_scale
    a = mu0 * N * I * r ** 2
    b = mu0 * N * I * r * (y)
    c = (r ** 2 + x ** 2 + y ** 2)
    d = 2 * r * y
    theta_list = xrange(0,2*math.pi, 2*math.pi/100)
    sum = 0
    for theta in theta_list:
        sum += dBx(a,b,c,d,theta)
    return sum

def dBx(a,b,c,d,theta):
    return (a - b*math.sin(theta))/(4 * math.pi)/(c - d * math.sin(theta)) ** 1.5


def By(x,y):
    global dBy
    r = coil_radius * simulation_scale
    N = num_coil
    I = current
    mu0 = 4 * math.pi * 10 ** -7
    d = dist_coil * simulation_scale

    a  = mu0 * N * I * r * x
    b =  (x ** 2 + y **2 + r ** 2)
    c = 2 * r * y
    theta_list = xrange(0, 2 * math.pi, 2 * math.pi / 1000)
    sum = 0
    for theta in theta_list:
        sum += dBy(a, b, c, theta)
    return sum

def dBy(a,b,c,theta):
    return - a * math.sin(theta) / (4 * math.pi) / (b - c * math.sin(theta)) ** 1.5

circ1 = shapes.circle(pos=(0, 0), radius=coil_radius + coil_radius_width / 2)
circ2 = shapes.circle(pos=(0, 0), radius=coil_radius - coil_radius_width / 2)

straight1 = [(-(dist_coil / 2 - coil_width / 2), 0, 0), (-(dist_coil / 2 + coil_width / 2), 0, 0)]
ring1 = extrusion(pos=straight1, shape=circ1 - circ2, color=color.red)

straight2 = [(dist_coil / 2 - coil_width / 2, 0, 0), (dist_coil / 2 + coil_width / 2, 0, 0)]
ring2 = extrusion(pos=straight2, shape=circ1 - circ2, color=color.blue)

# Making rail
rail = box(pos=(0, rail_y, 0), length=100, height=1, width=10)

# Making car
car_center = -30
probe_tip = box(pos=(car_center + 10, probe_y, 0), length=10, height=1, width=1.5, color=color.red)
probe_body = box(pos=(car_center, probe_y, 0), length=10, height=1, width=5, color=color.red)
car_body = box(pos=(car_center, probe_y - 1.5, 0), length=14, height=2, width=7, color=color.green)
car_wheel1 = cylinder(pos=(car_center - 5, probe_y - 1.5, -4), axis=(0, 0, 0.5), radius=1.5, color=color.green)
car_wheel2 = cylinder(pos=(car_center + 5, probe_y - 1.5, -4), axis=(0, 0, 0.5), radius=1.5, color=color.green)
car_wheel3 = cylinder(pos=(car_center - 5, probe_y - 1.5, 4), axis=(0, 0, -0.5), radius=1.5, color=color.green)
car_wheel4 = cylinder(pos=(car_center + 5, probe_y - 1.5, 4), axis=(0, 0, -0.5), radius=1.5, color=color.green)

def setleft(evt):
    global subprocess
    subprocess.Popen(["coil.pdf"], shell=True)

m = w.menubar # Refers to the menubar, which can have several menus

menu = wx.Menu()
item = menu.Append(-1, 'Open Document', 'Make box rotate to the left')
w.win.Bind(wx.EVT_MENU, setleft, item)
m.Append(menu, 'Options')