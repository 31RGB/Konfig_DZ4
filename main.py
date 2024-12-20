import argparse
from assembler import assemble
from interpreter import interpret

def main():
    parser = argparse.ArgumentParser(description="Assembler and Interpreter for Virtual Machine")
    subparsers = parser.add_subparsers(dest="command")

    #Ассемблер
    assemble_parser = subparsers.add_parser("assemble")
    assemble_parser.add_argument("input_file", help="Path to input assembly file")
    assemble_parser.add_argument("output_file", help="Path to output binary file")
    assemble_parser.add_argument("log_file", help="Path to log file")

    #Интерпретатор
    interpret_parser = subparsers.add_parser("interpret")
    interpret_parser.add_argument("input_file", help="Path to input binary file")
    interpret_parser.add_argument("output_file", help="Path to output result file")
    interpret_parser.add_argument("memory_range", type=int, nargs=2, help="Memory range to output")

    args = parser.parse_args()

    if args.command == "assemble":
        assemble(args.input_file, args.output_file, args.log_file)
    elif args.command == "interpret":
        interpret(args.input_file, args.output_file, args.memory_range)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()