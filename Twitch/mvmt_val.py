#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 12:24:53 2016

@author: Varoon
"""

#takes array. Returns -1 if sum of vals is nonpositive. Else returns the index of the max val.            
def mvmt_val_helper(arr):
    if sum(arr)<=0:
        return -1
    else:
        return arr.index(max(arr))

# returns 0 if no inputs from twitch. Otherwise outputs distinct value for each cardinal and intercardinal 
# direction. All values between 0 and 10, inclusive. Powers of two guarantee distinctiveness under addition
        
def get_mvmt_val(commands,team):    
    if sum(commands[team][0:2])==0 or sum(commands[team])==0:     #if no forward or backward movement, side movement is irrelevent
        return 0
    
    #beyond this, assuming forward/backward movement.     
    forward_back_val=mvmt_val_helper(commands[team][0:2])
    left_right_val=mvmt_val_helper(commands[team][2:4])
    if left_right_val == -1:
        return 2**(forward_back_val)
    return 2**(forward_back_val) + 2**(left_right_val+2)
    
