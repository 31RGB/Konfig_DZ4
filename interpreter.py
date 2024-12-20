import struct
import yaml

class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.memory = [0] * 1024  #Размер памяти, который можно регулировать

    def load_constant(self, value):
        self.stack.append(value)

    def read_memory(self, offset):
        if not self.stack:
            raise RuntimeError("Stack underflow during memory read.")
        address = self.stack.pop() + offset
        self.stack.append(self.memory[address])

    def write_memory(self):
        if len(self.stack) < 2:
            raise RuntimeError("Stack underflow during memory write.")
        value = self.stack.pop()
        address = self.stack.pop()
        self.memory[address] = value

    def bitwise_not(self):
        if not self.stack:
            raise RuntimeError("Stack underflow during bitwise NOT operation.")
        self.stack.append(~self.stack.pop())

    def execute(self, instructions):
        for instruction in instructions:
            opcode = instruction[0]
            if opcode == 21:  # Загрузка констант
                self.load_constant(instruction[1])
            elif opcode == 30:  # Чтение из памяти
                self.read_memory(instruction[1])
            elif opcode == 13:  # Запись в память
                self.write_memory()
            elif opcode == 27:  # Побитовое НЕ
                self.bitwise_not()
            else:
                raise ValueError(f"Unknown opcode: {opcode}")

def interpret(input_file, output_file, memory_range):
    vm = VirtualMachine()

    with open(input_file, 'rb') as f:
        binary_data = f.read()

    instructions = []
    i = 0
    while i < len(binary_data):
        opcode = binary_data[i]
        if opcode == 21:  # Загрузка констант
            value = struct.unpack('<I', binary_data[i+1:i+5])[0]
            instructions.append((opcode, value))
            i += 5
        elif opcode == 30:  # Чтение из памяти
            offset = struct.unpack('<H', binary_data[i+1:i+3])[0]
            instructions.append((opcode, offset))
            i += 3
        elif opcode in [13, 27]:  # Запись в память или побитовое НЕ
            instructions.append((opcode,))
            i += 1
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    vm.execute(instructions)

    result = {"memory": vm.memory[memory_range[0]:memory_range[1]]}
    with open(output_file, 'w') as f:
        yaml.dump(result, f)