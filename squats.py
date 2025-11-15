#a, b, c, dimensiunile knees->hip->ankle
from numpy.ma.core import arccos


#S0 -> S1 -> S2 -> S1 -> S0
#In starea unu se incrementeaza reperatarile, daca a fost facuta una
#Actualizam starea de indata ce incepem actiunea
#In starea 3 ajungem daca ne am dus suficient de jos
#Apoi facem traseul.

class Squat:
    def __init__(self):
        self.state = "S0"
        self.angle = 180 #in grade calculat
        self.number_counter = 0
        self.rep_made = 0
        self.message = "start"
    def event(self):
        #cea initiala cand nu faci nimic
        if self.state == "S0":
            if self.rep_made == 1:
                self.number_counter = self.number_counter + 1
                self.rep_made = 0 #Resetam repetarea
                self.message = "Start"
            if self.angle < 160:  #As pus 180, dar nu cred ca o sa calculeze vreodata pana la 180
                self.state = "S1"

        #Starea intermediara
        elif self.state == "S1":
            if self.angle < 90:
                self.state = "S2"
            if self.angle > 160:
                self.state = "S1"
                if self.rep_made == 0:
                    self.message = "You should go deeper"

        #starea finala
        elif self.state == "S2":
            self.rep_made = 1
            if self.angle > 90:
                self.state = "S1"
                self.message = "Good Job"
    def new_angle (self, a_point, b_point, c_point):
        a = side_length(a_point, b_point)
        b = side_length(b_point, c_point)
        c = side_length(c_point, a_point)
        self.angle = angle_calc(a, b, c)
    def get_number_count (self):
        return self.number_counter.__str__()

def angle_calc (a, b, c):
    #ne folosim de formula c2 = a2 + b2 − 2ab cos(C)
    #noua ne trebuie unghiul b
    cos = (c * c + a * a - b * b) / (2 * c * a)
    angle = arccos (cos)
    return angle

def side_length(a, b):
    #pentru 2D a si b de forma (x, y)
    #sqrt ((bx - ax) ^ 2 + (by - ay) ^ 2)
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

#in 3D
#   return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2) ** 0.5

