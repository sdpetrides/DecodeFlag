# Decodes SAM Flags in Python
# @author: Stephen Petrides
# @usage: $ python3 decodeFlag.py <optional flags> <input_file.sam> <optional_output_file.sam>
# @usage: $ python3 decodeFlag.py -man to print Commands and Options section of the manual

import sys
import json


# Convert Method
# Takes FLAG in string form and returns the corresponding descriptions in list form
def convert(flag_int):

	flag_list = []
	count = 2048

	while count > 0:
		if flag_int >= count and flag_int - count >= 0:
			flag_list.insert(0, flag_dict_template[count])
			FLAG_count_update(count)
			flag_int -= count
		count //= 2

	if len(flag_list) is 0:
		flag_list.append("FLAG is 0")

	return flag_list



# FLAG Count Update Method
# Takes FLAG in string and updates the global flag_count_dict to
# trank the count of each description in the file
def FLAG_count_update (flag_int):
	#flag_int = int(flag_str)
	temp_list = flag_count_dict[flag_int]
	temp_list[0] = temp_list[0] + 1
	flag_count_dict[flag_int] = temp_list



# FLAG Combo Count Update Method
# Takes FLAG in string and updates the global flag_combo_count_dict to
# track the count of each FLAG combination
def FLAG_combo_count_update (flag_int):
	if flag_int in flag_combo_count_dict: 
		flag_combo_count_dict[flag_int] = flag_combo_count_dict[flag_int] + 1
	else:
		flag_combo_count_dict[flag_int] = 1



# MAIN

# Declare globals
flag_dict_template = {
		1 : "Template having multiple segments in sequencing",
		2 : "Each segment properly aligned according to the aligner",
		4 : "Segment unmapped",
		8 : "Next segment in the template unmapped",
		16 : "SEQ being reverse complemented",
		32 : "SEQ of the next segment in the template being reverse standed",
		64 : "The first segment in the template",
		128 : "The last segment in the template",
		256 : "Secondary alignment",
		512 : "Not passing filters, such as platform/vender quality controls",
		1024 : "PCR or optical duplicate",
		2048 : "Supplementary alignment"
	}

flag_count_dict = {
		1 : [0, "Template having multiple segments in sequencing"],
		2 : [0, "Each segment properly aligned according to the aligner"],
		4 : [0, "Segment unmapped"],
		8 : [0, "Next segment in the template unmapped"],
		16 : [0, "SEQ being reverse complemented"],
		32 : [0, "SEQ of the next segment in the template being reverse standed"],
		64 : [0, "The first segment in the template"],
		128 : [0, "The last segment in the template"],
		256 : [0, "Secondary alignment"],
		512 : [0, "Not passing filters, such as platform/vender quality controls"],
		1024 : [0, "PCR or optical duplicate"],
		2048 : [0, "Supplementary alignment"]
	}

flag_combo_count_dict = {
		0 : 0
	}

# Set Parameters and Filenames
argc = len(sys.argv)
qname_set = set()
param_count = 1
param_set = set()

while param_count <= argc-1:
	param_str = sys.argv[param_count]
	if param_str[0] == '-':
		if param_str != '-qname' and param_str != '-qname_file':
			param_set.add(sys.argv[param_count])
			param_count+=1
		elif param_str != '-qname_file':
			param_set.add(sys.argv[param_count])
			param_count+=1
			while param_count < argc-1:	
				param_str = sys.argv[param_count]
				if param_str != '-qname_end':
					qname_set.add(sys.argv[param_count])
					param_count+=1
				else:
					param_count+=1
					break
		else:
			param_set.add(sys.argv[param_count])
			param_count+=1
			qname_file = open(sys.argv[param_count])
			param_count+=1
			for line in qname_file:
				qname_set.add(line.strip())
	else:
		break

if '-man' in param_set:
	print("Basic Command Structure:\n", 
		"\t$ python3 decodeFlag.py <optional flags> <input_file.sam> <optional_output_file.sam>\n\n", 
		"\tIf output file is not specified decodeFlag will print the results in the terminal.\n", 
		"\tWithout any flags specified decodeFlag will print the FLAG descriptions for each alignment in the ",
		"SAM file as well as the descriptions count and the FLAG combinations count.\n",
		"\tFilenames cannot start with `-`.",
		"\nOptional Flags\n",
		"\tCan come in any order but must begin with `-`.\n\n",
		"\t-man\n",
		"\t\tPrints Commands and Options section of MANUAL.\n",
		"\t-o\n",
		"\t\tSpecifies that an output file is to be included. Without this, the output file with not be created and/or filled in.\n",
		"\t-d_count\n",
		"\t\tDoes not print the descriptions count section.\n",
		"\t-combo_count\n",
		"\t\tDoes not print the FLAG combinations count section.\n",
		"\t-qname <QNAME_1> <QNAME_2> -qname_end\n",
		"\t\tPrints FLAG descriptions for the alignments with the matching qname.\n",
		"\t\t# QNAMEs must come between -qname and -qname_end flags. Any number of QNAMEs can be included.\n",
		"\t-qname_file <QNAME_FILE>\n",
		"\t\t# Prints FLAG descriptions for the alignments with the matching qname for the QNAMEs provided in the file.\n",
		"\t\t# QNAMEs must be separate lines with no extra characters in the file. Any number of QNAMEs can be included.\n",
		"\t\t# The filename must follow imediately after the -qname_file flag.\n")
	sys.exit()

file_name = sys.argv[param_count]
param_count+=1

# No Output File
if '-o' not in param_set:

	file_input = open(file_name, 'rt')

	for line in file_input:
		words = line.split()
		first_word = words[0]
		if first_word[0] is not '@' and qname_set and first_word in qname_set:

			flag_int = int(words[1])

			flag_list = convert(flag_int)
			FLAG_combo_count_update(flag_int)

			print(first_word, sep='', end='\n')
			for item in flag_list:
				print(item, sep='', end='\n')

			
			print('\n')

	if '-d_count' not in param_set:
		print('Descriptions Count\n')
		for pair in sorted(flag_count_dict.values(), reverse=True):
			print(pair, sep=':\t', end='\n')
		print('\n')
	if '-combo_count' not in param_set:
		print('FLAG Combinations Count\n')
		for pair in sorted(flag_combo_count_dict.items()):
			print(pair, sep=':\t', end='\n')
		print('\n')
	file_input.close()

# Output File
else:
	file_name_2 = sys.argv[argc-1]

	file_input = open(file_name, 'rt')
	file_output = open(file_name_2, 'wt')

	file_input = open(file_name, 'rt')
	for line in file_input:
		words = line.split()
		first_word = words[0]
		if first_word[0] is not '@':
			flag_int = int(words[1])

			flag_list = convert(flag_int)
			FLAG_combo_count_update(flag_int)

			file_output.write(first_word + '\n')
			for item in flag_list:
				file_output.write(item + '\n')
			
			file_output.write('\n')

	if '-d_count' not in param_set:
		file_output.write('Descriptions Count\n')
		for pair in sorted(flag_count_dict.values(), reverse=True):
			file_output.write(json.dumps(pair) + '\n')
		file_output.write('\n')
	if '-combo_count' not in param_set:
		file_output.write('FLAG Combinations Count\n')
		for pair in sorted(flag_combo_count_dict.items()):
			file_output.write(json.dumps(pair) + '\n')

		file_output.write('\n')

	file_input.close()
	file_output.close()




