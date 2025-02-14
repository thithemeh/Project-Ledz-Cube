#Imported libraries for the project:
#
#mediapipe and cv2 for image capturing and image processing
#pygame and OpenGL to generate the 3D Rubik's Cube model
#pyrebase for communication with the firebase data storage
import pyrebase
import cv2
import mediapipe as mp
import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Firebase storage information
config = {
    "apiKey": 
    "authDomain": 
    "databaseURL": 
    "projectId":
    "databaseURL":
    "storageBucket":
    "messagingSenderId":
    "appId":
    "measurementId": 
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

#Function that detects lowered fingers
def identifica_dedos_dobrados(landmarks):
    pontas_dedos = [4, 8, 12, 16, 20]

    dedos_dobrados = [0] * 5

    if landmarks[4].x > landmarks[3].x:
        dedos_dobrados[0] = 1

    for idx, tip in enumerate(pontas_dedos[1:], start=1):
        if landmarks[tip].y > landmarks[tip - 2].y:
            dedos_dobrados[idx] = 1

    return dedos_dobrados

#Function responsible for the rotation of
#Rubik's Cube faces
def giroface(cuboMagico,i):
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

    data = {"Movimento": "R"}
    database.child("ledz_cube").set(data)

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
    data = {"Movimento": "L"}
    database.child("ledz_cube").set(data)

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
    data = {"Movimento": "U"}
    database.child("ledz_cube").set(data)

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
    data = {"Movimento": "D"}
    database.child("ledz_cube").set(data)

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
    data = {"Movimento": "F"}
    database.child("ledz_cube").set(data)

def B(cuboMagico):
    linCimCim = [0] * 4
    for i in range(1, 4):
        linCimCim[i] = cuboMagico[2][1][i]
    for i in range(1, 4):
        cuboMagico[2][1][i] = cuboMagico[4][i][3]
        cuboMagico[4][i][3] = cuboMagico[3][3][i]
        cuboMagico[3][3][i] = cuboMagico[6][i][1]
        cuboMagico[6][i][1] = linCimCim[4 - i]
    giroface(cuboMagico, 5)
    data = {"Movimento": "B"}
    database.child("ledz_cube").set(data)

#Function responsible for shuffling the cube
def S(cuboMagico):
    for i in range(1, 20):
        valor = random.randint(1,6)
        if i == 1:
            R(cuboMagico)
        elif i == 2:
            L(cuboMagico)
        elif i == 3:
            U(cuboMagico)
        elif i == 4:
            D(cuboMagico)
        elif i == 5:
            F(cuboMagico)
        else:
            B(cuboMagico)

#Function responsible for restarting the cube
def reiniciar(cuboMagico):
    for i in range(1, 7):
        for j in range(1, 4):
            for k in range(1, 4):
                cuboMagico[i][j][k] = i

#Function that identifies the information sent by the
#mobile app to the Firebase storage
def mover_app(cuboMagico):
    movimento = database.child("ledz_cube").child("Movimento").get()
    acao = movimento.val()
    print(acao)
    if acao == '"R"':
        R(cuboMagico)
    elif acao == '"L"':
        L(cuboMagico)
    elif acao == '"U"':
        U(cuboMagico)
    elif acao == '"D"':
        D(cuboMagico)
    elif acao == '"F"':
        F(cuboMagico)
    elif acao == '"B"':
        B(cuboMagico)
    elif acao == '"S"':
        S(cuboMagico)
    elif acao == '"I"':
        reiniciar(cuboMagico)

#Function that rotates the cube accordingly to the
#lowered fingers
def rotacionar(dedos_dobrados, cuboMagico):
    if dedos_dobrados == [1, 0, 0, 0, 0]:
        R(cuboMagico)
    elif dedos_dobrados == [0, 1, 0, 0, 0]:
        U(cuboMagico)
    elif dedos_dobrados == [0, 0, 1, 0, 0]:
        D(cuboMagico)
    elif dedos_dobrados == [0, 0, 0, 1, 0]:
        L(cuboMagico)
    elif dedos_dobrados == [0, 0, 0, 0, 1]:
        F(cuboMagico)
    elif dedos_dobrados == [1, 1, 1, 1, 1]:
        B(cuboMagico)
    elif dedos_dobrados == [0, 1, 1, 1, 1]:
        mover_app(cuboMagico)

#Function that shows the current state of the cube
def mostrarCubo(cuboMagico):
    for j in range(1, 4):
        print("      ", end="")
        for k in range(1, 4):
            print(cuboMagico[2][j][k], end=" ")
        print()
    for i in range(1, 4):
        for j in range(1, 4):
            print(cuboMagico[6][i][j], end=" ")
        for j in range(1, 4):
            print(cuboMagico[1][i][j], end=" ")
        for j in range(1, 4):
            print(cuboMagico[4][i][j], end=" ")
        print("  ", end="")
        for j in range(1, 4):
            print(cuboMagico[5][i][j], end=" ")
        print()
    for j in range(1, 4):
        print("      ", end="")
        for k in range(1, 4):
            print(cuboMagico[3][j][k], end=" ")
        print()
    print()

#Creation of the 3d model
mapa_cores = {
    1: (1, 0, 0),   #red
    2: (0, 1, 0),   #green
    3: (1, 0.5, 0), #orange
    4: (1, 1, 0),   #yellow
    5: (1, 1, 1),   #white
    6: (0, 0, 1),   #blue
    7: (0, 0, 0)    #black
}

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

arestas = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

faces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

#Class that defines the 27 smaller cube that constitute
#the larger cube
class Cubo:
    def __init__(self, indices_cor, posicao):
        self.colors = [mapa_cores[index] for index in indices_cor]
        self.position = posicao

    def atualizar_cor(self, novos_indices_cor):
        self.colors = [mapa_cores[index] for index in novos_indices_cor]

    def exibir_cubo(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glBegin(GL_QUADS)
        for i in range(len(faces)):
            glColor3fv(self.colors[i])
            for vertice in faces[i]:
                glVertex3fv(vertices[vertice])
        glEnd()

        glBegin(GL_LINES)
        glColor3fv((0, 0, 0))
        for aresta in arestas:
            for vertice in aresta:
                glVertex3fv(vertices[vertice])
        glEnd()
        glPopMatrix()

#Function responsible for generating the 27 smaller cubes
def criar_cubos():
    cubos = []
    for x in range(3):
        for y in range(3):
            for z in range(3):
                indices_cor = [1,2,3,4,5,6]
                posicao = (x * 2 - 2, y * 2 - 2, z * 2 - 2)
                cubos.append(Cubo(indices_cor, posicao))
    return cubos

def correspondencia(cuboMagico, cubes):
    cubes[0].atualizar_cor([cuboMagico[5][3][3],cuboMagico[6][3][1],7,7,7,cuboMagico[3][3][1]])
    cubes[1].atualizar_cor([7, cuboMagico[6][3][2], 7, 7, 7, cuboMagico[3][2][1]])
    cubes[2].atualizar_cor([7, cuboMagico[6][3][3], cuboMagico[1][3][1], 7, 7, cuboMagico[3][1][1]])
    cubes[3].atualizar_cor([cuboMagico[5][2][3], cuboMagico[6][2][1], 7, 7, 7, 7])
    cubes[4].atualizar_cor([7, cuboMagico[6][2][2], 7, 7, 7, 7])
    cubes[5].atualizar_cor([7, cuboMagico[6][2][3], cuboMagico[1][2][1], 7, 7, 7])
    cubes[6].atualizar_cor([cuboMagico[5][1][3], cuboMagico[6][1][1], 7, 7, cuboMagico[2][1][1], 7])
    cubes[7].atualizar_cor([7, cuboMagico[6][1][2], 7, 7, cuboMagico[2][2][1], 7])
    cubes[8].atualizar_cor([7, cuboMagico[6][1][3], cuboMagico[1][1][1], 7, cuboMagico[2][3][1], 7])
    cubes[9].atualizar_cor([cuboMagico[5][3][2], 7, 7, 7, 7, cuboMagico[3][3][2]])
    cubes[10].atualizar_cor([7, 7, 7, 7, 7, cuboMagico[3][2][2]])
    cubes[11].atualizar_cor([7, 7, cuboMagico[1][3][2], 7, 7, cuboMagico[3][1][2]])
    cubes[12].atualizar_cor([cuboMagico[5][2][2], 7, 7, 7, 7, 7])
    cubes[14].atualizar_cor([7, 7, cuboMagico[1][2][2], 7, 7, 7])
    cubes[15].atualizar_cor([cuboMagico[5][1][2], 7, 7, 7, cuboMagico[2][1][2], 7])
    cubes[16].atualizar_cor([7, 7, 7, 7, cuboMagico[2][2][2], 7])
    cubes[17].atualizar_cor([7, 7, cuboMagico[1][1][2], 7, cuboMagico[2][3][2], 7])
    cubes[18].atualizar_cor([cuboMagico[5][3][1], 7, 7, cuboMagico[4][3][3], 7, cuboMagico[3][3][3]])
    cubes[19].atualizar_cor([7, 7, 7, cuboMagico[4][3][2], 7, cuboMagico[3][2][3]])
    cubes[20].atualizar_cor([7, 7, cuboMagico[1][3][3], cuboMagico[4][3][1], 7, cuboMagico[3][1][3]])
    cubes[21].atualizar_cor([cuboMagico[5][2][1], 7, 7, cuboMagico[4][2][3], 7, 7])
    cubes[22].atualizar_cor([7, 7, 7, cuboMagico[4][2][2], 7, 7])
    cubes[23].atualizar_cor([7, 7, cuboMagico[1][2][3], cuboMagico[4][2][1], 7, 7])
    cubes[24].atualizar_cor([cuboMagico[5][1][1], 7, 7, cuboMagico[4][1][3], cuboMagico[2][1][3], 7])
    cubes[25].atualizar_cor([7, 7, 7, cuboMagico[4][1][2], cuboMagico[2][2][3], 7])
    cubes[26].atualizar_cor([7, 7, cuboMagico[1][1][3], cuboMagico[4][1][1], cuboMagico[2][3][3], 7])

#Initializing the matrix that will represent the Rubik's cube
cuboMagico = [[[0] * 4 for _ in range(4)] for _ in range(7)]
for i in range(1, 7):
    for j in range(1, 4):
        for k in range(1, 4):
            cuboMagico[i][j][k] = i

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -20)

    cubos = criar_cubos()

    rot_x, rot_y = 0, 0
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(frame_rgb)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
               for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        rot_x -= 30
                    elif event.key == pygame.K_DOWN:
                        rot_x += 30
                    elif event.key == pygame.K_LEFT:
                        rot_y -= 30
                    elif event.key == pygame.K_RIGHT:
                        rot_y += 30
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0.0, 0.0, -20)

            glRotatef(rot_x, 1, 0, 0)
            glRotatef(rot_y, 0, 1, 0)

            correspondencia(cuboMagico, cubos)

            for cubo in cubos:
                cubo.exibir_cubo()

            pygame.display.flip()
            pygame.time.wait(5)

            dedos_dobrados = identifica_dedos_dobrados(hand_landmarks.landmark)
            rotacionar(dedos_dobrados, cuboMagico)
            mostrarCubo(cuboMagico);

            nomes_dedos = ['Polegar', 'Indicador', 'Medio', 'Anelar', 'Minimo']
            for idx, dobrado in enumerate(dedos_dobrados):
                nome = nomes_dedos[idx]
                if dobrado:
                    status = 'Abaixado'
                else:
                    status = 'Levantado'
                cv2.putText(frame, f'{nome}: {status}', (10, 20 + idx * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f'Polegar - R', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f'Indicador - U', (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f'Medio - D', (10, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f'Anelar - L', (10, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f'Minimo - F', (10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f'Todos - B', (10, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('d'):
            break

        time.sleep(0.3)
if __name__ == '__main__':
    main()
    pygame.quit()
    quit()





