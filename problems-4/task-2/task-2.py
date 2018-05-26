import copy
from threading import Timer
from tkinter import *
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox


class Field(object): 

    _shifts = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[False for i in range(self.width)] for j in range(self.height)]

    def count_neighbours(self, x_pos, y_pos):
        neighbours = 0
        for shift in Field._shifts:
            if self.cells[(y_pos + shift[1]) % self.height][(x_pos + shift[0]) % self.width]:
                neighbours += 1
        return neighbours

    def make_step(self):
        new_cell_states = copy.deepcopy(self.cells)
        for j in range(self.height):
            for i in range(self.width):
                neighbours = self.count_neighbours(i, j)
                if self.cells[j][i]:
                    if neighbours < 2 or neighbours > 3:
                        new_cell_states[j][i] = False
                    else:
                        new_cell_states[j][i] = True
                else:
                    if neighbours == 3:
                        new_cell_states[j][i] = True
                    else:
                        new_cell_states[j][i] = False
        self.cells = copy.deepcopy(new_cell_states)


class Application(Frame):
    def __init__(self, root=None):
        super().__init__(root)

        self.root = root
        self.timer = None
        self.is_running = BooleanVar(value=False)
        self._interval = DoubleVar()

        self.but_open = Button(self, text="Open file", command=self.open_file)
        self.but_step = Button(self, text="Make step", command=self.make_step)
        self.but_clear = Button(self, text="Clear", command=self.clear)
        self.but_run = Checkbutton(self, text="Run", command=self.run_game,
                                   variable=self.is_running)
        self.but_timer_x1 = Radiobutton(self, text="x1", variable=self._interval, value=2)
        self.but_timer_x2 = Radiobutton(self, text="x2", variable=self._interval, value=1)
        self.but_timer_x4 = Radiobutton(self, text="x4", variable=self._interval, value=0.5)
        self.canvas = Canvas(root, width=601, height=601,
                             bg="white")
        self.canvas.bind('<Button-1>', self.mouse_clicked)
        self.root.bind("<<Run>>", self.run_game)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.scrollbar_hor = Scrollbar(self, orient="horizontal")
        self.scrollbar_vert = Scrollbar(self, orient="vertical")
        self.canvas.config(xscrollcommand=self.scrollbar_hor.set)
        self.canvas.config(yscrollcommand=self.scrollbar_vert.set)
        self.scrollbar_hor.config(command=self.canvas.xview)
        self.scrollbar_vert.config(command=self.canvas.yview)
        self.scrollbar_hor.pack(side="right", fill="y")
        self.scrollbar_vert.pack(side="bottom")

        self.pack()
        self.but_open.pack(side="left")
        self.but_step.pack(side="left")
        self.but_clear.pack(side="left")
        self.but_run.pack(side="left")
        self.but_timer_x1.pack(side="left")
        self.but_timer_x2.pack(side="left")
        self.but_timer_x4.pack(side="left")
        self.but_timer_x1.select()
        self.canvas.pack(side="top")

        self.field = Field(30, 30)

        self.root.update()
        self.cell_width = self.canvas.winfo_width() // self.field.width
        self.cell_height = self.canvas.winfo_height() // self.field.height
        self.cell_width = 30
        self.cell_height = 30
        self.draw_field()

    def mouse_clicked(self, event):
        self.field.cells[((event.y-1) // self.cell_height) % self.field.height]\
            [((event.x-1) // self.cell_width) % self.field.width] = \
            not self.field.cells[((event.y-1) // self.cell_height) % self.field.height]\
            [((event.x-1) // self.cell_width) % self.field.width]
        self.draw_field()

    def draw_field(self):
        self.canvas.delete(ALL)
        for j in range(self.field.height):
            for i in range(self.field.width):
                if self.field.cells[j][i]:
                    color = 'pink'
                else:
                    color = 'white'
                self.canvas.create_rectangle(1+i*self.cell_width, 1+j*self.cell_height,
                                             1+(i+1)*self.cell_width, 1+(j+1)*self.cell_height,
                                             fill=color, outline='black', width=1)

    def clear(self):
        for j in range(self.field.height):
            for i in range(self.field.width):
                self.field.cells[j][i] = False
        self.draw_field()

    def make_step(self):
        self.field.make_step()
        self.draw_field()
        # if self.timer:
        #   self.run_game()

    def run_game(self, event=None):
        if self.is_running.get():
            self.timer = Timer(self._interval.get(), self.root.event_generate, ["<<Run>>"])
            self.timer.start()
        else:
            self.timer.cancel()
        self.make_step()

    def open_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.clear()
            self.parse_file(filename)
            self.draw_field()

    def handle_parse_error(self, error):
        self.clear()
        messagebox.showerror("Error", error)

    def parse_file(self, filename):
        with open(filename, 'r') as fin:
            for line in fin:
                args = line.replace('\n', '').split(' ')
                if len(args) != 2:
                    self.handle_parse_error("Wrong file ")
                else:
                    x_pos = int(args[0])
                    y_pos = int(args[1])
                    if x_pos < 0 or x_pos > self.field.width or \
                            y_pos < 0 or y_pos > self.field.height:
                        self.handle_parse_error("Wrong coordinates")
                        return
                    self.field.cells[y_pos][x_pos] = True

    def on_close(self):
        self.is_running = False
        if self.timer:
            self.timer.cancel()
        self.root.destroy()

master = Tk()
app = Application(master)
app.mainloop()
