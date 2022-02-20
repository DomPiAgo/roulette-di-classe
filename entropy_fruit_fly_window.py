#!/usr/bin/python
# -*- coding: utf-8 -*-
from Bio import Entrez
from Bio import SeqIO
import pandas as pd
from scipy.stats import entropy
from textwrap import wrap

import PySimpleGUI as sg

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")

def evaluate_entropy(name,chunksize=100000):
    # Entropia degli acidi nucleici nel DNA del moscerino della frutta
    # https://www.ncbi.nlm.nih.gov/data-hub/taxonomy/7227/
    Entrez.email = 'melanogaster@drosophila.an'

    # Sequenze DNA di riferimento https://www.ncbi.nlm.nih.gov/genome/47
    handle = Entrez.esearch(db='nuccore',term=name)
    record = Entrez.read(handle)
    handle.close()

    id_chromosome = (record['IdList'])[0]

    handle = Entrez.efetch(db='nuccore', rettype='fasta', retmode='text', id=id_chromosome)
    chromosome = SeqIO.read(handle, 'fasta')
    handle.close()

    totalcounts_nucleobases  = None
    entropyarray = {}
    i=0
    for dna_subseq in wrap(str(chromosome.seq), chunksize):
        dna_series = pd.Series(list(dna_subseq))
        counts_nucleobases = dna_series.value_counts().drop(labels=['N'],errors='ignore')
        entropyarray[i]=entropy(counts_nucleobases, base=2)
        i += chunksize
        if totalcounts_nucleobases is None:
            totalcounts_nucleobases = counts_nucleobases
        else:
            totalcounts_nucleobases = totalcounts_nucleobases.add(counts_nucleobases, fill_value=0)

    return { 'description' : chromosome.description,
             'entropy' : entropyarray,
             'totalentropy' : entropy(totalcounts_nucleobases, base=2) }
    
def main():
    fruit_fly_chromosomes = {'Chromosome X'  : 'NC_004354.4',
                             'Chromosome 2L' : 'NT_033779.5',
                             'Chromosome 2R' : 'NT_033778.4',
                             'Chromosome 3L' : 'NT_037436.4',
                             'Chromosome 4'  : 'NC_004353.4',
                             'Chromosome 3R' : 'NT_033777.3',
                             'Chromosome Y'  : 'NC_024512.1'}

    menu_def = [['&File', ['&Start',
                           [ 'Drosophila Melanogaster',
                             list(fruit_fly_chromosomes.keys()),
                             '---', 'COVID-19'
                             ],'---', 'E&xit']],
                    ['&Help', '&About...']]

    sg.theme('SystemDefault')

    layout = [[sg.Menu(menu_def,key='-MENU-')],
              [sg.Text(size=(50,1), font=('Helvetica', 20), key='-DESCRIPTION-'),sg.Text(size=(30,1), font=('Helvetica', 20), key='-ENTROPY-')],
              [sg.Canvas(size=(1280, 720), key='-CANVAS-')],
              [sg.Slider(range=(1, 100000), default_value=100000, size=(100, 10), orientation="h",enable_events=True, key="-SLIDER-")]]

    window = sg.Window("Entropy Fruit Fly", layout,  return_keyboard_events=True, use_default_focus=False,
                     resizable=True, element_justification='c', finalize=True)
    window['-SLIDER-'].bind('<ButtonRelease-1>', ' Release')
    #window.Maximize()
    running = False
    # ---===--- Loop taking in user input --- #
    while True:
        event, values = window.read(timeout=100)

        if event in (sg.WIN_CLOSED, 'Exit'):
            sg.popup_animated(None)
            break
        #print(event, values)
        if event == 'About...':
            sg.popup('Entropy Drosophila Melanogaster', 'Version 1.1', '© Davide Cerizza')
        if 'Chromosome' in event:
            window['-DESCRIPTION-'].update(fruit_fly_chromosomes[event])
            event = '-SLIDER- Release'
        if event == 'COVID-19':
            window['-DESCRIPTION-'].update('NC_045512.2')
            event = '-SLIDER- Release'
        if event == '-SLIDER- Release' and not running and window['-DESCRIPTION-'].get() != '' :
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, message='Wait..',text_color='black',
                              background_color='white', transparent_color='white',
                              time_between_frames=100)
            running = True
            window['-SLIDER-'].update(disabled=True)
            window.perform_long_operation(
                lambda : evaluate_entropy((window['-DESCRIPTION-'].get().split())[0]
                                          ,int(values['-SLIDER-'])), '-OPERATION DONE-')         
        elif event  == '-OPERATION DONE-':
            sg.popup_animated(None)
            running = False
            window['-SLIDER-'].update(disabled=False)

            if 'figure_canvas_agg' in locals():
                figure_canvas_agg.get_tk_widget().forget()
            plt.close('all')

            plt.figure(1, facecolor="#F0F0F0", figsize=[12.8,7.20])
            plt.xlim(0, list((values[event])['entropy'].keys())[-1])
            plt.step((values[event])['entropy'].keys(), (values[event])['entropy'].values())
            plt.ylabel("Entropy")
            plt.grid(color='b', linestyle='--', linewidth=0.5)

            figure_canvas_agg = FigureCanvasTkAgg(plt.gcf(), window['-CANVAS-'].TKCanvas)
            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
            
            window['-DESCRIPTION-'].update((values[event])['description'])
            window['-ENTROPY-'].update('Nucleobases Entropy = %.10f' % (values[event])['totalentropy'])
            
        if running:
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, message='Wait..',text_color='black',
                              background_color='white', transparent_color='white',
                              time_between_frames=100)
    window.close()

if __name__ == '__main__':
    main()
