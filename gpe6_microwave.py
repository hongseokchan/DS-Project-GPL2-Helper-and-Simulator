from __future__ import division, print_function
from visual import *
from visual.graph import *
import wx
import visual
import subprocess

def xrange2(start,end,step):
    tmp = start
    L = []
    while tmp <= end:
        L.append(tmp)
        tmp += step
    return L
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
g = gdisplay(window=w, x=window.dwidth, y=disp.height + 50, width=(L * 2), height=Hgraph, xtitle='theta(rad)',
                 ytitle='I(W/m^2)')
Intensity_distribution = gcurve(display=g.display, color=color.blue)

#physical variables
slit_width = 0.015

dist_L = 0.5
dist_slit = 0.2

wave_length = 0.03

reflection_coeff_floor = 0.9
reflection_coeff_trans = 0.9
h = 0.2

#g = gdisplay(window=w, x = window.dwidth, y=disp.height + 50, width=(L * 2), height=Hgraph,xtitle='x(m)', ytitle = 'B(T)')
#Intensity_distribution = gcurve(display = g.display, color = color.blue)


# Place buttons, radio buttons, a scrolling text object, and a slider
# in the right half of the window. Positions and sizes are given in
# terms of pixels, and pos(0,0) is the upper left corner of the window.
p = w.panel  # Refers to the full region of the window in which to place widgets

wx.StaticText(p, pos=(d, 4), size=(L - 2 * d, d), label='Simulated video',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

wx.StaticText(p, pos=(d + 20 + L/2, disp.height+26), size=(L - 2 * d, d), label='Intensity Distribution',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

default_padding = 10

def start_dist_simul(evt):
    global lbox, center, lrail, lplate, lnail, tri1, tri2, lmicrowave, rmicrowave, rbox, rrail, rplate, rnail, g
    global w, Intensity_distribution, xrange2, dist_slit_simul
    lbox.visible = False
    center.visible = False
    lrail.visible = False
    lplate.visible = False
    lnail.visible = False
    tri1.visible = False
    tri2.visible = False
    lmicrowave.visible = False
    rmicrowave.visible = False
    rbox.visible = False
    rnail.visible = False
    rplate.visible = False
    rrail.visible = False

    try:
        global sleetbox1, tri, triangleplate, sleetbox2, sleet2, sleet1, sleet3
        sleetbox1.visible = False
        tri.visible = False
        triangleplate.visible = False
        sleetbox2.visible = False
        sleet1.visible = False
        sleet2.visible = False
        sleet3.visible = False
    except:
        pass

    lbox = box(pos=(-8, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    center = cylinder(pos=(0, 2, 0), radius=4, axis=(0, -3, 0), color=(0.3, 0.3, 0.3), material=materials.shiny)
    lrail = box(pos=(-10, 0.5, 0), length=20, width=2, height=1, material=materials.wood)
    lplate = box(pos=(-11, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8), material=materials.shiny)
    lnail = cylinder(pos=(-12, 20, 0), axis=(-0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)

    t = -25
    theta = 0
    theta2 = theta

    tri1 = shapes.trapezoid(top=10, height=1, width=14, rotate=pi - math.atan(2))
    tri2 = shapes.trapezoid(top=10, height=1, width=14, rotate=-pi / 2 + math.atan(2))
    k = 12 / sqrt(5)
    k1 = k
    lmicrowave = extrusion(pos=paths.rectangle(pos=(-3, 20, 0), height=k, width=k, up=(-1, 0, 0)), shape=tri1,
                           color=color.white, material=materials.plastic)
    rmicro_path = [vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) - sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) - sin(theta) * k1 / 2, 20 - k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) + k1 / 2 * sin(theta), 20 - k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + cos(theta) * k1 / 2)]
    rmicrowave = extrusion(pos=rmicro_path, shape=tri2, color=color.white, material=materials.plastic)
    rbox = box(pos=(40 + t, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    rrail = box(pos=(50, 0.5, 0), length=100, width=2, height=1, material=materials.wood)
    rplate = box(pos=(43 + t, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8),
                 material=materials.shiny)
    rnail = cylinder(pos=(44 + t, 20, 0), axis=(0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)

    #making light wave

    t = 0
    k = 2 * math.pi / wave_length
    w = 0.99 * 10 ** 10 * 2 * math.pi
    A = 3
    simulation_scale = 0.01
    floor_reflection_coefficient = reflection_coeff_floor
    trans_reflection_coefficient = reflection_coeff_trans
    J = []

    dist_list = xrange2(-25,50,0.1)
    for i in range(len(dist_list)):
        rate(30)
        t = i * 10 ** -11

        L1 = lbox.pos.x
        L2 = rbox.pos.x

        direct_1_x_list = xrange2(L1, L2, 2)
        direct_3_x_1_list = xrange2(L1, L2, 2)
        direct_3_x_2_list = xrange2(L1, L2, 2)
        direct_3_x_3_list = xrange2(L1, L2, 2)

        for j in range(len(J)):
            J[j].visible = False
            J[j] = 0
        J = []
        H = lbox.pos.y
        for j in range(len(direct_1_x_list)):
            x_pos = direct_1_x_list[j] * simulation_scale
            if direct_1_x_list[j] > (L1 + L2) / 2:
                floor_reflect_x_pos = direct_1_x_list[j]
                floor_reflect_y_pos = 2 * H / (L2 - L1) * (floor_reflect_x_pos - (L1 + L2) / 2)
                amplitude = floor_reflection_coefficient * A * math.cos(k * (
                            (((L2 - L1) / 2) ** 2 + H ** 2) ** 0.5 * simulation_scale + ((floor_reflect_x_pos - (
                                L1 + L2) / 2) ** 2 + floor_reflect_y_pos ** 2) ** 0.5 * simulation_scale) - w * t + math.pi)
                floor_reflect = arrow(pos=(floor_reflect_x_pos, floor_reflect_y_pos, 0), axis=(
                -H / (((L2 - L1) / 2) ** 2 + (H) ** 2) ** 0.5 * amplitude,
                (L2 - L1) / 2 / (((L2 - L1) / 2) ** 2 + (H) ** 2) ** 0.5 * amplitude, 0), shaftwidth=0.2,
                                      color=color.blue)
                J.append(floor_reflect)
            else:
                floor_reflect_x_pos = direct_1_x_list[j]
                floor_reflect_y_pos = - 2 * H / (L2 - L1) * (floor_reflect_x_pos - L1) + H
                amplitude = A * math.cos(k * ((floor_reflect_x_pos - L1) ** 2 + (
                            floor_reflect_y_pos - H) ** 2) ** 0.5 * simulation_scale - w * t)
                floor_reflect = arrow(pos=(floor_reflect_x_pos, floor_reflect_y_pos, 0), axis=(
                H / (((L2 - L1) / 2) ** 2 + (H) ** 2) ** 0.5 * amplitude,
                (L2 - L1) / 2 / (((L2 - L1) / 2) ** 2 + (H) ** 2) ** 0.5 * amplitude, 0), shaftwidth=0.2,
                                      color=color.blue)
                J.append(floor_reflect)
            direct_1 = arrow(pos=(direct_1_x_list[j], H, 0), axis=(0, A * math.cos(k * x_pos - w * t), 0),
                             shaftwidth=0.2, color=color.red)
            J.append(direct_1)
        '''
        for i in range(len(direct_3_x_1_list)):
            x_pos = direct_3_x_1_list[i] * simulation_scale
            direct_3_1 = arrow(pos=(direct_3_x_1_list[i], h, -3), axis=(0, A * math.cos(k * x_pos - w * t), 0), shaftwidth=0.2,color=color.green)
            J.append(direct_3_1)

        for i in range(len(direct_3_x_2_list)):
            x_pos = direct_3_x_2_list[i] * simulation_scale
            direct_3_2 = arrow(pos=(direct_3_x_2_list[i], h, -2), axis=(0, trans_reflection_coefficient * A * math.cos(k * ((L2 - L1) * simulation_scale + (L2 * simulation_scale - x_pos)) - w * t + math.pi), 0), shaftwidth=0.2,color=color.green)
            J.append(direct_3_2)
        '''
        for j in range(len(direct_3_x_3_list)):
            x_pos = direct_3_x_3_list[j] * simulation_scale
            direct_3_3 = arrow(pos=(direct_3_x_3_list[j], H, 0), axis=(
            0, trans_reflection_coefficient ** 2 * A * math.cos(k * ((L2 - L1) * simulation_scale * 2 + x_pos) - w * t),
            0), shaftwidth=0.2, color=color.green)
            J.append(direct_3_3)

        tri1.visible = False
        tri2.visible = False
        lmicrowave.visible = False
        rmicrowave.visible = False
        rbox.visible = False
        rrail.visible = False
        rplate.visible = False
        rnail.visible = False
        t = dist_list[i]
        d = (rbox.pos.x - lbox.pos.x) * 0.01

        theta = 0
        theta2 = theta

        tri1 = shapes.trapezoid(top=10, height=1, width=14, rotate=pi - math.atan(2))
        tri2 = shapes.trapezoid(top=10, height=1, width=14, rotate=-pi / 2 + math.atan(2))
        k = 12 / sqrt(5)
        k1 = k
        lmicrowave = extrusion(pos=paths.rectangle(pos=(-3, 20, 0), height=k, width=k, up=(-1, 0, 0)), shape=tri1,
                               color=color.white, material=materials.plastic)
        rmicro_path = [vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                              -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                       vector((35 + t) * cos(theta2) - sin(theta) * k1 / 2, 20 + k1 / 2,
                              -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                       vector((t + 35) * cos(theta2) - sin(theta) * k1 / 2, 20 - k1 / 2,
                              -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                       vector((t + 35) * cos(theta2) + k1 / 2 * sin(theta), 20 - k1 / 2,
                              -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                       vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                              -(35 + t) * sin(theta2) + cos(theta) * k1 / 2)]
        rmicrowave = extrusion(pos=rmicro_path, shape=tri2, color=color.white, material=materials.plastic)
        rbox = box(pos=(40 + t, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
        rrail = box(pos=(50, 0.5, 0), length=100, width=2, height=1, material=materials.wood)
        rplate = box(pos=(43 + t, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8),
                     material=materials.shiny)
        rnail = cylinder(pos=(44 + t, 20, 0), axis=(0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)

        Intensity_distribution.plot(pos = (d,dist_slit_simul(d)))


def start_double_simul(evt):
    global lbox, center, lrail, lplate, lnail, tri1, tri2, lmicrowave, rmicrowave, rbox, rrail,rplate,rnail,g
    global w, Intensity_distribution, xrange2, double_slit


    lbox.visible = False
    center.visible = False
    lrail.visible = False
    lplate.visible = False
    lnail.visible = False
    tri1.visible = False
    tri2.visible = False
    lmicrowave.visible = False
    rmicrowave.visible = False
    rbox.visible = False
    rnail.visible = False
    rplate.visible = False
    rrail.visible = False
    try:
        global sleetbox1, tri, triangleplate,sleetbox2,sleet2,sleet1,sleet3
        sleetbox1.visible = False
        tri.visible = False
        triangleplate.visible = False
        sleetbox2.visible = False
        sleet1.visible = False
        sleet2.visible = False
        sleet3.visible = False
    except:
        pass


    lbox = box(pos=(-40, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    center = cylinder(pos=(0, 2, 0), radius=4, axis=(0, -3, 0), color=(0.3, 0.3, 0.3), material=materials.shiny)
    lrail = box(pos=(-30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
    lplate = box(pos=(-43, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8), material=materials.shiny)
    lnail = cylinder(pos=(-44, 20, 0), axis=(-0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)

    #making slit
    sleetbox1 = extrusion(path=paths.line(start=(-2, 6, 0), end=(2, 6, 0)), shape=shapes.triangle(length=3 * sqrt(3)))
    tri = shapes.triangle(length=3 * sqrt(3) * 1.8)
    triangleplate = extrusion(pos=paths.line(start=(0, 4, -1.5), end=(0, 4, 1.5)), shape=tri, color=(0.2, 0.2, 0.2),
                              material=materials.plastic)

    sleetbox2 = box(pos=(0, 9.8, 0), length=1.5, width=28, height=2.3, color=(0.8, 0.8, 0.8), material=materials.shiny)
    sleet2 = box(pos=(0, 20, -7.5 - dist_slit * 5), length=1, width=10, height=19, color=(0.6, 0.6, 0.6), material=materials.shiny)
    sleet1 = box(pos=(0, 20, 0), length=1, width=5, height=19, color=(0.6, 0.6, 0.6), material=materials.shiny)
    sleet3 = box(pos=(0, 20, 7.5 + dist_slit * 5), length=1, width=10, height=19, color=(0.6, 0.6, 0.6), material=materials.shiny)


    t = dist_L / 0.1 * 10 - 20
    theta = - math.pi / 2
    theta2 = theta

    tri1 = shapes.trapezoid(top=10, height=1, width=14, rotate=pi - math.atan(2))
    tri2 = shapes.trapezoid(top=10, height=1, width=14, rotate=-pi / 2 + math.atan(2))
    k = 12 / sqrt(5)
    k1 = k
    lmicrowave = extrusion(pos=paths.rectangle(pos=(-35, 20, 0), height=k, width=k, up=(-1, 0, 0)), shape=tri1,
                           color=color.white, material=materials.plastic)
    rmicro_path = [vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) - sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) - sin(theta) * k1 / 2, 20 - k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) + k1 / 2 * sin(theta), 20 - k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + cos(theta) * k1 / 2)]
    rmicrowave = extrusion(pos=rmicro_path, shape=tri2, color=color.white, material=materials.plastic)
    rbox = box(pos=(40 + t, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    rrail = box(pos=(30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
    rplate = box(pos=(43 + t, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8),
                 material=materials.shiny)
    rnail = cylinder(pos=(44 + t, 20, 0), axis=(0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)
    rbox.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rplate.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rnail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rrail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)

    #theta_list = xrange2(-math.pi/2, math.pi/2, 0.01)
    start = -pi/2
    end = pi/2
    step = 0.01
    tmp = start
    theta_list = []
    while tmp <= end:
        theta_list.append(tmp)
        tmp += step
    for i in range(len(theta_list)):
        rate(30)
        tri1.visible = False
        tri2.visible = False
        lmicrowave.visible = False
        rmicrowave.visible = False
        rbox.visible = False
        rrail.visible = False
        rplate.visible = False
        rnail.visible = False

        theta = theta_list[i]
        theta2 = theta

        tri1 = shapes.trapezoid(top=10, height=1, width=14, rotate=pi - math.atan(2))
        tri2 = shapes.trapezoid(top=10, height=1, width=14, rotate=-pi / 2 + math.atan(2))
        k = 12 / sqrt(5)
        k1 = k
        lmicrowave = extrusion(pos=paths.rectangle(pos=(-35, 20, 0), height=k, width=k, up=(-1, 0, 0)), shape=tri1,
                               color=color.white, material=materials.plastic)
        rmicro_path = [vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                       -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                       vector((35 + t) * cos(theta2) - sin(theta) * k1 / 2, 20 + k1 / 2,
                              -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                       vector((t + 35) * cos(theta2) - sin(theta) * k1 / 2, 20 - k1 / 2,
                              -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                       vector((t + 35) * cos(theta2) + k1 / 2 * sin(theta), 20 - k1 / 2,
                              -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                       vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                              -(35 + t) * sin(theta2) + cos(theta) * k1 / 2)]
        rmicrowave = extrusion(pos=rmicro_path, shape=tri2, color=color.white, material=materials.plastic)
        rbox = box(pos=(40 + t, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
        rrail = box(pos=(30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
        rplate = box(pos=(43 + t, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8),
                     material=materials.shiny)
        rnail = cylinder(pos=(44 + t, 20, 0), axis=(0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)
        rbox.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
        rplate.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
        rnail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
        rrail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)

        Intensity_distribution.plot(pos = (theta,double_slit(theta)))

def start_single_simul(evt):
    global lbox, center, lrail, lplate, lnail, tri1, tri2, lmicrowave, rmicrowave, rbox, rrail, rplate, rnail, g, Intensity_distribution
    global single_slit, xrange2
    lbox.visible = False
    center.visible = False
    lrail.visible = False
    lplate.visible = False
    lnail.visible = False
    tri1.visible = False
    tri2.visible = False
    lmicrowave.visible = False
    rmicrowave.visible = False
    rbox.visible = False
    rnail.visible = False
    rplate.visible = False
    rrail.visible = False

    try:
        global sleetbox1, tri, triangleplate, sleetbox2, sleet2, sleet1, sleet3
        sleetbox1.visible = False
        tri.visible = False
        triangleplate.visible = False
        sleetbox2.visible = False
        sleet1.visible = False
        sleet2.visible = False
        sleet3.visible = False
    except:
        pass

    lbox = box(pos=(-40, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    center = cylinder(pos=(0, 2, 0), radius=4, axis=(0, -3, 0), color=(0.3, 0.3, 0.3), material=materials.shiny)
    lrail = box(pos=(-30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
    lplate = box(pos=(-43, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8), material=materials.shiny)
    lnail = cylinder(pos=(-44, 20, 0), axis=(-0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)

    t = dist_L / 0.1 * 10 - 20
    theta = - math.pi / 2
    theta2 = theta

    tri1 = shapes.trapezoid(top=10, height=1, width=14, rotate=pi - math.atan(2))
    tri2 = shapes.trapezoid(top=10, height=1, width=14, rotate=-pi / 2 + math.atan(2))
    k = 12 / sqrt(5)
    k1 = k
    lmicrowave = extrusion(pos=paths.rectangle(pos=(-35, 20, 0), height=k, width=k, up=(-1, 0, 0)), shape=tri1,
                           color=color.white, material=materials.plastic)
    rmicro_path = [vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) - sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) - sin(theta) * k1 / 2, 20 - k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) + k1 / 2 * sin(theta), 20 - k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + cos(theta) * k1 / 2)]
    rmicrowave = extrusion(pos=rmicro_path, shape=tri2, color=color.white, material=materials.plastic)
    rbox = box(pos=(40 + t, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    rrail = box(pos=(30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
    rplate = box(pos=(43 + t, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8),
                 material=materials.shiny)
    rnail = cylinder(pos=(44 + t, 20, 0), axis=(0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)
    rbox.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rplate.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rnail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rrail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)

    theta_list = xrange2(-math.pi / 2, math.pi / 2, 0.01)
    for i in range(len(theta_list)):
        rate(30)
        tri1.visible = False
        tri2.visible = False
        lmicrowave.visible = False
        rmicrowave.visible = False
        rbox.visible = False
        rrail.visible = False
        rplate.visible = False
        rnail.visible = False

        theta = theta_list[i]
        theta2 = theta

        tri1 = shapes.trapezoid(top=10, height=1, width=14, rotate=pi - math.atan(2))
        tri2 = shapes.trapezoid(top=10, height=1, width=14, rotate=-pi / 2 + math.atan(2))
        k = 12 / sqrt(5)
        k1 = k
        lmicrowave = extrusion(pos=paths.rectangle(pos=(-35, 20, 0), height=k, width=k, up=(-1, 0, 0)), shape=tri1,
                               color=color.white, material=materials.plastic)
        rmicro_path = [vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                              -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                       vector((35 + t) * cos(theta2) - sin(theta) * k1 / 2, 20 + k1 / 2,
                              -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                       vector((t + 35) * cos(theta2) - sin(theta) * k1 / 2, 20 - k1 / 2,
                              -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                       vector((t + 35) * cos(theta2) + k1 / 2 * sin(theta), 20 - k1 / 2,
                              -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                       vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                              -(35 + t) * sin(theta2) + cos(theta) * k1 / 2)]
        rmicrowave = extrusion(pos=rmicro_path, shape=tri2, color=color.white, material=materials.plastic)
        rbox = box(pos=(40 + t, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
        rrail = box(pos=(30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
        rplate = box(pos=(43 + t, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8),
                     material=materials.shiny)
        rnail = cylinder(pos=(44 + t, 20, 0), axis=(0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)
        rbox.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
        rplate.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
        rnail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
        rrail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)

        Intensity_distribution.plot(pos=(theta, single_slit(theta)))

def change_simul_double(evt):
    global dist_L, slit_width, wave_length, dist_slit, reflection_coeff_floor,reflection_coeff_trans,h, L, Hgraph, default_padding
    global lbox, center, lrail, lplate, lnail, tri1, tri2, lmicrowave, rmicrowave, rbox, rrail, rplate, rnail, Intensity_distribution, p
    global start_dist_simul, start_double_simul, start_single_simul
    global change_simul_dist,change_simul_single,change_simul_double
    lbox.visible = False
    center.visible = False
    lrail.visible = False
    lplate.visible = False
    lnail.visible = False
    tri1.visible = False
    tri2.visible = False
    lmicrowave.visible = False
    rmicrowave.visible = False
    rbox.visible = False
    rnail.visible = False
    rplate.visible = False
    rrail.visible = False
    try:
        global sleetbox1, tri, triangleplate, sleetbox2, sleet2, sleet1, sleet3
        sleetbox1.visible = False
        tri.visible = False
        triangleplate.visible = False
        sleetbox2.visible = False
        sleet1.visible = False
        sleet2.visible = False
        sleet3.visible = False
    except:
        pass

    lbox = box(pos=(-40, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    center = cylinder(pos=(0, 2, 0), radius=4, axis=(0, -3, 0), color=(0.3, 0.3, 0.3), material=materials.shiny)
    lrail = box(pos=(-30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
    lplate = box(pos=(-43, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8), material=materials.shiny)
    lnail = cylinder(pos=(-44, 20, 0), axis=(-0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)

    # making slit
    sleetbox1 = extrusion(path=paths.line(start=(-2, 6, 0), end=(2, 6, 0)), shape=shapes.triangle(length=3 * sqrt(3)))
    tri = shapes.triangle(length=3 * sqrt(3) * 1.8)
    triangleplate = extrusion(pos=paths.line(start=(0, 4, -1.5), end=(0, 4, 1.5)), shape=tri, color=(0.2, 0.2, 0.2),
                              material=materials.plastic)

    sleetbox2 = box(pos=(0, 9.8, 0), length=1.5, width=28, height=2.3, color=(0.8, 0.8, 0.8), material=materials.shiny)
    sleet2 = box(pos=(0, 20, -7.5 - dist_slit * 5), length=1, width=10, height=19, color=(0.6, 0.6, 0.6),
                 material=materials.shiny)
    sleet1 = box(pos=(0, 20, 0), length=1, width=5, height=19, color=(0.6, 0.6, 0.6), material=materials.shiny)
    sleet3 = box(pos=(0, 20, 7.5 + dist_slit * 5), length=1, width=10, height=19, color=(0.6, 0.6, 0.6),
                 material=materials.shiny)

    t = dist_L / 0.1 * 10 - 20
    theta = - math.pi / 2
    theta2 = theta

    tri1 = shapes.trapezoid(top=10, height=1, width=14, rotate=pi - math.atan(2))
    tri2 = shapes.trapezoid(top=10, height=1, width=14, rotate=-pi / 2 + math.atan(2))
    k = 12 / sqrt(5)
    k1 = k
    lmicrowave = extrusion(pos=paths.rectangle(pos=(-35, 20, 0), height=k, width=k, up=(-1, 0, 0)), shape=tri1,
                           color=color.white, material=materials.plastic)
    rmicro_path = [vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) - sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) - sin(theta) * k1 / 2, 20 - k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) + k1 / 2 * sin(theta), 20 - k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + cos(theta) * k1 / 2)]
    rmicrowave = extrusion(pos=rmicro_path, shape=tri2, color=color.white, material=materials.plastic)
    rbox = box(pos=(40 + t, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    rrail = box(pos=(30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
    rplate = box(pos=(43 + t, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8),
                 material=materials.shiny)
    rnail = cylinder(pos=(44 + t, 20, 0), axis=(0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)
    rbox.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rplate.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rnail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rrail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    slit_width = 0.015
    dist_slit = 0.3
    wave_length = 0.03
    dist_L = 0.5

    reflection_coeff_floor = 0.9
    reflection_coeff_trans = 0.9
    h = 0.2

    # if it comes from single slit
    try:
        global start_simul, change_ui1, change_ui2, slit_width_slider,  dist_L_slider, wave_length_slider, dist_slit_slider
        global slit_width_text, slit_width_tt , dist_L_tt, dist_L_text, wave_length_tt, wave_length_text, dist_slit_text,dist_slit_tt

        start_simul.Destroy()
        change_ui1.Destroy()
        change_ui2.Destroy()
        slit_width_slider.Destroy()
        dist_L_slider.Destroy()
        wave_length_slider.Destroy()
        slit_width_text.Destroy()
        slit_width_tt.Destroy()
        dist_L_text.Destroy()
        dist_L_tt.Destroy()
        wave_length_text.Destroy()
        wave_length_tt.Destroy()
    except:
        pass

    # if it comes from varying dist
    try:
        global h_text, h_slider, h_tt, reflection_coeff_floor_text, reflection_coeff_floor_tt, reflection_coeff_floor_slider, reflection_coeff_trans_text, reflection_coeff_trans_tt, reflection_coeff_trans_slider
        global start_simul,change_ui1,change_ui2, wave_length_tt,wave_length_text,wave_length_slider
        wave_length_slider.Destroy()
        wave_length_text.Destroy()
        wave_length_tt.Destroy()

        h_text.Destroy()
        h_slider.Destroy()
        h_tt.Destroy()
        reflection_coeff_floor_text.Destroy()
        reflection_coeff_floor_slider.Destroy()
        reflection_coeff_floor_tt.Destroy()
        reflection_coeff_trans_tt.Destroy()
        reflection_coeff_trans_text.Destroy()
        reflection_coeff_trans_slider.Destroy()
    except:
        pass

    start_simul = wx.Button(p, label='Start Simulation - double slit', pos=(L * 1.25, L * 0.65 + default_padding))
    start_simul.Bind(wx.EVT_BUTTON, start_double_simul)

    change_ui1 = wx.Button(p, label='Changing the UI to single slit simulation',
                           pos=(L * 1.18, L * 0.75 + default_padding))
    change_ui1.Bind(wx.EVT_BUTTON, change_simul_single)

    change_ui2 = wx.Button(p, label='Changing the UI to varying distance simulation',
                           pos=(L * 1.13, L * 0.85 + default_padding))
    change_ui2.Bind(wx.EVT_BUTTON, change_simul_dist)

    def slit_width_text_change(evt):  # called on slider events
        global slit_width
        slit_width = slit_width_slider.GetValue() / 1000
        slit_width_text.SetLabel(str(slit_width))

    slit_width_slider = wx.Slider(p, pos=(1.0 * L, 0.1 * L + default_padding), size=(0.9 * L, 20), minValue=0,
                                  maxValue=100)
    slit_width_slider.Bind(wx.EVT_SCROLL, slit_width_text_change)
    slit_width_tt = wx.StaticText(p, pos=(1.0 * L, 0.05 * L + default_padding), label='slit_width')
    slit_width_text = wx.StaticText(p, pos=(1.7 * L, 0.05 * L + default_padding), label='0')

    slit_width_slider.SetValue(slit_width * 1000)
    slit_width_text.SetLabel(str(slit_width))

    def dist_slit_text_change(evt):  # called on slider events
        global dist_slit
        dist_slit = dist_slit_slider.GetValue() / 200
        dist_slit_text.SetLabel(str(dist_slit))

    dist_slit_slider = wx.Slider(p, pos=(1.0 * L, 0.25 * L + default_padding), size=(0.9 * L, 20), minValue=0,
                                 maxValue=100)
    dist_slit_slider.Bind(wx.EVT_SCROLL, dist_slit_text_change)
    dist_slit_tt = wx.StaticText(p, pos=(1.0 * L, 0.2 * L + default_padding), label='Distance between Slit')
    dist_slit_text = wx.StaticText(p, pos=(1.7 * L, 0.2 * L + default_padding), label='0')

    dist_slit_slider.SetValue(dist_slit * 200)
    dist_slit_text.SetLabel(str(dist_slit))

    def dist_L_text_change(evt):  # called on slider events
        global dist_L
        dist_L = dist_L_slider.GetValue() / 100
        dist_L_text.SetLabel(str(dist_L))

    dist_L_slider = wx.Slider(p, pos=(1.0 * L, 0.4 * L + default_padding), size=(0.9 * L, 20), minValue=0, maxValue=100)
    dist_L_slider.Bind(wx.EVT_SCROLL, dist_L_text_change)
    dist_L_tt = wx.StaticText(p, pos=(1.0 * L, 0.35 * L + default_padding),
                              label='Distance between slit and reciever')
    dist_L_text = wx.StaticText(p, pos=(1.7 * L, 0.35 * L + default_padding), label='0')

    dist_L_slider.SetValue(dist_L * 100)
    dist_L_text.SetLabel(str(dist_L))

    def wave_length_text_change(evt):  # called on slider events
        global wave_length
        wave_length = wave_length_slider.GetValue() / 1000
        wave_length_text.SetLabel(str(wave_length))

    wave_length_slider = wx.Slider(p, pos=(1.0 * L, 0.55 * L + default_padding), size=(0.9 * L, 20), minValue=0,
                                   maxValue=100)
    wave_length_slider.Bind(wx.EVT_SCROLL, wave_length_text_change)
    wave_length_tt = wx.StaticText(p, pos=(1.0 * L, 0.5 * L + default_padding), label='wave_length')
    wave_length_text = wx.StaticText(p, pos=(1.7 * L, 0.5 * L + default_padding), label='0')

    wave_length_slider.SetValue(wave_length * 1000)
    wave_length_text.SetLabel(str(wave_length))

def change_simul_single(evt):
    global dist_L,slit_width, wave_length, dist_slit, reflection_coeff_floor,reflection_coeff_trans,h, L, Hgraph, default_padding
    global lbox, center, lrail, lplate, lnail, tri1, tri2, lmicrowave, rmicrowave, rbox, rrail, rplate, rnail, p
    global start_dist_simul, start_double_simul, start_single_simul
    lbox.visible = False
    center.visible = False
    lrail.visible = False
    lplate.visible = False
    lnail.visible = False
    tri1.visible = False
    tri2.visible = False
    lmicrowave.visible = False
    rmicrowave.visible = False
    rbox.visible = False
    rnail.visible = False
    rplate.visible = False
    rrail.visible = False
    try:
        global sleetbox1, tri, triangleplate, sleetbox2, sleet2, sleet1, sleet3
        sleetbox1.visible = False
        tri.visible = False
        triangleplate.visible = False
        sleetbox2.visible = False
        sleet1.visible = False
        sleet2.visible = False
        sleet3.visible = False
    except:
        pass

    lbox = box(pos=(-40, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    center = cylinder(pos=(0, 2, 0), radius=4, axis=(0, -3, 0), color=(0.3, 0.3, 0.3), material=materials.shiny)
    lrail = box(pos=(-30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
    lplate = box(pos=(-43, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8), material=materials.shiny)
    lnail = cylinder(pos=(-44, 20, 0), axis=(-0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)

    t = dist_L / 0.1 * 10 - 20
    theta = - math.pi / 2
    theta2 = theta

    tri1 = shapes.trapezoid(top=10, height=1, width=14, rotate=pi - math.atan(2))
    tri2 = shapes.trapezoid(top=10, height=1, width=14, rotate=-pi / 2 + math.atan(2))
    k = 12 / sqrt(5)
    k1 = k
    lmicrowave = extrusion(pos=paths.rectangle(pos=(-35, 20, 0), height=k, width=k, up=(-1, 0, 0)), shape=tri1,
                           color=color.white, material=materials.plastic)
    rmicro_path = [vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) - sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) - sin(theta) * k1 / 2, 20 - k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) + k1 / 2 * sin(theta), 20 - k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + cos(theta) * k1 / 2)]
    rmicrowave = extrusion(pos=rmicro_path, shape=tri2, color=color.white, material=materials.plastic)
    rbox = box(pos=(40 + t, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    rrail = box(pos=(30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
    rplate = box(pos=(43 + t, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8),
                 material=materials.shiny)
    rnail = cylinder(pos=(44 + t, 20, 0), axis=(0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)
    rbox.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rplate.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rnail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rrail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)


    slit_width = 0.015
    dist_slit = 0.3
    wave_length = 0.03
    dist_L = 0.5

    reflection_coeff_floor = 0.9
    reflection_coeff_trans = 0.9
    h = 0.2

    try:
        #if it comes from double slit
        global start_simul, change_ui1,change_ui2, slit_width_slider, dist_slit_slider, dist_L_slider,wave_length_slider
        global slit_width_text,slit_width_tt,dist_slit_tt,dist_slit_text,dist_L_tt,dist_L_text,wave_length_tt,wave_length_text
        start_simul.Destroy()
        change_ui1.Destroy()
        change_ui2.Destroy()
        slit_width_slider.Destroy()
        dist_slit_slider.Destroy()
        dist_L_slider.Destroy()
        wave_length_slider.Destroy()
        slit_width_text.Destroy()
        slit_width_tt.Destroy()
        dist_slit_text.Destroy()
        dist_slit_tt.Destroy()
        dist_L_text.Destroy()
        dist_L_tt.Destroy()
        wave_length_text.Destroy()
        wave_length_tt.Destroy()
    except:
        pass

    try:
        #if it comes from varying dist simulation
        global h_text, h_slider,h_tt, reflection_coeff_floor_text, reflection_coeff_floor_tt, reflection_coeff_floor_slider, reflection_coeff_trans_text, reflection_coeff_trans_tt, reflection_coeff_trans_slider
        global start_simul, change_ui1, change_ui2, wave_length_tt, wave_length_text, wave_length_slider
        wave_length_slider.Destroy()
        wave_length_text.Destroy()
        wave_length_tt.Destroy()
        h_text.Destroy()
        h_slider.Destroy()
        h_tt.Destroy()
        reflection_coeff_floor_text.Destroy()
        reflection_coeff_floor_slider.Destroy()
        reflection_coeff_floor_tt.Destroy()
        reflection_coeff_trans_tt.Destroy()
        reflection_coeff_trans_text.Destroy()
        reflection_coeff_trans_slider.Destroy()
    except:
        pass

    #single simulation UI design

    start_simul = wx.Button(p, label='Start Simulation - single slit', pos=(L * 1.25, L * 0.55 + default_padding))
    start_simul.Bind(wx.EVT_BUTTON, start_single_simul)

    change_ui1 = wx.Button(p, label='Changing the UI to double slit simulation',
                           pos=(L * 1.17, L * 0.65 + default_padding))
    change_ui1.Bind(wx.EVT_BUTTON, change_simul_double)

    change_ui2 = wx.Button(p, label='Changing the UI to varying distance simulation',
                           pos=(L * 1.13, L * 0.75 + default_padding))
    change_ui2.Bind(wx.EVT_BUTTON, change_simul_dist)

    def slit_width_text_change(evt):  # called on slider events
        global slit_width
        slit_width = slit_width_slider.GetValue() / 1000
        slit_width_text.SetLabel(str(slit_width))

    slit_width_slider = wx.Slider(p, pos=(1.0 * L, 0.1 * L + default_padding), size=(0.9 * L, 20), minValue=0,
                                  maxValue=100)
    slit_width_slider.Bind(wx.EVT_SCROLL, slit_width_text_change)
    slit_width_tt = wx.StaticText(p, pos=(1.0 * L, 0.05 * L + default_padding), label='slit_width')
    slit_width_text = wx.StaticText(p, pos=(1.7 * L, 0.05 * L + default_padding), label='0')

    slit_width_slider.SetValue(slit_width * 1000)
    slit_width_text.SetLabel(str(slit_width))

    def dist_L_text_change(evt):  # called on slider events
        global dist_L
        dist_L = dist_L_slider.GetValue() / 100
        dist_L_text.SetLabel(str(dist_L))

    dist_L_slider = wx.Slider(p, pos=(1.0 * L, 0.25 * L + default_padding), size=(0.9 * L, 20), minValue=0, maxValue=100)
    dist_L_slider.Bind(wx.EVT_SCROLL, dist_L_text_change)
    dist_L_tt = wx.StaticText(p, pos=(1.0 * L, 0.2 * L + default_padding),
                              label='Distance between transmitter and reciever')
    dist_L_text = wx.StaticText(p, pos=(1.7 * L, 0.2 * L + default_padding), label='0')

    dist_L_slider.SetValue(dist_L * 100)
    dist_L_text.SetLabel(str(dist_L))

    def wave_length_text_change(evt):  # called on slider events
        global wave_length
        wave_length = wave_length_slider.GetValue() / 1000
        wave_length_text.SetLabel(str(wave_length))

    wave_length_slider = wx.Slider(p, pos=(1.0 * L, 0.4 * L + default_padding), size=(0.9 * L, 20), minValue=0,
                                   maxValue=100)
    wave_length_slider.Bind(wx.EVT_SCROLL, wave_length_text_change)
    wave_length_tt = wx.StaticText(p, pos=(1.0 * L, 0.35 * L + default_padding), label='wave_length')
    wave_length_text = wx.StaticText(p, pos=(1.7 * L, 0.35 * L + default_padding), label='0')

    wave_length_slider.SetValue(wave_length * 1000)
    wave_length_text.SetLabel(str(wave_length))

def change_simul_dist(evt):
    global dist_L, slit_width, wave_length, dist_slit, reflection_coeff_floor,reflection_coeff_trans,h, p, L, Hgraph, default_padding
    global h_tt,reflection_coeff_floor_tt,reflection_coeff_trans_tt, h_slider,h_text,reflection_coeff_floor_slider,reflection_coeff_floor_text,reflection_coeff_trans_slider,reflection_coeff_trans_text
    global start_dist_simul,start_double_simul,start_single_simul
    global change_simul_dist, change_simul_single, change_simul_double
    slit_width = 0.015
    dist_slit = 0.3
    wave_length = 0.03
    dist_L = 0.5
    global lbox, center, lrail, lplate, lnail, tri1, tri2, lmicrowave, rmicrowave, rbox, rrail, rplate, rnail
    lbox.visible = False
    center.visible = False
    lrail.visible = False
    lplate.visible = False
    lnail.visible = False
    tri1.visible = False
    tri2.visible = False
    lmicrowave.visible = False
    rmicrowave.visible = False
    rbox.visible = False
    rnail.visible = False
    rplate.visible = False
    rrail.visible = False
    try:
        global sleetbox1, tri, triangleplate, sleetbox2, sleet2, sleet1, sleet3
        sleetbox1.visible = False
        tri.visible = False
        triangleplate.visible = False
        sleetbox2.visible = False
        sleet1.visible = False
        sleet2.visible = False
        sleet3.visible = False
    except:
        pass

    lbox = box(pos=(-8, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    center = cylinder(pos=(0, 2, 0), radius=4, axis=(0, -3, 0), color=(0.3, 0.3, 0.3), material=materials.shiny)
    lrail = box(pos=(-30, 0.5, 0), length=60, width=2, height=1, material=materials.wood)
    lplate = box(pos=(-11, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8), material=materials.shiny)
    lnail = cylinder(pos=(-12, 20, 0), axis=(-0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)

    t = -25
    theta = 0
    theta2 = theta

    tri1 = shapes.trapezoid(top=10, height=1, width=14, rotate=pi - math.atan(2))
    tri2 = shapes.trapezoid(top=10, height=1, width=14, rotate=-pi / 2 + math.atan(2))
    k = 12 / sqrt(5)
    k1 = k
    lmicrowave = extrusion(pos=paths.rectangle(pos=(-3, 20, 0), height=k, width=k, up=(-1, 0, 0)), shape=tri1,
                           color=color.white, material=materials.plastic)
    rmicro_path = [vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) - sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) - sin(theta) * k1 / 2, 20 - k1 / 2,
                          -(35 + t) * sin(theta2) - cos(theta) * k1 / 2),
                   vector((t + 35) * cos(theta2) + k1 / 2 * sin(theta), 20 - k1 / 2,
                          -(35 + t) * sin(theta2) + k1 / 2 * cos(theta)),
                   vector((35 + t) * cos(theta2) + sin(theta) * k1 / 2, 20 + k1 / 2,
                          -(35 + t) * sin(theta2) + cos(theta) * k1 / 2)]
    rmicrowave = extrusion(pos=rmicro_path, shape=tri2, color=color.white, material=materials.plastic)
    rbox = box(pos=(40 + t, 20, 0), height=7, width=7, length=5, color=(0.5, 0.5, 0.5))
    rrail = box(pos=(50, 0.5, 0), length=100, width=2, height=1, material=materials.wood)
    rplate = box(pos=(43 + t, 10.75, 0), height=21.5, width=4, length=1, color=(0.8, 0.8, 0.8),
                 material=materials.shiny)
    rnail = cylinder(pos=(44 + t, 20, 0), axis=(0.5, 0, 0), color=color.black, material=materials.shiny, radius=1)
    rbox.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rplate.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rnail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)
    rrail.rotate(axis=(0, 1, 0), origin=(0, 0, 0), angle=theta)

    reflection_coeff_floor = 0.9
    reflection_coeff_trans = 0.9
    h = 0.2

    try:
        # if it comes from double slit
        global start_simul, change_ui1, change_ui2, slit_width_slider, dist_slit_slider, dist_L_slider, wave_length_slider
        global slit_width_text, slit_width_tt, dist_slit_tt, dist_slit_text, dist_L_tt, dist_L_text, wave_length_tt, wave_length_text
        start_simul.Destroy()
        change_ui1.Destroy()
        change_ui2.Destroy()
        dist_L_slider.Destroy()
        wave_length_slider.Destroy()
        dist_L_text.Destroy()
        dist_L_tt.Destroy()
        wave_length_text.Destroy()
        wave_length_tt.Destroy()
        slit_width_slider.Destroy()
        slit_width_text.Destroy()
        slit_width_tt.Destroy()
        dist_slit_slider.Destroy()
        dist_slit_text.Destroy()
        dist_slit_tt.Destroy()

        print(1)
    except:
        pass

    try:
        # if it comes from single slit
        global start_simul, change_ui1, change_ui2, slit_width_slider, dist_L_slider, wave_length_slider, dist_slit_slider
        global slit_width_text, slit_width_tt, dist_L_tt, dist_L_text, wave_length_tt, wave_length_text, dist_slit_text, dist_slit_tt

        start_simul.Destroy()
        change_ui1.Destroy()
        change_ui2.Destroy()
        slit_width_slider.Destroy()
        dist_L_slider.Destroy()
        wave_length_slider.Destroy()
        slit_width_text.Destroy()
        slit_width_tt.Destroy()
        dist_L_text.Destroy()
        dist_L_tt.Destroy()
        wave_length_text.Destroy()
        wave_length_tt.Destroy()
    except:
        pass

    start_simul = wx.Button(p, label='Start Simulation - varying dist', pos=(L * 1.25, L * 0.65 + default_padding))
    start_simul.Bind(wx.EVT_BUTTON, start_dist_simul)

    change_ui1 = wx.Button(p, label='Changing the UI to single slit simulation',
                           pos=(L * 1.18, L * 0.75 + default_padding))
    change_ui1.Bind(wx.EVT_BUTTON, change_simul_single)

    change_ui2 = wx.Button(p, label='Changing the UI to double slit simulation',
                           pos=(L * 1.17, L * 0.85 + default_padding))
    change_ui2.Bind(wx.EVT_BUTTON, change_simul_double)

    def h_text_change(evt):  # called on slider events
        global h
        h = h_slider.GetValue() / 100
        h_text.SetLabel(str(h))

    h_slider = wx.Slider(p, pos=(1.0 * L, 0.1 * L + default_padding), size=(0.9 * L, 20), minValue=0,
                                  maxValue=100)
    h_slider.Bind(wx.EVT_SCROLL, h_text_change)
    h_tt = wx.StaticText(p, pos=(1.0 * L, 0.05 * L + default_padding), label='height of the device')
    h_text = wx.StaticText(p, pos=(1.7 * L, 0.05 * L + default_padding), label='0')

    h_slider.SetValue(h * 100)
    h_text.SetLabel(str(h))

    def reflection_coeff_floor_text_change(evt):  # called on slider events
        global reflection_coeff_floor
        reflection_coeff_floor = reflection_coeff_floor_slider.GetValue() / 100
        reflection_coeff_floor_text.SetLabel(str(reflection_coeff_floor))

    reflection_coeff_floor_slider = wx.Slider(p, pos=(1.0 * L, 0.25 * L + default_padding), size=(0.9 * L, 20), minValue=0,
                                 maxValue=100)
    reflection_coeff_floor_slider.Bind(wx.EVT_SCROLL, reflection_coeff_floor_text_change)
    reflection_coeff_floor_tt = wx.StaticText(p, pos=(1.0 * L, 0.2 * L + default_padding), label='Reflection coefficient at the floor')
    reflection_coeff_floor_text = wx.StaticText(p, pos=(1.7 * L, 0.2 * L + default_padding), label='0')

    reflection_coeff_floor_slider.SetValue(reflection_coeff_floor * 100)
    reflection_coeff_floor_text.SetLabel(str(reflection_coeff_floor))

    def reflection_coeff_trans_text_change(evt):  # called on slider events
        global reflection_coeff_trans
        reflection_coeff_trans = reflection_coeff_trans_slider.GetValue() /100
        reflection_coeff_trans_text.SetLabel(str(reflection_coeff_trans))

    reflection_coeff_trans_slider = wx.Slider(p, pos=(1.0 * L, 0.4 * L + default_padding), size=(0.9 * L, 20), minValue=0, maxValue=100)
    reflection_coeff_trans_slider.Bind(wx.EVT_SCROLL, reflection_coeff_trans_text_change)
    reflection_coeff_trans_tt = wx.StaticText(p, pos=(1.0 * L, 0.35 * L + default_padding),
                              label='Reflection coefficient at microwave device')
    reflection_coeff_trans_text = wx.StaticText(p, pos=(1.7 * L, 0.35 * L + default_padding), label='0')

    reflection_coeff_trans_slider.SetValue(reflection_coeff_trans * 100)
    reflection_coeff_trans_text.SetLabel(str(reflection_coeff_trans))

    def wave_length_text_change(evt):  # called on slider events
        global wave_length
        wave_length = wave_length_slider.GetValue() / 1000
        wave_length_text.SetLabel(str(wave_length))

    wave_length_slider = wx.Slider(p, pos=(1.0 * L, 0.55 * L + default_padding), size=(0.9 * L, 20), minValue=0,
                                   maxValue=100)
    wave_length_slider.Bind(wx.EVT_SCROLL, wave_length_text_change)
    wave_length_tt = wx.StaticText(p, pos=(1.0 * L, 0.5 * L + default_padding), label='wave_length')
    wave_length_text = wx.StaticText(p, pos=(1.7 * L, 0.5 * L + default_padding), label='0')

    wave_length_slider.SetValue(wave_length * 1000)
    wave_length_text.SetLabel(str(wave_length))


h_slider = 0
h_text = 0
h_tt = 0
reflection_coeff_trans_text = 0
reflection_coeff_trans_slider = 0
reflection_coeff_trans_tt = 0
reflection_coeff_floor_text = 0
reflection_coeff_floor_slider = 0
reflection_coeff_floor_tt = 0

start_simul = wx.Button(p, label='Start Simulation - double slit', pos=(L * 1.25, L * 0.65+default_padding))
start_simul.Bind(wx.EVT_BUTTON, start_double_simul)

change_ui1 = wx.Button(p, label='Changing the UI to single slit simulation', pos=(L * 1.18, L * 0.75+default_padding))
change_ui1.Bind(wx.EVT_BUTTON, change_simul_single)

change_ui2 = wx.Button(p, label='Changing the UI to varying distance simulation', pos=(L * 1.13, L * 0.85+default_padding))
change_ui2.Bind(wx.EVT_BUTTON, change_simul_dist)

def slit_width_text_change(evt):  # called on slider events
    global slit_width
    slit_width = slit_width_slider.GetValue() / 1000
    slit_width_text.SetLabel(str(slit_width))

slit_width_slider = wx.Slider(p, pos=(1.0 * L, 0.1 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=100)
slit_width_slider.Bind(wx.EVT_SCROLL,  slit_width_text_change)
slit_width_tt = wx.StaticText(p, pos=(1.0 * L, 0.05 * L+default_padding), label='slit_width')
slit_width_text = wx.StaticText(p, pos=(1.7 * L, 0.05 * L+default_padding), label='0')

slit_width_slider.SetValue(slit_width * 1000)
slit_width_text.SetLabel(str(slit_width))

def dist_slit_text_change(evt):  # called on slider events
    global dist_slit
    dist_slit = dist_slit_slider.GetValue() / 200
    dist_slit_text.SetLabel(str(dist_slit))

dist_slit_slider = wx.Slider(p, pos=(1.0 * L, 0.25 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=100)
dist_slit_slider.Bind(wx.EVT_SCROLL, dist_slit_text_change)
dist_slit_tt = wx.StaticText(p, pos=(1.0 * L, 0.2 * L+default_padding), label='Distance between Slit')
dist_slit_text = wx.StaticText(p, pos=(1.7 * L, 0.2 * L+default_padding), label='0')

dist_slit_slider.SetValue(dist_slit * 200)
dist_slit_text.SetLabel(str(dist_slit))

def dist_L_text_change(evt):  # called on slider events
    global dist_L
    dist_L = dist_L_slider.GetValue() / 100
    dist_L_text.SetLabel(str(dist_L))

dist_L_slider = wx.Slider(p, pos=(1.0 * L, 0.4 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=100)
dist_L_slider.Bind(wx.EVT_SCROLL, dist_L_text_change)
dist_L_tt = wx.StaticText(p, pos=(1.0 * L, 0.35 * L+default_padding), label='Distance between transmitter and reciever')
dist_L_text = wx.StaticText(p, pos=(1.7 * L, 0.35 * L+default_padding), label='0')

dist_L_slider.SetValue(dist_L * 100)
dist_L_text.SetLabel(str(dist_L))

def wave_length_text_change(evt):  # called on slider events
    global wave_length
    wave_length = wave_length_slider.GetValue() / 1000
    wave_length_text.SetLabel(str(wave_length))

wave_length_slider = wx.Slider(p, pos=(1.0 * L, 0.55 * L+default_padding), size=(0.9 * L, 20), minValue=0, maxValue=100)
wave_length_slider.Bind(wx.EVT_SCROLL, wave_length_text_change)
wave_length_tt = wx.StaticText(p, pos=(1.0 * L, 0.5 * L+default_padding), label='wave_length')
wave_length_text = wx.StaticText(p, pos=(1.7 * L, 0.5 * L+default_padding), label='0')

wave_length_slider.SetValue(wave_length * 1000)
wave_length_text.SetLabel(str(wave_length))

#physcs simulation

def double_slit(theta):
    def distance(a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
    d = dist_slit
    # slit width
    w = slit_width
    R = dist_L
    k = 2 * math.pi / wave_length

    source_list = xrange2(-w / 2, w / 2, w / 1000)

    E_sum = 0
    for j in range(len(source_list)):
        r10 = (0, source_list[j] + d / 2)
        r11 = (0, source_list[j] - d / 2)
        r2 = (R * math.cos(theta), R * math.sin(theta))
        distance1 = distance(r10, r2)
        distance2 = distance(r11, r2)
        E_sum += math.cos(k * distance1) + math.cos(k * distance2)
    return E_sum ** 2

def single_slit(theta):
    def distance(a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    d = slit_width
    R = dist_L
    k = 2 * math.pi / wave_length

    source_list = xrange2(-d / 2, d / 2, d / 1000)
    E_sum = 0
    for j in range(len(source_list)):
        r1 = (0, source_list[j])
        r2 = (R * math.cos(theta), R * math.sin(theta))
        dist = distance(r1, r2)
        E_sum += math.cos(k * dist)
    return E_sum ** 2

def dist_slit_simul(dist):
    k = 2 * math.pi / wave_length
    r1 = reflection_coeff_floor
    r2 = reflection_coeff_trans
    E1 = - r1 / (dist ** 2 / 4 + h ** 2) ** 1.0 * math.cos(k * (dist ** 2 + h ** 2) ** 0.5)
    E2 = 1 / dist * math.cos(k * dist)
    E3 = 1 / dist * r2 ** 2 / dist ** 2 * math.cos(3 * k * dist)
    return (E1 + E2 + E3) ** 2

lbox = box(pos = (-40,20,0), height = 7, width = 7, length = 5, color = (0.5,0.5,0.5))
center = cylinder(pos = (0,2,0), radius =4, axis = (0,-3,0), color = (0.3,0.3,0.3), material = materials.shiny)
lrail = box(pos = (-30,0.5,0), length = 60, width = 2, height = 1, material = materials.wood)
lplate = box(pos = (-43,10.75,0), height = 21.5, width = 4, length = 1, color = (0.8,0.8,0.8), material = materials.shiny)
lnail = cylinder(pos = (-44,20,0), axis = (-0.5,0,0), color = color.black, material = materials.shiny, radius = 1)


t=-10
theta = 0
theta2 = theta

tri1 = shapes.trapezoid(top = 10, height = 1, width = 14, rotate = pi - math.atan(2))
tri2 = shapes.trapezoid(top = 10, height = 1, width = 14, rotate = -pi/2 + math.atan(2))
k = 12/sqrt(5)
k1 = k
lmicrowave = extrusion(pos = paths.rectangle(pos = (-35,20,0), height = k, width = k, up = (-1,0,0)), shape = tri1, color = color.white, material = materials.plastic)
rmicro_path = [vector((35+t)*cos(theta2)+sin(theta)*k1/2,20+k1/2,-(35+t)*sin(theta2)+k1/2*cos(theta)),vector((35+t)*cos(theta2)-sin(theta)*k1/2,20+k1/2,-(35+t)*sin(theta2)-cos(theta)*k1/2),vector((t+35)*cos(theta2)-sin(theta)*k1/2,20-k1/2,-(35+t)*sin(theta2)-cos(theta)*k1/2),vector((t+35)*cos(theta2)+k1/2*sin(theta),20-k1/2,-(35+t)*sin(theta2)+k1/2*cos(theta)),vector((35+t)*cos(theta2)+sin(theta)*k1/2,20+k1/2,-(35+t)*sin(theta2)+cos(theta)*k1/2)]
rmicrowave = extrusion(pos = rmicro_path, shape = tri2, color = color.white, material = materials.plastic)
rbox = box(pos = (40+t,20,0), height = 7, width = 7, length = 5, color = (0.5,0.5,0.5))
rrail = box(pos = (30,0.5,0), length = 60, width = 2, height = 1, material = materials.wood)
rplate = box(pos = (43+t,10.75,0), height = 21.5, width = 4, length = 1, color = (0.8,0.8,0.8), material = materials.shiny)
rnail = cylinder(pos = (44+t,20,0), axis = (0.5,0,0), color = color.black, material = materials.shiny, radius = 1)
rbox.rotate(axis = (0,1,0), origin = (0,0,0), angle = theta)
rplate.rotate(axis = (0,1,0), origin = (0,0,0), angle = theta)
rnail.rotate(axis = (0,1,0), origin = (0,0,0), angle = theta)
rrail.rotate(axis = (0,1,0), origin = (0,0,0), angle = theta)

#making slit
sleetbox1 = extrusion(path=paths.line(start=(-2, 6, 0), end=(2, 6, 0)), shape=shapes.triangle(length=3 * sqrt(3)))
tri = shapes.triangle(length=3 * sqrt(3) * 1.8)
triangleplate = extrusion(pos=paths.line(start=(0, 4, -1.5), end=(0, 4, 1.5)), shape=tri, color=(0.2, 0.2, 0.2),
                          material=materials.plastic)
sleetbox2 = box(pos=(0, 9.8, 0), length=1.5, width=28, height=2.3, color=(0.8, 0.8, 0.8), material=materials.shiny)
sleet2 = box(pos=(0, 20, -8.5), length=1, width=10, height=19, color=(0.6, 0.6, 0.6), material=materials.shiny)
sleet1 = box(pos=(0, 20, 0), length=1, width=5, height=19, color=(0.6, 0.6, 0.6), material=materials.shiny)
sleet3 = box(pos=(0, 20, 8.5), length=1, width=10, height=19, color=(0.6, 0.6, 0.6), material=materials.shiny)
def setleft(evt):
    global subprocess
    subprocess.Popen(["microwav.pdf"], shell=True)

m = w.menubar # Refers to the menubar, which can have several menus

menu = wx.Menu()
item = menu.Append(-1, 'Open Document', 'Make box rotate to the left')
w.win.Bind(wx.EVT_MENU, setleft, item)
m.Append(menu, 'Options')