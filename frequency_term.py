import os, time
import os.path
import re
import fitz
from threading import Thread
from queue import Queue
from colorist import Color, Effect

def search(line, lo, hi, input_to_find, c, q, q_two):
    counted = 0
    words, separate_dashes = [], []
    times_used = [0] * len(input_to_find) # Each index is for each word and (or) phrase to be searched

    """
    [1]
    
    Title: N/A
    Author: Haren, M;  Amery, M
    Date: Feb. 1, 2009; Jun. 26, 2016
    Code Version: N/A
    Availability: https://stackoverflow.com/questions/500864/case-insensitive-regular-expression-without-re-compile
    
    """
    
    # Use regular expression to find the use of the word an (or) phrase in each line
    for input_in in range(0, len(input_to_find)): 
        for section in range(lo, hi): # Index range used to search for the word and (or) phrase 
            if c == True:
                """ Another reference to [1] """
                result = re.findall(input_to_find[input_in], line[section], re.IGNORECASE) # If word and (or) phrase in that range is found
            else:
                result = re.findall(input_to_find[input_in], line[section])
            times_used[input_in] += len(result) # Increase value of corresponding index to that word that was searched

    # Count the words in each line of this thread
    for line_num in range(lo, hi):
        format_line = line[line_num].strip().split()
        for word in format_line:
            if word == '': # Ignore blank spaces so it doesn't count as words
                continue
            elif '--' in word:
                separate_dashes += word.split('--')
                continue
            words.append(word)
            
    q.put(times_used) # Total the number of times it was used for this part of the array
    
    # Use to find the words counted (and count the words delimited by double dashes)
    counted = len(words) + len(separate_dashes)
    
    q_two.put(counted) # Total the number of words used for this part of the array

    """
    [2]
    
    Title: N/A
    Author: W3schools
    Date: N/A
    Code version: N/A
    Availability: https://www.w3schools.com/python/ref_func_map.asp, https://www.w3schools.com/python/trypython.asp?filename=demo_ref_map2
    
    """
    
def total_uses(arr, arr_two): # Used to total the arrays from the Queue 
    return arr + arr_two # Sum of the arrays

if __name__=='__main__':
    novel, to_find = [], []
    queue = Queue()
    queue_two = Queue()
    words_counted = 0
    accepted_type = ['txt', 'docx', 'pdf', 'epub']
    extract_text_file = 'frequencyCounter.txt'
    case_insensitive = True
    
    print(f'\n{Effect.BOLD}This program is used to analyze text. This program can count the total amount of words in ' +
          f' a document, count the number of times a phrase and (or) word is used (at one time), and determine ' +
          f' the relative frequency of the word and (or) phrase. This program uses RegEx to search for the use ' +
          f' of each word and (or) phrase.{Effect.OFF}\n')
    
    # Gives the user three attempts for the correct input
    for attempts in range(1, 4):
        file_name = input('Enter your file name and type (accepted file types: .epub, .pdf, .txt, and .docx): ') 
        file_name = file_name.strip() # In case the user has the right name, but put spaces
        
        file_ext = file_name.split('.') 
        
        """
        [3]
        
        Title: N/A
        Author: RichieHindle; Feil, T
        Date: Aug. 9, 2011; Oct. 10, 2023
        Code version: N/A
        Availability: https://stackoverflow.com/questions/6996603/how-can-i-delete-a-file-or-folder-in-python
        
        """

        # If-statement to ensure the file exists before action, will exit if it does not 
        if os.path.isfile(file_name) == False:
            """ 
            [4]
            
            Title: N/A
            Author: Bagterp, J
            Date: 2023
            Availability: https://stackoverflow.com/questions/73750465/color-print-in-python
            
            """
            print(f'\n{Color.YELLOW}{Effect.BOLD}This file does not exist, is not in this directory, or does not contain a file type{Effect.OFF}{Color.OFF} \n') 
        elif file_ext[len(file_ext) - 1] not in accepted_type:
            print(f'\n{Color.YELLOW}{Effect.BOLD}This is an invalid file type; please try again{Effect.OFF}{Color.OFF} \n')
        else:
            break

        # If the user does not have the correct input by the third attempt
        if attempts == 3:
            """ Similar to the "Looping . . ." used for the Linux code in OS Security """
            print('Terminating . . . ')
            exit()

    # Word and (or) phrase to search for based on the user's input
    for attempts in range(1, 4):
        print('The following characters will be ignored if entered: "$, ^, *, (, ), +, |, \\, ?, [, ], {, }" and blank responses will not be accepted.')
        word_or_phrase = input('\nEnter which word and/or phrase to be searched. Enter "$!" if the results should be case sensitive. Use "/" to separate each word or phrase: ')

        """
        [16]
        
        Title: N/A
        Author: Filonenko, O
        Date: Jul. 17, 2017
        Code version: N/A
        Availability: https://stackoverflow.com/questions/45142327/how-to-replace-multiple-matches-groups-with-regexes
    
        """
        
        if '$!' in word_or_phrase:
            # Geeks
            word_or_phrase = word_or_phrase.replace('$!', '/')
            case_insensitive = False
            
        """
        [5]
        
        Title: N/A
        Author: Tomerikoo; petezurich
        Date: Mar. 14, 2020; Apr. 6, 2021
        Code version: N/A
        Availability: https://stackoverflow.com/questions/60684350/replace-multiple-characters-using-re-sub
    
        """
        
        # Remove input that contains RegEx parameters
        word_or_phrases = re.sub(r'[\$\^\*\(\)\+\|\\?\[\]\{\}]', '', word_or_phrase)
        
        """
        [6]
        
        Title: N/A
        Author: W3schools; freeCodeCamp
        Date: N/A
        Code version: N/A
        Availability: https://www.w3schools.com/python/ref_string_split.asp; https://www.freecodecamp.org/news/python-strip-how-to-trim-a-string-or-line/
        
        """
        # Split the input, and separate each word and (or) phrase so each can be found 
        for entered in word_or_phrases.split('/'):
            if entered == ' ': # Does not include blank spaces (not including blank space before or after words) 
                continue 
            elif entered == '': # Does not accept empty string if there is a / used without a word and (or) phrase behind it 
                continue
            to_find.append(entered) # Put word to be searched in this array

        if len(to_find) == 0: # The user left the input empty
            print(f'\n{Color.YELLOW}{Effect.BOLD}A blank cannot be searched; please try again{Effect.OFF}{Color.OFF}\n')
        else:
            break

        # If the user does not have correct input by the third attempt
        if attempts == 3:
            print('Terminating . . . ')
            exit()
            
    try:
        if '.txt' in file_name: # CHARDET
            line = []
            file = open(file_name, 'rb')
            for lines in file:
                """
                [7]
                
                Title: N/A
                Author: Olumide, S
                Date: April 10, 2023
                Code version: N/A
                Availability: https://www.freecodecamp.org/news/python-bytes-to-string-how-to-convert-a-bytestring/
                
                """
                lines = lines.decode() # To remove and translate remaining encoded values
                """ 
                [8]
                
                Title: N/A
                Author: Uriel
                Date: Jul. 17, 2017
                Availability: https://stackoverflow.com/questions/45142327/how-to-replace-multiple-matches-groups-with-regexes
                
                """
                
                """ Similar, but I don't think I directly referenced: https://stackoverflow.com/questions/53604478/python3-convert-apostrophe-unicode-string """
                convert = re.sub(r'[‘’“”—]', lambda c: {'‘': '\'', '’': '\'', '“': '"', '”': '"', '—': '--'}[c.group(0)], lines)
                line.append(convert)
            """
            [9]
            
            Title: N/A
            Author: Artifex Software
            Date: N/A
            Code version: N/A
            Availability: https://pymupdf.readthedocs.io/en/latest/the-basics.html; https://pymupdf.readthedocs.io/en/latest/document.html#Document.needs_pass
        
            """
        else:
            old_file = fitz.open(file_name)
            if old_file.needs_pass == True: # Used to open password protected files
                for attempts in range(1, 4):
                    pwd = input('\nThis file is password protected. Enter the password: ')
                    if old_file.authenticate(pwd) == 0:
                        print(f'\n{Color.YELLOW}{Effect.BOLD}This password is incorrect. The program will terminate after three inccorect attempts.{Effect.OFF}{Color.OFF}\n')
                    else:
                        break
                    if attempts == 3:
                        print('Terminating . . . ')
                        exit()
            new_file = open(extract_text_file, 'w') # Used to write text to new file (done similart to Artifex documentation)
            for page in old_file:
                """ Another reference to [8] """
                convert = re.sub(r'[‘’“”—]', lambda c: {'‘': '\'', '’': '\'', '“': '"', '”': '"', '—': '--'}[c.group(0)], page.get_text())
                new_file.write(convert)
            new_file.close()
            old_file.close()

            # Read the text (ignores images) from the original file format
            file = open(extract_text_file, 'r')
            """
            [10]
            
            Title: N/A
            Author: Pavithra B
            Date: May 9, 2020
            Code version: N/A
            Availability: https://stackoverflow.com/questions/55254230/how-to-find-the-length-of-the-file-in-python3
            
            """
            line = file.readlines()
            file.close()
    except FileNotFoundError:
            print(f'\n{Color.RED}FileNotFoundError: This file does not exist or is not in this directory{Color.OFF}\n')
            print('Terminating . . .')
            exit()
        
    total = [0] * len(to_find) # Creates index number based on how many words and (or) phrases to be searched     

    
    print(f'\n. . .\n')
    time.sleep(1)
    
    """
    [11]
    
    Title: N/A
    Author: Agrawal, R
    Date: Mar. 26, 2024
    Code Version: N/A
    Availability: https://www.naukri.com/code360/library/how-to-clear-a-screen-in-python
    
    """
    # Does not apply to IDLE
    if os.name == 'nt': # For a Windows OS
        os.system('cls')
    else: # For macOS or Linux
        os.system('clear')

    for j in range(os.cpu_count()): # Number of threads based on user's CPU
        # The start index for each thread
        lo_index = int ((j) * (len(line) / os.cpu_count())) # Total length of novel used so array of text can be searched
        # The end index for each thread
        hi_index = int ((j + 1) * (len(line) / os.cpu_count()))
        
        # What each thread is supposed to do
        t = Thread(target=search, args=(line, lo_index, hi_index, to_find, case_insensitive, queue, queue_two))
        t.start()
        t.join()
        
        """
        [12]
        
        Title: N/A
        Author: W3schools
        Date: N/A
        Code version: N/A
        Availability: https://www.w3schools.com/python/ref_func_map.asp; https://www.w3schools.com/python/trypython.asp?filename=demo_ref_map2
    
        """

        total = list(map(total_uses, (total), (queue.get()))) # Map used to add totals to total for result
        words_counted = words_counted + queue_two.get() # PDF seems to be the only file with a discrepancy in the words counted
    
    """
    [13]
    
    Title: N/A
    Author: Schneider, I; Melebius
    Date: May 24, 2012, Dec. 18, 2023
    Code version: N/A
    Availability: https://stackoverflow.com/questions/1823058/how-to-print-a-number-using-commas-as-thousands-separators
    
    """
    
    print('Words counted: ' + f'{words_counted:,}' + '\n') # This word count was compared to WordCounter.net

    for i in range(len(total)):
        frequency = (total[i] / words_counted) # Determine this for each index
        if total[i] > 1:
            print('\nWord or phrase: [' + str(to_find[i]) + ']\n')
            print('Number of uses: ' + str(total[i]) + ' times') # Display uses 
        else:
            print('\nWord or phrase: [' + str(to_find[i]) + ']\n')
            print('Number of uses: ' + str(total[i]) + ' time') # Display uses 
        """
        [14]
        Title: N/A
        Author: W3schools
        Date: N/A
        Code version: N/A
        Availability: https://www.w3schools.com/python/ref_func_round.asp
        
        """
        print('Relative frequency: ' + str(round(frequency, 5)) + ' or ' + str(round(frequency * 100, 4)) + '%\n') # Display frequency

        print('\n* * *\n')

    """
    [15]
    
    Title: N/A
    Author: RichieHindle; Feil, T
    Date: Aug. 9, 2011; Oct. 10, 2023
    Code version: N/A
    Availability: https://stackoverflow.com/questions/6996603/how-can-i-delete-a-file-or-folder-in-python
        
    """

    # Remove the file
    if os.path.isfile(extract_text_file):
        os.remove(extract_text_file)
