import customtkinter as ctk
from draw_surface import DrawSurface
from tool_panel import ToolPanel
from settings import *

class App(ctk.CTk):
    def __init__(self):
        # Create window
        super().__init__()
        
        # Window settings
        self.geometry('800x600')
        self.title('Whiteboard')
        self.iconbitmap(resource_path('paint_ico.ico'))
        ctk.set_appearance_mode('light')
        
        # Data
        self.color_string = ctk.StringVar(value='000')
        self.brush_float = ctk.DoubleVar(value=0.1) # 0.1 <-> 1
        self.erase_bool = ctk.BooleanVar(value=False)
        
        # Widgets
        self.draw_surface = DrawSurface(self, self.color_string, self.brush_float, self.erase_bool)
        self.tool_panel = ToolPanel(self, self.brush_float, self.color_string, self.draw_surface.undo, self.draw_surface.redo, self.draw_surface.save, self.draw_surface.open, self.clear_canvas, self.erase_bool)
        
        # Undo/Redo events
        self.bind('<Control-z>', self.draw_surface.undo)
        self.bind('<Control-Z>', self.draw_surface.redo)
        
        # Save events
        self.bind('<Control-s>', lambda event: self.draw_surface.save(event, self.tool_panel))
        
        # Open events
        self.bind('<Control-o>', lambda event: self.draw_surface.open(event, self.tool_panel))
        
        # Mousewheel event
        self.bind('<MouseWheel>', self.adjust_brush_size)
        
        # Color picker event
        self.bind('<Tab>', self.color_pick)
        
        # Init window
        self.mainloop()
        
    def color_pick(self, event):
        # Find all drawn items at the mouse cursor on the canvas
        items = self.draw_surface.find_overlapping(event.x, event.y, event.x, event.y)
        
        # If items were found at the location
        if items:
            # Get the id of the topmost item
            item_id = items[-1]
            
            # Retrieve the color of the item
            item_color = self.draw_surface.itemcget(item_id, 'fill')
            
            # Set the color string to the color found, so long as its not the canvas color
            if item_color != '#f5f6ff':
                self.color_string.set(item_color[1:])
        else:
            print(f'No color at ({event.x}, {event.y})')
        
    def adjust_brush_size(self, event):
        new_brush_size = self.brush_float.get() + 0.05 * event.delta/120
        new_brush_size = min(1, max(0.1, new_brush_size))
        self.brush_float.set(new_brush_size)
        
    def clear_canvas(self):
        self.draw_surface.delete('all')
    
if __name__ == '__main__':
    loadfont(resource_path('PixulBrush.ttf'))
    
    App()