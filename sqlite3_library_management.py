from sample_books import sample_books
import os
from datetime import datetime
import time
import keyboard

import sqlite3 

class Book:
    def  __init__(self,title,author,ISBN,status):  #,status
        self.title=title
        self.author=author
        self.ISBN=ISBN
        self.status="Available"

    def  __str__(self):
        return f'{self.title}, {self.author}, {self.ISBN}, {self.status}\n\n'


class Library:
    def  __init__(self,library_name):
        self.library_name=library_name
        self.list_all_books=[]
        self.list_book_in_library=[]
        self.list_of_borrowed_books=[]

        self.clients_list=[]

    def display_books_in_library(self):
        now=datetime.now()
        formatted_datetime=now.strftime("%H:%M:%S  %d-%m-%Y")
        self.list_book_in_library.sort(key=lambda book: book.title)
        display_book_text=""
        counter=0
        for book in self.list_book_in_library:
            counter+=1
            #display_book_text+=f'│{counter:3}│-{book.title:45}│{book.author:25}│{book.ISBN:20}│{book.status}  │\n├─────────────────────────────────────────────────────────────────────────────────────────────────────────────┤\n'
            display_book_text+=f'│{counter:3}│-{book.title:45}│{book.author:25}│{book.ISBN:20}│{book.status}  │\n├-------------------------------------------------------------------------------------------------------------┤\n'

        title_text=f"\nBooks in the Library:{self.library_name} TIME DATE: {formatted_datetime} "
            
        header_0="┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐" 
        
        header="│No.|Book Name                                     │Author                   │ISBN                │STATUS     │"
        between_text="├─────────────────────────────────────────────────────────────────────────────────────────────────────────────┤"
        #between_text="├─------------------------------------------------------------------------------------------------------------┤"
        
        last_text="└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘"
        
        
     
        print(title_text)
        print(header_0)
        print(header)
        print(between_text)
        print(display_book_text)
        print(last_text)

    def display_borrowed_books(self):
        display_borrowed_books_text=""
        counter=0
        for book in self.list_of_borrowed_books:
            counter+=1
            display_borrowed_books_text+=f'│{counter:3}│{book[0]:45}│{book[1]:21}│{book[2]:5}          │\n├───────────────────────────────────────────────────────────────────────────────────────┤\n'
        header_0="┌───────────────────────────────────────────────────────────────────────────────────────┐"  
            
        header="│No.│Book Name                                    │Borrowed Person      │Duration (days)│"

        between_text="├───────────────────────────────────────────────────────────────────────────────────────┤"
        last_text="└───────────────────────────────────────────────────────────────────────────────────────┘"

        
        print(header_0)
        print(header)
        print(between_text)
        print(display_borrowed_books_text)

    def add_new_book_to_library(self,book):
        if book.title in self.list_book_in_library:                 #self.list_all_books:
            print(f'THE BOOK {book} is already in library')
            return

        else:
            self.list_all_books.append(book)
            self.list_book_in_library.append(book)
            return self.list_all_books
            #print(f'the book : {book.title} added to library')

    def remove_a_book_from_library(self,book):
        if book not in self.list_all_books:
            print('that book does not in the library')
            return
        else:
            self.list_all_books.remove(book)
            
            print(f'the book : {book.title} removed from library')

    def borrow_a_book(self,book,who_borrowed,borrow_duration):

        if book not in self.list_book_in_library:
            print('This book is borrowed ')

        elif book not in self.list_all_books:
            print('This book is not in the Library')

        else:
            
            self.list_of_borrowed_books.append((book.title,who_borrowed,borrow_duration))
            book.status='Borrowed'
            self.list_book_in_library.remove(book)

    def return_book_to_library(self,duration_passed=0):
        books_to_return = []
        updated_borrowed_books=[]

        for book_tuple in self.list_of_borrowed_books:
            book, who_borrowed, borrow_duration = book_tuple
            borrow_duration -= duration_passed

            if borrow_duration <= 0:
                print(f'{book} duration is over')
                books_to_return.append(book_tuple)

            # Find the book object in the list_all_books
                for book_obj in self.list_all_books:
                    if book_obj.title == book:
                        book_obj.status = 'Available'
                        self.list_book_in_library.append(book_obj)
                        break
            else:
                #book_tuple = (book, who_borrowed, borrow_duration)
                updated_borrowed_books.append((book,who_borrowed, borrow_duration))

        for book_tuple in books_to_return:
            self.list_of_borrowed_books.remove(book_tuple)

        self.list_of_borrowed_books=updated_borrowed_books


    def client_add(self,date,who_borrowed,client_borrowed_book,client_email,client_tel):
 
        client_data=[date,who_borrowed,client_borrowed_book,client_email,client_tel]
        self.clients_list.append((client_data))

    def show_clients_info(self):
        text_client=""
        counter=0
        for client in self.clients_list:
            counter+=1
            text_client+=f'│{counter:3}│{client[0]:16}│{client[1]:43}│{client[2]:45}│{client[3]:25}│{client[4]:17}│\n'

        header_0="┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐"
        header="│No.│DATE            │CLIENT NAME                                │BORROWED BOOK                                │CLIENT EMAIL             │CLIENT TEL       │"
        print(header_0)
        print(header)
        print(text_client)
    

 #--------------------------- END OF CLASSES--------------------------------            


        

def add_start_books(library):
    for book in sample_books:
        library.add_new_book_to_library(Book(*book))

def add_new_book(library): #added database 
    new_book_title=input('Book Title: ? ')
    new_book_writer=input('The Author ?')
    new_book_ISBN=input('ISBN Number ?')
    new_book_status='Available'

    header=f"""┌─────────────────────────────────────────────────┐
│Book Title:{new_book_title:35}   │
│Book Writer:{new_book_writer:25}            │
│Book ISBN:{new_book_ISBN:25}              │    
└─────────────────────────────────────────────────┘"""
    print(header)
    new_book_entry_confirmation=input('Is this information True ? (y/n)')
    if new_book_entry_confirmation=='y':

        

        new_book=Book(new_book_title,new_book_writer,new_book_ISBN,new_book_status)
        
        if new_book.title in library.list_book_in_library:
            print('this book already in the library')
            return

        else:

        
            library.add_new_book_to_library(new_book)

            conn=sqlite3.connect('library_database.db')
            c=conn.cursor()
            c.execute("INSERT INTO Books (TITLE,AUTHOR,ISBN,STATUS) VALUES(?,?,?,?)",(new_book_title,new_book_writer,new_book_ISBN,new_book_status))
            conn.commit()
            conn.close()


        
        print(f' {new_book_title} is registered to the library')
        time.sleep(2)
        clear_screen()
        return
    elif new_book_entry_confirmation=='n':
        return 




def remove_a_book_from_library(library):
    
    library.display_books_in_library()
    
    book_to_remove_index=int(input(' which book will be removed from the library ? 0 for main menu '))

    if book_to_remove_index==0:
        return 
    library.remove_a_book_from_library(library.list_all_books[book_to_remove_index-1])



def borrow_a_book(library):
    library.display_books_in_library()
    now=datetime.now()
    formatted_time=now.strftime("%H:%M:%S")
    formatted_date=now.strftime("%d-%m-%Y")

    while True:
        try:
            index_book_to_borrow=int(input('Book number ?:  '))
            if index_book_to_borrow<1 or index_book_to_borrow>len(library.list_book_in_library):
                raise ValueError
            break
        except ValueError:
            print('invalid selection integer between 1-{len(library.list_book_in_library}')
        
              
    who_want_to_borrow=input('Client Name     ')
    borrow_duration=int(input('Duration ?   '))
    client_email=input('Clients Email ? ')
    client_tel=input('Client Tel' )
    conn=sqlite3.connect('library_database.db')
    c=conn.cursor()
    c.execute("INSERT INTO Clients (DATE,CLIENT_NAME,BORROWED_BOOK,EMAIL,CLIENT_TEL) VALUES (?,?,?,?,?)",(formatted_date,who_want_to_borrow,library.list_book_in_library[index_book_to_borrow-1].title,client_email,client_tel))
    conn.commit()
    conn.close()
              

    library.client_add(formatted_date,who_want_to_borrow,library.list_book_in_library[index_book_to_borrow-1].title,client_email,client_tel)
    library.borrow_a_book(library.list_book_in_library[index_book_to_borrow-1],who_want_to_borrow,borrow_duration)

 

def display_borrowed_books(library):
    library.display_borrowed_books()


def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')


def save_to_file(library):
    file_name=input('Enter a File Name 0 for cancel')
    if file_name=='0':
        return 
    file_name=file_name+'.txt'
    save_file=open(file_name,'w')
    library.list_book_in_library.sort(key=lambda book: book.title)
    
    for book in library.list_book_in_library:
        save_file.write(str(book))

    save_file.close()

def show_client_record(library):
    library.show_clients_info()



def quit_program():
    clear_screen()
    ask_to_quit=input("""
┌──────────────────────────────────┐
│ Are you sure to Quit ? (y/n)     │ 
├──────────────────────────────────┤
└──────────────────────────────────┘""")

    if ask_to_quit=='y':
        return True 

    elif ask_to_quit=='n':
        return False 
    else:
        print('invalid option just y or no')
        return False  

def create_database():
    clear_screen()
    ask_to_create=input('are you sure to create a new database ?')
    if ask_to_create=='y':
        conn=sqlite3.connect('library_database.db')
        c=conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Books(TITLE,AUTHOR,ISBN,STATUS)")
        c.execute("CREATE TABLE IF NOT EXISTS Clients(DATE,CLIENT_NAME,BORROWED_BOOK,EMAIL,CLIENT_TEL)")
        conn.commit()
        conn.close()
    else:
        return

def insert_first_books(library):

    try:
        
        conn=sqlite3.connect('library_database.db')
        c=conn.cursor()
        for book in sample_books:
            c.execute("INSERT INTO Books VALUES(?,?,?,?)",book)

        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(f'Error {e}')
                  
    

def print_top(menu_text):
    rows, columns = os.get_terminal_size()

    # Print the menu at the top of the screen
    print(menu_text.center(columns))

    # Move the cursor to the bottom of the menu
    menu_rows = menu_text.count('\n') + 1
    print('\033[{};1H'.format(menu_rows + 1), end='')

    # Return the row number where the next output should start
    return menu_rows + 1


    

#MY LIBRARY 

my_library=Library('CITY LIBRARY')

add_start_books(my_library)


duration=0


    

menu_text=f""" 
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                                         MENU OPTIONS                                      │ 
├───────────────────────────────────────────────────────────────────────────────────────────┤
│1- Display Books in The Library   │ 7-Save to File          │                              │
│2- Add New Book to the Library    │ 8-Show Client Record    │                              │
│3- Remove a Book from the Library │ 9-Clear Screen          │                              │
│4- Borrow a Book                  │ 10-Quit Program         │                              │
│5- Borrowed Books                 │ 11-Create Database      │                              │  
│6- Pass Turn                      │ 12-Insert First Books   │                              │
│                                  │ 13-                     │                              │
│                                  │                         │                              │
└───────────────────────────────────────────────────────────────────────────────────────────┘
"""




#MAIN LOOP 
while True:
    
    print(menu_text)
    user_choice = input('selection: ').strip()
    
    #menu=print_top(menu_text)
    
    if user_choice=='1':

        clear_screen()
        my_library.display_books_in_library()
    
    elif user_choice=='2':
        clear_screen()
        add_new_book(my_library)

    elif user_choice=='3':
        clear_screen()
        remove_a_book_from_library(my_library)
        clear_screen()

    elif user_choice=='4':
        clear_screen()
        borrow_a_book(my_library)

    elif user_choice=='5':
        clear_screen()
        my_library.display_borrowed_books()

    elif user_choice=='6':
        clear_screen()
        my_library.display_books_in_library()
        my_library.display_borrowed_books()
        duration+=1
        my_library.return_book_to_library(1)

    elif user_choice=='7':
        save_to_file(my_library)

    elif user_choice=='8':
        clear_screen()
        show_client_record(my_library)

    elif user_choice=='9':
        clear_screen()
        

    elif user_choice=='10':
        if quit_program():
            break
        else:
            clear_screen()

    elif user_choice=='11':
        create_database()

    elif user_choice=='12':
        insert_first_books(my_library)
        
    
            
    else:
        print ('Invalid Selection')

    #print('\033[{};1H'.format(starting_row + 3), end='')
         

