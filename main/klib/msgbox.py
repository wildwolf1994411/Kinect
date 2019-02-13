import wx, pdb

class Msgbox(wx.Frame):

    def __init__(self, parent, title):   
        self.font = wx.Font(28, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Arial')  
        self.font_button = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Arial')    
        self.width  = 750 #400*2
        self.height = 420 # 260*2
        self.sizer_w= 10
        self.sizer_h= 10
        super(Msgbox, self).__init__(parent, title=title, 
            size=(self.width, self.height), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.fname  = 'Jane'
        self.lname  = 'Doe'
        self.age    = 'unknown'
        self.gender = 'unknown' 
        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):
      
        self.panel = wx.Panel(self)
        
        sizer = wx.GridBagSizer(self.sizer_w, self.sizer_h)

        line = wx.StaticLine(self.panel)
        sizer.Add(line, pos=(1, 0), span=(0, int(self.width/self.sizer_w)), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)
        # Name
        text1 = wx.StaticText(self.panel, label="First Name", style = wx.ALIGN_CENTRE_HORIZONTAL)
        text1.SetFont(self.font)
        sizer.Add(text1, pos=(2, 0), span=(0,0) , flag=wx.LEFT, border=20)

        self.tc1 = wx.TextCtrl(self.panel)
        sizer.Add(self.tc1, pos=(2, 1), flag=wx.EXPAND)

        text2 = wx.StaticText(self.panel, label="Last Name", style = wx.ALIGN_CENTRE_HORIZONTAL)
        text2.SetFont(self.font)
        sizer.Add(text2, pos=(2, 2), span=(0,0), flag=wx.LEFT)

        self.tc2 = wx.TextCtrl(self.panel)
        sizer.Add(self.tc2, pos=(2, 3), span=(0,1), flag=wx.EXPAND)

        # Age
        text3 = wx.StaticText(self.panel, label="Age")
        text3.SetFont(self.font)
        sizer.Add(text3, pos=(3, 0), span=(0,0), flag=wx.LEFT, border=20)

        self.tc3 = wx.TextCtrl(self.panel)
        sizer.Add(self.tc3, pos=(3, 1), span=(0, 0), flag=wx.EXPAND)

        sb = wx.StaticBox(self.panel, label="Please Select Your Gender")
        sb.SetFont(self.font)
        self.rb_female = wx.RadioButton(self.panel, label="Female")
        self.rb_female.SetFont(self.font)
        self.rb_male   = wx.RadioButton(self.panel, label="Male")
        self.rb_male.SetFont(self.font)
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        boxsizer.Add(self.rb_female, 
            flag=wx.Center|wx.TOP, border=5)
        boxsizer.Add(self.rb_male,
            flag=wx.Center, border=5)
        sizer.Add(boxsizer, pos=(4, 0), span=(0, 4), 
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)

        button1 = wx.Button(self.panel, size=(200,50), label="Ok")
        sizer.Add(button1, pos=(5, 0), span=(0, 0), flag=wx.LEFT, border=10)
        button1.SetFont(self.font_button)
        button1.Bind(wx.EVT_BUTTON, self.ok)

        button2 = wx.Button(self.panel, size=(200,50), label="Cancel")
        sizer.Add(button2, pos=(5, 3), span=(0, 0), 
            flag=wx.RIGHT, border=5)
        button2.SetFont(self.font_button)
        button2.Bind(wx.EVT_BUTTON, self.cancel)

        sizer.AddGrowableCol(1)
        
        self.panel.SetSizer(sizer)
        # self.panel.SetBackgroundColour((170, 0, 255))

    def ok(self, event):
        self.fname = self.tc1.GetValue()
        self.lname = self.tc2.GetValue()
        self.name = '%s %s' %(self.fname.lower(), self.lname.lower())
        try:
            self.age = int(self.tc3.GetValue())
        except:
            self.age = self.tc3.GetValue()
        if self.rb_female.GetValue():
            self.gender = 'female'
        elif self.rb_male.GetValue():
            self.gender = 'male'
        error = ''
        error_flag = False
        if len(self.lname) == 0 or len(self.fname) == 0:
            error = 'please enter your name\n'
            error_flag = True
        if self.age != '':
            if type(self.age) == int:
                if 0 < self.age < 150:
                    pass
                else:
                    error = 'age out of range\n'
                    error_flag = True
            elif self.age != 'unknown' and type(self.age) != int:
                error = 'age should be an integer\n'
                error_flag = True
        else:
            error = 'please enter your age\n'
            error_flag = True

        if (not self.rb_female.GetValue()) and (not self.rb_male.GetValue()) :
            error += 'please choose your gender'
            error_flag = True
        if error_flag:
            dlg = wx.MessageDialog(self.panel, error,'', wx.YES_NO | wx.ICON_ERROR)
            result = dlg.ShowModal() == wx.ID_YES
            dlg.Destroy()          
        else:
            message = 'Is the following infomation correct?\nName: %s\nAge: %s\nGender: %s' %(self.fname+' '+self.lname, self.age, self.gender)
            dlg = wx.MessageDialog(self.panel, message,'Double check the infomation', wx.YES_NO | wx.ICON_INFORMATION)
            result = dlg.ShowModal() == wx.ID_YES
            if result:
                dlg.Destroy()
                self.Destroy()
            else:
                dlg.Destroy()

    def cancel(self, event):
        self.fname = 'Jane'
        self.lname = 'Doe'
        self.name = '%s %s' %(self.fname.lower(), self.lname.lower())
        self.age = 'unknown'
        self.gender = 'unknown'
        message = 'Do you want to use following information?\nName: %s\nAge: %s\nGender: %s' %(self.fname+' '+self.lname, self.age, self.gender)
        dlg = wx.MessageDialog(self.panel, message,'Double check the infomation', wx.YES_NO | wx.ICON_INFORMATION)
        result = dlg.ShowModal() == wx.ID_YES
        if result:
            dlg.Destroy()
            self.Destroy()
        else:
            dlg.Destroy()
        self.fname = ''
        self.lname = ''
        self.tc1.SetValue('')
        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.rb_female.SetValue(False)
        self.rb_male.SetValue(False)

        

# if __name__ == '__main__':
#     app = wx.App()
#     ex = Msgbox(None, title="Welcome")
#     app.MainLoop()

