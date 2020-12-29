# -*- coding: utf-8 -*-
"""
Minimum Edit Distance - GUI : Dynamic Programming
Implemented based on http://www.stanford.edu/class/cs124/lec/med.pdf

@author: Denis
"""

import numpy as np
import PySimpleGUI as sg

#sg.theme_previewer()


#Function takes in 2 words and returns the minimum Edit distance between the two Strings
#Edits include Deletion, Insertion or Substitution 
#Call function with Levenshtein=True if substitutions should have cost of 2. Default is 1
def min_edit_distance(word1, word2, Levenshtein=False):
    
    #Determining cost based on type
    cost = 1
    if Levenshtein:
        cost = 2
    
    
    m = len(word1) #word1 is x
    n = len(word2) #word2 is y
    
    #direction_matrix = np.zeros([n, m]) #implement this if you want to allow backtracking
    value_table = np.zeros([n+1, m+1]) 
    
    
    #x
    for i in range(m+1):
        value_table[0, i] = i
    #print(value_table)
    
    #y
    for i in range(n+1):
        value_table[i, 0] = i
    #print(value_table)
    
    
    '''
    FORMULA being used
    D(i,j) = min{ 
            D(i-1,j)+1
            D(i,j-1)+1
            D(i-1,j-1) + {
                        1; if X(i) != Y(j)  #Change to 2 if using Levenshtein
                        0; if X(i) == Y(j) #X being word1, Y being word2
                        }
        }
    '''
    for i in range(1, m+1): 
        for j in range(1, n+1):
            #Do all checks in here
            possible_values = np.zeros(3)
            possible_values[0] = value_table[j, i-1] + 1 
            possible_values[1] = value_table[j-1, i] + 1
            
            possible_values[2] = value_table[j-1, i-1]
            if word1[i-1] != word2[j-1]:
                possible_values[2] = possible_values[2] + cost #cost: default 1, if Levenshtein then 2
                #else add zero so dont do anything
                
            value_table[j, i] = np.amin(possible_values)
            
        #If Want step by step insert here
        #Uncomment to print after each iteration
        #print( value_table)
    
        
    return value_table

# print("Minimum Distance: ", min_edit_distance("intention", "execution"))
# print("Minimum Distance (Levenshtein): ", min_edit_distance("intention", "execution", True))
# print("------------------------------------------------")



sg.theme('DarkBlue9')


layout = [  [sg.Text('Enter 2 words')],
            [sg.Text('Enter First Word'), sg.InputText()],
            [sg.Text('Enter Second Word'), sg.InputText()],
            [sg.Button('Calculate'), sg.Button('Exit')]]

window = sg.Window('Minimum Edit Distance', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    print('You entered ', values)
    # values[0] -> first word, values[1] -> second word
    
    #New Window
    window.hide()
    firstNum = int(len(values[0])+1)
    secondNum = int(len(values[1])+1)
    pad_x = pad_y = 10;
    if firstNum > 6:
        if firstNum > 10:
            pad_x = 0
        else:
            pad_x = 5
    if secondNum > 6:
        if secondNum > 10:
            pad_y = 0
        else:
            pad_y = 5
    vals = min_edit_distance(values[0], values[1])
    topText = [[sg.T(str(i), size=(4, 2),pad=(pad_x,pad_y)) for i in (" " + values[0])]]
    empty = [[sg.T(" ", size=(4, 2),pad=(pad_x,pad_y))]]
    top = [[sg.Column(empty), sg.Column(topText)]]
    grid = [[sg.Text(str(vals[j][i]), size=(4, 2), pad=(pad_x,pad_y)) for i in range(firstNum)] for j in range(secondNum)]
    sideText = [[sg.T(str(i), size=(4, 2),pad=(pad_x,pad_y))] for i in (" " + values[1])]
    whole = [[sg.Column(sideText), sg.Column(grid)]]
    #sg.Frame("",)
    layout2 = top;
    layout2 += whole;
    layout2 += [[sg.Text('Min Edit Distance: ' + str(vals[-1][-1]))],       # note must create a layout from scratch every time. No reuse
                   [sg.Button('Back')]]

    win2 = sg.Window('Solution', layout2)
    while True:
        ev2, vals2 = win2.read()
        if ev2 == sg.WIN_CLOSED or ev2 == 'Back':
            win2.close()
            window.UnHide()
            break

window.close()

