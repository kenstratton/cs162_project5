import tkinter as tk
import random as rn

# W = Width, H = Height, X/Y = X/Y coords, S = Space
# C = Color, T = Vertex coord, LEN = Length, L = Limit
WINDOW_W = 700
WINDOW_H = 550
CANVAS_W = WINDOW_W*0.8
CANVAS_H = WINDOW_H*0.83
CANVAS_X = (WINDOW_W-CANVAS_W)/2.15
CANVAS_Y = (WINDOW_H-CANVAS_H)/1.25
RECT_W = 45
RECT_H = 30
RECT_S = 8
LOW_C = "blue"
MID_C = "green2"
HIGH_C = "red"
CNTLR_W = 25
CNTLR_H = 10
METER_T = 50
METER_LEN = 100
SPEED = 1500
SPEED_L = 1000
SPEED_S = 2000

# Id of an ongoing after method of Tkinter
AFTER_ID = None

# A list of 100 int values in ascending order
VALUES = []
for i in range(100):
    if i == 0:
        VALUES.append(rn.randint(1, 10))
    else:
        VALUES.append(VALUES[i-1] + rn.randint(1,10))


# [CLASS] Provides manipulation of anumation speed of a search process in Canvas
class SpeedController:
    def __init__(self, canvas):
        self.canvas = canvas

        # Y of a mouse cursor and a controller
        self.mouse_y = None
        self.cntlr_y = METER_T + (SPEED-SPEED_L)/SPEED_S*METER_LEN

        # Draws a speed meter
        for i in range(2):
            txt_y = METER_T-CNTLR_H if i==0 else METER_T+METER_LEN+20
            txt = "Fast" if i==0 else "Slow"
            canvas.create_text(CANVAS_W-22, txt_y, text=txt, font=("",13), fill="black")
        canvas.create_line(
            CANVAS_W-10-CNTLR_W/2,
            METER_T+CNTLR_H/2,
            CANVAS_W-10-CNTLR_W/2,
            METER_T+METER_LEN+CNTLR_H/2,
            fill="black"
        )
        # Draws a speed controller
        canvas.create_rectangle(
            CANVAS_W-10-CNTLR_W,
            self.cntlr_y,
            CANVAS_W-10,
            self.cntlr_y+CNTLR_H,
            width=1,
            tag="cntlr_bar",
            fill="orange",
            outline="black"
        )

        # Event handlers for clicking, moving, and releasing a controller
        canvas.tag_bind("cntlr_bar", "<Button-1>", self.cntlr_click)
        canvas.tag_bind("cntlr_bar", "<B1-Motion>", self.cntlr_move)
        canvas.tag_bind("cntlr_bar", "<ButtonRelease-1>", self.cntlr_stop)

    # Gets Y of a mouse cursor
    def cntlr_click(self, evnt):
        self.mouse_y = evnt.y_root

    # Moves Y of a controller the same distance of a moved cursor
    def cntlr_move(self, evnt):
        dst = evnt.y_root - self.mouse_y
        new_pos = self.cntlr_y+dst
        # Speed adjustment works when the moved Y of a controller meets a meter scale
        if 0 <= new_pos-METER_T <= METER_LEN:
            self.canvas.moveto("cntlr_bar", CANVAS_W-35, new_pos)
            self.change_animation_speed(new_pos)

    # Initializes Y of a cursor and resets Y of a controller (instance properties)
    def cntlr_stop(self, evnt):
        self.mouse_y = None
        y = self.canvas.bbox("cntlr_bar")
        self.cntlr_y = y[1]

    # Adjusts the SPEED variable based on the chaged Y of a controller
    def change_animation_speed(self, change):
        global SPEED
        change_rate = float((change-METER_T)/METER_LEN)
        SPEED = int(SPEED_L + (SPEED_S*change_rate))


# [CLASS] Draws requiremets to illustrate a searching process in a Canvas field
class Canvas(tk.Canvas):
    def __init__(self, root):
        super().__init__(
            root, width=CANVAS_W, height=CANVAS_H, bg="white"
        )
        self.place(x=CANVAS_X, y=CANVAS_Y)
        self.root = root
        self.cntlr = SpeedController(self)
        self.rect_ids = [] # Ids of rectangles of 100 int values
        self.num_ids = []  # Ids of texts of 100 int values

        # Texts of low, mid, high to be highlighted in a searching process
        for i in range(3):
            if i == 0:
                tag = "low"
                color = LOW_C
            elif i == 1:
                tag = "mid"
                color = MID_C
            else:
                tag = "high"
                color = HIGH_C
            self.create_text(
                CANVAS_W*(0.3+0.2*i),
                (CANVAS_H-(RECT_H+RECT_S)*10)/2.4,
                text=f"{tag.upper()} : ",
                font=("", 16),
                fill=color,
                tag=f"txt_{tag}"
            )

        # Rectangles and texts for 100 init values
        for i in range(10):
            for ii in range(10):
                self.rect_ids.append(self.create_rectangle(
                    (CANVAS_W-RECT_W*10)/2+RECT_W*ii,
                    (CANVAS_H-(RECT_H+RECT_S)*10)/1.2+(RECT_S+RECT_H)*i,
                    (CANVAS_W-RECT_W*10)/2+RECT_W*(ii+1),
                    (CANVAS_H-(RECT_H+RECT_S)*10)/1.2+(RECT_S+RECT_H)*i+RECT_H,
                    width=1,
                    outline="black",
                    tag="rect"
                ))
                self.num_ids.append(self.create_text(
                    (CANVAS_W-450)/2+RECT_W*ii+RECT_W/1.95,
                    (CANVAS_H-(RECT_H+RECT_S)*10)/1.2+(RECT_S+RECT_H)*i+RECT_H/2,
                    text=f"{VALUES[i*10+ii]}",
                    font=("",14),
                    fill="black",
                    disabledfill = "#dddddd",
                    tag = f"num_{i*10+ii}"
                ))

    # Updates numbers that low, mid, high texts highlight
    def change_pos_num(self, tag, num):
        self.itemconfig(f"txt_{tag}", text=f"{tag.upper()} : {num}")

    # Changes the color of a rectangle (no arguments = all rectangles turn in white )
    def change_rect_color(self, tag_or_id="rect", color="white"):
        self.itemconfig(tag_or_id, fill=color)

    # Changes the states of int value texts (disabled = it turns in non-candidate color)
    def change_num_state(self, low=None, high=None):
        if low is None:
            for i in range(100):
                self.itemconfig(self.num_ids[i], state="normal")
        else:
            for i in range(low, high):
                self.itemconfig(self.num_ids[i], state="disabled")

    """ Updates values and colors of rectangles and texts in a Canvas field
    based on indexes of 100 values identified as low, mid, and high
    (no arguments = initializes the all elements)"""
    def update_search_board(self, low=None, mid=None, high=None):
        val_l = VALUES[low] if low != None else ""
        val_m = VALUES[mid] if mid != None else ""
        val_h = VALUES[high] if high != None else ""
        self.change_pos_num("low", val_l)
        self.change_pos_num("mid", val_m)
        self.change_pos_num("high", val_h)
        self.change_rect_color()

        if low != None:
            self.change_rect_color(self.rect_ids[low], LOW_C)
            self.change_rect_color(self.rect_ids[high], HIGH_C)
            self.change_rect_color(self.rect_ids[mid], MID_C)

    def search_animation(self, rslt, trgt):
            if self.root.bi_search.records:
                rec = self.root.bi_search.records[0]

                 # Clarifies a updated scale of non-candidate vlaues in a Canvas field
                if rec["state"] == "UP":
                    self.change_num_state(0, rec["low"])
                else:
                    self.change_num_state(rec["high"]+1, 100)

                self.update_search_board(rec["low"], rec["mid"], rec["high"])
                self.root.bi_search.records.pop(0)

                # Back to the begining with updated arguments after adjustable delay
                global AFTER_ID
                AFTER_ID = self.root.after(SPEED, self.search_animation, rslt, trgt)
            else:
                self.root.lbl_rslt.config(text=f"Result : {rslt}")
                self.root.process_end(trgt)

# [CLASS] Searching process
"""Evaluates the relationship of the target value 
and the value at the middle of a 100-value list,
and decide completion or searching again in candidates
narrowed to half greater or smaller than the mid-located value"""
class BinarySearch:
    def __init__(self, root):
        self.root = root
        self.canvas = root.canvas
        self.records = []

    def search(self, trgt, low, high):
        self.records.clear()
        state = None

        # Evaluates if all candidates have been processed already
        while low <= high:
            mid = (low + high)//2
            self.records.append(
                {"low":low, "mid":mid, "high":high, "state":state}
            )
            if trgt == VALUES[mid]:
                return True
            else:
                if trgt > VALUES[mid]:
                    low = mid + 1
                    state = "UP"
                elif trgt < VALUES[mid]:
                    high = mid - 1
                    state = "DOWN"
        return False


# [CLASS] Set up GUI display and principal objects
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg="orange")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.title("Binary Search")

        self.canvas = Canvas(self)
        self.bi_search = BinarySearch(self)

        # Text box and submit Button for user input
        self.txt_box = tk.Entry(self, width=6, bg="white", fg="black")
        self.txt_box.place(x=WINDOW_W*0.35, y=20)
        self.btn = tk.Button(self, text="->", bg="white", command=self.process)
        self.btn.place(x=WINDOW_W*0.46, y=20)

        # Labels for the result and exceptions
        self.lbl_rslt = tk.Label(self, text="Result : ", font=("", 19), bg="white", fg="black")
        self.lbl_rslt.place(x=WINDOW_W*0.55, y=20)
        self.lbl_e = tk.Label(self, text = "", fg="red", bg="orange")
        self.lbl_e.place(x=WINDOW_W*0.35, y=50)

    # Get user input and start processing int validation and a search
    def process(self):
        self.lbl_rslt.config(text="Result : ")
        inpt = self.txt_box.get()
        if self.is_int(inpt):
            if AFTER_ID is not None:  # Cancels ongoing search
                self.after_cancel(AFTER_ID)
            self.canvas.change_num_state()
            rslt = self.bi_search.search(int(inpt), 0, len(VALUES)-1)
            self.canvas.search_animation(rslt, inpt)
        # Without no ongoing search, initializes a Canvas field for wrong input
        elif AFTER_ID is None:
            self.canvas.change_num_state()
            self.canvas.update_search_board()

    # Reset the id of after method and the input-output area for search
    def process_end(self, txt=""):
        global AFTER_ID
        AFTER_ID = None
        self.txt_box.delete(0, tk.END)
        self.txt_box.insert(0, txt)
        self.lbl_e.config(text="")

    # Evaluate if the input can become int, and show the warning if not
    def is_int(self, inpt):
        try:
            int(inpt)
            self.lbl_e.config(text="")
            return True
        except ValueError:
            self.lbl_e.config(text="*Please input an integral number.")
            return False


# [FUNCTION] Create the GUI application
def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()