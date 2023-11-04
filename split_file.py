#!/usr/bin/env python3

import os
import sys
import multiprocessing

def split_lines(input_file, output_dir, start, end):
    with open(input_file, 'r') as input_text_file:
        lines = input_text_file.readlines()[start:end]

    for index, line in enumerate(lines):
        output_file = os.path.join(output_dir, f'text_{start + index}.txt')
        with open(output_file, 'w') as output_text_file:
            output_text_file.write(line)

def main():
    if len(sys.argv) != 4:
        print("Usage: python split_file.py input_file.txt output_directory nprocs")
    else:
        input_file = sys.argv[1]
        output_dir = sys.argv[2]
        nprocs = int(sys.argv[3])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(input_file, 'r') as input_text_file:
            lines = input_text_file.readlines()

        chunk_size = len(lines) // nprocs
        processes = []

        for i in range(nprocs):
            start = i * chunk_size
            end = start + chunk_size if i < nprocs - 1 else len(lines)
            process = multiprocessing.Process(target=split_lines, args=(input_file, output_dir, start, end))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()

if __name__ == "__main__":
    main()
