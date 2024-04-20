# SnapchatHTML
SnapchatHTML Extractor and Organizer
Take your SnapChat conversation HTML and input the filename into the program and it will read through, remove most unneccesary bits, reorder from oldest to newest, and convert names at the same time, if you wish.

    html_file_name = "Conversationhtml.html"
    
    delete_text_saved_lines() also converts names through ELIF statements.
    
    if line == 'dray-cyber':
        f_out.write('Insert-Whatever-I-Want-To-Be-Called: \n')
        #Repeat or delete depending on how many people.

After removing useless data there is a bunch of spaces, but to leave the txt readable we need to leave some, so in process_file() we check against an array of names. "names = ['jake', 'pookie', 'etc']" put the names of the people in the conversation. Now that you have the html name inserted and the names inserted run the program and it will do the rest.

This program also converts time stamps. Say "2023-10-16 13:25:32 UTC" to "2023-10-16 13:25:32 UTC \ October 16, 2023 1:25:32 PM" for easier reading.
