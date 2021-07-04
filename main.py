# Core Packages
import difflib
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog
import PyPDF2
from tkinter import filedialog
import torch
import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

# NLP Pkgs
from spacy_summarization import text_summarizer
from gensim.summarization import summarize
from nltk_summarization import nltk_summarizer

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Structure and Layout
window = Tk()
window.title("Summaryzer GUI")
window.geometry("700x400")
window.config(background='black')

style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition='wn', )

# TAB LAYOUT
tab_control = ttk.Notebook(window, style='lefttab.TNotebook')

tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

# ADD TABS TO NOTEBOOK
tab_control.add(tab3, text=f'{"Extractive":^20s}')
tab_control.add(tab2, text=f'{"Abstractive":^20s}')

label1 = Label(tab3, text='Extractive Summrize', padx=5, pady=5)
label1.grid(column=1, row=0)


label2 = Label(tab2, text='Abstractive Summrize',padx=5, pady=5)
label2.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')

def get_summary():
    model = T5ForConditionalGeneration.from_pretrained ('t5-small')
    tokenizer = T5Tokenizer.from_pretrained ('t5-small')
    device = torch.device ('cpu')
    text = str(url_display1.get('1.0', tk.END))
    preprocess_text = text.strip ().replace ("\n", "")
    t5_prepared_Text = "summarize: " + preprocess_text
    tokenized_text = tokenizer.encode (t5_prepared_Text, return_tensors="pt").to (device)

    summary_ids = model.generate (tokenized_text,
                                  num_beams=4,
                                  no_repeat_ngram_size=2,
                                  min_length=30,
                                  max_length=100,
                                  early_stopping=True)

    output = tokenizer.decode (summary_ids[0], skip_special_tokens=True)

    Str1 = text
    str2 = output
    printt = difflib.SequenceMatcher(None, Str1, str2, False).ratio() * 100

    edited = len(text)-len(output)
    Precision = (len(text)+len(output)+edited)/2
    Precisioncalc = Precision / 100

    result =("\n\nSummarized text: \n", output)," Precision = " , Precisioncalc  , " similarity = " , printt

    tab2_display_text.insert(tk.END, result)

def open_pdf():
    open_file = filedialog.askopenfilename(
        initialdir="C:/gui/",
        title="Open PDF File",
        filetypes=(
            ("PDF Files", "*.pdf"),
            ("All Files", ".")))

    if open_file:
        pdf_file = PyPDF2.PdfFileReader(open_file)
        page = pdf_file.getPage(0)
        page_stuff = page.extractText()
        io = page_stuff.split()
        url_display.insert(3.0, io)


def open_pdf1():
    open_file = filedialog.askopenfilename(
        initialdir="C:/gui/",
        title="Open PDF File",
        filetypes=(
            ("PDF Files", "*.pdf"),
            ("All Files", ".")))

    if open_file:
        pdf_file = PyPDF2.PdfFileReader(open_file)
        page = pdf_file.getPage(0)
        page_stuff = page.extractText()
        io = page_stuff.split()
        url_display1.insert(3.0, io)


def clear_display_result():
    tab3_display_text.delete('1.0', END)

# Clear For URL
def clear_url_entry():
    url_entry.delete(0, END)


# Open File to Read and Process
def openfiles():
    file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files", ".txt"), ("All files", "*")))
    read_text = open(file1).read()
    url_display.insert(tk.END, read_text)


def get_text():
    raw_text = str(url_entry.get())
    page = urlopen(raw_text)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    url_display.insert(tk.END, fetched_text)


def get_url_summary():
    raw_text = url_display.get('1.0', tk.END)
    final_text = text_summarizer(raw_text)
    result = '\nSummary:{}'.format(final_text)
    tab3_display_text.insert(tk.END, result)


def use_spacy ():

    raw_text = url_display.get('1.0', tk.END)
    final_text = text_summarizer(raw_text)
    print(final_text)

    Str1 = raw_text
    str2 = text_summarizer(raw_text)
    printt = difflib.SequenceMatcher(None, Str1, str2, False).ratio() * 100

    Precision = len(raw_text) + len(nltk_summarizer(raw_text)) / len(raw_text)
    Precisioncalc = Precision / 100
    result = '\nSpacy Summary:{}\n'.format(final_text)," Precision = " , Precisioncalc  , " similarity = " , printt
    tab3_display_text.insert(tk.END, result)


def use_nltk():
    raw_text = url_display.get ('1.0', tk.END)
    final_text = nltk_summarizer (raw_text)
    print (final_text)

    Str1 = raw_text
    str2 = nltk_summarizer(raw_text)
    printt = difflib.SequenceMatcher(None, Str1, str2, False).ratio() * 100

    Precision = len(raw_text) + len(nltk_summarizer(raw_text)) / len(raw_text)
    Precisioncalc = Precision / 100
    result = '\nNLTK Summary:{}\n'.format(final_text)," Precision = " , Precisioncalc  , " similarity  = " , printt
    tab3_display_text.insert(tk.END, result)

def use_gensim():
    raw_text = url_display.get ('1.0', tk.END)
    final_text = summarize(raw_text)
    print (final_text)
    Str1 = raw_text
    str2 = summarize(raw_text)
    printt = difflib.SequenceMatcher(None, Str1, str2, False).ratio() * 100

    Precision = len(raw_text) + len(nltk_summarizer(raw_text)) / len(raw_text)
    Precisioncalc = Precision / 100
    result ='\nGensim Summary:{}\n'.format(final_text)," Precision = " , Precisioncalc  , " similarity = " , printt
    tab3_display_text.insert(tk.END, result)


# URL TAB
l1 = Label(tab3, text="Enter URL To Summarize")
l1.grid(row=1, column=0)

raw_entry = StringVar()
url_entry = Entry(tab3, textvariable=raw_entry, width=50)
url_entry.grid(row=1, column=1)

# BUTTONS
button1 = Button(tab3, text="Reset", command=clear_url_entry, width=12, bg='#03A9F4', fg='#fff')
button1.grid(row=4, column=0, padx=10, pady=10)

button2 = Button(tab3, text="Get Text", command=get_text, width=12, bg='#03A9F4', fg='#fff')
button2.grid(row=4, column=1, padx=10, pady=10)

button3 = Button(tab3, text="Open File", width=12, command=openfiles, bg='#c5cae9')
button3.grid(row=5, column=0, padx=10, pady=10)

button4 = Button(tab3, text="Open PDF", width=12, command=open_pdf, bg='#c5cae9')
button4.grid(row=5, column=1, padx=10, pady=10)

button5 = Button(tab3, text="SpaCy", command=use_spacy, width=12, bg='red', fg='#fff')
button5.grid(row=8, column=0, padx=10, pady=10)

button6 = Button(tab3, text="Clear Result", command=clear_display_result, width=12, bg='#03A9F4', fg='#fff')
button6.grid(row=9, column=1, padx=10, pady=10)

button7 = Button(tab3, text="NLTK", command=use_nltk, width=12, bg='#03A9F4', fg='#fff')
button7.grid(row=8, column=1, padx=10, pady=10)

button8 = Button(tab3, text="Gensim", command=use_gensim, width=12, bg='#03A9F4', fg='#fff')
button8.grid(row=9, column=0, padx=10, pady=10)
# Display Screen For Result
url_display = ScrolledText(tab3, height=10)
url_display.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

tab3_display_text = ScrolledText(tab3, height=10)
tab3_display_text.grid(row=11, column=0, columnspan=3, padx=5, pady=5)



l1 = Label(tab2, text="Enter URL To Summarize")
l1.grid(row=1, column=0)

raw_entry1 = StringVar()
url_entry1 = Entry(tab2, textvariable=raw_entry, width=50)
url_entry1.grid(row=1, column=1)

# BUTTONS

button9 = Button(tab2, text="Reset", command=clear_url_entry, width=12, bg='#03A9F4', fg='#fff')
button9.grid(row=4, column=0, padx=10, pady=10)

button10 = Button(tab2, text="Get Text", command=get_text, width=12, bg='#03A9F4', fg='#fff')
button10.grid(row=4, column=1, padx=10, pady=10)

button11 = Button(tab2, text="Open File", width=12, command=openfiles, bg='#c5cae9')
button11.grid(row=5, column=0, padx=10, pady=10)

button12 = Button(tab2, text="Open PDF", width=12, command=open_pdf1, bg='#c5cae9')
button12.grid(row=5, column=1, padx=10, pady=10)

button13 = Button(tab2, text="Clear Result", command=clear_display_result, width=12, bg='#03A9F4', fg='#fff')
button13.grid(row=9, column=1, padx=10, pady=10)

button14 = Button(tab2, text="Abstract", command=get_summary, width=12, bg='#03A9F4', fg='#fff')
button14.grid(row=9, column=0, padx=10, pady=10)

url_display1 = ScrolledText(tab2, height=10)
url_display1.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

tab2_display_text = ScrolledText(tab2, height=10)
tab2_display_text.grid(row=11, column=0, columnspan=3, padx=5, pady=5)

window.mainloop()

