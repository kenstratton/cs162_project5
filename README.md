# Project 5 (Searching)
**Tools :**</br>
・python 3.10.0</br>
・tkinter 8.6.11</br>
・pytest 6.2.5

**Binary Search?**</br>
・prepare a collection of candidate values sorted in ascending order</br>
・Repeat the following steps until presence or absence of the target value is found:
1. See if the target matches the value at the center in a candidate scale between both ends of the collection as a "low" and a "high".</br>
2. If they don't match, evaluate the target is greater or smaller than the mid-located value.</br>
3. If the target is greater, restart from the Step 1 with a new candidate scale which takes the mid-located value plus 1 as a "low" and keeps a "high" as it was.</br>
\* If smaller, the scale takes the mid-located value plus -1 as a "high" and keeps a "low" as it was.

**GUI :**</br>
・The tkinter provides numerous widget classes which help create GUI with thier methods.</br>
・The mainly used widgets for this were Entry, Button, Label, and Canvas.</br>
・The details of how they were used are in explanation for steps of achieving the search system.
![gui_sample](https://user-images.githubusercontent.com/77530003/139821750-4abc40dc-4d18-411d-8fb5-eda76a354de8.gif)

## Each steps to achieve the searching program
### ▼ Create a collection of 100 int values
・Repeat adding a value plus 1~10 more than that previously added.

    # A list-type variable of 100 candidate values in ascending order 
    VALUES = []
    for i in range(100):
        if i == 0:
            VALUES.append(rn.randint(1, 10))
        else:
            VALUES.append(VALUES[i-1] + rn.randint(1,10))

### ▼ Create a GUI to display the collection of int values as rectangles
・Rectangles with value texts are drawn by methods of the Canvas widget.</br>
・Rectangles -> *.create_rectangle()*</br>
・Values(text) -> *.create_text()*</br>
・Prepare the double structure of For loops, and each repeats 10 times.</br>
・Each number text holds a tag that consists of the tens place from the top layer loop and the ones place from the the second layer.

    # class Canvas
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
                tag = "txt_num"
            ))

<img width="400" alt="Screen Shot 2021-11-01 at 23 28 43" src="https://user-images.githubusercontent.com/77530003/139687967-483f5ff1-f749-4267-9697-6a3eaf440118.png">

### ▼ Include a text box in the GUI to allow a user to enter a value to search for
・The Entry widget provides the input space
    
    # class Application 
    self.txt_box = tk.Entry(self, width=6, bg="white", fg="black")
    self.txt_box.place(x=WINDOW_W*0.35, y=20)
    
<img width="250" alt="Screen Shot 2021-11-02 at 0 09 35" src="https://user-images.githubusercontent.com/77530003/139694206-9b38c62c-2c6e-4201-919c-251258b27bec.png">

### ▼ Include a button to start the searching
・The Button widget provides the input space

    # class Application 
    self.btn = tk.Button(self, text="->", bg="white", command=self.process)
    self.btn.place(x=WINDOW_W*0.46, y=20)
    
<img width="250" alt="Screen Shot 2021-11-02 at 0 23 03" src="https://user-images.githubusercontent.com/77530003/139696282-22b639e8-7fa9-4d54-9a66-15319f0647f6.png">

### ▼ Highlight the candidate value at each step of the searching
<img width="400" alt="Screen Shot 2021-11-03 at 1 13 41" src="https://user-images.githubusercontent.com/77530003/139904655-ed504c4b-13da-42d8-82ff-bf0f91297b82.png">
**Animation:**</br>
・After a search has ended, its processing is displayed by the Canvas class with *animation()*.</br>
・Args of *animation()* are a target value and records of a result(True/False) and candidates given by the searching.</br>
・The highlighting process of a candidate scale in *animation()* -> *.update_search_board()*</br>

    # class Canvas
    def animation(self, rslt, trgt):
        if self.root.bi_search.records:
            rec = self.root.bi_search.records[0]

            # Clarifies a updated scale of non-candidate vlaues in a Canvas field
            if rec["state"] == "UP":
                self.change_num_state(0, rec["low"])
            else:
                self.change_num_state(rec["high"]+1, 100)

            self.update_search_board(rec["low"], rec["mid"], rec["high"])
            self.root.bi_search.records.pop(0)

            # Calls itself directory after adjustable delay
            global AFTER_ID
            AFTER_ID = self.root.after(SPEED, self.animation, rslt, trgt)
        else:
            self.root.lbl_rslt.config(text=f"Result : {rslt}")
            self.root.process_end(trgt)

**Records of A Search:**</br>
・BinarySearch().records -> [ { "low":low, "mid":mid, "high":high, state }, {}.. ]</br>
・low, mid, high -> each index of candidate-deciding values in a collection of int value </br>
・state -> UP/DOWN : UP -> a target is greater than a mid value, DOWN -> a target is less than a mid value

**Candidate:**</br>
・Values responsible for ruling a candidate scale are shown above rectangles, and each of them is colored.</br>
・"Low" -> blue, "Mid" -> green, and "High" -> red</br>
・Excecute highlighting a candidate scale -> *.update_search_board()*</br>
・Display the ruling value -> *.change_pos_num()*</br>
・Highlight the rectangle of the ruling value -> *.change_rect_color()*</br>

    # class Canvas
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
            
    # Updates numbers that low, mid, high texts highlight
    def change_pos_num(self, tag, num):
        self.itemconfig(f"txt_{tag}", text=f"{tag.upper()} : {num}")
        
    # Changes the color of a rectangle (no arguments = all rectangles turn in white )
    def change_rect_color(self, tag_or_id="rect", color="white"):
        self.itemconfig(tag_or_id, fill=color)
 
**Non-Candidate:**</br>
・Text of non-candidate values turnes opaque for being disabled.</br>
・Each of value texts has id that is based to find and disable non-candidate values</br>
・Disable or Activate value texts -> *change_num_state()*</br>

    # class Canvas
    # Changes the states of int value texts (disabled = it turns in non-candidate color)
    def change_num_state(self, low=None, high=None):
        if low is None:
            self.itemconfig("txt_num", state="normal")
        else:
            for i in range(low, high):
                self.itemconfig(self.num_ids[i], state="disabled")
 
### ▼ Pause after highlighting the candidate value but before moving on
・Pausing was implemented with *.after()* of tkinter.</br>
・The *animation()* has a pausing point at the end that takes some moment and calls itself again.</br>
・There is a speed-controlling slider in a canvas field.</br>
・Moving the slider changes the SPEED variable which impacts the pausing time length.</br>
・SPEED is updated by the SpeedController class -> *.change_animation_speed()* 
・Formula to update the SPEED by moving the slider: m-tm + s-scl \* (c-p / c-scl)</br>
\* m-tm = Minimum time length, s-scl = Scale of time length, c-p = Controller position, c-scl = Scale of an area controller is movable

    # class Canvas .animation()
    global AFTER_ID             # A variable holds id of after()
    AFTER_ID = self.root.after(SPEED, self.animation, rslt, trgt)
    
    # class SpeedController
    def change_animation_speed(self, change):
        global SPEED
        change_rate = float((change-METER_T)/METER_LEN)   # Equals (c-p / c-scl) in the above formula
        SPEED = int(SPEED_L + (SPEED_S*change_rate))

### ▼ Make it obvious when absence or presence of the target is found
・The result of existence of the target is shown as "Result : True/False" next to a submit button.</br>
・The Label widget displays the result text.</br>
・Alteraton of the text is executed at the end of *animation()*.</br>

    # class Canvas .animation()
    self.root.lbl_rslt.config(text=f"Result : {rslt}")

    # class Application
    self.lbl_rslt = tk.Label(self, text="Result : ", font=("", 19), bg="white", fg="black")
    self.lbl_rslt.place(x=WINDOW_W*0.55, y=20)
<img width="280" alt="Screen Shot 2021-11-03 at 0 54 52" src="https://user-images.githubusercontent.com/77530003/139887703-95a0a7b5-f109-498c-9a86-66438f80e1fe.png">

## Add tests
### ▼ Kinds of tests to verify the functionality of the searching
・It should be necessary to test whether the whole program by user input is proessed in expected order and gives an appropriate outcome.</br>
・A tester would need to prepare some data to get output in a supposed situation.</br>

### ▼ Test for Searching (pytest)
・Required data is set in conftest.py supported by the *.fixture()* decorator.</br>
・Use the pytest-mock plugin to use *mock* objects.</br>
・*Mock* helps alter output of methods for a while and test if interdependent methods or classes can properly work.</br>
・Fake a method for specific tests by *mocker* fixture -> *mocker.patch()* , 1st arg = a method path, 2nd = return_value</br>
・Test whether a mocked method has been called only once -> *.assert_called_once_with()*, 1st arg = a method path, 2nd.. = args of the method

<img width="1069" alt="Screen Shot 2021-11-03 at 0 23 09" src="https://user-images.githubusercontent.com/77530003/139880169-dabfe081-6c41-48bc-be41-8bdfb175c21e.png">
