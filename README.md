# Project 5 (Searching)
**Tools :**</br>
・python 3.10.0</br>
・tkinter 8.6.11</br>
・pytest 6.2.5

**Binary Search?**</br>
\* prepare a collection of candidate values sorted in ascending order</br>
Repeat the following steps until presence or absence of the target value is found:
1. See if the target matches the value at the center position of candidates.</br>
2. If they don't match, evaluate the target is greater or smaller than the mid-located value.</br>
3. If the target is greater, restart from the Step 1 with candidates greater than the mid-located value.</br>
   If smaller, take the opposite candidate scale.

**GUI :**</br>
・The tkinter provides numerous widget classes which help create GUI with thier methods.</br>
・The mainly used widgets for this were Entry, Button, Label, and Canvas.</br>
・The details of how they were used are in explanation for steps of achieving the search system.
<img width="400" alt="Screen Shot 2021-11-01 at 22 58 36" src="https://user-images.githubusercontent.com/77530003/139686406-30f91d73-b0c0-4979-b46d-1b4b7783e8e4.png">

## Each steps to achieve the searching program
### ▼ Create a collection of 100 int values
・Repeat adding a value plus 1~10 more than that previously added.

<img width="600" alt="Screen Shot 2021-11-01 at 23 02 37" src="https://user-images.githubusercontent.com/77530003/139684237-58252c81-99aa-4aa4-bd52-34f164d82574.png">

### ▼ Create a GUI to display the collection of int values as rectangles
・Rectangles with number texts are drawn by methods of the Canvas widget.</br>
・Rectangles -> .create_rectangle()</br>
・Numbers(text) -> .create_text()</br>
・Prepare the double structure of For loops, and each repeats 10 times.</br>
・Each number text holds a tag that consists of the tens place from the top layer loop and the ones place from the the second layer.

<img width="600" alt="Screen Shot 2021-11-01 at 23 26 57" src="https://user-images.githubusercontent.com/77530003/139695592-e816a413-fd2a-4399-a0bc-f3252300d7f8.png">
<img width="400" alt="Screen Shot 2021-11-01 at 23 28 43" src="https://user-images.githubusercontent.com/77530003/139687967-483f5ff1-f749-4267-9697-6a3eaf440118.png">

### ▼ Include a text box in the GUI to allow a user to enter a value to search for
・The Entry widget provides the input space

<img width="250" alt="Screen Shot 2021-11-02 at 0 09 35" src="https://user-images.githubusercontent.com/77530003/139694206-9b38c62c-2c6e-4201-919c-251258b27bec.png">

### ▼ Include a button to start the search process
・The Button widget provides the input space

<img width="250" alt="Screen Shot 2021-11-02 at 0 23 03" src="https://user-images.githubusercontent.com/77530003/139696282-22b639e8-7fa9-4d54-9a66-15319f0647f6.png">

### ▼ Highlight the candidate value at each step of the searching process,
**Binarysearch:**

### ▼ Make it obvious when it has either found the value it is searching for or knows that the value is not in the data set.

## Add tests
### ▼ Kinds of tests to verify the functionality of the searching

### ▼ Implemented Tests
