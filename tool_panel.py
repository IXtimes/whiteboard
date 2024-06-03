import customtkinter as ctk
from tkinter import Canvas
from tkinter import Menu
from settings import *
from PIL import Image

class ToolPanel(ctk.CTkToplevel):
    def __init__(self, parent, brush_float, color_string, undo, redo, save, open, clear_canvas, erase_bool):
        # configure toolbox window
        super().__init__()
        self.geometry('200x400')
        self.title('Tools')
        self.resizable(False, False)
        self.after(200, lambda:self.iconbitmap(resource_path('toolbox_ico.ico'))) # alternative to getting the icon to work for this window
        self.attributes('-topmost', True) # keep the window always on top
        self.protocol('WM_DELETE_WINDOW', self.close_app) # close entire program when closed
        self.parent = parent
        
        # traces
        self.brush_float = brush_float
        self.brush_float.trace_add('write', self.update_point_label)
        
        # binds
        self.save = save
        self.open = open
        self.bind('<Control-s>', self.save_canvas)
        self.bind('<Control-o>', self.open_canvas)
        
        # layout
        self.columnconfigure((0,1,2), weight=1, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure(1, weight=3, uniform='a')
        self.rowconfigure((2,3,4), weight=1, uniform='a')
        
        # widgets
        ColorSliderPanel(self, color_string)
        BrushSizeSlider(self, self.brush_float)
        ColorPanel(self, color_string)
        BrushPreview(self, color_string, brush_float, erase_bool)
        Button(self, image_path=resource_path('undo.png'), row=0, col=2, func=undo)
        Button(self, image_path=resource_path('clear.png'), row=0, col=1, func=clear_canvas)
        Button(self, image_path=resource_path('save.png'), row=1, col=0, func=self.save_canvas)
        Button(self, image_path=resource_path('open.png'), row=1, col=1, func=self.open_canvas)
        Button(self, image_path=resource_path('redo.png'), row=1, col=2, func=redo)
        ctk.CTkLabel(self, textvariable=color_string, font=ctk.CTkFont(family='PixulBrush', size=12), text_color='#deddde', fg_color='transparent').place(anchor='ne', relx=0.99, rely=0)
        #ctk.CTkLabel(self, text='#', font=ctk.CTkFont(family='PixulBrush', size=12), text_color='#deddde', fg_color='transparent').place(anchor='ne', relx=0.815, rely=0)
        self.point_label = ctk.CTkLabel(self, text='', fg_color='#deddde', font=ctk.CTkFont(family='PixulBrush', size=9), text_color='#333941', corner_radius=5)
        self.point_label.grid(row=3, column = 0, sticky='snew', padx=5, pady=5)
        self.update_point_label()
        
    def save_canvas(self, event = None):
        self.iconify()
        self.save()
        self.deiconify()
        
    def open_canvas(self, event = None):
        self.iconify()
        self.open()
        self.deiconify()
        
    def close_app(self):
        self.parent.quit()
        
    def update_point_label(self, *args):
        self.point_label.configure(text=f'{round(self.brush_float.get() * 50, 1)}px')
        
class BrushPreview(Canvas):
    def __init__(self, parent, color_string, brush_float, erase_bool):
        super().__init__(master=parent, background=BRUSH_PREVIEW_BG, bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=0, column=1, columnspan=2, sticky='snew')
        
        # data
        self.color_string = color_string
        self.brush_float = brush_float
        self.erase_bool = erase_bool
        
        # canvas setup
        self.x = 0
        self.y = 0
        self.max_length = 0
        
        # traces
        self.color_string.trace_add('write', self.update)
        self.brush_float.trace_add('write', self.update)
        self.erase_bool.trace_add('write', self.update)
        
        # configure
        self.bind('<Configure>', self.setup)
    
    def setup(self, event):
        self.x = event.width / 2
        self.y = event.height / 2
        self.max_length = (event.height / 2) * 0.8
        self.update()
        
    def update(self, *args):
        self.delete('all')
        current_radius = self.max_length * self.brush_float.get()
        color = f'#{self.color_string.get()}' if not self.erase_bool.get() else '#ebebeb'
        self.create_oval(self.x - current_radius, self.y - current_radius, self.x + current_radius, self.y + current_radius , fill=color, outline=color if not self.erase_bool.get() else 'black', dash=4)
        
class ColorSliderPanel(ctk.CTkFrame):
    def __init__(self, parent, color_string):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky='snew', padx=5, pady=5)
        
        # data
        self.color_string = color_string
        self.r_int = ctk.IntVar(value=self.color_string.get()[0])
        self.g_int = ctk.IntVar(value=self.color_string.get()[1])
        self.b_int = ctk.IntVar(value=self.color_string.get()[2])
        
        # traces
        self.color_string.trace_add('write', self.set_color)
        
        # layout
        self.rowconfigure((0,1,2), weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')
        
        # widgets
        ctk.CTkSlider(self, command = lambda value: self.set_single_color('r', value), button_color=SLIDER_RED, button_hover_color=SLIDER_RED, from_=0, to=15, number_of_steps=16, variable=self.r_int).grid(row=0, column=0, padx = 2)
        ctk.CTkSlider(self, command = lambda value: self.set_single_color('g', value), button_color=SLIDER_GREEN, button_hover_color=SLIDER_GREEN, from_=0, to=15, number_of_steps=16, variable=self.g_int).grid(row=1, column=0, padx = 2)
        ctk.CTkSlider(self, command = lambda value: self.set_single_color('b', value), button_color=SLIDER_BLUE, button_hover_color=SLIDER_BLUE, from_=0, to=15, number_of_steps=16, variable=self.b_int).grid(row=2, column=0, padx = 2)
        
    def set_single_color(self, color, value):
        # get the current color as a list
        current_color_list = list(self.color_string.get())
        
        # set the specific channel specified to the value specified, and push the new value to the color string
        match color:
            case 'r': current_color_list[0] = COLOR_RANGE[int(value)]
            case 'g': current_color_list[1] = COLOR_RANGE[int(value)]
            case 'b': current_color_list[2] = COLOR_RANGE[int(value)]
        self.color_string.set(f'{"".join(current_color_list)}')
        
    def set_color(self, *args):
        self.r_int.set(COLOR_RANGE.index(self.color_string.get()[0]))
        self.g_int.set(COLOR_RANGE.index(self.color_string.get()[1]))
        self.b_int.set(COLOR_RANGE.index(self.color_string.get()[2]))
        
class BrushSizeSlider(ctk.CTkFrame):
    def __init__(self, parent, brush_float):
        super().__init__(parent)
        self.grid(row=2, column=0, columnspan=3, sticky='snew', padx=5, pady=5)
        # slider
        ctk.CTkSlider(self, variable=brush_float, from_=0.1, to=1).pack(fill='x', expand=True, padx=5, pady=5)
        
class ColorPanel(ctk.CTkFrame):
    def __init__(self, parent, color_string):
        super().__init__(parent, fg_color='transparent')
        self.grid(row=1, column=0, columnspan=3, sticky='snew', pady = 5, padx = 5)
        self.color_string = color_string
        
        # layout
        self.rowconfigure(tuple(range(COLOR_ROWS)), weight=1, uniform='b')
        self.columnconfigure(tuple(range(COLOR_COLS)), weight=1, uniform='b')
        
        # widgets
        for row in range(COLOR_ROWS):
            for col in range(COLOR_COLS):
                color = COLORS[row][col]
                ColorFieldButton(self, row, col, color)
                
    def pick_color(self, color):
        self.color_string.set(color)
                
class ColorFieldButton(ctk.CTkButton):
    def __init__(self, parent, row, col, color):
        # generate the hover color
        hover_color = ''
        for hex in color:
            hover_color += COLOR_RANGE[max(COLOR_RANGE.index(hex) - 2, 0)]   
        
        # construct and place button 
        super().__init__(parent, fg_color='#' + color, hover_color='#' + hover_color, text='', corner_radius=1, command = lambda:parent.pick_color(color))
        self.grid(row=row, column=col, sticky='snew', padx=0.8, pady=0.8)
        
        # data
        self.color = color
        
class Button(ctk.CTkButton):
    def __init__(self, parent, image_path, row, col, func):
        image = ctk.CTkImage(light_image=Image.open(image_path).resize((48,48), Image.BOX), dark_image=Image.open(image_path).resize((48,48), Image.BOX))
        super().__init__(parent, text='', image=image, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, command=func)
        self.grid(row=row + 3, column=col, sticky='snew', padx=5, pady=5)