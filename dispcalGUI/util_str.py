#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
try:
	from functools import reduce
except ImportError:
	# Python < 2.6
	pass

def asciize(obj):
	"""
	Turn several unicode chars into an ASCII representation.
	
	This function either takes a string or an exception as argument (when used 
	as error handler for encode or decode).
	
	"""
	subst = {
		u"\u00a9": "(C)", # U+00A9 copyright sign
		u"\u00ae": "(R)", # U+00AE registered sign
		u"\u00b2": "2", # U+00B2 superscript two
		u"\u00b3": "3", # U+00B3 superscript three
		u"\u00b9": "1", # U+00B9 superscript one
		u"\u00d7": "x", # U+00D7 multiplication sign
		u"\u2013": "-", # U+2013 en dash
		u"\u2014": "-", # U+2014 em dash
		u"\u2015": "-", # U+2015 horizontal bar
		u"\u2026": "...", # U+2026 ellipsis
		u"\u2212": "-", # U+2212 minus sign
	}
	chars = ""
	if isinstance(obj, Exception):
		for char in obj.object[obj.start:obj.end]:
			chars += subst.get(char, u"_")
		return chars, obj.end
	else:
		return obj.encode("ASCII", "asciize")

codecs.register_error("asciize", asciize)


def center(text, width = None):
	"""
	Center (mono-spaced) text.
	
	If no width is given, the longest line 
	(after breaking at each newline) is used as max width.
	
	"""
	text = text.split("\n")
	if width is None:
		width = 0
		for line in text:
			if len(line) > width:
				width = len(line)
	i = 0
	for line in text:
		text[i] = line.center(width)
		i += 1
	return "\n".join(text)


def universal_newlines(txt):
	"""
	Return txt with all new line formats converted to POSIX newlines.
	
	"""
	return txt.replace("\r\n", "\n").replace("\r", "\n")


def strtr(txt, replacements):
	"""
	String multi-replace, a bit like PHP's strtr.
	
	replacements can be a dict or a list.
	If it is a list, all items are replaced with the empty string ("").
	
	"""
	if hasattr(replacements, "iteritems"):
		replacements = replacements.iteritems()
	else:
		replacements = zip(replacements, [""] * len(replacements))
	for srch, sub in replacements:
		txt = txt.replace(srch, sub)
	return txt


def wrap(text, width = 70):
	"""
	A word-wrap function that preserves existing line breaks and spaces.
	
	Expects that existing line breaks are posix newlines (\\n).
	
	"""
	return reduce(lambda line, word, width=width: '%s%s%s' %
		(line,
		' \n'[(len(line)-line.rfind('\n')-1
			+ len(word.split('\n',1)[0]
				) >= width)],
		word),
		text.split(' ')
		)
