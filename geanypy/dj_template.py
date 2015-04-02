#!/usr/bin/env python
# -*- coding: utf-8 -*-

import geany
import scintilla_constants as sc
import scilexer_constants as scl
import re

DJANGO_VARIABLE_INDICATOR = 19
DJANGO_TAG_INDICATOR = 20
DJANGO_COMMENT_INDICATOR = 21
VARIABLE_REGEX = re.compile(r'\{\{.*?\}\}')
TAG_REGEX = re.compile(r'\{\%.*?\%\}')
COMMENT_REGEX = re.compile(r'\{\#.*?\#\}')
SCLEX_HTML = 4


class DjangoTemplatePlugin(geany.Plugin):
    __plugin_name__ = 'Django Teplate'
    __plugin_version__ = '0.0.1'
    __plugin_description__ = 'A little crutch for support Django templates (highlight {{}} and {%%})'
    __plugin_author__ = 'Alexandr Nagovitsyn <gejzenbug@gmail.com>'

    def __init__(self):
        #self.
        geany.signals.connect('document_open', self.on_open_file)
        geany.signals.connect('editor-notify', self.on_notify)

    def cleanup(self):
        pass

    def on_open_file(self, signal_manager, document):
        sci = document.editor.scintilla
        lex = sci.send_message(sc.SCI_GETLEXER)
        
        if lex == SCLEX_HTML:
            #print "THIS IS HTML!"
            for line in xrange(sci.get_line_count()):
                self.mark_tags_in_line(sci, line)
        
    def document_is_djtemplate(self, document):
        return True

    def on_notify(self, obj, editor, nt):
        sci = editor.scintilla
        lex = sci.send_message(sc.SCI_GETLEXER)
        if lex == SCLEX_HTML:
            #print nt.nmhdr.code
            if nt.nmhdr.code == sc.SCN_UPDATEUI:
                #if nt.modification_type == sc.SC_MOD_INSERTTEXT or nt.modification_type == sc.SC_MOD_DELETETEXT: 
                line = sci.get_current_line()
                sci.indicator_clear(sci.get_position_from_line(line), 
                                    sci.get_line_length(line))
                self.mark_tags_in_line(sci, line)

    def mark_tags_in_line(self, sci, line):
        for tag in TAG_REGEX.finditer(sci.get_line(line)):
            sci.send_message(sc.SCI_SETINDICATORCURRENT, DJANGO_TAG_INDICATOR, 0);
            sci.send_message(sc.SCI_INDICSETSTYLE, DJANGO_TAG_INDICATOR, sc.INDIC_CONTAINER);
            sci.send_message(sc.SCI_INDICSETFORE, DJANGO_TAG_INDICATOR, 0xFF8300);
            sci.send_message(sc.SCI_INDICSETALPHA, DJANGO_TAG_INDICATOR, 100);
            sci.send_message(sc.SCI_INDICATORFILLRANGE, 
                             sci.get_position_from_line(line) + tag.start(), 
                             len(tag.group()));
        
        for var in VARIABLE_REGEX.finditer(sci.get_line(line)):
            sci.send_message(sc.SCI_SETINDICATORCURRENT, DJANGO_VARIABLE_INDICATOR, 0);
            sci.send_message(sc.SCI_INDICSETSTYLE, DJANGO_VARIABLE_INDICATOR, sc.INDIC_CONTAINER);
            sci.send_message(sc.SCI_INDICSETFORE, DJANGO_VARIABLE_INDICATOR, 0x0083FF);
            sci.send_message(sc.SCI_INDICSETALPHA, DJANGO_VARIABLE_INDICATOR, 100);
            sci.send_message(sc.SCI_INDICATORFILLRANGE, 
                             sci.get_position_from_line(line) + var.start(), 
                             len(var.group()));
                             
        for comment in COMMENT_REGEX.finditer(sci.get_line(line)):
            sci.send_message(sc.SCI_SETINDICATORCURRENT, DJANGO_COMMENT_INDICATOR, 0);
            sci.send_message(sc.SCI_INDICSETSTYLE, DJANGO_COMMENT_INDICATOR, sc.INDIC_CONTAINER);
            sci.send_message(sc.SCI_INDICSETFORE, DJANGO_COMMENT_INDICATOR, 0x838383);
            sci.send_message(sc.SCI_INDICSETALPHA, DJANGO_COMMENT_INDICATOR, 100);
            sci.send_message(sc.SCI_INDICATORFILLRANGE, 
                             sci.get_position_from_line(line) + comment.start(), 
                             len(comment.group()));
