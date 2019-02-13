import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d as gf
from collections import defaultdict
import numpy as np
from math import acos
import pygame, pdb
import pandas as pd
import os.path
from openpyxl import load_workbook
from initial_param.kparam import Kparam

class Evaluation(object):
    def __init__(self):
        self.upperbnd = 0
        self.words = defaultdict(list)
        self.kp = Kparam()
        self.font_size = 80

    def joint_angle(self, joints, idx=[0, 1, 2], offset=0):
        """ finding the angle between 3 joints.
            default joints are left shld, elbow, wrist.
        """
        if joints.shape[0] == 33:
            offset = 4
        # Elbow - sholder
        vec1 = np.array([joints[(offset+idx[1])*3+0]-joints[(offset+idx[0])*3+0],
                         joints[(offset+idx[1])*3+1]-joints[(offset+idx[0])*3+1],
                         joints[(offset+idx[1])*3+2]-joints[(offset+idx[0])*3+2]])
        # Elbow - Wrist
        vec2 = np.array([joints[(offset+idx[1])*3+0]-joints[(offset+idx[2])*3+0],
                         joints[(offset+idx[1])*3+1]-joints[(offset+idx[2])*3+1],
                         joints[(offset+idx[1])*3+2]-joints[(offset+idx[2])*3+2]])

        costheta = vec1.dot(vec2)/sum(vec1**2)**.5/sum(vec2**2)**.5
        return acos(costheta)*180/np.pi

    def breath_plot(self, ana, exeno):
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        if len(ana.hs.hstate) == 0:  # only did breathe test (i.e. exer 1)
            ax.plot(gf(ana.brth.breath_list, 5), color='g')
            if len(ana.brth.ngframe) != 0:
                for i in ana.brth.ngframe:
                    y1 = ana.brth.breath_list[i]
                    y2 = y1 - 20  
                    ax.annotate('Not deep breathing', xy=(i, y1-2), xytext=(i, y2),\
                                arrowprops=dict(facecolor='red', shrink=0.05),)
            plt.title('Breathe in and out')
            fig.savefig('output/Exer%s_bio_1.jpg' % str(exeno))
            plt.close(fig)
    
    def breath_hand_plot(self, ana, exeno, scale=5):
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        ax.plot(ana.hs.hstate[:, 0]*15, color='b')
        ax.plot(ana.hs.hstate[:, 1]*15-20, color='r')
        ax.plot(gf(ana.brth.breath_list, scale), color='g')
        if len(ana.brth.ngframe) != 0:
            for i in ana.brth.ngframe:
                y1 = ana.brth.breath_list[i]#/self.breath_list[0]*2
                y2 = 1.5*10
                ax.annotate('breathing not deep enough', xy=(i, y1), xytext=(i, y2),\
                            arrowprops=dict(facecolor='red', shrink=0.05),)
        if len(ana.brth.missingbreath) != 0:
            for i in ana.brth.missingbreath:
                x = sum(i)/2
                y1 = ana.brth.breath_list[x]#/self.breath_list[0]*2 
                y2 = 1*10
                ax.annotate('missing breathing', xy=(x, y1), xytext=(x, y2),\
                            arrowprops=dict(facecolor='green', shrink=0.05),)
        plt.title('Breathe in and out & hands open and close')
        fig.savefig('output/Exer%s_biohoc_1.jpg' %str(exeno)) 
        plt.close(fig)
  

    def cutdata(self, data, length=4):
        """ if data too long (user do more than default repitition), cut it
            if data too short (user do less than default repitition), add ''
        """
        if len(data) == length:
            return data
        elif len(data) > length:
            data = data[:length]
        else:
            data = data + ['']*length-len(data)
        return data

    def run(self, exeno, ana):
        """ exercise performance evaluation
        """
        if exeno == 1 :
            self.breath_plot(ana, exeno)
            if len(ana.brth.brth_diff) == 0:
                return ['','','']
            return [min(ana.brth.brth_diff), max(ana.brth.brth_diff),
                    np.mean(ana.brth.brth_diff)]        
        elif exeno == 2:
            self.breath_hand_plot(ana, exeno)
            return [min(ana.brth.brth_diff), max(ana.brth.brth_diff), 
                    np.mean(ana.brth.brth_diff), ana.brth.sync_rate]
        elif exeno == 3:
            self.breath_hand_plot(ana, exeno, 10)
            langle = list(np.vstack([ana.dtw.Lcangle, ana.dtw.Ltangle]).T.flatten())
            rangle = list(np.vstack([ana.dtw.Rcangle, ana.dtw.Rtangle]).T.flatten())
            rangle = (rangle+['-NaN']*8)[:8]
            langle = (langle+['-NaN']*8)[:8]         
            result = rangle + [np.mean(ana.dtw.Rcangle), np.mean(ana.dtw.Rtangle)]+ langle + [np.mean(ana.dtw.Lcangle), np.mean(ana.dtw.Ltangle)]
            return result            
        elif exeno == 4:
            langle = list(np.vstack([ana.dtw.Lcangle, ana.dtw.Ltangle]).T.flatten())
            rangle = list(np.vstack([ana.dtw.Rcangle, ana.dtw.Rtangle]).T.flatten())
            return rangle + [np.mean(rangle[::2]), np.mean(rangle[1::2])]+ langle + [np.mean(langle[::2]), np.mean(langle[1::2])]
        elif exeno == 5:
            max_right = np.abs(ana.swing.angle_ini - np.min(ana.swing.min_ary[1:, 1]))
            min_right = np.abs(ana.swing.angle_ini - np.max(ana.swing.min_ary[1:, 1]))
            max_left  = np.abs(ana.swing.angle_ini - np.max(ana.swing.max_ary[1:, 1]))
            min_left  = np.abs(ana.swing.angle_ini - np.min(ana.swing.max_ary[1:, 1]))
            return [max_right, min_right, max_left, min_left]
        elif exeno == 6:
            return [max(ana.shld.dep_diff).astype(float), min(ana.shld.dep_diff).astype(float)]
        elif exeno == 7:
            max_hold  = np.max(ana.clsp.holdtime)
            min_hold  = np.min(ana.clsp.holdtime)
            mean_hold = np.mean(ana.clsp.holdtime)
            #clasp_rate = 1.*ana.clsp.claspsuc/ana.clsp.cnt
            return [max_hold, min_hold, mean_hold]
        else:
            raise ImportError('Did not define this ecercise yet.')
    def cmphist(self, log, userinfo, exeno, time, data=[]):
        """  compare user's latest data with its historical data
        """
        if not all(x == '' for x in data):
            if not os.path.isfile('./output/compare.txt'):
                text_file = open("./output/compare.txt", "w") 
            else:
                text_file = open("./output/compare.txt", "a")
            date = '-'.join(map(str,[time.year,time.month,time.day,time.hour,time.minute]))
            str0 = '\n%10s: %s\n%10s: %s\n%10s: %s\n'% ('Exercise', exeno, 'Username', userinfo.name, 'Date', date)

            text_file.write(str0)
            print(str0)
            if os.path.isfile(log.excelPath):
                name = userinfo.name
                df = pd.read_excel(log.excelPath, sheet_name='exercise %s' %exeno)
                cols = log.colname[exeno][4:-1]  # donot neet common & errmsg info
                roi = df[df['name'] == name]  # rows of interest
                def_val = df[df['name'] == '$IDEAL VALUE$']
                def_val = def_val.values.tolist()[0][4:4+len(cols)]
                history = []
                terms = []
                for col in cols:
                    history.append(round(roi[col].mean(),2))
                    terms.append(col)
                str1 = '%40s | %18s | %15s | %16s\n'%('Terms', 'In history record', 'This time', 'Results')
                print(str1)
                text_file.write(str1)
                for i in xrange(len(cols)):
                    if def_val[i] == 'bigger is better':  # lager value is preferred
                        if history[i] >= data[i]:
                            evaluation = 'worsen'
                        else:
                            evaluation = 'improve'
                        num = round(abs(data[i]-history[i])/history[i]*100, 2)
                    else:  # should compare with default values
                        if abs(history[i]-def_val[i]) >= abs(data[i]-def_val[i]):
                            evaluation = 'improve'
                        else:
                            evaluation = 'worsen'
                        num = round(abs(abs(data[i]-def_val[i])-abs(history[i]-def_val[i]))/def_val[i]*100, 2)
                    
                    str2 = '%40s | %18s | %15s | %6s%s %8s\n' %(terms[i], history[i], round(data[i], 2), num, '%', evaluation) 
                    print(str2)
                    text_file.write(str2)
            else:
                str1 = 'No historical data for this user.\n'
                print(str1)
                text_file.write(str1)
            text_file.close()
        else:
            print('Did not capture any data.')
    def errmsg(self, errs=[], dolist=None, contents=['Breathing eval', 'Hand eval', 'Exercise motion',\
                                                     'Shoulder State', 'Clasp & Spread', 'Swing']):
        """ According to the test results, showing evaluation results.
        """
        print('\nevaluation:\n')
        for idx, err in enumerate(errs):
            if len(err) != 0:
                for i, text in enumerate(set(err)):
                    if i == 0:
                        print (('%18s' % contents[idx])+' : '+text)
                    else:
                        print (('%18s' % '')+' : '+text)
            elif dolist[idx]:  # done without err
                print(('%18s' % contents[idx])+' : Perfect !!\n')
            else:
                pass
                #print(('%18s' % contents[idx])+' : Did not test this part.')

    def position(self, surface, region=1):
        """According to the scene type, ratio and the region number
           set up different upper bound and lower bound to the text"""
        self.upperbnd = self.kp.eval_sec[region-1]*surface.get_height()/1080.
        self.leftbnd = self.kp.eval_LB*surface.get_width()/1920.

        return (self.leftbnd, self.upperbnd) 

    def blit_text(self, surface, exeno, kp, text=None, region=1, pos=(0, 0), emph=False, ita=False, fsize=0, color=None):
        """Creat a text surface, this surface will change according to the scene type,
           ratio and the region number. According to the size of the surface, the text 
           will auto change line also auto change size
        """
        color = self.kp.c_guide if color is None else color

        if fsize != 0:
            self.font_size = fsize
        else:
            if region == 1:
                self.font_size = self.kp.eval_fs_title
                emph = True
            elif region == 2:
                self.font_size = self.kp.eval_fs_guide
                emph = True
            elif region == 3:
                self.font_size = self.kp.eval_fs_msg
            elif region == 4:
                self.font_size = self.kp.eval_fs_cnt
                emph = True
            elif region == 5:
                self.font_size = self.kp.eval_fs_msg
            else:
                pass
        self.font = pygame.font.SysFont(self.kp.s_normal, self.font_size, bold=emph, italic=ita)

        self.space = self.font.size(' ')[0]
        if text == None:
            words = self.words[exeno]
        else:
            words = [word.split(' ') for word in text.splitlines()]
        if region != 0:
            (x, y) = self.position(surface, region)
            x_ori, y_ori = x, y
        else:  # customize position
            (x, y) = pos
            x_ori, y_ori = x, y

        max_width = (self.kp.eval_RB-self.kp.eval_LB)*surface.get_width()/1920.
        max_height = (self.kp.eval_sec[region]-self.kp.eval_sec[region-1])*surface.get_height()/1080.

        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width+x_ori:  # change line(row)
                    x = x_ori  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + self.space
            x = x_ori  # Reset the x
            y += word_height  # Start on new row.
        # if y > max_height + y_ori:
        #     if self.font_size > 12:
        #         self.font_size = self.font_size - 2
        #         if emph:
        #             self.font = pygame.font.SysFont(self.kp.s_emp, self.font_size, bold=True)
        #         else:
        #             self.font = pygame.font.SysFont(self.kp.s_normal, self.font_size)
        # elif y < max_height  - 40 :
        #     # print 'small'
        #     if self.font_size < 100:
        #         self.font_size = self.font_size + 1
        #         if emph:
        #             self.font = pygame.font.SysFont(self.kp.s_emp, self.font_size, bold=True)
        #         else:
        #             self.font = pygame.font.SysFont(self.kp.s_normal, self.font_size)            
                


