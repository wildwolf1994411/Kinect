import wx 
from collections import defaultdict
import numpy as np
import pandas as pd
import bodygame3
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import wx
import wx.lib.mixins.inspection as WIT

class Info():
    def __init__(self):
        self.name   = 'jane doe'
        self.age    = 'unknown'
        self.gender = 'unknown'

class Welcome_win(wx.Frame):
    def __init__(self, info, parent, title): 
        self.info = info
        self.game = None
        self.font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Arial')    
        super(Welcome_win, self).__init__(parent, title = title,size = (410, 350))
        panel = wx.Panel(self) 
        sizer = wx.GridBagSizer(30, 30)
        button1 = wx.Button(panel, size=(300,50), label="Live Evaluation")
        button1.SetFont(self.font)
        button1.Bind(wx.EVT_BUTTON, self.open_bodygame)
        sizer.Add(button1, pos=(1, 1), span=(1, 0))

        button2 = wx.Button(panel, size=(300,50), label="Exercise Instruction")
        button2.SetFont(self.font)
        button2.Bind(wx.EVT_BUTTON, self.open_instruction)
        sizer.Add(button2, pos=(2, 1), span=(1, 0))

        button3 = wx.Button(panel, size=(300,50), label="History Review")
        button3.SetFont(self.font)
        button3.Bind(wx.EVT_BUTTON, self.open_history)
        sizer.Add(button3, pos=(3, 1), span=(1, 0))

        panel.SetSizer(sizer)
        # panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground) 
        self.Show(True)  

    def open_bodygame(self, event):
        # myobject = event.GetEventObject()
        # myobject.Disable()
        self.game = bodygame3.BodyGameRuntime(self.info)
        self.game.run()
        if self.game.kp._done:
            self.Destroy()
        
    def open_instruction(self, event):
        instruct = Instrcution_win(None, 'Instruction')

    def open_history(self, event):
        history  = History_view(None, self.info) 

    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("./data/bkimgs/BUMfk9.jpg")
        dc.DrawBitmap(bmp, 0, 0)

class Instrcution_win(wx.Frame): 
            
    def __init__(self, parent, title): 
        self.init_text()
        super(Instrcution_win, self).__init__(parent, title=title, size=(1250, 600))
            
        panel = wx.Panel(self) 
        box = wx.BoxSizer(wx.HORIZONTAL) 
        self.font = wx.Font(28, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Arial')    
        self.text = wx.TextCtrl(panel, size = (1000,600), style = wx.TE_MULTILINE|wx.TE_READONLY) 
        self.text.SetFont(self.font)
        self.text.SetBackgroundColour((179, 236, 255))      
        languages = [self.str['exe'][1], self.str['exe'][2], self.str['exe'][3], self.str['exe'][4],\
                     self.str['exe'][5], self.str['exe'][6], self.str['exe'][7]]  

        box2 = wx.BoxSizer(wx.VERTICAL) 
        lst = wx.ListBox(panel, size = (250, 600*0.9), choices=languages, style=wx.LB_SINGLE)
        lst.SetBackgroundColour((255, 255, 255))  
        button1 = wx.Button(panel, label="Close")
        button1.Bind(wx.EVT_BUTTON, self.close)

        box2.Add(lst,0,wx.EXPAND)
        box2.Add(button1,1,wx.EXPAND)

        box.Add(box2,0,wx.EXPAND) 
        box.Add(self.text, 1, wx.EXPAND)   
        panel.SetSizer(box)
        panel.Fit() 
            
        self.Centre() 
        self.Bind(wx.EVT_LISTBOX, self.onListBox, lst) 
        self.Show(True)  

 
    def init_text(self):
        self.str = defaultdict(dict)
        self.str['exe'][1] = 'Exercise 1 : Muscle Tighting Deep Breathing'
        self.str['exe'][2] = 'Exercise 2 : Over The Head Pumping'
        self.str['exe'][3] = 'Exercise 3 : Push Down Pumping'
        self.str['exe'][4] = 'Exercise 4 : Horizontal Pumping'
        self.str['exe'][5] = 'Exercise 5 : Reach to the Sky'
        self.str['exe'][6] = 'Exercise 6 : Shoulder Rolls'
        self.str['exe'][7] = 'Exercise 7 : Clasp and Spread'

        self.str['ins'][1] = '\n  '\
                             '\n1. Put your hands on the belly position.'\
                             '\n2. Wait until the sign shows "start breath in/out."'\
                             '\n3. Do deep breathing 4 times.'\
                             '\n4. Put down your hands.'

        self.str['ins'][2] = '\n  '\
                             '\n1. Raise your harms up and hold there.'\
                             '\n2. Wait until the sign shows "start breath in/out."'\
                             '\n3. Do deep breathing 4 times.' \
                             '\n4. Put down your arms.'

        self.str['ins'][3] = '\n  '\
                             '\n1. Raise your arms up.'\
                             '\n2. Lower your elbows, let shoulder-elbow-hand be a V-shape.'\
                             '\n3. Raise your arms up again.'\
                             '\n4. Repeat this repetition 4 times.'\
                             '\n5. Put down your arms.'

        self.str['ins'][4] = '\n  '\
                             '\n1. Raise your arms up till "T-pose."'\
                             '\n2. Move arms slowly to the chest.'\
                             '\n3. Back to "T-pose".'\
                             '\n4. Repeat this repetition 4 times.'\
                             '\n5. Put down your arms.'

        self.str['ins'][5] = '\n  '\
                             '\n1. Raise your arms up  as high as possible and clasp.'\
                             '\n2. Bend your body to the left.'\
                             '\n3. Bend your body to the right.'\
                             '\n4. Repeat 4 times.'\
                             '\n5. Put down your arms.'

        self.str['ins'][6] = '\n  '\
                             '\n1. Put your hands on the belly position.'\
                             '\n2. Rotate you shoulder.'\
                             '\n3. Repeat 4 times.'\
                             '\n4. Put down your hands.'

        self.str['ins'][7] = '\n  '\
                             '\n1. Raise and clasp your arms till the belly position.'\
                             '\n2. Raise clasped hands toward to your forehead and keep elbows together.'\
                             '\n3. Slide your heands to the back of your head and spread the elbows open wide.'\
                             '\n4. Back to the belly position.'\
                             '\n5. Repeat 4 times.'\
                             '\n6. Put down your arms.'
        
        self.str['note'][1] = 'Tips :'\
                                '\n1. Tighten your muscle as much as you can.'\
                                '\n2. Breathe as deep as you can.'
        self.str['note'][2] = 'Tips :'\
                                '\n1. When you breathe in, you also need to close your hands.'\
                                '\n2. When you breathe out, you also need to open your hands.'\
                                '\n3. Breathe as deep as you can.'
        self.str['note'][3] = 'Tips :'\
                                '\n1. When you raise up your arms, make sure that your hand, elbow and shoulder are straight.'\
                                '\n2. When bending the elbow, hand-elbow-shoulder should be "V-shape" not "L-shape"'\
 
        self.str['note'][4] = 'Tips :'\
                                '\n1. When doing "T-pose", make sure that your hand, elbow and shoulder are straight'\
                                '\n2. When closing hands, make sure that your hand, and shoulder are in the same height.'\

        self.str['note'][5] = 'Tips :'\
                                '\n1. When bending the body, make sure that your hand, elbow and shoulder are straight.'\
                                '\n2. Keep your body staight'

        self.str['note'][6] = 'Tips :'\
                                '\n1. Let your shoulders rotation movement as large as possible.'

        self.str['note'][7] = 'Tips :'\
                                '\n1. When raising the arms to the forehead, keeping two elbows as close as possible.'\
                                '\n2. When the hands is in the back of your head, spread the elnows open as wide as possible.'\
                                '\n3. Keep your body staight.'

    def onListBox(self, event): 
        self.text.Clear()
        ex = event.GetEventObject().GetSelection()+1
        self.text.AppendText(self.str['exe'][ex]+self.str['ins'][ex]+'\n\n')
        self.text.AppendText(self.str['note'][ex])

    def close(self, event):
        self.Destroy()

class History_view( wx.Frame ):	
    def __init__(self, parent, info = Info(), title = 'welcome'):
        super(History_view, self).__init__(parent, title = title, size = (850, 520))
        self.info = info
        self.InitUI()
        self.Show()  

    def InitUI(self, path = './output/log.xlsx'):
        self.font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)  
        self.path = path
        log_xl = pd.ExcelFile(path)
        self.panel = wx.Panel(self)

        box1 = wx.BoxSizer(wx.VERTICAL) 
        box2 = wx.BoxSizer(wx.VERTICAL)
        box3 = wx.BoxSizer(wx.HORIZONTAL)

        info_text = 'Name: '+self.info.name.title()+'\nGender: '+self.info.gender.title()+'     Age: '+str(self.info.age)
        info = wx.StaticText(self.panel, wx.ID_ANY, label = info_text)
        info.SetFont(self.font)
        box1.Add(info, 0, wx.EXPAND)

        ex_choices = log_xl.sheet_names
        self.choice = wx.Choice(self.panel, choices=ex_choices)
        self.choice.SetFont(self.font)
        self.choice.Bind(wx.EVT_CHOICE, self.update_choice)
        box1.Add(self.choice, 1, wx.EXPAND)
        box2.Add(box1, 0)

        self.lst = wx.ListBox(self.panel, size = (330, 300), choices = [], style = wx.LB_SINGLE)
        self.lst.SetFont(self.font)
        self.Bind(wx.EVT_LISTBOX, self.update_figure, self.lst)     
        box2.Add(self.lst, 1, wx.EXPAND)
        box3.Add(box2, 0, wx.EXPAND)


        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        box3.Add(self.canvas, 1, wx.EXPAND)

        self.panel.SetSizer(box3) 
        self.panel.Fit() 

    def update_choice (self, event):
        cur_choice = self.choice.GetSelection()
        self.df = pd.read_excel(self.path, sheetname=cur_choice)
        self.lst.Clear()
        lst_choice = self.df.columns.values.tolist()
        idx_1 = [i for i, elem in enumerate(lst_choice) if 'time' in elem][0]+1
        idx_2 = [i for i, elem in enumerate(lst_choice) if 'errmsg' in elem][0]
        self.lst.InsertItems(lst_choice[idx_1:idx_2], 0)
    
    def update_figure(self, event):
        df_name  = self.df[self.df['name'] == self.info.name]
        df_ideal = self.df[self.df['name'] == '$IDEAL VALUE$']
        item = self.lst.GetStringSelection()
        y = np.array(df_name[item])
        x = np.arange(0, len(y), 1)
        x_name = df_name['time'].tolist()
        self.axes.clear()    
        self.axes.bar(x, y, color='g')
        if df_ideal[item].dtype == float:
            cri = df_ideal[item][0]
            self.axes.axhline(cri, color='r', linestyle='-', linewidth=4)
        else:
            cri = 0
        self.axes.set_title(item)
        self.axes.set_xticks(x)
        self.axes.set_ylim(0,max(np.max(y),cri)+10)
        self.axes.set_xticklabels(x_name, rotation=25, fontsize=10)
        self.canvas.draw()