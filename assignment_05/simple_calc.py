# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Simple Calculator
--------------------------------------------------------------------------
License:   
Copyright 2018 <Sammi Lu>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Simple calculator that will 
  - Take in two numbers from the user
  - Take in an operator from the user
  - Perform the mathematical operation and provide the number to the user
  - Repeat

Operations:
  - addition
  - subtraction
  - multiplication
  - division
  - exponentiation
  - left shift (integer)
  - right shift (integer)
  - modulo

Error conditions:
  - Invalid operator --> Program should exit
  - Invalid number   --> Program should exit

--------------------------------------------------------------------------
"""

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

import sys
import operator

# convert python version
if sys.version[0] == "2":
    input = raw_input

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# 10.3 operator
operators = {
    "+"   : operator.add,
    "-"   : operator.sub,
    "*"   : operator.mul,
    "/"   : operator.truediv,
    "pow" : pow,
    ">>"  : operator.rshift,
    "<<"  : operator.lshift,
    "mod" : operator.mod
}

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def get_user_input():
    print("Get User Input")
    
    try:
        
        num1 = float(input("  1st number                   : "))
        num2 = float(input("  2nd number                   : "))
        op   = input("  Operator (+, -, *, /, pow, >>, <<, mod): ")
        
        return (num1, num2, op)
    except:
        print("\nInvalid Input")
        return(None, None, None)
        
# End def
    
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

# testing of script / library
if __name__ == "__main__":
    while True:
        print ("Simple Calculator")
        
        
        (num1, num2, op) = get_user_input()
        
        try:
            func = operators[op]
            # print("{0}".format(func))
            try:
                result = func(num1,num2)
                # integer type for >> and <<
            except TypeError:
                result = func(int(num1),int(num2))
            print(result)
        except:
            #if (number1 is None) or (number2 is None) or (func is None):
            #   print ("Quitting")
            #   break
            print("Quitting")
            break

if __name__ == "__main__":
  pass