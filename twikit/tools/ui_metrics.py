import re
import os
import json
from datetime import datetime, timedelta

function_regex = re.compile(r'function\s?[^\.][\w|,|\s|-|_|\$]*.+?\{([^\.][\s|\S]*(?=\}))')
init_nums_regex = re.compile(r'var [A-Za-z0-9]{64}=[0-9]+')
basic_math_regex = re.compile(r'[a-z0-9]{64}=(~|\^|\||&|[A-Za-z0-9]{64})')
func_ending_regex = re.compile(r'}\([a-z0-9]{64},[a-z0-9]{64},[a-z0-9]{64}\)')


def unix_milli_day(timestamp):
    # Convert milliseconds to a timedelta
    delta = timedelta(milliseconds=timestamp)

    # Calculate the UTC datetime by subtracting the delta from the Unix epoch
    epoch = datetime(1970, 1, 1)
    return (epoch + delta).day

def math_xor(a, b, c):
    return (b ^ a) | (c ^ b)

def math_right_shift(a, b, c):
    num = 0
    for i in range(8):
        if (a & 1) == 0:
            num += a
        if (b & 1) == 0:
            num += b
        if (c & 1) == 0:
            num += c
        a >>= 1
        b >>= 1
        c >>= 1
    return num % 256

def solve_ui_metrics(code) -> dict:

    matches = function_regex.findall(code)
    matches = function_regex.findall(matches[0])
    matches = function_regex.findall(matches[0])
    script = matches[0]
    operations = script.split(";")
    solution = {}

    inside_right_shift_func = False
    right_shift_func_key = ""
    inside_math_xor_func = False
    math_xor_func_key = ""

    for op in operations:
        # get initial numbers
        if init_nums_regex.search(op):
            parts = init_nums_regex.search(op).group().split("=")
            value = int(parts[1])
            solution[parts[0][4:]] = value
            continue
        
        # basic math, like xxx ^ xxx, ~xxx, etc.
        if basic_math_regex.search(op) and "new Date" not in op:
            sign_change = False
            math_done = False
            
            # handle ~, which changes the sign
            if "~" in op:
                # handle rather it's a `~(xxx ^ xxx)` op or not.
                if "(" in op:
                    # trim off `~(` and `)`
                    tmp = op.split("=")
                    new_part = tmp[1][2:-1]
                    op = f"{tmp[0]}={new_part}"
                else:
                    # trim off just `~`
                    tmp = op.split("=")
                    new_part = tmp[1][1:]
                    op = f"{tmp[0]}={new_part}"
                sign_change = True
            
            parts = op.split("=")
            # handle all the different operations
            if "^" in parts[1]:
                tmp = parts[1].split("^")
                solution[parts[0]] = solution[tmp[0]] ^ solution[tmp[1]]
                math_done = True
            if "|" in parts[1]:
                tmp = parts[1].split("|")
                solution[parts[0]] = solution[tmp[0]] | solution[tmp[1]]
                math_done = True
            if "&" in parts[1]:
                tmp = parts[1].split("&")
                solution[parts[0]] = solution[tmp[0]] & solution[tmp[1]]
                math_done = True
            
            if sign_change:
                if math_done:
                    solution[parts[0]] = -(solution[parts[0]] + 1)
                else:
                    solution[parts[0]] = -(solution[parts[1]] + 1)
        
        if "new Date" in op:
            parts = op.split("=")
            op_parts = parts[1].split("^")
            solution[parts[0]] = solution[op_parts[0]] ^ unix_milli_day(solution[op_parts[1].split("*")[0].split("(")[1]] * 10000000000)
        
        # detect the rightShiftFunc starting
        if "document.createElement('div')" in op and not inside_right_shift_func:
            inside_right_shift_func = True
            right_shift_func_key = op.split("=function")[0]
        
        # detect the rightShiftFunc ending
        if func_ending_regex.search(op) and inside_right_shift_func:
            inside_right_shift_func = False
            in_params = op[2:-1].split(",")
            solution[right_shift_func_key] = math_right_shift(solution[in_params[0]], solution[in_params[1]], solution[in_params[2]])
            right_shift_func_key = ""
        
        # detect the mathXORFunc starting
        if "function(){return this." in op and not inside_math_xor_func:
            inside_math_xor_func = True
            math_xor_func_key = op.split("=")[0]
        
        # detect the mathXORFunc ending
        if func_ending_regex.search(op) and inside_math_xor_func:
            inside_math_xor_func = False
            in_params = op[2:-1].split(",")
            solution[math_xor_func_key] = math_xor(solution[in_params[0]], solution[in_params[1]], solution[in_params[2]])
            math_xor_func_key = ""
        
        if op.startswith("return {'rf"):
            in_params = op.split(",")[-1].split(":")
            solution[in_params[0].strip("'")] = in_params[1].strip("'")
            solution = {'rf': solution}
            break

    return str(solution).replace('\'', '\\"')


if __name__ == "__main__":
    # load sample file
    with open("./sample.js", "r") as f:
        code = f.read()
        solution = solve_ui_metrics(code)
        print(solution)