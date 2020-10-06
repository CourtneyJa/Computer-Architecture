PRINT_TIM = 0b00000001
HALT      = 0b00000010
PRINT_NUM = 0b00000011 
SAVE = 0b00000100
PRINT_REGISTER = 0b00000101
ADD = 0b00000110

memory = [
    PRINT_TIM,
    PRINT_NUM,
    42,
    PRINT_NUM,
    SAVE,
    2,
    10,
    SAVE,
    3,
    10,
    ADD,
    2,
    3,
    PRINT_REGISTER,
    2,
    HALT
]
#cabinets in your shop: registers
#storage unit: cache
#warehouse outside town: RAM
#registers
# - treat as variables, physically located on pc
# names R0 - R7 - used to transfer data 
registers = [0] * 8 

#cpu should step thru memory and take actions based on commanda it finds
#a data driven machine
#program counter, a pointer
pc = 0
running = True
while running:
    command = memory[pc]
        
    if command == PRINT_TIM:
        print("Tim!")

    elif command == PRINT_NUM:
        pc += 1
        number = memory[pc + 1]
        print(number)
    
    elif command == SAVE:
        #get out the args
        #pc+1 = reg index, pc+2 = value
        reg_idx = memory[pc +1]
        value = memory[pc + 2]
        #incre pc 
        pc += 2
    
    elif command == PRINT_REGISTER:
        #get args
        reg_idx = memory[pc +1]
        #argu is a pointer to a register
        value = registers[reg_idx]
        print(value)
        #incre pc
        pc += 1

    elif command == ADD:
        #get args
        reg_idx_1 = memory[pc +1]
        reg_idx_2 = memory[pc +2]
        #add registers
        registers[reg_idx_1] = registers[reg_idx_1] + registers[reg_idx_2]
        #incre pc
        pc += 2
        
    elif command == HALT:
         running = False

    else:
        print('unknown command')
        running = False

    pc += 1