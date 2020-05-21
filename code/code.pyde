add_library('controlP5')
add_library('video')

class axis:    
    def __init__(self,x11,x12,x21,x22,y11,y12,y21,y22):
        self.x11 = x11
        self.x12 = x12
        self.x21 = x21
        self.x22 = x22
        
        self.y11 = y11
        self.y12 = y12
        self.y21 = y21
        self.y22 = y22
    
    def show(self):
        n1 = 6
        n2 = 6 
        
        stroke(230,230,230,180)
        
        line(self.x11, self.y12, self.x11, -self.y11)
        line(self.x12, self.y12, self.x12, -self.y11)
        text(self.x22, self.x12, 15)
        
        line(self.x11, self.y11, self.x12, self.y11)
        line(self.x11, -self.y12, self.x12, -self.y12)
        text(self.y22, -42, -self.y12)
        text(self.y21, -42, self.y11)
        
        pushMatrix()
        stroke(230,230,230,50)
        for i in range(n1):
            x = self.x11 + i*(self.x12/n1)
            line(x, -self.y11, x, self.y12)
            
        for i in range(n2):
            y = self.y11 + i*(-2*self.y11/n2)
            line(self.x11, y, self.x12, y)
        popMatrix()
        
        
def applyforce(x1,y1,x2,y2): 
    m = (y2-y1)/(x2-x1)
    return m,x1,y1,x2,y2

def integral(a,r,m,b,s,c):
    v = ((c*m*cos(c*r)-c*cos(a*c)*m)*s + m*sin(c*r) + (-c*m*r-b*c)*cos(c*r) + (a*c*cos(a*c)-sin(a*c))*m + b*c*cos(a*c)) / (c*c)
    return v

def cosh(x):
    return (exp(x)+exp(-x))/2

def catnaria(x,L,lamda,t):
    r = (t*cos(PI/4)/lamda)
    x1 = (x-L/2)/r
    x2 = -(L/2)/r
    y = r*cosh(x1)-r*cosh(x2)
    return y

def f(x, x_p, y_p):
    for i in range(len(x_p)-1):
        if x_p[i] <= x <= x_p[i+1]:
            m,s,b,x2,y2 = applyforce(x_p[i], y_p[i], x_p[i+1], y_p[i+1])
            return -1*(m*(x-s)+b)
        
def f_odd(x):
    T = 2*a.x22
    for n in range(0, 10000):
        if (0 + T*n <= x <= a.x22 + T*n):
            return f((x-T*n), x_p, y_p)
        
        if (-a.x22 + T*n <= x <= 0 + T*n):
            return -f(-(x-T*n), x_p, y_p)
        
        if (0 - T*n <= x <= a.x22 - T*n):
            return f((x+T*n), x_p, y_p)
        
        if (-a.x22 - T*n <= x <= 0 - T*n):
            return -f(-(x+T*n), x_p, y_p)

class particle:
    def __init__(self, x, y):
        self.x1 = x
        self.y1 = y
        self.x2 = map(self.x1, a.x11, a.x12, a.x21, a.x22)
        
    def show(self):
        ellipse(self.x1, self.y1, 1, 1)
        
    def wave_dalambert(self, t, v):
        x = self.x2
        x1 = x-(v*t)
        x2 = x+(v*t)
        y2 = (f_odd(x1)+f_odd(x2))/2
        y1 = map(y2, a.y21, a.y22, -a.y11, a.y12)
        self.y1 = y1

    def wave_furier(self,k,g,v,t,L2):
        x = self.x2
        y = 0
        
        for n in range(2,3):
            fn = (v*n)/(2*L2)*(1-((L2*k)/(v*n*PI))**(2))**(1/2)
            dy = .10*(cos(2*PI*fn*t) + (k/(2*PI*fn))*sin(2*PI*fn*t))*sin((n*PI*x)/L2)
            y += dy
        y2 = exp(-k*t)*y
        y2 += catnaria(x,0.7,S.lamda,v)
        y1 = map(y2, a.y21, a.y22, -a.y11, a.y12)
        self.y1 = -y1
        
        
class string:
    def __init__(self, n, L, k, g, v, d, dt):
        self.t = 0
        self.k = k
        self.g = g
        self.v = v
        self.d = d
        self.dt = dt
        self.c = sqrt(v/d)
        self.lamda = .024
        self.L = L
        self.L2 = a.x22
        print(a.x22)
        self.FC = []
        self.P = []
        for i in range(2):
            P = []
            self.P.append(P)
        
        for i in range(n+1):
            x1 = i*(L/n)
            for i in range(2):
                n_p = particle(x1, 0)
                self.P[i].append(n_p)
                
            
    def fourier_coefficients(self,f_n,iterations,x_p,y_p):
        for n in range(1,iterations):
            total = 0
            c = (n*PI)/self.L2
            for i in range(2):
                m,x1,y1,x2,y2 = applyforce(x_p[i],y_p[i],x_p[i+1],y_p[i+1])
                total += (2/self.L2)*integral(x1,x2,m,y1,x1,c)
            self.FC.append(total)
            
    def update(self):
        for i in range(len(self.P[0])):
            self.P[0][i].wave_dalambert(self.t, self.c)
            self.P[1][i].wave_furier(self.k, self.g, self.c, self.t, self.L2)
        self.t += self.dt
        
    def show(self):
        strokeWeight(5)
        for n in range(2):
            P = self.P
            if n == 0:
                stroke(35, 79, 182,70)
                #for i in range(len(self.P[0])-1):
                    #P[0][i].show()
                    #line(P[0][i].x1, P[0][i].y1, P[0][i+1].x1, P[0][i+1].y1)
            if n == 1:
                stroke(35, 79, 182,150)
                for i in range(len(self.P[1])-1):
                    line(P[1][i].x1, P[1][i].y1, P[1][i+1].x1, P[1][i+1].y1)

def mousePressed():
    movie.jump(71)
    if (-a.y11 < (height/2+s2)-mouseY < a.y12):
        x1 = map(mouseX-(width/2-s1), a.x11, a.x12, a.x21, a.x22)
        y1 = map((height/2+s2)-mouseY, -a.y11, a.y12, a.y21, a.y22)
        x = [0.0, x1, 0.7]
        y = [0.0, y1, 0.0]
        resetSkech(x, y, n, L, k, g, v, d, dt)
        
    else:
        resetSkech(x_p, y_p, n, L, slider1.value, slider2.value, slider3.value, slider5.value, slider4.value/frameRate)
        
def resetSkech(x_i, y_i, n_i, L_i, k_i, g_i, v_i, d_i, dt_i):
    global x_p
    x_p = x_i
    global y_p
    y_p = y_i
    global n
    n = n_i
    global L
    L = L_i
    global k
    k = k_i
    global g
    g = g_i
    global v
    v = v_i
    global d
    d = d_i
    global dt
    dt = dt_i
    global S
    S = string(n, L, k, g, v, d, dt)
    S.fourier_coefficients(1, 50, x_p, y_p)

def movieEvent(m):
    m.read() 
            
def setup():
    frameRate(60)
    size(1000,500)
   
    x11 = 0.0
    x12 = 700.0
    x21 = 0.0
    x22 = .70
    
    y11 = 150.0
    y12 = 150.0
    y21 = -0.20
    y22 = 0.20
    
    global a
    a =  axis (x11, x12, x21, x22, y11, y12, y21, y22) 
    
    global s1
    s1 = 350
    global s2
    s2 = 30
    
    x_i = [0.0, 0.3, 0.7]
    y_i = [0.0, -0.3, 0.0]
    
    n = 50
    L = x12
    k_i = 10.06
    g_i = 9.81
    v_i = 1.16
    d_i = .0012
    dt_i = 0.0043  
    
    global movie
    movie = Movie(this, "string.mov")
    movie.loop()
    movie.volume(0)
    
    global slider1
    cp5 = ControlP5(this)
    slider1 = cp5.addSlider("Friccion").setPosition(width/2-s1 + 10, 20).setSize(120, 20).setRange(0, k_i+30).setValue(k_i).setDecimalPrecision(2)
    
    global slider2
    cp5 = ControlP5(this)
    slider2 = cp5.addSlider("Gravedad").setPosition(width/2-s1 + 10, 70).setSize(120, 20).setRange(0, g_i+10).setValue(g_i).setDecimalPrecision(2)
    
    global slider3
    cp5 = ControlP5(this)
    slider3 = cp5.addSlider("Tension").setPosition(width/2-s1 + 200, 20).setSize(120, 20).setRange(0, v_i+10).setValue(v_i).setDecimalPrecision(2)
    
    global slider4
    cp5 = ControlP5(this)
    slider4 = cp5.addSlider("Tiempo").setPosition(width/2-s1 + 200, 70).setSize(120, 20).setRange(0.000,1).setValue(dt_i).setDecimalPrecision(4)
    
    global slider5
    cp5 = ControlP5(this)
    slider5 = cp5.addSlider("D. Lineal").setPosition(width/2-s1 + 380, 70).setSize(120, 20).setRange(0,d_i+.01).setValue(d_i).setDecimalPrecision(4)

    resetSkech(x_i, y_i, n, L, k_i, g_i, v_i, d_i, dt_i)
    
def draw():
    background(5)
    stroke(250)
    strokeWeight(1)
    print(frameRate)
    pushMatrix()
    translate(width/2-s1, height/2+s2)
    #image(movie, a.x11-50, a.y11-30, a.x12+100, -2*a.y12+10)
    a.show()
    S.update()
    S.show()
    text("Tiempo:", 10, -a.y12-10)    
    text(S.t, 60, -a.y12-10)
    popMatrix()
