import re
from datetime import datetime
from bs4 import BeautifulSoup

def parsehtmlr():
    # Open the HTML file and parse it
    with open(html_file_name, 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    # Extract the text from the HTML
    text = soup.get_text(separator='\n')

    # Create the name of the text file
    txt_file_name = html_file_name.rsplit('.', 1)[0] + '.txt'

    # Write the text to the text file
    with open(txt_file_name, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

    print(f"Text has been extracted and saved to {txt_file_name}")
    return txt_file_name


def process_file(input_file, output_file, names):
    global new_file_name
# Open the text file and read the lines into a list
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Create a list of tuples, each containing a timestamp-message block
    blocks_with_timestamps = []
    block_lines = []
    timestamp = ''  # Initialize timestamp

    for line in lines:
        if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC', line):
            # We've reached a new timestamp, so save the previous block (if any)
            if block_lines:
                blocks_with_timestamps.append((timestamp, ''.join(block_lines)))
            # Start a new block with this timestamp
            timestamp = line.strip()
            block_lines = [line]
        else:
            # This line is part of the current block
            block_lines.append(line)
    # Don't forget to save the last block
    if block_lines:
        blocks_with_timestamps.append((timestamp, ''.join(block_lines)))

    # Sort the list of tuples by the timestamp
    blocks_with_timestamps.sort()

    # Extract the blocks from the sorted list of tuples
    sorted_blocks = [block for timestamp, block in blocks_with_timestamps]

    # Create the name of the new text file
    new_file_name = "sorted_" + file_name
    # Write the sorted blocks to the new text file
    with open(new_file_name, 'w', encoding='utf-8') as new_file:
        new_file.writelines(sorted_blocks)

    print(f"Blocks have been reordered and saved to {new_file_name}")
    with open(input_file, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()

    with open(output_file, 'w', encoding='utf-8') as f_out:
        remove_next_empty_line = False
        for i, line in enumerate(lines):
            if 'UTC' in line:
                f_out.write('\n' + line)
                remove_next_empty_line = True
            elif any(name in line for name in names): #
                f_out.write(line)
                # Check if the next line is empty and remove it
                if i < len(lines) - 1 and lines[i + 1].strip() == '':
                    remove_next_empty_line = True
                else:
                    remove_next_empty_line = False
            elif remove_next_empty_line:
                remove_next_empty_line = False
                if line.strip(): 
                    f_out.write(line)
                else:
                    continue  
            else:
                f_out.write(line)



def convert_timestamps(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for line in lines:
            if 'UTC' in line:
                timestamp = line.split('UTC')[0].strip()
                try:
                    timestamp_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    formatted_time = timestamp_dt.strftime('%B %d, %Y %I:%M:%S %p').replace(' 0', ' ')
                    f_out.write(f"{line.strip()} \\ {formatted_time}\n")
                except ValueError:
                    f_out.write(line)
            else:
                f_out.write(line)
def delete_text_saved_lines(input_file, output_file, names):
    name_mappings = {}
    for name in names:
        new_name = input(f"What should '{name}' be converted to? ")
        name_mappings[name] = new_name

    with open(input_file, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for line in lines:
            line = line.strip()
            if line in names:
                converted_name = name_mappings[line]
                f_out.write(f"{converted_name}: \n")
            elif line not in ['TEXT', 'Saved']:  # Do Not Remove.
                f_out.write(line + '\n')  # Do Not Remove.

if __name__ == "__main__":
    html_file_name = "myhtmler.html"
    names = ['name1', 'name2', 'name3']
    input_file = "sorted_" + str(parsehtmlr())
    output_file = input_file  # Output file with converted timestamps
    print("html converted")
    process_file(input_file, output_file, names)
    print("Processing complete.")
    delete_text_saved_lines(input_file, output_file, names)
    print("lines deleted, names corrected")
    convert_timestamps(input_file, output_file)
    print("Timestamp conversion complete.")
