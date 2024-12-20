import struct
import yaml

def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    binary_output = []
    log_output = []

    for line in lines:
        parts = line.strip().split()
        opcode = int(parts[0])
        operands = list(map(int, parts[1:]))

        if opcode == 21:  # Загрузка констант
            instruction = struct.pack('<B I', opcode, operands[0])
        elif opcode == 30:  # Чтение из памяти
            instruction = struct.pack('<B H', opcode, operands[0])
        elif opcode in [13, 27]:  # Запись в память или побитовое НЕ
            instruction = struct.pack('<B', opcode)
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

        binary_output.append(instruction)
        log_output.append({"opcode": opcode, "operands": operands})

    with open(output_file, 'wb') as f:
        for instruction in binary_output:
            f.write(instruction)

    with open(log_file, 'w') as f:
        yaml.dump(log_output, f)