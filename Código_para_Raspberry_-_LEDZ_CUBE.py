import time
from rpi_ws281x import *
import argparse
import firebase_admin
from firebase_admin import credentials, firestore, db

cred = credentials.Certificate('')
firebase_admin.initialize_app(cred, {
    'databaseURL': ''
})

#Led strip information
LED_COUNT      = 171
LED_PIN        = 18
LED_FREQ_HZ    = 800000
LED_DMA        = 10 
LED_BRIGHTNESS = 65
LED_INVERT     = False
LED_CHANNEL    = 0   

# Initializing the matrix that will represent the Rubik's Cube
cuboMagico = [[[0] * 4 for _ in range(4)] for _ in range(7)]
for i in range(1, 7):
    for j in range(1, 4):
        for k in range(1, 4):
            cuboMagico[i][j][k] = i

# Functions responsible for face rotation movements
def giroface(cuboMagico, i):
    cor = cuboMagico[i][1][1]
    cuboMagico[i][1][1] = cuboMagico[i][3][1]
    cuboMagico[i][3][1] = cuboMagico[i][3][3]
    cuboMagico[i][3][3] = cuboMagico[i][1][3]
    cuboMagico[i][1][3] = cor
    cor = cuboMagico[i][1][2]
    cuboMagico[i][1][2] = cuboMagico[i][2][1]
    cuboMagico[i][2][1] = cuboMagico[i][3][2]
    cuboMagico[i][3][2] = cuboMagico[i][2][3]
    cuboMagico[i][2][3] = cor

def R(cuboMagico):
    colDirFr = [0] * 4
    for i in range(1, 4):
        colDirFr[i] = cuboMagico[1][i][3]
    for i in range(1, 4):
        cuboMagico[1][i][3] = cuboMagico[3][i][3]
        cuboMagico[3][i][3] = cuboMagico[5][4 - i][1]
        cuboMagico[5][4 - i][1] = cuboMagico[2][i][3]
        cuboMagico[2][i][3] = colDirFr[i]
    giroface(cuboMagico, 4)

def L(cuboMagico):
    colEsqFr = [0] * 4
    for i in range(1, 4):
        colEsqFr[i] = cuboMagico[1][i][1]
    for i in range(1, 4):
        cuboMagico[1][i][1] = cuboMagico[2][i][1]
        cuboMagico[2][i][1] = cuboMagico[5][4 - i][3]
        cuboMagico[5][4 - i][3] = cuboMagico[3][i][1]
        cuboMagico[3][i][1] = colEsqFr[i]
    giroface(cuboMagico, 6)

def U(cuboMagico):
    linCimFr = [0] * 4
    for i in range(1, 4):
        linCimFr[i] = cuboMagico[1][1][i]
    for i in range(1, 4):
        cuboMagico[1][1][i] = cuboMagico[4][1][i]
        cuboMagico[4][1][i] = cuboMagico[5][1][i]
        cuboMagico[5][1][i] = cuboMagico[6][1][i]
        cuboMagico[6][1][i] = linCimFr[i]
    giroface(cuboMagico, 2)

def D(cuboMagico):
    linBaiFr = [0] * 4
    for i in range(1, 4):
        linBaiFr[i] = cuboMagico[1][3][i]
    for i in range(1, 4):
        cuboMagico[1][3][i] = cuboMagico[6][3][i]
        cuboMagico[6][3][i] = cuboMagico[5][3][i]
        cuboMagico[5][3][i] = cuboMagico[4][3][i]
        cuboMagico[4][3][i] = linBaiFr[i]
    giroface(cuboMagico, 3)

def F(cuboMagico):
    linBaiCim = [0] * 4
    for i in range(1, 4):
        linBaiCim[i] = cuboMagico[2][3][i]
    for i in range(1, 4):
        cuboMagico[2][3][i] = cuboMagico[6][4 - i][3]
        cuboMagico[6][4 - i][3] = cuboMagico[3][1][4 - i]
        cuboMagico[3][1][4 - i] = cuboMagico[4][i][1]
        cuboMagico[4][i][1] = linBaiCim[i]
    giroface(cuboMagico, 1)

def B(cuboMagico):
    linCimCim = [0] * 4
    for i in range(1, 4):
        linCimCim[i] = cuboMagico[2][1][i]
    for i in range(1, 4):
        cuboMagico[2][1][i] = cuboMagico[4][i][3]
        cuboMagico[4][i][3] = cuboMagico[3][3][4-i]
        cuboMagico[3][3][4-i] = cuboMagico[6][4-i][1]
        cuboMagico[6][4-i][1] = linCimCim[i]
    giroface(cuboMagico, 5)

# Function responsible for setting the cube to its initial stage
def reiniciar(cuboMagico):
    for i in range(1, 7):
        for j in range(1, 4):
            for k in range(1, 4):
                cuboMagico[i][j][k] = i

# Converts a value present in the matrix to a correspondent color in
# the Led strip
def converteValCor(val):
    if(val == 1):
        return Color(255,0,0)
    elif(val == 2):
        return Color(0,255,0)
    elif (val == 3):
        return Color(255, 90, 0)
    elif (val == 4):
        return Color(255, 255, 0)
    elif (val == 5):
        return Color(255, 255, 255)
    elif (val == 6):
        return Color(0,0,255)

# Function responsible for corresponding the color in the cube
# to the color of a specific Led in the Led strip
def correspondencia(cuboMagico, pixels):
    pixels.setPixelColor(20, converteValCor(cuboMagico[3][3][3]))
    pixels.setPixelColor(17, converteValCor(cuboMagico[3][2][3]))
    pixels.setPixelColor(2, converteValCor(cuboMagico[3][1][3]))
    pixels.setPixelColor(5, converteValCor(cuboMagico[3][1][2]))
    pixels.setPixelColor(14, converteValCor(cuboMagico[3][2][2]))
    pixels.setPixelColor(23, converteValCor(cuboMagico[3][3][2]))
    pixels.setPixelColor(26, converteValCor(cuboMagico[3][3][1]))
    pixels.setPixelColor(11, converteValCor(cuboMagico[3][2][1]))
    pixels.setPixelColor(8, converteValCor(cuboMagico[3][1][1]))
    pixels.setPixelColor(39, converteValCor(cuboMagico[1][3][1]))
    pixels.setPixelColor(42, converteValCor(cuboMagico[1][3][2]))
    pixels.setPixelColor(45, converteValCor(cuboMagico[1][3][3]))
    pixels.setPixelColor(78, converteValCor(cuboMagico[1][2][1]))
    pixels.setPixelColor(81, converteValCor(cuboMagico[1][2][2]))
    pixels.setPixelColor(84, converteValCor(cuboMagico[1][2][3]))
    pixels.setPixelColor(117, converteValCor(cuboMagico[1][1][1]))
    pixels.setPixelColor(120, converteValCor(cuboMagico[1][1][2]))
    pixels.setPixelColor(123, converteValCor(cuboMagico[1][1][3]))
    pixels.setPixelColor(29, converteValCor(cuboMagico[6][3][1]))
    pixels.setPixelColor(32, converteValCor(cuboMagico[6][3][2]))
    pixels.setPixelColor(35, converteValCor(cuboMagico[6][3][3]))
    pixels.setPixelColor(68, converteValCor(cuboMagico[6][2][1]))
    pixels.setPixelColor(71, converteValCor(cuboMagico[6][2][2]))
    pixels.setPixelColor(74, converteValCor(cuboMagico[6][2][3]))
    pixels.setPixelColor(107, converteValCor(cuboMagico[6][1][1]))
    pixels.setPixelColor(110, converteValCor(cuboMagico[6][1][2]))
    pixels.setPixelColor(113, converteValCor(cuboMagico[6][1][3]))
    pixels.setPixelColor(49, converteValCor(cuboMagico[4][3][1]))
    pixels.setPixelColor(52, converteValCor(cuboMagico[4][3][2]))
    pixels.setPixelColor(55, converteValCor(cuboMagico[4][3][3]))
    pixels.setPixelColor(88, converteValCor(cuboMagico[4][2][1]))
    pixels.setPixelColor(91, converteValCor(cuboMagico[4][2][2]))
    pixels.setPixelColor(94, converteValCor(cuboMagico[4][2][3]))
    pixels.setPixelColor(127, converteValCor(cuboMagico[4][1][1]))
    pixels.setPixelColor(130, converteValCor(cuboMagico[4][1][2]))
    pixels.setPixelColor(133, converteValCor(cuboMagico[4][1][3]))
    pixels.setPixelColor(59, converteValCor(cuboMagico[5][3][1]))
    pixels.setPixelColor(62, converteValCor(cuboMagico[5][3][2]))
    pixels.setPixelColor(65, converteValCor(cuboMagico[5][3][3]))
    pixels.setPixelColor(98, converteValCor(cuboMagico[5][2][1]))
    pixels.setPixelColor(101, converteValCor(cuboMagico[5][2][2]))
    pixels.setPixelColor(104, converteValCor(cuboMagico[5][2][3]))
    pixels.setPixelColor(137, converteValCor(cuboMagico[5][1][1]))
    pixels.setPixelColor(140, converteValCor(cuboMagico[5][1][2]))
    pixels.setPixelColor(143, converteValCor(cuboMagico[5][1][3]))
    pixels.setPixelColor(145, converteValCor(cuboMagico[2][1][1]))
    pixels.setPixelColor(148, converteValCor(cuboMagico[2][1][2]))
    pixels.setPixelColor(151, converteValCor(cuboMagico[2][1][3]))
    pixels.setPixelColor(154, converteValCor(cuboMagico[2][2][3]))
    pixels.setPixelColor(157, converteValCor(cuboMagico[2][2][2]))
    pixels.setPixelColor(160, converteValCor(cuboMagico[2][2][1]))
    pixels.setPixelColor(163, converteValCor(cuboMagico[2][3][1]))
    pixels.setPixelColor(166, converteValCor(cuboMagico[2][3][2]))
    pixels.setPixelColor(169, converteValCor(cuboMagico[2][3][3]))
    pixels.show()

# Function responsible to read the information sent from the app
# to the Firebase storage
def mover_app(cuboMagico):
    ref = db.reference('ledz_cube/Movimento')
    acao = ref.get()
    ref2 = db.reference('Permissao/Permissao')
    permissao = ref2.get()
    if permissao == '1' or permissao == 1:
        if acao == '"R"' or acao == 'R':
            R(cuboMagico)
            ref2.set(0)
            time.sleep(0.4)
        elif acao == '"L"' or acao == 'L':
            L(cuboMagico)
            ref2.set(0)
            time.sleep(0.4)
        elif acao == '"U"' or acao == 'U':
            U(cuboMagico)
            ref2.set(0)
            time.sleep(0.4)
        elif acao == '"D"' or acao == 'D':
            D(cuboMagico)
            ref2.set(0)
            time.sleep(0.4)
        elif acao == '"F"' or acao == 'F':
            F(cuboMagico)
            ref2.set(0)
            time.sleep(0.4)
        elif acao == '"B"' or acao == 'B':
            B(cuboMagico)
            ref2.set(0)
            time.sleep(0.4)
        elif acao == '"I"':
            reiniciar(cuboMagico)
            ref2.set(0)
            time.sleep(0.4)
            
def apagarLeds(fita, cor, delay = 10):
    for i in range(fita.numPixels()):
        fita.setPixelColor(i, cor)
        fita.show()
        time.sleep(delay/1000.0)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    pixels = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    pixels.begin()
    apagarLeds(pixels, Color(0, 0, 0))
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            mover_app(cuboMagico)
            correspondencia(cuboMagico,pixels)
            time.sleep(0.3)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
