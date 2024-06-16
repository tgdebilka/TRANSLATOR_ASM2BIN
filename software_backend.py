"""----------------------------------------------------------------------------------------------------"""
import re
from instructions_set import command_dict
"""----------------------------------------------------------------------------------------------------"""
# CONSTANTS:
OPERAND_TYPES = ["#data", "data_addr", "code_addr", "bit_addr"]
VALID_OPERANDS = ['A', '@R0', '@R1', 'R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'C', '@DPTR']
OPERAND_PATTERNS = [
    (r'^#([0-9A-Fa-f])+h', "Hexadecimal immediate value"),
    (r'^([0-9A-Fa-f])+h', "Hexadecimal direct address"),
    (r'^([0-9A-Fa-f])+$', "Decimal direct address or immediate value"),
]
"""----------------------------------------------------------------------------------------------------"""



"""----------------------------------------------------------------------------------------------------"""
def operand_checker(operand):
    """
    Check the type of the operand and return the appropriate string.
    """
    if operand in VALID_OPERANDS:
        return operand
    for i, (pattern, _) in enumerate(OPERAND_PATTERNS):
        if re.findall(pattern, operand):
            print(f"Found {OPERAND_PATTERNS[i][1]}")
            return OPERAND_TYPES[i]
    print("Assuming bit address")
    return "bit_addr"

"""----------------------------------------------------------------------------------------------------"""



"""----------------------------------------------------------------------------------------------------"""
def read_file(filename):
    with open(filename, 'r') as file:
        lines = [line.rstrip().replace(',', '').split(" ") for line in file]
        lines = [['0x' + part if part.isnumeric() else part for part in line] for line in lines]
    return lines

"""----------------------------------------------------------------------------------------------------"""



"""----------------------------------------------------------------------------------------------------"""
def decode_command(command):
    """
    Decode a command and return the appropriate hexadecimal opcode.
    """
    try:
        opcode = command_dict[command[0]]
        if isinstance(opcode, int):
            return hex(opcode)[2:].upper()
        elif len(command) == 2:
            getting_key = operand_checker(command[1])
            return hex(opcode[getting_key])[2:].upper()
        elif len(command) == 3:
            getting_key_inx1 = operand_checker(command[1])
            getting_key_inx2 = operand_checker(command[2])
            return hex(opcode[f'{getting_key_inx1},{getting_key_inx2}'])[2:].upper()
        else:
            raise ValueError(f"Command has invalid number of parts: {command}")
    except (KeyError, ValueError) as e:
        print(f"Invalid command input: {command}. Error: {e}")
        raise
"""----------------------------------------------------------------------------------------------------"""