from common import get_file

def main() -> None:

    inputs = [
        "a_an_example.in.txt",
        "b_basic.in.txt",
        "c_coarse.in.txt",
        "d_difficult.in.txt",
        "e_elaborate.in.txt",
    ]

    for input in inputs:
        with open(get_file(f"practice\{input}"), "r") as f:
            f.readlines()
        print()

if __name__ == '__main__':
    main()