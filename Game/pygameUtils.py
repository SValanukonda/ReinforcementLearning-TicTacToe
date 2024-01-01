import pygame 
import sys
class Utils:

    def drawBlackLine(surfObj,strtPos,endPos):
            pygame.draw.line(surfObj, (0, 0, 0),strtPos,endPos, 10)

    def drawBlueLine(surfObj,strtPos,endPos):
            pygame.draw.line(surfObj, (0, 0, 255),strtPos,endPos,8)


    def showmsg(strng,dur=None):
        pygame.display.set_caption(strng)
        if(dur):
            pygame.time.wait(dur)
            pygame.display.set_caption("")
        


    def drawX(surfObj,pos,width):
        pygame.draw.line(surfObj, (255, 0, 0), ((pos[0] - width), (pos[1] - width)),
                                 ((pos[0] + width), (pos[1] + width)), 15)
        pygame.draw.line(surfObj, (255, 0, 0), (pos[0] - width, pos[1] + width),
                                 (pos[0] + width, pos[1] - width), 15)
        
    def drawO(surfObj,pos,radius):
         pygame.draw.circle(surfObj, (0, 255, 0), pos,radius, 15)

    def displayMouseInput():
        while(True):
            for event in pygame.event.get():
                if(event.type==pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                if(event.type==pygame.MOUSEBUTTONDOWN):
                    pos=pygame.mouse.get_pos()
                    return(pos)
    
    def keyboardInput():
        while(True):
            for event in pygame.event.get():
                if(event.type==pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                if(event.type == pygame.KEYDOWN):
                    return(pygame.key.name(event.key))