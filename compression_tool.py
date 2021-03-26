import sys
import os.path

# define some constants
LEN = 16384
BUF_LEN = 4096


def check_file_exists(file):
    if not os.path.isfile(file):
        return False
    return True


# compress the given file using the LZW algorithm
def LZW_compress(f_in, f_out):
    # the new entries added in the dictionary are added at dict_i index
    # and it starts at 256, because the first 255 entries are going to
    # be reserved for the ASCII characters
    dict_i = 256

    # create and init the dictionary
    # add each character in the ASCII table in the dictionary
    sequence_dict = dict([(chr(i), i) for i in range(dict_i)])

    # set prev to the first byte from the text
    prev = f_in.read(1).decode("latin1")

    # build the dictionary table
    while True:
        # read a BUF_LEN block of bytes
        buf = f_in.read(BUF_LEN).decode("latin1")

        # if the end of the file is reached, break
        if not buf:
            break

        for c in buf:
            # concatenate prev.c
            temp = prev + c

            # if prev is in sequence_dict, set prev = prev.c
            if temp in sequence_dict:
                prev = temp
            # if prev is not yet in sequence_dict
            else:
                # add the index of prev in dict to f_out
                # find out the index
                index = sequence_dict[prev]

                # write to the output file
                f_out.write(str(index) + " ")

                # if the maximum number of keys is smaller than LEN
                # add prev.c to the dictionary
                if dict_i <= LEN:
                    sequence_dict[temp] = dict_i
                    dict_i += 1

                # set prev to c
                prev = c

    # write the index of prev in the dictionary
    # find out the index
    index = sequence_dict[prev]

    # write to the output file
    f_out.write(str(index) + " ")


# decompress the given file using the LZW algorithm
def LZW_decompress(f_in, f_out, endian):
    # keep a flag for the first index for easier manipulation
    # of the numbers in the input file
    first_index = True

    # the new entries added in the dictionary are added at dict_i index
    # and it starts at 256, because the first 255 entries are going to
    # be reserved for the ASCII characters
    dict_i = 256

    # create and init the dictionary
    # add each character in the ASCII table in the dictionary
    sequence_dict = dict([(i, chr(i)) for i in range(dict_i)])

    # set current to the first index in
    current = 0

    for line in f_in:
        for number in line.split():

            # set current to the first index found in the input file
            # and write it to the output file
            if first_index:
                current = int(number)
                f_out.write((ord(sequence_dict[current])).to_bytes(1, byteorder=endian))

                # set first_index to false as it is called only once
                # in the beginning
                first_index = False
                continue

            previous = current
            current = int(number)

            # if there exists sequence_dict[current]
            if current <= dict_i - 1:
                s = sequence_dict[current]
                for i in s:
                    f_out.write((ord(i).to_bytes(1, byteorder=endian)))

                # insert in sequence_dict[dict_i] = sequence_dict[previous].s[0]
                temp = sequence_dict[previous] + s[0]
                sequence_dict[dict_i] = temp

                # increment dict_i
                dict_i += 1
            # if the dictionary does not yet contain an entry at index current
            else:
                s = sequence_dict[previous] + sequence_dict[previous][0]

                # write s to the output file
                for i in s:
                    f_out.write((ord(i).to_bytes(1, byteorder=endian)))

                # insert s in sequence_dict at dict_i index
                sequence_dict[dict_i] = s

                # increment dict_i
                dict_i += 1


def compress_decompress(input_path, output_path, mode):
    # check if the input file exists
    if not check_file_exists(input_path):
        print("No such file or directory")
        exit(3)

    # the input and output files have to be open differently according to the
    # mode given by the client
    # if the mode is -c:
    #       - the input file should be opened in binary mode
    #       - the output file should be opened in normal mode
    # if the mode is -d:
    #       - the input file should be opened in normal mode
    #       - the output file should be opened in binary mode

    # the default modes to open the input and output files are
    # by default, 'r' and 'w'
    read_mode = "r"
    write_mode = "w"

    if mode == "-c":
        read_mode += "b"
    elif mode == "-d":
        write_mode += "b"

    # open the input file
    f_in = open(input_path, read_mode)

    # if the file output does not exist, create it
    # if it exists, overwrite its contents
    f_out = open(output_path, write_mode)

    # compress/decompress based on the mode
    if mode == "-c":
        LZW_compress(f_in, f_out)
    elif mode == "-d":
        # sys.byteorder returns a string containing information about
        # whether the system is using big/little endian
        # This information is needed for .to_bytes()
        LZW_decompress(f_in, f_out, sys.byteorder)

    # close the input and output files
    f_in.close()
    f_out.close()


def main():
    # compression_tool mode input_file output_file
    # mode: -c/-d

    # save the number of arguments
    nb_arg = len(sys.argv)

    # if there are not three arguments given
    if nb_arg != 4:
        print("Incorrect number of arguments given.")
        print("Please use the tool as such: "
              "python compression_tool.py mode input_file output_file")
        sys.exit(1)

    # inspect argv[1] and make sure it is a valid mode
    if sys.argv[1] != "-c" and sys.argv[1] != "-d":
        print(sys.argv[1] + " mode is not recognized")
        sys.exit(2)

    # compress/decompress the given file
    compress_decompress(sys.argv[2], sys.argv[3], sys.argv[1])


# run main()
if __name__ == "__main__":
    main()
