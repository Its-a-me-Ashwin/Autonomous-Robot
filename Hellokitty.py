"""
**************************************************************************
*                  E-Yantra Robotics Competition
*                  ================================
*  This software is intended to check version compatiability of open source software
*  Theme: Thirsty Crow
*  MODULE: Task1.1
*  Filename: detect.py
*  Version: 1.0.0  
*  Date: October 31, 2018
*  
*  Author: e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
**************************************************************************
"""

import numpy as np
import cv2
import cv2.aruco as aruco
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import pygame
cap = cv2.VideoCapture(0)

texture_object = None
texture_background = None
camera_matrix = None
dist_coeff = None
cap = cv2.VideoCapture(0)
INVERSE_MATRIX = np.array([[ 1.0, 1.0, 1.0, 1.0],
                           [-1.0,-1.0,-1.0,-1.0],
                           [-1.0,-1.0,-1.0,-1.0],
                           [ 1.0, 1.0, 1.0, 1.0]])

################## Define Utility Functions Here #######################
"""
Function Name : getCameraMatrix()
Input: None
Output: camera_matrix, dist_coeff
Purpose: Loads the camera calibration file provided and returns the camera and
         distortion matrix saved in the calibration file.
"""
def getCameraMatrix():
        global camera_matrix, dist_coeff
        with np.load('System.npz') as X:
                camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
def getCameraMatrix_return():
	with np.load('System.npz') as X:
		camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
	return camera_matrix, dist_coeff
def detect_markers(img, camera_matrix, dist_coeff):
        markerLength = 100
        aruco_list = []
	######################## INSERT CODE HERE ########################
        j=0
        aruco_dict=aruco.Dictionary_get(aruco.DICT_5X5_250)
        parameters=aruco.DetectorParameters_create()
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        corners,ids,_=aruco.detectMarkers(img_gray,aruco_dict,parameters=parameters)
        for i in corners:
                id_cur=ids[j]
                j+=1
                rvec, tvec, _= aruco.estimatePoseSingleMarkers(i,100,camera_matrix,dist_coeff)
                centerX=0
                centerY=0
                for x,y in i[0]:
                        centerX+=x
                        centerY+=y
                centerX/=4
                centerY/=4
                aruco_list.append((id_cur,(centerX,centerY),rvec,tvec))
                #print (aruco_list)
	##################################################################
        return aruco_list


########################################################################

############# Main Function and Initialisations ########################
"""
Function Name : main()
Input: None
Output: None
Purpose: Initialises OpenGL window and callback functions. Then starts the event
         processing loop.
"""



cam, dist = getCameraMatrix_return()
cap1=cv2.VideoCapture(1)
data = None
i=0;
while(i < 10):
    # Capture frame-by-frame
    ret, frame = cap1.read()
    if ret != True:
            break
    # Our operations on the frame come here
    if cv2.waitKey(1) & 0xFF == ord('p'):
        data=(detect_markers(frame, cam, dist))
        print(len(data))
        if (len(data) != 0):
            i+=1

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('f'):
        break

# When everything done, release the capture
        

cap1.release()
cv2.destroyAllWindows()
print(data)
aruco_id=[]
aruco_pos=[]
aruco_tvec=[]
aruco_rvec=[]
try:
    for aruco in data:
        aruco_id.append(aruco[0])
        aruco_pos.append(aruco[1])
        aruco_tvec.append(aruco[2])
        aruco_rvec.append(aruco[3])
except:
    print('Died')



def main():
        
        glutInit()
        getCameraMatrix()
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(625, 100)
        glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
        window_id = glutCreateWindow("OpenGL")
        init_gl()
        glutDisplayFunc(drawGLScene)
        glutIdleFunc(drawGLScene)
        glutReshapeFunc(resize)
        glutMainLoop()

"""
Function Name : init_gl()
Input: None
Output: None
Purpose: Initialises various parameters related to OpenGL scene.
"""  
def init_gl():
        global texture_object, texture_background
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0) 
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)   
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        texture_background = glGenTextures(1)
        texture_object = glGenTextures(1)
"""
Function Name : resize()
Input: None
Output: None
Purpose: Initialises the projection matrix of OpenGL scene
"""
def resize(w,h):
        ratio = 1.0* w / h
        glMatrixMode(GL_PROJECTION)
        glViewport(0,0,w,h)
        gluPerspective(45, ratio, 0.1, 100.0)

"""
Function Name : drawGLScene()
Input: None
Output: None
Purpose: It is the main callback function which is called again and
         again by the event processing loop. In this loop, the webcam frame
         is received and set as background for OpenGL scene. ArUco marker is
         detected in the webcam frame and 3D model is overlayed on the marker
         by calling the overlay() function.
"""
def drawGLScene():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        ar_list = []
        ret, frame = cap.read()
        if ret == True:
                draw_background(cv2.imread("background.jpg"))
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                ar_list = data #detect_markers(frame, cam, dist)
                for i in ar_list:
                        if i[0] == 0:
                                overlay(frame, ar_list, i[0],"texture_1.png")
                        if i[0] == 2:
                                overlay(frame, ar_list, i[0],"texture_2.png")
                        if i[0] == 1:
                                overlay(frame, ar_list, i[0],"texture_3.png")
                        if i[0] == 3:
                                overlay(frame, ar_list, i[0],"texture_4.png")              
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
        glutSwapBuffers()
        
########################################################################

######################## Aruco Detection Function ######################
"""
Function Name : detect_markers()
Input: img (numpy array)
Output: aruco list in the form [(aruco_id_1, centre_1, rvec_1, tvec_1),(aruco_id_2,
        centre_2, rvec_2, tvec_2), ()....]
Purpose: This function takes the image in form of a numpy array, camera_matrix and
         distortion matrix as input and detects ArUco markers in the image. For each
         ArUco marker detected in image, paramters such as ID, centre coord, rvec
         and tvec are calculated and stored in a list in a prescribed format. The list
         is returned as output for the function
"""

def detect_markers(img):
        aruco_list = []
        ################################################################
        #################### Same code as Task 1.1 #####################
        ################################################################
        j=0
        aruco_dict=aruco.Dictionary_get(aruco.DICT_5X5_250)
        parameters=aruco.DetectorParameters_create()
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        corners,ids,_=aruco.detectMarkers(img_gray,aruco_dict,parameters=parameters)
        for i in corners:
                id_cur=ids[j]
                j+=1
                rvec, tvec, _= aruco.estimatePoseSingleMarkers(i,100,camera_matrix,dist_coeff)
                centerX=0
                centerY=0
                for x,y in i[0]:
                        centerX+=x
                        centerY+=y
                centerX/=4
                centerY/=4
                aruco_list.append((id_cur,(centerX,centerY),rvec,tvec))
        return aruco_list
########################################################################


################# This is where the magic happens !! ###################
############### Complete these functions as  directed ##################
"""
Function Name : draw_background()
Input: img (numpy array)
Output: None
Purpose: Takes image as input and converts it into an OpenGL texture. That
         OpenGL texture is then set as background of the OpenGL scene
"""

def draw_background(img):
        textbg=[0]
        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glEnable(GL_TEXTURE_2D);
        glBindTexture(GL_TEXTURE_2D, textbg[0]);
        glLoadIdentity();
        # convert image to OpenGL texture format
        bg_image = cv2.flip(img, 0)
        bg_image = Image.fromarray(bg_image)
        ix = bg_image.size[0]
        iy = bg_image.size[1]
        bg_image = bg_image.tobytes("raw", "BGRX", 0, -1)
        # create background texture
        glBindTexture(GL_TEXTURE_2D,textbg[0])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
        # draw background
        glBindTexture(GL_TEXTURE_2D,textbg[0])
        glPushMatrix()
        glTranslatef(0.0,0.0,-10.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-5.0, -4.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 5.0, -4.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 5.0,  4.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-5.0,  4.0, 0.0)
        glEnd()
        glPopMatrix()
        return None

"""
Function Name : init_object_texture()
Input: Image file path
Output: None
Purpose: Takes the filepath of a texture file as input and converts it into OpenGL
         texture. The texture is then applied to the next object rendered in the OpenGL
         scene.
"""
def init_object_texture(image_filepath):
        tex = cv2.imread(image_filepath)
        glMatrixMode(GL_MODELVIEW)
        texture=[0]
        theTexMap=pygame.image.load(image_filepath)
        textureData = pygame.image.tostring(theTexMap, "RGBA", 1)
        width = theTexMap.get_width()
        height = theTexMap.get_height()
        # Pixel alignment: each row is word aligned (aligned to a 4 byte boundary)
        #    Therefore, no need to call glPixelStore( GL_UNPACK_ALIGNMENT, ... );
        glGenTextures(1, texture[0])            # Create The Texture
        glBindTexture(GL_TEXTURE_2D, texture[0])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        # Typical Texture Generation Using Data From The Bitmap  
        #glTexImage2D(GL_TEXTURE_2D, 0, 3, theTexMap.size[1], theTexMap.size[0], 0, GL_RGB, GL_UNSIGNED_BYTE, theTexMap.tobytes("raw", "RGBA", 0, -1) );
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        return None

"""
Function Name : overlay()
Input: img (numpy array), aruco_list, aruco_id, texture_file (filepath of texture file)
Output: None
Purpose: Receives the ArUco information as input and overlays the 3D Model of a teapot
         on the ArUco marker. That ArUco information is used to
         calculate the rotation matrix and subsequently the view matrix. Then that view matrix
         is loaded as current matrix and the 3D model is rendered.

         Parts of this code are already completed, you just need to fill in the blanks. You may
         however add your own code in this function.
"""
def overlay(img, ar_list, ar_id, texture_file):
        for x in ar_list:
                if ar_id == x[0]:
                        centre, rvec, tvec = x[1], x[2], x[3]
        rmtx = cv2.Rodrigues(rvec)[0]
        view_matrix = view_matrix = np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvec[0][0][0]],
                        [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvec[0][0][1]],
                        [rmtx[2][0],rmtx[2][1],rmtx[2][2],tvec[0][0][2]],
                        [0.0       ,0.0       ,0.0       ,1.0    ]])
        view_matrix = view_matrix * INVERSE_MATRIX
        view_matrix = np.transpose(view_matrix)
        m=50
        pts = np.float32([[-m,m,0],[m,m,0],[-m,-m,0],[-m,m,m]])
        pt_dict = {}
        imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
        for i in range(len(pts)):
                pt_dict[tuple(pts[i])] = tuple(imgpts[i].ravel())
        src = pt_dict[tuple(pts[0])]
        dst1 = pt_dict[tuple(pts[1])]
        dst2 = pt_dict[tuple(pts[2])]
        dst3 = pt_dict[tuple(pts[3])]
        dist = math.sqrt((dst1[0]-dst2[0])**2+(dst1[1]-dst2[1])**2)
        init_object_texture(texture_file)
        texture = [0]
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture[0])
        glTranslatef(+(tvec[0][0][0]*2)/250,-(tvec[0][0][1]*2)/200+1,-5)
        glRotatef(rvec[0][0][2]*180/math.pi,0,1,0)#correct
        glRotatef(-rvec[0][0][1]*180/math.pi,0,0,1)#correct
        glRotatef(rvec[0][0][0]*180/math.pi+200,1,0,0)#correct
        glutSolidTeapot(dist/200)
        glFlush()
        glDisable(GL_TEXTURE_2D)
        glPushMatrix()
        glLoadMatrixd(view_matrix)
        glutSolidTeapot(0.5)
        glPopMatrix()


########################################################################

if __name__ == "__main__":
        try:
            main()
        except:
            print('Died')
        
