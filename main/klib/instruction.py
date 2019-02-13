from collections import defaultdict
from initial_param.kparam import Kparam
import pygame, pdb

pygame.init()

class Exeinst(object):
    "Exercise instruxtion"
    def __init__(self):
        self.leftbnd = 0
        self.upperbnd = 0
        self.str = defaultdict(dict)
        self.words = defaultdict(dict)
        self.kp = Kparam()
        self.part = [0, 0.5, 5./6, 1]

        self.str['name'][1] = 'Muscle Tighting Deep Breathing'
        self.str['name'][2] = 'Over The Head Pumping'
        self.str['name'][3] = 'Push Down Pumping'
        self.str['name'][4] = 'Horizontal Pumping'
        self.str['name'][5] = 'Reach to the Sky'
        self.str['name'][6] = 'Shoulder Rolls'
        self.str['name'][7] = 'Clasp and Spread'

        self.str['exe'][1] = 'Exercise 1 : Muscle Tighting Deep Breathing'\
                             '\n  '\
                             '\n1. Put your hands on the belly position.'\
                             '\n2. Wait until the sign shows "start breath in/out."'\
                             '\n3. Do deep breathing 4 times.'\
                             '\n4. Put down your hands.'

        self.str['exe'][2] = 'Exercise 2 : Over The Head Pumping'\
                             '\n  '\
                             '\n1. Raise your arms up and hold there.'\
                             '\n2. Wait until the sign shows "start breath in/out."'\
                             '\n3. Do deep breathing 4 times.' \
                             '\n4. Put down your arms.'

        self.str['exe'][3] = 'Exercise 3 : Push Down Pumping'\
                             '\n  '\
                             '\n1. Raise your arms up.'\
                             '\n2. Lower your elbows, let shoulder-elbow-hand be a V-shape.'\
                             '\n3. Raise your arms up again.'\
                             '\n4. Repeat this repetition 4 times.'\
                             '\n5. Put down your arms.'

        self.str['exe'][4] = 'Exercise 4 : Horizontal Pumping'\
                             '\n  '\
                             '\n1. Raise your arms up till "T-pose."'\
                             '\n2. Move arms slowly to the chest.'\
                             '\n3. Back to "T-pose".'\
                             '\n4. Repeat this repetition 4 times.'\
                             '\n5. Put down your arns.'

        self.str['exe'][5] = 'Exercise 5 : Reach to the Sky'\
                             '\n  '\
                             '\n1. Raise your arms up  as high as possible and clasp.'\
                             '\n2. Bend your body to the left.'\
                             '\n3. Bend your body to the right.'\
                             '\n4. Repeat 4 times.'\
                             '\n5. Put down your arms.'

        self.str['exe'][6] = 'Exercise 6 : Shoulder Rolls'\
                             '\n  '\
                             '\n1. Put your hands on the belly position.'\
                             '\n2. Rotate you shoulder.'\
                             '\n3. Repeat 4 times.'\
                             '\n4. Put down your arms.'

        self.str['exe'][7] = 'Exercise 7 : Clasp and Spread'\
                             '\n  '\
                             '\n1. Raise and clasp your arms till the belly position.'\
                             '\n2. Raise clasped hands toward to your forehead and keep elbows together.'\
                             '\n3. Slide your heands to the back of your head and spread the elbows open wide.'\
                             '\n4. Back to the belly position.'\
                             '\n5. Repeat 4 times.'\
                             '\n6. Put down your arms.'

        
        self.str['note'][1] = '\nTips :'\
                                '\n1. Tighten your muscle as much as you can.'\
                                '\n2. Breathe as deep as you can.'
        self.str['note'][2] = '\nTips :'\
                                '\n1. When you breathe in, you also need to close your hands.'\
                                '\n2. When you breathe out, you also need to open your hands.'\
                                '\n3. Breathe as deep as you can.'
        self.str['note'][3] = '\nTips :'\
                                '\n1. When you raise up your hands, make sure that your hand, elbow and shoulder are straight.'\
                                '\n2. When bending the elbow, hand-elbow-shoulder should be "V-shape" not "L-shape"'\
 
        self.str['note'][4] = '\nTips :'\
                                '\n1. When doing "T-pose", make sure that your hand, elbow and shoulder are straight'\
                                '\n2. When closing hands, make sure that your hand, and shoulder are in the same height.'\

        self.str['note'][5] = '\nTips :'\
                                '\n1. When bending the body, make sure that your hand, elbow and shoulder are straight.'\
                                '\n2. Keep your body staight'

        self.str['note'][6] = '\nTips :'\
                                '\n1. Let your shoulders rotation movement as large as possible.'

        self.str['note'][7] = '\nTips :'\
                                '\n1. When raising the arms to the forehead, keeping two elbows as close as possible.'\
                                '\n2. When the hands is in the back of your head, spread the elnows open as wide as possible.'\
                                '\n3. Keep your body staight.'

        self.words['exe'][1] = [word.split(' ') for word in self.str['exe'][1].splitlines()]
        self.words['exe'][2] = [word.split(' ') for word in self.str['exe'][2].splitlines()]
        self.words['exe'][3] = [word.split(' ') for word in self.str['exe'][3].splitlines()]
        self.words['exe'][4] = [word.split(' ') for word in self.str['exe'][4].splitlines()]
        self.words['exe'][5] = [word.split(' ') for word in self.str['exe'][5].splitlines()]
        self.words['exe'][6] = [word.split(' ') for word in self.str['exe'][6].splitlines()]
        self.words['exe'][7] = [word.split(' ') for word in self.str['exe'][7].splitlines()]

        self.words['note'][1] = [word.split(' ') for word in self.str['note'][1].splitlines()]
        self.words['note'][2] = [word.split(' ') for word in self.str['note'][2].splitlines()]
        self.words['note'][3] = [word.split(' ') for word in self.str['note'][3].splitlines()]
        self.words['note'][4] = [word.split(' ') for word in self.str['note'][4].splitlines()]
        self.words['note'][5] = [word.split(' ') for word in self.str['note'][5].splitlines()]
        self.words['note'][6] = [word.split(' ') for word in self.str['note'][6].splitlines()]
        self.words['note'][7] = [word.split(' ') for word in self.str['note'][7].splitlines()]

        self.title = [''.join(self.str['name'][x]) for x in range(1, 8)]
        self.title = ['Exercise '+repr(i+1)+': '+self.title[i] for i in range(len(self.title))]
        self.title.append('(Press 1~7 to do Execise 1~7.)')
        self.words['title'][0] = [word.split(' ') for word in self.title]

        self.font_size = self.kp.inst_size
        # self.font = pygame.font.SysFont('Arial', self.font_size)
        #self.space = self.font.size(' ')[0]  # The width of a space.

    def position(self, surface, ratio, stype, region=1, height=0):
        """According to the scene type, ratio and the region number
           set up different upper bound and lower bound to the text"""
        if stype == 2:
            self.leftbnd = int(surface.get_width()*ratio)
            self.upperbnd = height*self.part[region-1]
        else:
            self.leftbnd = int(surface.get_width()*(1-ratio))
            self.upperbnd = height*self.part[region-1]
        return (self.leftbnd, self.upperbnd + 20)

    def show_list(self, surface, exeno):
        """Creat a text surface, this surface will change according to the scene type,
           ratio and the region number. According to the size of the surface, the text 
           will auto change line also auto change the font size"""
        self.font = pygame.font.SysFont(self.kp.s_normal, 60)
        self.space = self.font.size(' ')[0]  # The width of a space.

        words = self.words['title'][0]
        max_width = (self.kp.video_RB - self.kp.video_LB)*surface.get_width()/1920.
        max_height = (self.kp.video1_UB - self.kp.video1_UB)*surface.get_height()/1080.
        (x, y) = (self.kp.video_LB*surface.get_width()/1920., self.kp.video1_UB*surface.get_height()/1080.)
        x_ori, y_ori = x, y

        for idx, line in enumerate(words):
            if idx+1 == exeno:
                color = self.kp.c_eval_err
            else:
                color = self.kp.c_eval_well
            for word in line:
                word_surface = self.font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width+x_ori:
                    x = x_ori  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + self.space
            x = x_ori  # Reset the x.
            y += word_height  # Start on new row.


    # def blit_text(self, surface, exeno, kp, strtype='exe', text=None, region=1, emph=False, color=None):
    #     """Creat a text surface, this surface will change according to the scene type,
    #        ratio and the region number. According to the size of the surface, the text 
    #        will auto change line also auto change the font size"""
    #     color = self.kp.c_inst if color is None else color
    #     if emph:
    #         self.font = pygame.font.SysFont(self.kp.s_emp, self.font_size, bold=True, italic=True)
    #     else:
    #         self.font = pygame.font.SysFont(self.kp.s_normal, self.font_size)
    #     self.space = self.font.size(' ')[0]  # The width of a space.
    #     if text == None:  # if there is no assign text, use the text in data base 
    #         words = self.words[strtype][exeno]
    #     else:
    #         words = [word.split(' ') for word in text.splitlines()]

    #     if kp.scene_type == 2:  # avatar in upper-left, color frame in lower-right
    #         max_width = surface.get_width()*(1-kp.ratio)
    #         height = surface.get_height()*kp.ratio
    #     else:
    #         max_width = surface.get_width()*kp.ratio
    #         height = surface.get_height()*(1-kp.ratio)

    #     max_height = height*self.part[region]

    #     (x, y) = self.position(surface, kp.ratio, kp.scene_type, region, height)
    #     x_ori, y_ori = x, y

    #     for line in words:
    #         for word in line:
    #             word_surface = self.font.render(word, 0, color)
    #             word_width, word_height = word_surface.get_size()
    #             if x + word_width >= max_width+x_ori:
    #                 x = x_ori  # Reset the x.
    #                 y += word_height  # Start on new row.
    #             surface.blit(word_surface, (x, y))
    #             x += word_width + self.space
    #         x = x_ori  # Reset the x.
    #         y += word_height  # Start on new row.

        # if y > max_height + y_ori:  # change font size if it is out of the boundary
        #     # print 'large'
        #     if self.font_size > 12:
        #         self.font_size = self.font_size - 1
        #         if emph:
        #             self.font = pygame.font.SysFont(self.kp.s_emp, self.font_size, bold=True, italic=True)
        #         else:
        #             self.font = pygame.font.SysFont(self.kp.s_normal, self.font_size)
        # elif y < max_height  - 40 :
        #     # print 'small'
        #     if self.font_size < 40:
        #         self.font_size = self.font_size + 1
        #         if emph:
        #             self.font = pygame.font.SysFont(self.kp.s_emp, self.font_size, bold=True, italic=True)
        #         else:
        #             self.font = pygame.font.SysFont(self.kp.s_normal, self.font_size)   
