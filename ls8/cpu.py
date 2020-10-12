"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
SP = 7

#for Computer Architecture Sprint
CMP = 0b10100111
JMP = 0b01010100 
JEQ = 0b01010101 
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #need ram, register, and program counter?
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[SP] = 0xF4
        self.flag = 0B00000000
        self.halted = False

    def load(self):
        """Load a program into memory."""

        try:
            address = 0
            with open(sys.argv[1]) as file:
                for line in file:
                    split_it= line.split("#")
                    value = split_it[0].strip()
                    if value == "":
                        continue
                    try:
                        instruction = int(value, 2)
                    except ValueError:
                        print(f"Invalid number '{value}'")
                        sys.exit(1)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]} {sys.argv[1]} file not found")
            sys.exit()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #code for sprint
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            if self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.reg[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
                
        while not self.halted:
            instruction = self.ram_read(self.pc)
            reg_idx_1 = self.ram_read(self.pc + 1)
            reg_idx_2 = self.ram_read(self.pc + 2)
            self. execute_instruction(instruction, reg_idx_1, reg_idx_2)

    def execute_instruction(self, command, reg_idx_1, reg_idx_2):
        if command == HLT:
           self.halted = True
           self.pc += 1
        elif command == PRN:
            print(self.reg[reg_idx_1])
            self.pc += 2
        elif command == LDI:
            self.reg[reg_idx_1] = reg_idx_2
            self.pc += 3
        elif command == MUL:
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
            self.pc += 3
        elif command == PUSH:
            #to-dos
            #1 decrement the stack pointer
            self.reg[SP] -= 1
            #2 get the reg num to push
            reg_num = self.ram_read(self.pc +1)
            #3 get the value to push
            value = self.reg[reg_num]
            #4 copy the value to the stack pointer addy
            stack_head_addy = self.reg[SP]
            self.ram[stack_head_addy] = value
            #5 increment program counter
            self.pc +=2
        elif command == POP:
            #similar to push in what needs to be done
            #1 get reg that you'll pop into
            reg_num = self.ram_read(self.pc + 1)
            #2 get addy for the top of the stack
            stack_head_addy = self.reg[SP]
            #3 get value thats at the top
            value = self.ram_read(stack_head_addy)
            #4 store that value in a reg
            self.reg[reg_num] = value
            #5 increment the stack pointer
            self.reg[SP] += 1
            #6 increment the program counter 
            self.pc += 2

###code for sprint###
        elif command == CMP:
            opr_a = self.ram_read(self.pc + 1)
            opr_b = self.ram_read(self.pc + 2)
            self.alu("CMP", opr_a, opr_b)
            self.pc += 3
        elif command == JMP:
            register_num = self.ram_read(self.pc + 1)
            self.pc = self.reg[register_num]
        elif command == JEQ:
            if self.flag == 0b00000001:
                register_num = self.ram_read(self.pc + 1)
                self.pc = self.reg[register_num]
            else:
                self.pc += 2
        elif command == JNE:
            if self.flag != 0b00000001:
                register_num = self.ram_read(self.pc + 1)
                self.pc = self.reg[register_num]
            else:
                self.pc +=2
        else:
            self.pc +=1
