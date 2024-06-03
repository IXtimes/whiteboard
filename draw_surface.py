from tkinter import Canvas, filedialog
from settings import *
from PIL import Image, ImageTk, ImageGrab

class DrawSurface(Canvas):
    def __init__(self, parent, color_string, brush_float, erase_bool):
        # initalization
        super().__init__(master=parent,background=CANVS_BG, bd=0, highlightthickness=0, relief='ridge')
        self.pack(expand=True, fill='both')
        
        # data
        self.color_string = color_string
        self.brush_float = brush_float
        self.erase_bool = erase_bool
        self.allow_draw = False
        
        # start position
        self.old_x = None
        self.old_y = None
        self.opened_image = None
        
        # history and future
        self.history = []
        self.detailed_history = []
        self.future = []
        
        # input
        self.bind('<Motion>', self.draw)
        self.bind('<Button-1>', lambda event:self.activate_draw(event, False))
        self.bind('<Button-3>', lambda event:self.activate_draw(event, True))
        self.bind('<ButtonRelease>', self.deactivate_draw)
        
    def draw(self, event):
        # check if drawing is allowed
        if self.allow_draw:
            # only draw a line if we have legacy points
            if self.old_x and self.old_y:
                # draw line between current position and legacy
                self.create_brush_line((event.x, event.y), (self.old_x, self.old_y))
            
            # update legacy
            self.old_x = event.x
            self.old_y = event.y
    
    def undo(self, event = None):
        # check if there is history left
        if len(self.history) > 0:
            # get the last drawn stroke in the history
            last = self.history.pop()
            
            # get the last drawn stroke from the detailed history
            detailed_last = self.detailed_history.pop()
            
            # append the detailed history to the future to redo
            self.future.append(detailed_last)
            
            # iterate and delete the contents of the stroke intercepted
            for line in last:
                self.delete(line)
                
    def redo(self, event = None):
        # check if there is a future left
        if len(self.future) > 0:
            # get the last drawn stroke in the future
            next = self.future.pop()
            
            # push immediately to the detailed history
            self.detailed_history.append(next)
            
            # make a new stroke object
            stroke = []
            
            # iterate and draw the stroke in its entirety,
            for line in next:
                stroke.append(self.create_line(line[0], line[1], fill=line[2], width=line[3], capstyle='round'))
            
            # append it to the history to undo
            self.history.append(stroke)
                
    def save(self, event = None, tool_panel = None):
        # if a toolpanel is specified, hide it
        if tool_panel:
            tool_panel.iconify()
        
        # get the bounding box of the canvas
        bbox = self.winfo_rootx(), self.winfo_rooty(), self.winfo_rootx() + self.winfo_width(), self.winfo_rooty() + self.winfo_height()
        
        # get the file path as a dialog
        try:
            filename = filedialog.asksaveasfile(initialfile='untitled-whiteboard.png', mode='w', defaultextension='.png', filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]).name # File dialog to get a file path to save at
        except:
            filename = ''

        # check if it exists
        if filename:
            # grab the screen area that the image is displayed
            img = ImageGrab.grab(bbox)
            
            # save the image at the filepath
            img.save(filename)
            
        # if a toolpanel is specified, show it
        if tool_panel:
            tool_panel.deiconify()
        
    def open(self, event = None, tool_panel = None):
        # if a toolpanel is specified, hide it
        if tool_panel:
            tool_panel.iconify()
            
        # get the file path of the image to open
        filename = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")])
        
        # check if it exists
        if filename:
            # open and convert to an imageTK
            img = Image.open(filename)
            self.opened_image = ImageTk.PhotoImage(img)
            
            # clear canvas and draw the image
            self.delete('all')
            self.create_image(0, 0, image=self.opened_image, anchor='nw')
            
            # clear history and future
            self.history.clear()
            self.future.clear()
            
        # if a toolpanel is specified, show it
        if tool_panel:
            tool_panel.deiconify()
    
    def create_brush_line(self, start, end):
        # set the brush size of the line from the float passed
        brush_size = self.brush_float.get() * 50
        
        # get the current color based on the erase bool
        color = f'#{self.color_string.get()}' if not self.erase_bool.get() else f'{CANVS_BG}'
        
        # draw the line in the canvas, store the result in the current stroke for undo purposes
        self.current_stroke.append(self.create_line(start, end, fill=color, width=brush_size, capstyle='round'))
        
        # add a detailed footprint of this line
        self.current_detailed_stroke.append((start, end, color, brush_size))
    
    def activate_draw(self, event, erase):
        # flag drawing to be allowed
        self.allow_draw = True
        
        # create a new list to store the current stroke, clear future
        self.current_stroke = []
        self.current_detailed_stroke = []
        self.future = []
        
        # toggle the eraser if applicable
        self.erase_bool.set(erase)
        
        # create an inital dot when the mouse is clicked
        self.create_brush_line((event.x, event.y), (event.x + 1, event.y + 1))
    
    def deactivate_draw(self, event):
        # flag drawing to not be allowed
        self.allow_draw = False
        
        # save the current stroke to the history(s)
        self.history.append(self.current_stroke)
        self.detailed_history.append(self.current_detailed_stroke)
        
        # toggle the eraser off
        self.erase_bool.set(False)
        
        # remove legacy points
        self.old_x = None
        self.old_y = None