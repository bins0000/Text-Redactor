import argparse
from project1 import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type = str, action = "append", help = "<Required> Set flag" , required = True)
    parser.add_argument("--concept", type = str, action = "append", help = "<Required> Set flag" , required = True)
    parser.add_argument("--output", type = str, help = "<Required> Set output folder" , required = True)
    parser.add_argument("--names", action = "store_true", help = "Set flag")
    parser.add_argument("--dates", action = "store_true", help = "Set flag")
    parser.add_argument("--genders", action = "store_true", help = "Set flag")
    parser.add_argument("--phones", action = "store_true", help = "Set flag")
    parser.add_argument("--address", action = "store_true", help = "Set flag")
    parser.add_argument("--stats", type = str, help = "<Required> Set stats type" , required = True)
    args = parser.parse_args()
    if args.input:
        main.main(args.input, args.concept, args.output, args.names, args.dates, args.genders, args.phones, args.address, args.stats)


