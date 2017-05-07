#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [NB: Il 7.3.2017 ho aggiunto alcune righe inutili, segnate con #debug.
#  Cancellale quando ho finito di lavorare sul file di Edoardo.]
#
# Questo script rinomina il file e opera i cambiamenti di base per
# esportare un file XML/TEI di fonti documentarie
# da ALIM1 ad ALIM2 livello 0
#
# Come si usa:
# 1) Crea una directory 'versioni_originarie' nella cartella di lavoro
# 2) Metti in quella cartella i file .xml da editare
# 3) Fai girare lo script
#
# È scritto in Python 3.4, ma funziona anche in Python 2.7
# per via del modulo __future__
# from __future__ import print_function
#
# Dovrebbe funzionare in Linux. Non l'ho testato in OSX o
# in altri sistemi operativi meno funzionali.
#
# Nella variabile 'prefix' ho messo il prefisso con unità,
# responsabile e livello di codifica: il suo valore va cambiato
# se un'altra unità di ricerca usa lo script.

####################################
# IMPORTA MODULI E SETTA VARIABILI #
####################################

from __future__ import print_function
import os
import sys
import re
import glob
import subprocess
import xml.etree.ElementTree as ET

# Sigla per unità, responsabile e livello di codifica nel nome del file
prefix = '[PA-PM-0]'

# Clear screen
#os.system('clear')
subprocess.call(['clear'])




#####################################
# FUNZIONE CHE EDITA I SINGOLI FILE #
#####################################

def alim2fyDoc (myInputFile):
    """ Questa funzione usa il modulo ElementTree per editare il DOM """

    with open(myInputFile) as myI:

        print('Sto lavorando sul file ' + myInputFile)

        # Il namespace
        n = '{http://www.tei-c.org/ns/1.0}' 
        ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        # Elemento root (teiCorpus)
        tree = ET.parse(myInputFile)
        root = tree.getroot()

        ######################
        # TEIHEADER RACCOLTA #
        ######################

        # Titolo della raccolta
        corpusTitle = tree.findtext(n+'teiHeader/'+n+'fileDesc/'+n+'titleStmt/'+n+'title')
        if 'Arezzo' in corpusTitle: 
            corpusTitleOnly, corpusTitleVolume = corpusTitle.split(' vol. ')
        else:
            corpusTitleOnly, corpusTitleVolume = corpusTitle.split(' - ')

        # Copertura cronologica della raccolta
        corpus_notesStmt = tree.find(n+'teiHeader/'+n+'fileDesc/'+n+'notesStmt')
        for c_note in corpus_notesStmt.findall(n+'note'):
            if c_note.text.startswith('Copertura cronologica da: '):
                coperTextDa = c_note.find(n+'date').text
                coperAttrDa = c_note.find(n+'date').get('when')
                corpus_notesStmt.remove(c_note)
            elif c_note.text.startswith('Copertura cronologica a: '):
                coperTextA = c_note.find(n+'date').text
                coperAttrA = c_note.find(n+'date').get('when')
                corpus_notesStmt.remove(c_note)
                cop = ET.SubElement(corpus_notesStmt, 'note')
                cop.text = 'Copertura cronologica della raccolta: '
                cop_data = ET.SubElement(cop, 'date')
                cop_data.set('from', coperAttrDa)
                cop_data.set('to', coperAttrA)
                cop_data.text = coperTextDa + '-' + coperTextA

        # Curatori nel teiHeader della raccolta: rimuovo 'author' da 'titleStmt'
        corpus_titleStmt = tree.find(n+'teiHeader/'+n+'fileDesc/'+n+'titleStmt')
        ct_author = corpus_titleStmt.find(n+'author')
        corpus_titleStmt.remove(ct_author)

        for ctr in corpus_titleStmt.findall(n+'respStmt'):
            # TeiHeader della raccolta: rimuovo un 'respStmt' ridondante 
            if ctr.find(n+'resp').text == 'compilato da':
                corpus_titleStmt.remove(ctr)
            # TeiHeader della raccolta: cambio il contenuto del 'respStmt' rimanente
            elif ctr.find(n+'resp').text == 'curato da':
                ctr.find(n+'resp').text = 'Edizione a stampa di riferimento curata da'

        # Aggiungo un respStmt per i curatori dell'edizione digitale
        curDigElem = ET.SubElement(corpus_titleStmt, 'respStmt')
        ET.SubElement(curDigElem, 'resp').text = 'Esportazione in formato TEI XML livello 0 effettuata da'
        moschettieri = ['Edoardo Ferrarini', 'Paolo Monella', 'Roberto Rosselli Del Turco']
        for moschettiere in moschettieri:
            ET.SubElement(curDigElem, 'name').text = moschettiere

        # Rimuovo un elemento 'author' ridondante (e semanticamente scorretto)
        corpus_sourceDesc_bibl = tree.find(n+'teiHeader/'+n+'fileDesc/'+n+'sourceDesc/'+n+'bibl')
        corpus_sourceDesc_bibl.remove(corpus_sourceDesc_bibl.find(n+'author'))

        # Aggiungo un paragrafo al publicationStmt del corpus per chiarire che si tratta dell'edizione digitale ALIM
        corpus_publicationStmt = tree.find(n+'teiHeader/'+n+'fileDesc/'+n+'publicationStmt')
        ET.SubElement(corpus_publicationStmt, 'p').text = 'Prima edizione digitale ALIM'

        ###############################
        # TEIHEADER SINGOLI DOCUMENTI #
        ###############################

        for d in root.findall(n+'TEI'): 

            # Ri-aggiungo l'attributo @xmlns anche ai singoli elementi TEI
            # (dato che tree.write lo aggiunge solo al root element)
            d.set('xmlns', 'http://www.tei-c.org/ns/1.0')

            # Gli elementi 'note' del documento
            notesStmtElem = d.find(n+'teiHeader/'+n+'fileDesc/'+n+'notesStmt')
            notes = notesStmtElem.findall(n+'note')
            for note in notes:
                nt = note.text

                # Estrae numero di volume e numero del documento all'interno del volume
                doc_title_elem = d.find(n+'teiHeader/'+n+'fileDesc/'+n+'titleStmt/'+n+'title')
                if nt.startswith('Segnatura: '):
                    if 'Arezzo' in corpusTitle: 
                        numDoc = doc_title_elem.text
                        volDoc = corpusTitleVolume
                    else:
                        testo_segn, segn = nt.split(': ')
                        volDoc, numDoc = segn.split('.')
                        notesStmtElem.remove(note)
                    print('corpusTitleOnly: '+corpusTitleOnly)  # debug
                    print('volume: ' + volDoc)  # debug
                    print('documento n.:', end=' ')
                    print(numDoc)  # debug
                    new_doc_title = corpusTitleOnly +', volume ' + volDoc + ', documento n. ' + numDoc
                    doc_title_elem.text = new_doc_title

                # Controlla la certezza della data
                if   nt == u'Certezza data: sì':
                    certData = 'high'
                    notesStmtElem.remove(note)
                elif nt == u'Certezza data: ':
                    certData = 'low'
                    notesStmtElem.remove(note)

                # Controlla la certezza del luogo
                if   nt == u'Certezza luogo: sì':
                    certLuogo = 'high'
                    notesStmtElem.remove(note)
                elif nt == u'Certezza luogo: ':
                    certLuogo = 'low'
                    notesStmtElem.remove(note)

                # Cancella le note vuote
                if nt == u'Regesto: ' or nt == u'Note: ' or nt == u'Natura: ':
                    notesStmtElem.remove(note)

            # respStmt in titleStmt del documento
            titleStmtElem = d.find(n+'teiHeader/'+n+'fileDesc/'+n+'titleStmt')
            resps = titleStmtElem.findall(n+'respStmt')
            for resp in resps:
                if resp.find(n+'resp').text == 'compilato da':
                    resp.find(n+'resp').text = 'Edizione digitale ALIM a cura di'
                    # Se il curatore dell'edizione digitale non c'è, inserisce il valore 'Sconosciuto'
                    if resp.find(n+'name').text == None: 
                        resp.find(n+'name').text = 'Sconosciuto'
                   #titleStmtElem.remove(resp)
                elif resp.find(n+'resp').text == 'curato da':
                    resp.find(n+'resp').text = 'Edizione a stampa di riferimento curata da'

            # sourceDesc del documento
            sd  = d.find(n+'teiHeader/'+n+'fileDesc/'+n+'sourceDesc') # sd = sourceDesc
            sdb = sd.find(n+'bibl')     # sdb = il sourceDesc/bibl esistente

            # crea i due nuovi bibl:
            # il bibl per l'edizione a stampa di riferimento
            p_sdb = ET.SubElement(sd, 'bibl')
            p_sdb.set('type', 'edizioneAStampaDiRiferimento')
            p_sdb.append(sdb.find(n+'title'))

            #doc_respStmt = p_sdb.append(corpus_sourceDesc_bibl.find(n+'respStmt')) # Viene dal tei Header del corpus
            p_sdb.append(corpus_sourceDesc_bibl.find(n+'respStmt')) # Viene dal tei Header del corpus
            p_sdb.find(n+'respStmt/'+n+'resp').text = 'Edizione a stampa di riferimento curata da' # aggiunta §

            p_sdb.append(corpus_sourceDesc_bibl.find(n+'pubPlace')) # Questo viene dal tei Header del corpus
            p_sdb.append(corpus_sourceDesc_bibl.find(n+'date')) # Questo viene dal tei Header del corpus
            doc_biblScope = sdb.find(n+'biblScope')
            doc_biblScope.set('unit', 'pp')
            p_sdb.append(doc_biblScope)

            # il bibl per il documento medievale
            o_sdb = ET.SubElement(sd, 'bibl')
            o_sdb.set('type', 'documentoMedievale')
            o_pubPlace = sdb.find(n+'pubPlace')
            o_pubPlace.set('cert', certLuogo)
            o_sdb.append(o_pubPlace)

            # Aggiusta la data del sourceDesc del documento e inseriscila nel bibl per il documento medievale
            ddd = sdb.findall(n+'date')     # ddd = le Due Date del Documento (iniziale e finale). È una lista
                                            # che dovrebbe includere due (e solo due) elementi 'date'
            if ddd[0].get('when') == ddd[1].get('when'):
                # Se le due date sono uguali (il che probabilmente avviene sempre), usa solo la prima delle due.
                # Non ho potuto dare semplicemente o_sdb.append(ddd[0]) perché altrimenti si portava dietro
                # il trattino finale.
                o_date = ET.SubElement(o_sdb, 'date')
                # Aggiunge il contenuto 'Data sconosciuta' se l'elemento 'date' è vuoto
                if ddd[0].text == None: 
                    o_date.text = 'Data sconosciuta'
                    o_date.set('when', '0000')
                    o_date.set('cert', certData)
                else:
                    o_date.text = ddd[0].text
                    o_date.set('when', ddd[0].get('when'))
                    o_date.set('cert', certData)
            else:
                # Se non lo sono, aggiungile entrambe, con @from e @to
                print('La data d\'inizio e quella di fine del documento non corrispondono: ' + new_doc_title)
                for myDate in ddd:
                    if myDate.text == None: 
                        myDate.text = 'Data sconosciuta'
                        myDate.set('when', '0000')
                o_date = ET.SubElement(o_sdb, 'date')
                if ddd[0].get('when') == '0000' or ddd[1].get('when') == '0000':
                    o_date.set('cert', certData)
                else:
                    o_date.set('cert', certData)
                o_date.set('from', ddd[0].get('when'))
                o_date.set('to'  , ddd[1].get('when'))
                o_date.text = ddd[0].text + '-' + ddd[1].text


            # Cancella il 'bibl' originario
            sd.remove(sdb)

            # Aggiungo un paragrafo al publicationStmt del doc. per chiarire che si tratta dell'edizione digitale ALIM
            doc_publicationStmt = d.find(n+'teiHeader/'+n+'fileDesc/'+n+'publicationStmt')
            ET.SubElement(doc_publicationStmt, 'p').text = 'Prima edizione digitale ALIM'
            


    # Archivia il file di input originario (esportato dallo "strumentino" di ALIM1
    # senza nessuna modifica), con 1.0 alla fine del nome file:
    #os.rename(myInputFile, prefix + ' ' + corpusTitle + '_v1.0.xml')

    # Dà al file modificato il suo nuovo nome (con v3.0 alla fine)
    myOutputFile = prefix + ' ' + corpusTitle + '_v3.0.xml'
    tree.write(myOutputFile, encoding="UTF-8", method="xml")
    
    # Controlla se il file è valido
    #subprocess.call([ 'xmllint', '--noout', '--dtdvalid', '/home/ilbuonme/alim/12/ursus/DTD/tei_all.dtd', newFN])
    #print('Il file è valido\n')
    
    # Quando l'utente dà invio, apre il file per il controllo finale
    #choice = raw_input('Inserisci invio per vedere il file in VIM e fare il controllo finale')
    #subprocess.call([ 'vim', newFN])


################################################
# IMPORTA I FILE DI INPUT E LANCIA LE FUNZIONI #
################################################
# File di input. Fa la trasformazione su ogni file contenuto
    # nella cartella il cui nome inizi con TEI, dato che i nomi dei file esportati
    # dallo "strumentino" sono del tipo TEI20151211160351.xml

for f in glob.glob('versioni_originarie/*xml'):
    alim2fyDoc(f)