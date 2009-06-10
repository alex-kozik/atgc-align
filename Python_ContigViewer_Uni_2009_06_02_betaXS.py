##########################################
#                                        #
# This program is the standalone version #
#   of Contig Viewer:                    #
# http://cgpdb.ucdavis.edu/              #
# Alexander Kozik and Brian Chan         #
# Copyright 2004 2005 2006 2007          #
# University of California Davis         #
#                                        #
##########################################

##########################################################################
#                                                                        #
# Copyright (C) 2004-2007 University of California at Davis              #
#                        UCD Genome Center                               #
# Michelmore lab.,  Alexander Kozik and Brian Chan                       #
#                                                                        #
# This program is free software. You can redistribute it                 #
# and/or modify it under the terms of the GNU General Public License     #
# ( http://www.gnu.org ) as published by the Free Software Foundation;   #
# either version 2 of the License, or (at your option) any later version.#
#                                                                        #
# In other words, you are free to modify, copy, or redistribute this     #
# source code and its documentation in any way you like, but you must    #
# distribute all derivative versions as free software under the same     #
# terms that we provided our code to you (i.e. the GNU General Public    #
# License). This precludes any use of the code in proprietary or         #
# commercial software unless your source code is made freely available.  #
#                                                                        #
# This program is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of             #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU       #
# General Public License for more details.                               #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this Contig Viewer release, in the file LICENSE;            #
# if not, write to the Free Software Foundation,                         #
# Inc., 675 Mass. Ave, Cambridge, MA 02139 USA.                          #
#                                                                        #
##########################################################################

import os, sys, urllib
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
from string import *
from string import atof
from string import replace
from math import log10
from math import fabs
import tkFont
import socket

# ====================================================
# global
g_interestListWin = 0        # these are for the interest win
g_interestListWin_open = 0
g_interestListIndex = 0
g_interestList_content = None

g_socketEnabled = 0
g_host = "127.0.0.1"
g_port = 2500

#######################################################
###            LIST OF CUSTOM PARAMETERS            ###
###                                                 ###
###
###  1A. DEFAULT PATH TO CAP3 ASSEMBLY FILES - g_path 
###
###  1B. LIST OF g_path VALUES IN DROP-DOWN MENU - g_path_list 
###
###
###  2A. DEFAULT CAP3 FILE EXTENSION - g_ext 
###
###  2B. LIST OF g_ext VALUES IN DROP-DOWN MENU - g_ext_list 
###
###
###  3A. DEFAULT PATH TO BLAST FILES - g_blastPath 
###
###  3B. LIST OF g_blastPath VALUES IN DROP-DOWN MENU - g_blastPath_list 
###
###
###  4A. DEFAULT BLAST FILE EXTENSION - g_blastFileExt 
###
###  4B. LIST OF g_blastPath VALUES IN DROP-DOWN MENU - g_blastFileExt_list 
###
###
###  5A. DEFAULT PATH TO PHP SCRIPT TO CALL SPLICE COORDINATES - g_phpFilePath 
###
###  5B. LIST OF g_phpFilePath VALUES IN DROP-DOWN MENU - g_phpFilePath_list
###
###
###  6A. DEFAULT PATH TO PHP SCRIPT TO CALL SINGLET SEQUENCES - g_phpFilePathContigData 
###
###  6B. LIST OF g_phpFilePathContigData VALUES IN DROP-DOWN MENU - g_phpFilePathContigData_list 
###
###
###  7A. DEFAULT COLOR SCHEME - db_source 
###
###  7B. LIST OF db_source VALUES IN DROP-DOWN MENU - db_source_list 
###
###
#######################################################

#######################################################
###                                                 ###
###   MODIFY CUSTOM PARAMETERS BELOW --+            ###
###                                    |            ###
###                                    V            ###
###                                                 ###
#######################################################

## 1 ##
g_path = "cgpdb.ucdavis.edu/SNP_Discovery_CDS/ContigViewer/cap3_cich/"
# g_path = "cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_contig_files/lactuca_solexa/"
g_path_list = ["cgpdb.ucdavis.edu/SNP_Discovery_CDS/ContigViewer/cap3_cich/", \
				"cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_contig_files/aster/", \
				"cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_contig_files/helianthus/", \
				"cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_contig_files/lactuca/", \
				"cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_contig_files/others/", \
				"cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_contig_files/lactuca_solexa/"]

## 2 ##
g_ext = ".aln"
# g_ext = ".4aln.out.fa.x.aln"
g_ext_list = [".aln", ".align", ".alignment", ".4aln.out.fa.x.aln"]

## 3 ##
g_blastPath = "cgpdb.ucdavis.edu/SNP_Discovery_CDS/ContigViewer/blast_cich/"
# g_blastPath = "cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_blast_files/lactuca_solexa/"

g_blastPath_list = ["cgpdb.ucdavis.edu/SNP_Discovery_CDS/ContigViewer/blast_cich/" , \
				"cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_blast_files/aster/", \
				"cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_blast_files/helianthus/", \
				"cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_blast_files/lactuca/", \
				"cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_blast_files/others/", \
				"cgpdb.ucdavis.edu/asteraceae_assembly/ContigViewer/python_viewer/data_blast_files/lactuca_solexa/"]


## 4 ##
g_blastFileExt = ".vs.ath.BlastX.txt"

## 5 ##
g_phpFilePath = "cgpdb.ucdavis.edu/SNP_Discovery_CDS/ContigViewer/get_viewer_coordinates_cich.php"

## 6 ##
g_phpFilePathContigData = "cgpdb.ucdavis.edu/SNP_Discovery_CDS/ContigViewer/get_viewer_contig_data_cich.php"

## 7 ##
db_source = "nine_letter_code_1"


### SOME OTHER PARAMETERS ###
prefix_type = 1
g_prefix = "Prefix_Type_1 (nine_letter_code_1)"
# g_prefix = "Prefix_Type_4 (nine_letter_code_4)"


g_use_blast = "FALSE"
# g_use_blast = "TRUE"

g_use_singleton = "FALSE"

g_hitnum = 12
g_display_GC = "TRUE"

g_blastInputFileName = "_x_blast.in"
g_blastOutputFileName = "_x_blast.out"

g_seqNameCharSpace = 22    # how much space the seqName's occupy

#g_tclshCmd = "tclsh81"
#g_tclshCmd = "tclsh8.1"
g_tclshCmd = "tclsh"
# g_blastParserScriptName = "tcl_blast_parser_123_V025.tcl"
g_blastParserScriptName = "tcl_blast_parser_123_V025S.tcl"

# ====================================================

class sequenceClass:

	def __init__(self, sn, sb, s, e):
		self.seqName = sn            # seq name
		self.seqBody = sb.upper()    # seq body
		self.start = s               # start index of seq
		self.end = e                 # end index of seq
		self.D_info =  []            # indexes of D (deletions)
		self.I_info =  []            # indexes of I (insertions)
		self.S_info =  []            # indexes of S (substitutions)
		self.XN_info = []            # indexes of x and N case

	def getSeqName(self):
		return self.seqName

	def getSeqBody(self):
		return self.seqBody

	def getSeqBodyChar(self, index):
		# print index, len(self.seqBody)
		if index < self.end:
			return self.seqBody[index]
		else:
			return " "

	def getStart(self):
		return self.start

	def getEnd(self):
		return self.end

	def append_D_info(self, di):
		self.D_info.append(di)
	def getD_info(self):
		return self.D_info

	def append_I_info(self, ii):
		self.I_info.append(ii)
	def getI_info(self):
		return self.I_info

	def append_S_info(self, si):
		self.S_info.append(si)
	def getS_info(self):
		return self.S_info

	def append_XN_info(self, xni):
		self.XN_info.append(xni)
	def getXN_info(self):
		return self.XN_info

# ===================================================


class contigViewerUserInputWindow( Frame ):

	def __init__(self):

		global prefix_type
		global db_source
		global g_path
		global g_ext
		global g_prefix
		global g_use_blast
		global g_use_singleton
		global g_blastFileExt
		global g_blastPath
		global g_phpFilePath
		global g_phpFilePathContigData

		self.config_URL_default = g_path
		self.config_Prefix_default = g_prefix
		self.config_EXT_default = g_ext
		self.config_bl_URL_default = g_blastPath
		self.config_bl_EXT_default = g_blastFileExt
		self.config_php_URL_default = g_phpFilePath
		self.config_php_URL_cda_default = g_phpFilePathContigData

		global g_host
		global g_port
		self.host = g_host
		self.port = g_port

		# set up the main window
		Frame.__init__(self)
		root = self.master
		root.title("Python Contig Viewer")
		# root.geometry( "300x300" )
		myRow = 0           # keep track of the row number (for grid manager)

		##################################
		######  BASIC FUNCTIONALITY ######

		frame_0 = Frame(root)
		frame_0.pack(side = TOP, fill = X)
		self.basic_label_str = "    Basic functions of Contig Viewer:    "
		self.bar_label_0 = Label(frame_0, text=self.basic_label_str)
		self.bar_label_0.pack()

		# first row
		frame_1 = Frame(root)
		frame_1.pack(side = TOP, fill = X)
		self.path_label = Label(frame_1, text="Path http://")
		self.path_label.pack(side = LEFT)

		############################################################
		##### MODIFY VARIABLES ACCORDING TO PARTICULAR PROJECT #####
		############################################################
		### URL to download sequences from web server
		self.URLarray = g_path_list 
		# self.URLarray = ["cgpdb.ucdavis.edu/brassica_assembly/ContigViewer/data_contig_files/brassica/"]
		############################################################
		#####              END OF MODIFICATION                 #####
		############################################################

		self.URL_str = StringVar()
		self.URL_str.set(self.config_URL_default) # init the path
		scrollbar = Scrollbar(frame_1, orient=VERTICAL)
		self.URL_optionMenu = Listbox(frame_1, height=4, width=86, selectmode=SINGLE, exportselection=0, yscrollcommand=scrollbar.set)
		self.URL_optionMenu.bind("<ButtonRelease-1>", self.define_path)
		scrollbar["command"] = self.URL_optionMenu.yview
		scrollbar.pack(side=RIGHT, fill=Y)
		for item in self.URLarray:
			self.URL_optionMenu.insert(END, item)
		self.URL_optionMenu.pack(fill = BOTH)
		self.URL_optionMenu.selection_set(0)

		# second row b
		frame_1b = Frame(root)
		frame_1b.pack(side = TOP, fill = X)
		self.sp_label = Label(frame_1b, text="ID Prefix:   ")
		self.sp_label.pack(side = LEFT)

		############################################################
		##### MODIFY VARIABLES ACCORDING TO PARTICULAR PROJECT #####
		############################################################

		### ID with suffix or prefix
		self.Prefix_array = ["Prefix_Type_1 (nine_letter_code_1)", \
				"Prefix_Type_2 (nine_letter_code_2)", \
				"Prefix_Type_3 (nine_letter_code_3)", \
				"Prefix_Type_4 (nine_letter_code_4)"]

		### MODIFYING THIS SECTION YOU ALSO NEED TO MODIFY FUNCTION "def define_Prefix"

		############################################################
		#####              END OF MODIFICATION                 #####
		############################################################

		#######################################################
		self.Prefix_str = StringVar()
		self.Prefix_str.set(self.config_Prefix_default) # init the path
		scrollbar = Scrollbar(frame_1b, orient=VERTICAL)
		self.Prefix_optionMenu = Listbox(frame_1b, height=4, width=86, selectmode=SINGLE, exportselection=0, yscrollcommand=scrollbar.set)
		self.Prefix_optionMenu.bind("<ButtonRelease-1>", self.define_Prefix)
		scrollbar["command"] = self.Prefix_optionMenu.yview
		scrollbar.pack(side=RIGHT, fill=Y)
		for item in self.Prefix_array:
			self.Prefix_optionMenu.insert(END, item)
		self.Prefix_optionMenu.pack(fill = X)
		self.Prefix_optionMenu.selection_set(0)

		######################################################

		# third row
		frame_2 = Frame(root)
		frame_2.pack(side = TOP, fill = X)
		self.contigID_label = Label(frame_2, text="Contig ID:")
		self.contigID_label.pack(side = LEFT)

		self.contigID_text = Entry(frame_2, name="contigID_text", width=24)
		self.contigID_text.bind( "<Return>", self.showWebFinding)
		self.contigID_text.pack(side = LEFT)
		# self.contigID_text.insert(0, "LACT_SATI.CST1.685")
		# LACT_SATI.CST1.685
		self.contigID_text.insert(0, "CICH_2CDS.CSA1.1112")
		# self.contigID_text.insert(0, "QG_CA_Contig1009")

		self.EXTarray = g_ext_list
		# self.EXTarray = [".aln", ".alignment", ".align", ".ali"]
		self.EXT_str = StringVar()
		self.EXT_str.set(self.config_EXT_default) # init the ext
		scrollbar = Scrollbar(frame_2, orient=VERTICAL)
		self.EXT_optionMenu = Listbox(frame_2, height=4, selectmode=SINGLE, exportselection=0, yscrollcommand=scrollbar.set)
		self.EXT_optionMenu.bind("<ButtonRelease-1>", self.define_EXT)
		scrollbar["command"] = self.EXT_optionMenu.yview
		scrollbar.pack(side=RIGHT, fill=Y)
		for item in self.EXTarray:
			self.EXT_optionMenu.insert(END, item)
		self.EXT_optionMenu.pack(side = RIGHT)
		self.EXT_optionMenu.selection_set(0)
		self.EXT_label = Label(frame_2, text="File Extension:")
		self.EXT_label.pack(side = RIGHT)

		frame_4c = Frame(root)
		frame_4c.pack(side = TOP, fill = X)
		self.bar_label_str = "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
		self.bar_label_a = Label(frame_4c, text=self.bar_label_str)
		self.bar_label_a.pack()

		# fourth row
		myRow = myRow + 1
		frame_3 = Frame(root)
		frame_3.pack(side = TOP, fill = X)
		self.webButton = Button(frame_3, text="  Get Data Remotely  ", command=self.showWebFinding)
		self.webButton.pack(side = LEFT)
		self.HDButton = Button(frame_3, text="Choose file form Hard Disk", command=self.showHDFinding)
		self.HDButton.pack(side = RIGHT)

		# fifth row
		frame_4a = Frame(root)
		frame_4a.pack(side = TOP, fill = X)
		self.bar_label_str = "====================================================="
		self.bar_label_a = Label(frame_4a, text=self.bar_label_str)
		self.bar_label_a.pack()

		###################################
		##### EXTENDED FUNCTIONALITY ######

		frame_4e = Frame(root)
		frame_4e.pack(side = TOP, fill = X)
		self.exp_label_str = " Extended functionality - for experienced users only: "
		self.bar_label_e = Label(frame_4e, text=self.exp_label_str)
		self.bar_label_e.pack()

		frame_4f = Frame(root)
		frame_4f.pack(side = TOP, fill = X)
		self.warn_label_str = "    (proper database setup is required)    "
		self.bar_label_f = Label(frame_4f, text=self.warn_label_str)
		self.bar_label_f.pack()

		###### USE BLAST REPORT TO DISPLAY INTRON-EXON POSITIONS #######

		# blast row c
		frame_1c = Frame(root)
		frame_1c.pack(side = TOP, fill = X)
		self.blast_label = Label(frame_1c, text="Use BLAST Report:   ")
		self.blast_label.pack(side = LEFT)

		###############################################################
		### USE BLAST
		Blast_array = ["false", "true"]
		###############################################################
		self.Blast_str = StringVar()
		self.Blast_str.set(Blast_array[0]) # init the path
		self.Blast_optionMenu = OptionMenu(frame_1c, self.Blast_str, \
			Blast_array[0], Blast_array[1], command=self.define_Blast)
		self.Blast_optionMenu.pack(fill = X, side = LEFT)

		self.ignore_label = Label(frame_1c, text="  Singleton: ")
		self.ignore_label.pack(side = LEFT)

		Singl_array = ["no", "yes"]
		self.Singl_str = StringVar()
		self.Singl_str.set(Singl_array[0]) # init the path
		self.Singl_optionMenu = OptionMenu(frame_1c, self.Singl_str, \
			Singl_array[0], Singl_array[1], command=self.define_Singl)
		self.Singl_optionMenu.pack(fill = X, side = LEFT)

		##########################################################

		frame_1d = Frame(root)
		frame_1d.pack(side = TOP, fill = X)
		self.bl_path_label = Label(frame_1d, text="BLAST http://")
		self.bl_path_label.pack(side = LEFT)

		############################################################
		##### MODIFY VARIABLES ACCORDING TO PARTICULAR PROJECT #####
		############################################################
		### URL to download BLAST report from web server
		self.bl_URLarray = g_blastPath_list 
		# self.bl_URLarray = ["cgpdb.ucdavis.edu/brassica_assembly/ContigViewer/data_blast_files/brassica/"]
		############################################################
		#####              END OF MODIFICATION                 #####
		############################################################

		self.bl_URL_str = StringVar()
		self.bl_URL_str.set(self.config_bl_URL_default) # init the path
		scrollbar = Scrollbar(frame_1d, orient=VERTICAL)
		self.bl_URL_optionMenu = Listbox(frame_1d, height=3, selectmode=SINGLE, exportselection=0, yscrollcommand=scrollbar.set)
		self.bl_URL_optionMenu.bind("<ButtonRelease-1>", self.define_blPath)
		scrollbar["command"] = self.bl_URL_optionMenu.yview
		scrollbar.pack(side=RIGHT, fill=Y)
		for item in self.bl_URLarray:
			self.bl_URL_optionMenu.insert(END, item)
		self.bl_URL_optionMenu.pack(fill = X)
		self.bl_URL_optionMenu.selection_set(0)

		frame_7 = Frame(root)
		frame_7.pack(side = TOP, fill = X)

		self.bl_EXTarray = [".vs.ath.BlastX.txt", ".vs.ath.BlastX.txt", \
					".vs.ath.BlastX.txt", ".vs.ath.BlastX.txt"]
		self.bl_EXT_str = StringVar()
		self.bl_EXT_str.set(self.config_bl_EXT_default) # init the ext
		scrollbar = Scrollbar(frame_7, orient=VERTICAL)
		self.bl_EXT_optionMenu = Listbox(frame_7, height=3, selectmode=SINGLE, exportselection=0, yscrollcommand=scrollbar.set)
		self.bl_EXT_optionMenu.bind("<ButtonRelease-1>", self.define_blFileExt)
		scrollbar["command"] = self.bl_EXT_optionMenu.yview
		scrollbar.pack(side=RIGHT, fill=Y)
		for item in self.bl_EXTarray:
			self.bl_EXT_optionMenu.insert(END, item)
		self.bl_EXT_optionMenu.pack(side = RIGHT)
		self.bl_EXT_optionMenu.selection_set(0)

		self.bl_EXT_label = Label(frame_7, text="BLAST file extension:")
		self.bl_EXT_label.pack(side = RIGHT)

		frame_8 = Frame(root)
		frame_8.pack(side = TOP, fill = X)
		self.php_path_label = Label(frame_8, text="coordinates: http://")
		self.php_path_label.pack(side = LEFT)

		############################################################
		##### MODIFY VARIABLES ACCORDING TO PARTICULAR PROJECT #####
		############################################################
		### URL to download BLAST report from web server
		### URL to get coordinates for blast
		self.php_URLarray = ["cgpdb.ucdavis.edu/brassica_assembly/ContigViewer/get_viewer_coordinates_brassica.php"]
		############################################################
		#####              END OF MODIFICATION                 #####
		############################################################

		self.php_URL_str = StringVar()
		self.php_URL_str.set(self.config_php_URL_default) # init the path
		scrollbar = Scrollbar(frame_8, orient=VERTICAL)
		self.php_URL_optionMenu = Listbox(frame_8, height=3, selectmode=SINGLE, exportselection=0, yscrollcommand=scrollbar.set)
		self.php_URL_optionMenu.bind("<ButtonRelease-1>", self.define_phpFilePath)
		scrollbar["command"] = self.php_URL_optionMenu.yview
		scrollbar.pack(side=RIGHT, fill=Y)
		for item in self.php_URLarray:
			self.php_URL_optionMenu.insert(END, item)
		self.php_URL_optionMenu.pack(fill = X)
		self.php_URL_optionMenu.selection_set(0)

		############################################################

		frame_9 = Frame(root)
		frame_9.pack(side = TOP, fill = X)
		self.php_contig_data_path_label = Label(frame_9, text="contig data: http://")
		self.php_contig_data_path_label.pack(side = LEFT)

		self.php_URL_cda = ["cgpdb.ucdavis.edu/brassica_assembly/ContigViewer/get_viewer_contig_data_brassica.php"]

		self.php_URL_contig_data_str = StringVar()
		self.php_URL_contig_data_str.set(self.config_php_URL_cda_default) # init the path
		scrollbar = Scrollbar(frame_9, orient=VERTICAL)
		self.php_URL_contig_data_optionMenu = Listbox(frame_9, height=3, selectmode=SINGLE, exportselection=0, yscrollcommand=scrollbar.set)
		self.php_URL_contig_data_optionMenu.bind("<ButtonRelease-1>", self.define_phpFilePathContigData)
		scrollbar["command"] = self.php_URL_contig_data_optionMenu.yview
		scrollbar.pack(side=RIGHT, fill=Y)
		for item in self.php_URL_cda:
			self.php_URL_contig_data_optionMenu.insert(END, item)
		self.php_URL_contig_data_optionMenu.pack(fill = X)
		self.php_URL_contig_data_optionMenu.selection_set(0)

		##########################################################
		##### END OF BLAST SECTION #####

		frame_4b = Frame(root)
		frame_4b.pack(side = TOP, fill = X)
		# self.bar_label_str = "====================================================="
		self.bar_label_b = Label(frame_4b, text=self.bar_label_str)
		self.bar_label_b.pack()

		# make menu
		self.makemenu()

  # ---------------------------------------------------

	def define_all(self):
		self.define_phpFilePathContigData("good")
		self.define_path("good")
		self.define_EXT("good")
		self.define_phpFilePath("good")
		self.define_blFileExt("good")
		self.define_blPath("good")
		self.define_Prefix("good")

	def define_phpFilePathContigData(self, somewhere):
		global g_phpFilePathContigData
		l = self.php_URL_contig_data_optionMenu.curselection()
		g_phpFilePathContigData = self.php_URL_cda[ int(l[0]) ]
		print "PHP contig data file path: " + g_phpFilePathContigData

	def define_path(self, somewhere):
		global g_path
		l = self.URL_optionMenu.curselection()
		g_path = self.URLarray[ int(l[0]) ]
		print "path: " + g_path

	def define_EXT(self, somewhere):
		global g_ext
		l = self.EXT_optionMenu.curselection()
		g_ext = self.EXTarray[ int(l[0]) ]
		print "ext: " + g_ext

	def define_phpFilePath(self, something):
		global g_phpFilePath
		l = self.php_URL_optionMenu.curselection()
		g_phpFilePath = self.php_URLarray[ int(l[0]) ]
		print "PHP file path: " + g_phpFilePath

	def define_blFileExt(self, something):
		global g_blastFileExt
		l = self.bl_EXT_optionMenu.curselection()
		g_blastFileExt = self.bl_EXTarray[ int(l[0]) ]
		print "Blast file extension: " + g_blastFileExt

	def define_blPath(self, somewhere):
		global g_blastPath
		l = self.bl_URL_optionMenu.curselection()
		g_blastPath = self.bl_URLarray[ int(l[0]) ]
		print "Blast path: " + g_blastPath

	def define_Singl(self, somehow):

		global g_use_singleton
		print somehow

		if somehow == "no":
			g_use_singleton = "FALSE"
		if somehow == "yes":
			g_use_singleton = "TRUE"

		print "SEQUENCE IS SINGLETON: " + g_use_singleton

	def define_Blast(self, whatever):

		global g_use_blast
		print whatever

		if whatever == "false":
			g_use_blast = "FALSE"
		if whatever == "true":
			g_use_blast = "TRUE"

		print "BLAST RESULTS: " + g_use_blast

  # ---------------------------------------------------

	def define_Prefix(self, s):

		global prefix_type
		global db_source

		# print "I am here!"
		l = self.Prefix_optionMenu.curselection()
		something = self.Prefix_array[ int(l[0]) ]

		prefix_type = 0

		############################################################
		##### MODIFY VARIABLES ACCORDING TO PARTICULAR PROJECT #####
		############################################################

		if something == "Prefix_Type_1 (nine_letter_code_1)":
			prefix_type = 1
			db_source = "nine_letter_code_1"
		if something == "Prefix_Type_2 (nine_letter_code_2)":
			prefix_type = 2
			db_source = "nine_letter_code_2"
		if something == "Prefix_Type_3 (nine_letter_code_3)":
			prefix_type = 3
			db_source = "nine_letter_code_3"
		if something == "Prefix_Type_4 (nine_letter_code_4)":
			prefix_type = 4
			db_source = "nine_letter_code_4"
		if something == "Prefix_Type_5 (user-defined)":
			prefix_type = 5
			db_source = "user-defined"

		############################################################
		#####              END OF MODIFICATION                 #####
		############################################################

		print prefix_type
		print db_source

  # ---------------------------------------------------

	def makemenu(self):
		self.menubar = Menu(self.master)
		self.master.config(menu=self.menubar)

		# add file pulldown menu
		file = Menu(self.menubar)
		file.add_command(label='Config file', command=self.openConfigWin)
		file.add_command(label='Client', command=self.openConnectClient)
		file.add_command(label='Quit', command=self.quit)
		self.menubar.add_cascade(label='File', underline=0, menu=file)

		# add help pulldown menu
		help = Menu(self.menubar)
		help.add_command(label='About', command=self.openAboutWin1)
		help.add_command(label='Input Files', command=self.openAboutWin2)
		help.add_command(label='Color Scheme', command=self.openAboutWin3)
		help.add_command(label='Key Bindings', command=self.openAboutWin4)
		help.add_command(label='Extended funct.', command=self.openAboutWin5)
		help.add_command(label='Search for substring', command=self.openAboutWin6)
		help.add_command(label='PerlPrimer', command=self.openAboutWin7)
		help.add_command(label='Config File', command=self.openAboutWinConfigFile)
		self.menubar.add_cascade(label='Help', underline=0, menu=help)

  # ---------------------------------------------------

	def quit(self):
		if askyesno('Really quit?', 'Are you sure you want to quit?'):
			Frame.quit(self)

  # ---------------------------------------------------

  # ==============================================================
  # Configuration file
  # ==============================================================

	def openConfigWin(self):

		# setup up a new window
		self.ConfigWin = Toplevel()
		self.ConfigWin.title("Config")
		self.ConfigWin.geometry( "160x120" )

		# frame 1
		frame_1 = Frame(self.ConfigWin)
		frame_1.pack(side = TOP, fill = BOTH, expand = True)

		# button "choose config file"
		self.configFile_btn = Button(frame_1, text = 'Choose Config File', command=self.getConfigFile, borderwidth=1)
		self.configFile_btn.pack(side = TOP)

		# button "restore to default"
		self.config2Default_btn = Button(frame_1, text = 'Restore to Default', command=self.config2Default, borderwidth=1)
		self.config2Default_btn.pack(side = TOP)

		# button "Close"
		self.configClose_btn = Button(frame_1, text = 'Close', command=self.ConfigWin.destroy, borderwidth=1)
		self.configClose_btn.pack(side = TOP)

	def getConfigFile(self):
		fp = askopenfile(title='Config file')
		lines = fp.readlines()
		fp.close()
		# parse the config lines
		for line in lines:
			line = strip(line)
			if len(line) == 0:    # empty line
				continue
			if line[0] == "#":   # comment line
				continue
			if ":" not in line:  # the key symbol
				continue
			array = split(line, ":", 1)
			k = array[0]
			v = strip(array[1], " \"")
			if k == "1. http path to contig files":
				L = self.URL_optionMenu.get(0, END)
				if v in L:
					for li in range(len(L)):
						if v == L[li]:
							self.URL_optionMenu.selection_clear(0, END)
							self.URL_optionMenu.selection_set(li)
							self.URL_optionMenu.see(li)
				else:
					self.URL_optionMenu.selection_clear(0, END)
					self.URL_optionMenu.insert(END, v)
					self.URL_optionMenu.selection_set(END)
					self.URL_optionMenu.see(END)
				self.define_path("good")
			elif k == "2. Colors":
				global g_barColors
				g_barColors = split(v, ", ")
			elif k == "3. Prefixes":
				user_defined_flag = 0
				L = self.Prefix_optionMenu.get(0, END)
				"""
				if v == "A_, B_, C_, D_":
					v = "Prefix_Type_1 (tomato)"
				elif v == "ABCDI, EFGHJ, KL, MN":
					v = "Prefix_Type_2 (lettuce)"
				elif v == "ABCDI, EFGHJ, KL, MN":
					v = "Prefix_Type_3 (sunflower)"
				elif v == "P__, Q__, R__, S__":
					v = "Prefix_Type_4 (arabidopsis)"
				else:
				"""
				global g_prefixes
				g_prefixes = split(v, ", ")
				v = "Prefix_Type_5 (user-defined)"
				# for prefix and color, we use internal var
				#   therefore we need to make this call
				global prefix_type
				global db_source
				prefix_type = 5
				db_source = "user-defined"

				if v in L:
					for li in range(len(L)):
						if v == L[li]:
							self.Prefix_optionMenu.selection_clear(0, END)
							self.Prefix_optionMenu.selection_set(li)
							self.Prefix_optionMenu.see(li)
				else:
					self.Prefix_optionMenu.selection_clear(0, END)
					self.Prefix_optionMenu.insert(END, v)
					self.Prefix_optionMenu.selection_set(END)
					self.Prefix_optionMenu.see(END)
					# add this type to the internal array
					if v not in self.Prefix_array:
						self.Prefix_array.append(v)

			elif k == "4. Position":
				global g_position
				s = strip(v)
				s = strip(s, "\"")
				s = strip(s, "[")
				s = strip(s, "]")
				g_position = s
				print g_position
			elif k == "5. Contig file ext":
				L = self.EXT_optionMenu.get(0, END)
				if v in L:
					for li in range(len(L)):
						if v == L[li]:
							self.EXT_optionMenu.selection_clear(0, END)
							self.EXT_optionMenu.selection_set(li)
							self.EXT_optionMenu.see(li)
				else:
					self.EXT_optionMenu.selection_clear(0, END)
					self.EXT_optionMenu.insert(END, v)
					self.EXT_optionMenu.selection_set(END)
					self.EXT_optionMenu.see(END)
				self.define_EXT("good")
			elif k == "6. BLAST http":
				L = self.bl_URL_optionMenu.get(0, END)
				if v in L:
					for li in range(len(L)):
						if v == L[li]:
							self.bl_URL_optionMenu.selection_clear(0, END)
							self.bl_URL_optionMenu.selection_set(li)
							self.bl_URL_optionMenu.see(li)
				else:
					self.bl_URL_optionMenu.selection_clear(0, END)
					self.bl_URL_optionMenu.insert(END, v)
					self.bl_URL_optionMenu.selection_set(END)
					self.bl_URL_optionMenu.see(END)
				self.define_blPath("good")
			elif k == "7. BLAST file ext":
				L = self.bl_EXT_optionMenu.get(0, END)
				if v in L:
					for li in range(len(L)):
						if v == L[li]:
							self.bl_EXT_optionMenu.selection_clear(0, END)
							self.bl_EXT_optionMenu.selection_set(li)
							self.bl_EXT_optionMenu.see(li)
				else:
					self.bl_EXT_optionMenu.selection_clear(0, END)
					self.bl_EXT_optionMenu.insert(END, v)
					self.bl_EXT_optionMenu.selection_set(END)
					self.bl_EXT_optionMenu.see(END)
				self.define_blFileExt("good")
			elif k == "8. PHP coord file http":
				L = self.php_URL_optionMenu.get(0, END)
				if v in L:
					for li in range(len(L)):
						if v == L[li]:
							self.php_URL_optionMenu.selection_clear(0, END)
							self.php_URL_optionMenu.selection_set(li)
							self.php_URL_optionMenu.see(li)
				else:
					self.php_URL_optionMenu.selection_clear(0, END)
					self.php_URL_optionMenu.insert(END, v)
					self.php_URL_optionMenu.selection_set(END)
					self.php_URL_optionMenu.see(END)
				self.define_phpFilePath("good")
			elif k == "9. contig data http":
				L = self.php_URL_contig_data_optionMenu.get(0, END)
				if v in L:
					for li in range(len(L)):
						if v == L[li]:
							self.php_URL_contig_data_optionMenu.selection_clear(0, END)
							self.php_URL_contig_data_optionMenu.selection_set(li)
							self.php_URL_contig_data_optionMenu.see(li)
				else:
					self.php_URL_contig_data_optionMenu.selection_clear(0, END)
					self.php_URL_contig_data_optionMenu.insert(END, v)
					self.php_URL_contig_data_optionMenu.selection_set(END)
					self.php_URL_contig_data_optionMenu.see(END)

				self.define_phpFilePathContigData("good")

	def config2Default(self):

		"""
		self.config_URL_default = g_path
		self.config_Prefix_default = g_prefix
		self.config_EXT_default = g_ext
		self.config_bl_URL_default = g_blastPath
		self.config_bl_EXT_default = g_blastFileExt
		self.config_php_URL_default = g_phpFilePath
		self.config_php_URL_cda_default = g_phpFilePathContigData
		"""

		global g_prefix
		g_prefix == "Prefix_Type_1 (tomato)"
		self.define_Prefix(g_prefix)

		# do the change
		self.URL_optionMenu.selection_clear(0, END)
		self.URL_optionMenu.selection_set(0)
		self.URL_optionMenu.see(0)
		self.Prefix_optionMenu.selection_clear(0, END)
		self.Prefix_optionMenu.selection_set(0)
		self.Prefix_optionMenu.see(0)
		self.EXT_optionMenu.selection_clear(0, END)
		self.EXT_optionMenu.selection_set(0)
		self.EXT_optionMenu.see(0)
		self.bl_URL_optionMenu.selection_clear(0, END)
		self.bl_URL_optionMenu.selection_set(0)
		self.bl_URL_optionMenu.see(0)
		self.bl_EXT_optionMenu.selection_clear(0, END)
		self.bl_EXT_optionMenu.selection_set(0)
		self.bl_EXT_optionMenu.see(0)
		self.php_URL_optionMenu.selection_clear(0, END)
		self.php_URL_optionMenu.selection_set(0)
		self.php_URL_optionMenu.see(0)
		self.php_URL_contig_data_optionMenu.selection_clear(0, END)
		self.php_URL_contig_data_optionMenu.selection_set(0)
		self.php_URL_contig_data_optionMenu.see(0)

		# update internal vars
		self.define_all()


  # ---------------------------------------------------

  # ==============================================================
  # Connect
  # ==============================================================

	def openConnectClient(self):
		self.openClientWin()

	def openClientWin(self):

		global g_host
		global g_port

		# setup up a new window and a new Text object
		self.ClientWin = Toplevel()
		self.ClientWin.title("Client")
		self.ClientWin.geometry( "200x150" )
		myFont = tkFont.Font(family="Courier", size="10")

		# the label
		frame_1 = Frame(self.ClientWin)
		frame_1.pack(side = TOP, fill = BOTH, expand = True)
		label1 = Label(frame_1, text='Connect to Perl Primer', width=20)
		label1.pack(side=TOP)

		# the IP field
		frame_host = Frame(self.ClientWin)
		frame_host.pack(side = TOP, fill = BOTH, expand = True)
		self.clientHost_label = Label(frame_host, text="Host:", width=6)
		self.clientHost_label.pack(side = LEFT)
		self.clientHost_text = Entry(frame_host, name="clientHost_text", width=20)
		self.clientHost_text.pack(side = LEFT)
		self.clientHost_text.insert(0, str(g_host))

		# the port field
		frame_port = Frame(self.ClientWin)
		frame_port.pack(side = TOP, fill = BOTH, expand = True)
		self.clientPort_label = Label(frame_port, text="Port:", width=6)
		self.clientPort_label.pack(side = LEFT)
		self.clientPort_text = Entry(frame_port, name="clientPort_text", width=6)
		self.clientPort_text.pack(side = LEFT)
		self.clientPort_text.insert(0, str(g_port))

		# frame 2
		frame_2 = Frame(self.ClientWin)
		frame_2.pack(side = TOP, fill = BOTH, expand = True)

		# the socket enable button
		self.clientSocketEnable_btn = Button(frame_2, text = 'Activate Socket', command=self.socketEnable, borderwidth=1)
		self.clientSocketEnable_btn.pack(side = TOP)
		# the socket disable button
		self.clientSocketDisable_btn = Button(frame_2, text = 'Deactivate Socket', command=self.socketDisable, borderwidth=1)
		self.clientSocketDisable_btn.pack(side = TOP)

		# button "Close"
		self.clientClose_btn = Button(frame_2, text = 'Close', command=self.ClientWin.destroy, borderwidth=1)
		self.clientClose_btn.pack(side = TOP)

	def socketEnable(self):
		global g_socketEnabled
		g_socketEnabled = 1
		print "Socket Activated"

	def socketDisable(self):
		global g_socketEnabled
		g_socketEnabled = 0
		print "Socket Deactivated"

	def clientConfirm(self):
		#self.host = socket.gethostname()
		self.host = self.clientHost_text.get()
		self.port = int( self.clientPort_text.get() )
		print "host: " + self.host
		print "port: " + str(self.port)
		
	def clientSend(self, packet):

		# check if enabled
		global g_socketEnabled
		if g_socketEnabled != 1:
			return

		# get host and port infomation
		[host, port] = [self.host, self.port]
		#create an INET, STREAMing socket
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#bind the socket to a public host, and a well-known port
		#self.clientSocket.bind((host, port))
		try:
			self.clientSocket.connect( (host, port) )
		except socket.error:
			print "connection failed"
		self.clientSocket.sendto(packet, (host, port))
		print "packet is sent to \"" + host + "\" at port " + str(port)
		print "packet content:"
		print packet
		self.clientSocket.close()


  # ==============================================================
  # Connect (end)
  # ==============================================================

  # ---------------------------------------------------

	def openAboutWin1(self):
		s = """
This program is the standalone program of 
the online version of Contig Viewer.
(http://cgpdb.ucdavis.edu)

It visualizes CAP3 alignments and highlights 
sequences of different genotypes by different 
colors.

It displayes all SNPs/InDels in a given 
alignment.

It helps to find (specify) regions on CAP3 
alignment for oligo design.

http://cgpdb.ucdavis.edu/SNP_Discovery/

Authors:
Alexander Kozik and Brian Chan

email: akozik@atgc.org

"""
		message_box = Toplevel()
		message_box.title("About Contig Viewer")
		message_box_fr = Frame(message_box)
		message_box_fr.pack(expand=0, fill=BOTH)
		message_lb = Label(message_box_fr, text = s)
		message_lb.grid(row=0, column=0)
		quitbutton = Button(message_box_fr, text = 'Close', command=message_box.destroy, borderwidth=1)
		quitbutton.grid(row=1, column=0)

  # ---------------------------------------------------

	def openAboutWin2(self):

		s = """
File input:

modified CAP3 alignment 

1. Remotely via http
or
2. from local hard drive

Contig ID examples:

tomato - "L_ABC_Contig2942"
number range: 1 - 3821

lettuce - "QG_CA_Contig6125"
number range: 1 - 8179

sunflower - "QH_CA_Contig901"
number range: 1 - 6760

arabidopsis - "ATH_Contig2931"
number range: 1 - 9487

Alignment file extension:
tomato - ".aln"
lettuce - ".alignment"
sunflower - ".alignment"
arabidopsis - ".align"

for customization see source code

"""
		message_box = Toplevel()
		message_box.title("Input Files")
		message_box_fr = Frame(message_box)
		message_box_fr.pack(expand=0, fill=BOTH)
		message_lb = Label(message_box_fr, text = s)
		message_lb.grid(row=0, column=0)
		quitbutton = Button(message_box_fr, text = 'Close', command=message_box.destroy, borderwidth=1)
		quitbutton.grid(row=1, column=0)

  # ---------------------------------------------------

	def openAboutWin3(self):

		s = """
Color Scheme:

tomato ID prefix:
"A_" - lightblue
"B_" - yellow
"C_" - green
"D_" - orange

lettuce and sunflower
third letter in ID:
"A, B, C, D or I" - orange
"E, F, G, H or J" - green
"K or L" - lightblue
"M or N" - yellow

to customize see and change source 
code under comments 
"MODIFY VARIABLES ACCORDING 
TO PARTICULAR PROJECT"

or

You can customize color scheme and 
other parameters using Config file.

"""
		message_box = Toplevel()
		message_box.title("Color Scheme")
		message_box_fr = Frame(message_box)
		message_box_fr.pack(expand=0, fill=BOTH)
		message_lb = Label(message_box_fr, text = s)
		message_lb.grid(row=0, column=0)
		quitbutton = Button(message_box_fr, text = 'Close', command=message_box.destroy, borderwidth=1)
		quitbutton.grid(row=1, column=0)

  # ---------------------------------------------------

	def openAboutWin4(self):

		s = """
Key bindings 
(Windows and *nix 
three button mouse):

Left mouse button:
set the left index (L)

Right mouse button:
set the right index (R)

Middle mouse button:
set the middle index (M)

Control + Left mouse button:
set the middle index (M)

Shift + Left mouse button:
set the left exclude index (LX)

Shift + Right mouse button:
set the right exclude index (RX)

----------------------
Note to Mac OS X users:
Key binding on three button
mouse may be slightly different.
Check it out before usage.

"""
		message_box = Toplevel()
		message_box.title("Key Binding")
		message_box_fr = Frame(message_box)
		message_box_fr.pack(expand=0, fill=BOTH)
		message_lb = Label(message_box_fr, text = s)
		message_lb.grid(row=0, column=0)
		macXbutton = Button(message_box_fr, text = 'Mac OS X notes', command=self.mac_OSX_notes, borderwidth=1, bg="gold")
		macXbutton.grid(row=1, column=0)
		quitbutton = Button(message_box_fr, text = 'Close', command=message_box.destroy, borderwidth=1)
		quitbutton.grid(row=2, column=0)

  # ---------------------------------------------------

	def mac_OSX_notes(self):

		s = """
MAC OS X NOTES:

There is a bug (annoyance):
When you use Contig Viewer in the
Extended mode, "Sequence Text" window
with alignment may look slightly shacking
and other windows may not respond.
In this case close "Sequence Text" window
and open it again by clicking anywhere on
graphical contig "Viewer" window. After
this action program should restore 
normal functionality.

-------------------

Three button mouse key binding:

Right button may act as a middle 
button compare to PC mouse
on Python Mac OS X interpreter.

Middle button (or wheel) may act as 
a right button compare to regular 
bindings as described in help.

You need to practice a little bit
to get familiar with 
mouse functionality.

"""

		message_box = Toplevel()
		message_box.title("Key Binding")
		message_box_fr = Frame(message_box)
		message_box_fr.pack(expand=0, fill=BOTH)
		message_lb = Label(message_box_fr, text = s)
		message_lb.grid(row=0, column=0)
		quitbutton = Button(message_box_fr, text = 'Close', command=message_box.destroy, borderwidth=1)
		quitbutton.grid(row=1, column=0)

  # ---------------------------------------------------

	def openAboutWin5(self):

		s = """

Extended functionality will be activated 
upon selection "Use BLAST Report - true"

Program will contact web server and run 
set of scripts and queries on database 
(proper database setup is required).

Program will extract data from BLAST report 
corresponding to specified Contig (sequence) 
and display BLAST hits with intron/exon 
positions on corresponding 
Arabidopsis sequences.

This functionality is under development.

See details about database setup and instructions at:
http://cgpdb.ucdavis.edu/SNP_Discovery/Py_ContigViewer/

"""
		message_box = Toplevel()
		message_box.title("Extended Functionality")
		message_box_fr = Frame(message_box)
		message_box_fr.pack(expand=0, fill=BOTH)
		message_lb = Label(message_box_fr, text = s)
		message_lb.grid(row=0, column=0)
		quitbutton = Button(message_box_fr, text = 'Close', command=message_box.destroy, borderwidth=1)
		quitbutton.grid(row=1, column=0)

  # ---------------------------------------------------

	def openAboutWin6(self):

		s = """

There is a search feature in the text sequence window. 

You can insert the search string into the forward search 
text field. 

The "case sensitive" check box indicates whether you want 
your search to be case sensitive. 

You can also input the reverse complement of your search 
string by either manually typing it, or by press the 
button labeled "Get Rev-Comp". 

The "search" button will perform the substring search on 
the two patterns in the Forward and Rev-Comp text fields. 
The Forward substring match will be colored in purple. 
the Reverse Complement substring match will be colored in 
green. The sequence text display will shift to the first 
found match. 

The button "Clear Selection" will clear the colors in the 
text sequence window. 

"""
		message_box = Toplevel()
		message_box.title("Search for substring")
		message_box_fr = Frame(message_box)
		message_box_fr.pack(expand=0, fill=BOTH)
		message_lb = Label(message_box_fr, text = s)
		message_lb.grid(row=0, column=0)
		quitbutton = Button(message_box_fr, text = 'Close', command=message_box.destroy, borderwidth=1)
		quitbutton.grid(row=1, column=0)

  # ---------------------------------------------------

	def openAboutWin7(self):

		s = """

Upon selection of regions for PCR oligo design there is an 
option to generate a fasta file which can be used by 
PerlPrimer program:
http://perlprimer.sourceforge.net/

After selection is done (you see two yellow boxes on the 
"Sequence Text" window and all fields in the "Indexes" 
window are filled), you can click "PerlPrimer" button.
New file in fasta format will be generated like:

>Contig2942 5prime_region[189-265] 3prime_region[332-411]
GGTTCCAATGGAGTTGTGATAAACGAAGAGCAGCACAAGCTCCCAATACCAAATTTAG
TACTACTGACCAATTATAAAGAGTAAATATAGAAGATTAGGGTTTTAAGATCTCTAAC
AAAATTGCACTGGGAAGAATCTGGTTCTTCAATTTTCTGGGATTTATCAGATCTGAAG
AAACTGAAGAGTGAAGTGGTAATCGTTGATAAGTGTATGTTCAAGGGAGGATTGTTTG
GATTTACTGAACTGTTGTTTGATGTGGTTTTGGAGAAGATAA

where "5prime_region" and "3prime_region" fields contain 
numerical values for selected regions for oligo design.

These values can be used by PerlPrimer or Primer3 programs.
PerlPrimer program can read this fasta file format directly.

With the client module connected to the remote machine 
running PerlPrimer, any valid selection (with the left box 
selection and the right selection) will be sent immediately 
to the remote machine. 

"""
		message_box = Toplevel()
		message_box.title("PerlPrimer")
		message_box_fr = Frame(message_box)
		message_box_fr.pack(expand=0, fill=BOTH)
		message_lb = Label(message_box_fr, text = s, justify=LEFT)
		message_lb.grid(row=0, column=0)
		quitbutton = Button(message_box_fr, text = 'Close', command=message_box.destroy, borderwidth=1)
		quitbutton.grid(row=1, column=0)

  # ---------------------------------------------------

	def openAboutWinConfigFile(self):

		s = """

Users can configure their selections in a user config file. A sample 
config file is presented below.

<!-- Beginning of config file -->
# ContigViewer config file for tomato project
1. http path to contig files: "cgpdb.ucdavis.edu/database/assembly/tomato/"
2. Colors: "lightblue, yellow, green, orange"
3. Prefixes: "A_, B_, C_, D_"
4. Position: "[0:2]"
5. Contig file ext: ".aln"
6. BLAST http: "cgpdb.ucdavis.edu/database/blast/tomato_vs_tigr/"
7. BLAST file ext: ".tom_vs_tigr_blastX.txt"
8. PHP coord file http: "cgpdb.ucdavis.edu/viewer/get_viewer_coordinates.php"
9. contig data http: "cgpdb.ucdavis.edu/viewer/get_viewer_contig_data.php"
<!-- End of config file -->

Any line with a leading "#" will be treated as a comment line, ignored.

Any empty line will be ignored as well.

For each configurable options, please change only the content inbetween the 
double quotes. Otherwise, this program may not be able to recognize your input, 
and thus discard your input. 


"""
		message_box = Toplevel()
		message_box.title("Config File Help")
		message_box_fr = Frame(message_box)
		message_box_fr.pack(expand=0, fill=BOTH)
		message_lb = Label(message_box_fr, text = s, justify=LEFT)
		message_lb.grid(row=0, column=0)
		quitbutton = Button(message_box_fr, text = 'Close', command=message_box.destroy, borderwidth=1)
		quitbutton.grid(row=1, column=0)

  # ---------------------------------------------------

	def showWebFinding(self, event=0):
		self.showFinding("website")

  # ---------------------------------------------------

	def showHDFinding(self, event=0):
		self.showFinding("Hard-Drive")

  # ---------------------------------------------------

	def showFinding( self, type ):

		global g_use_blast
		global g_use_singleton
		global g_path
		global g_contig_canvas_size

		# flags
		no_blast_flag = 0
		if g_use_blast == "FALSE":
			no_blast_flag = 1
		if g_use_blast == "TRUE":
			no_blast_flag = 0
		if g_use_singleton == "FALSE":
			singleton_flag = 0
		if g_use_singleton == "TRUE":
			singleton_flag = 1

		# get raw data
		rawData = ""
		if type == "website":
			rawData = self.getWebData()
		elif type == "Hard-Drive":
			rawData = self.getHDData()

		# retrieve separated data
		sequences_data, MM_info = self.getSequencesData(rawData)
		if sequences_data == "":
			singleton_flag = 1

		# get gap info
		gapInfo = []
		blastResult = []
		hitnum = 0
		if no_blast_flag == 0:
			gapInfo = self.getGapInfo(g_blastInputFileName, g_blastOutputFileName)
			print gapInfo
			# then pass gapInfo to cv, so that the gaps will be printed out

			# retrieve blast result data
			info2_list, webBlastResultData, hitnum, no_tigr_seq_flag = self.getBlastResultData()
			if len(webBlastResultData) != len(info2_list):
				showinfo('Error', "blast result contains different number of tigr sequences than that of info2")
				# there is error, probably one of the tigrID's is wrong
				#showinfo('Error', "invalid blast result data")
			if no_tigr_seq_flag != 1:
				for blastResult_i in range( hitnum ):
					info2Line = info2_list[blastResult_i]
					dirPosLine = webBlastResultData[blastResult_i]
					[contigID, tigrID, desp, norm_exp, identity, matches, overlap, \
						hit_N, Frame, est_s, est_e, ath_s, ath_e, len2, gaps] = info2Line
					[dir, pos] = split(dirPosLine)
					[seqLen1, seqLen2] = split(len2, "/")
					[est_s, est_e, ath_s, ath_e] = [int(est_s), int(est_e), int(ath_s), int(ath_e)]
					[seqLen1, seqLen2] = [int(seqLen1), int(seqLen2)]
					array1 = [tigrID, est_s, est_e, ath_s, ath_e, seqLen1, seqLen2]
					array2 = [dir, pos]
					blastResultData_record = [array1, array2]
					#print blastResultData_record
					blastResult.append( blastResultData_record )
				print blastResult
			# else:
			# singleton_flag = 1


		# if it is a singleton, we need extra info
		seqName = self.contigID_text.get()
		if singleton_flag != 0:
			# overwrite the error page, with the seq body
			if g_use_singleton == "TRUE":
				# use online script, getting data from the database
				rawData = self.getWebContigData()
				seqBody = rawData[0]  # should only have one line
			else:
				pagename = g_path + self.contigID_text.get() + g_ext
				remoteaddr = 'http://' + pagename
				remotefile = urllib.urlopen(remoteaddr)
				remotedata = remotefile.readlines()
				remotefile.close()
				lastLine = remotedata[-1]
				n, b = split(lastLine)
				seqBody = strip(b)
			# sequences_data should be empty, so add the singleton
			sequence = sequenceClass(seqName, seqBody, 1, len(seqBody))
			sequences_data = [ sequence ]
			g_contig_canvas_size = len(seqBody)
			MM_info = []

		# generate picture
		cv = contigViewerClass(seqName, rawData, sequences_data, MM_info, hitnum, blastResult, gapInfo, self)
		cv.generatePicture()
		cv.generateSeqTextWin()
		if no_blast_flag == 0:
			cv.generateBlastResultTextWin(g_blastInputFileName)
		else:
			print "not displaying blast result"
			pass
			# no blast result retrieved

  # ---------------------------------------------------

	def getGapInfo(self, savefileName="_input.txt", outfileName="_out.txt"):

		global g_blastPath
		global g_blastFileExt
		global g_tclshCmd
		global g_blastParserScriptName

		# get blast result online. (assuming the file comes without any problems)
		contigID = self.contigID_text.get()
		blastPage = g_blastPath + contigID + g_blastFileExt
		self.getWebFileAndSave(blastPage, savefileName)

		# analysize the blast result
		tclshCmd = g_tclshCmd
		inputName = savefileName
		outputName = outfileName
		options = "10 20 50 MATRIX"
		blastParserScriptName = g_blastParserScriptName
		cmdStr = tclshCmd + " " + blastParserScriptName + " " + inputName + " " + outputName + " " + options
		print cmdStr
		os.system(cmdStr)

		# find gaps
		global g_hitnum
		alignfilename = outputName + ".align"
		info2filename = outputName + ".info2"
		alignFile = open(alignfilename, "r")
		lines = alignFile.readlines()
		numLine = len(lines)
		#hitnum_limit = atoi( self.hitnum_text.get() )
		hitnum_limit = g_hitnum
		gapInfo = []
		i = 0  # curr line number
		while i < numLine:
			# get a record (5 lines)
			hitLine = lines[i]
			contigNameLine = lines[i+1]
			contigBodyLine = lines[i+2]
			tigrNameLine = lines[i+3]
			tigrBodyLine = lines[i+4]
			# analysis
			# analysize hitLine
			tempList = split(hitLine)
			hitNum = atoi(tempList[2])
			ALT_ALN_num = atoi(tempList[4])
			if hitNum > hitnum_limit:
				# increment the current line pointer
				i = i + 5
				continue
			if ALT_ALN_num != 1:
				# increment the current line pointer
				i = i + 5
				continue
			# analysize contigNameLine
			tempList = split(contigNameLine)
			contigName = tempList[0][1:]
			rangeStr = strip(tempList[1], "[]")
			tempList = split(rangeStr, "-")
			contigStart = atoi(tempList[0])
			contigEnd = atoi(tempList[1])
			# analysize contigBodyLine
			contigBody = strip(contigBodyLine)
			# analysize tigrNameLine
			tempList = split(tigrNameLine)
			tigrName = tempList[0][1:]
			rangeStr = strip(tempList[1], "[]")
			tempList = split(rangeStr, "-")
			tigrStart = atoi(tempList[0])
			tigrEnd = atoi(tempList[1])
			# analysize tigrBodyLine
			tigrBody = strip(tigrBodyLine)
			# good record, find gap
			lenC = len(contigBody)
			lenT = len(tigrBody)
			if lenC != lenT:
				print "lenC and lenT are different, can't find gap"
				# increment the current line pointer
				i = i + 5
				continue
			gapListC = []
			gapListT = []
			for char_i in range(lenC):
				charC = contigBody[char_i]
				charT = tigrBody[char_i]
				if charC == "-" and charT == "-":
					print "charC and charT are both - ..."
					return
				if charC != "-" and charT != "-":
					continue  # no gap
				if charC == "-":
					gapListC.append(char_i*3)
					gapListC.append(char_i*3+1)
					gapListC.append(char_i*3+2)
				if charT == "-":
					gapListT.append(char_i*3)
					gapListT.append(char_i*3+1)
					gapListT.append(char_i*3+2)
			record = [ hitNum, gapListC, gapListT ]
			gapInfo.append( record )

			# increment the current line pointer
			i = i + 5

 		return gapInfo

  # ---------------------------------------------------

	def dispCoord(self):
		info2_list, webBlastResultData, hitnum, no_tigr_seq_flag = self.getBlastResultData()
		print info2_list
		print webBlastResultData
		print hitnum
		print no_tigr_seq_flag

  # ---------------------------------------------------

	def getSequencesData(self, data):

		# init
		global g_use_singleton
		sequences_data = []
		MM_info = []
		global g_contig_canvas_size

		# error detection
		if data == "" and g_use_singleton == "FALSE":  # no file selected, or file is empty
			return "ERROR", "ERROR"
		if find(data[0], ".    :") == -1 and g_use_singleton == "FALSE":    # the first line should contain "<pre>"
			showinfo('Error', 'Input data is invalid')
			return "ERROR", "ERROR"

		# get each seq's name, body, start, end, MM_info
		for line in data:
			# ignore empty lines
			if strip(line) == "":
				continue
			# ignore lines with ".   :"
			#### FIND CONTIG CONSENSUS [DEFINED BY "-------------------------------------------------------" AT LEAST 60 TIMES]
			if find(line, ".    :") != -1 or find(line, "--------------------------------------------------------") != -1:
				continue
			seqName = ""
			seqBody = ""
			global g_seqNameCharSpace
			for i in range(len(line)):
				if i < g_seqNameCharSpace:    # read in seqName
					seqName = seqName + line[i]
				else:
					seqBody = seqBody + line[i]
			seqName = rstrip(seqName)
			seqBody = rstrip(seqBody)
			print seqName
			# print seqBody, len(seqBody), len(lstrip(seqBody))
			# get start index
			start = len(seqBody) - len(lstrip(seqBody)) + 1
			# get end index, and MM info (MM_info contains D, I and S indexes)
			end = len(rstrip(seqBody))
			seqBodyWithoutTags = seqBody
			# store data
			sequence = sequenceClass(seqName, seqBodyWithoutTags, start, end)
			sequences_data.append( sequence )

		# get contig index among the seq's and the end index of the contig
		contigIndex = len(sequences_data)-1   # index of the contig
		contigEnd = sequences_data[contigIndex].getEnd()
		g_contig_canvas_size = contigEnd

		# find all DIS and store indexes into MM_info
		MM_info = []
		for i in range(contigEnd):
			contigGene = sequences_data[contigIndex].getSeqBodyChar(i)
			for seqIndex in range(len(sequences_data)-1):
				gene = sequences_data[seqIndex].getSeqBodyChar(i)
				if gene == " ":    # gene doesn't exist
					continue
				if gene != contigGene:
					MM_info.append(i)
					break

		# analyze the D, I and S locations
		for mm in MM_info:      # for each MM location
			# get a column from seq's
			gene_array = []
			for seq in sequences_data:
				gene_array.append( seq.getSeqBodyChar(mm) )
			# distinguish it (D, I or S ?)
			contig_gene = gene_array.pop()    # this is the contig gene
			# NUCL = "ATGCNX"
			NUCL ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
			for i in range(len(gene_array)):
				gene = gene_array[i].upper()
				if gene == " ":           # ignore whte space
					continue
				if gene == contig_gene:   # the same? good
					continue
				if gene == 'X' and contig_gene == 'N':      # x and N case
					sequences_data[i].append_XN_info( mm )
					continue
				if gene in NUCL and contig_gene == '-':     # insertion
					sequences_data[i].append_I_info( mm )
					continue
				if gene == '-' and contig_gene in NUCL:     # deletion
					sequences_data[i].append_D_info( mm )
					continue
				if gene in NUCL and contig_gene in NUCL and gene != contig_gene:   # substitution
					sequences_data[i].append_S_info( mm )
					continue
				showinfo('Error', contig_gene + " " + gene + " " + str(i) + '\n' + "  Wrong nucleotide symbol  ")

		# determine the N area (gray area) in the contig
		contig_index = len(sequences_data) - 1
		contig_body = sequences_data[ contig_index ].getSeqBody()
		for i in range(len(contig_body)-2):
			gene1 = contig_body[i]
			gene2 = contig_body[i+1]
			gene3 = contig_body[i+2]
			### ? WHY 3 POSITIONS ? ###
			if gene1 == "N" and gene2 == "N" and gene3 == "N":
				sequences_data[ contig_index ].append_XN_info(i)
				# Notice, in fact we should store i, i+1, i+2
				#  but we only store i to avoid repeated data

		# return back all the analyzed data
		return sequences_data, MM_info

  # ---------------------------------------------------

	def getWebData(self):
		#pagename = self.URL_str.get() + self.contigID_text.get() + self.EXT_str.get()
		global g_path
		global g_ext
		print g_path
		print self.contigID_text.get()
		print g_ext
		pagename = g_path + self.contigID_text.get() + g_ext
		remoteaddr = 'http://' + pagename
		remotefile = urllib.urlopen(remoteaddr)
		remotedata = remotefile.readlines()
		remotefile.close()
		return remotedata

  # ---------------------------------------------------

	def getHDData(self):
		filename = askopenfilename()
		all_lines = ""
		if filename:
			all_lines = open(filename, 'r').readlines()
		return all_lines

  # ---------------------------------------------------

	def getBlastResultData(self):
		global g_hitnum
		no_tigr_seq_flag = 0
		# get data from info2
		info2Lines = self.getAllTigrInfoFromInfo2()
		info2_list = []
		tigrID_list = []
		#hitnum = atoi(self.hitnum_text.get())
		hitnum = g_hitnum
		# error checking
		if len(info2Lines) == 0 or find(info2Lines[0], "no_hits_found") != -1:
			no_tigr_seq_flag = 1
			return [ [], [], hitnum, no_tigr_seq_flag ]
		elif len(info2Lines) < hitnum:
			hitnum = len(info2Lines)
			# showinfo('Error', "Only " + str(hitnum) + " hit(s) available. Click OK to display up to " + str(hitnum) + " hit(s).")
		# gather info
		for line_i in range( len(info2Lines) ):
			if line_i == hitnum:
				break
			line = info2Lines[line_i]
			print line
			lineInfo = [contigID, tigrID, desp, norm_exp, identity, matches, overlap, \
				hit_N, Frame, est_s, est_e, ath_s, ath_e, len2, gaps] = split(line, "\t")
			info2_list.append( lineInfo )
			tigrID_list.append( tigrID )
		tigrID_list_str = join(tigrID_list, ",")
		# get dir and pos data from web
		global g_phpFilePath
		pagename = g_phpFilePath + "?" + tigrID_list_str
		remoteaddr = 'http://' + pagename
		remotefile = urllib.urlopen(remoteaddr)
		remotedata = remotefile.readlines()
		remotefile.close()
		return [info2_list, remotedata, hitnum, no_tigr_seq_flag]



  # ---------------------------------------------------

	def getAllTigrInfoFromInfo2(self):
		info2filename = g_blastOutputFileName + ".info2"
		fp = open(info2filename, "r")
		lines = fp.readlines()
		return lines

  # ---------------------------------------------------

	def getWebContigData(self):
		global g_phpFilePathContigData
		pagename = g_phpFilePathContigData + "?" + self.contigID_text.get()
		remoteaddr = 'http://' + pagename
		remotefile = urllib.urlopen(remoteaddr)
		remotedata = remotefile.readlines()
		remotefile.close()
		return remotedata

  # ---------------------------------------------------

	def getWebFileAndSave(self, url, saveLoc):
		remoteaddr = 'http://' + url
		print remoteaddr
		remotefile = urllib.urlopen(remoteaddr)
		fp_save = open(saveLoc, "w")
		for line in remotefile.readlines():
			fp_save.write(line)
		fp_save.close()
		remotefile.close()

# ===================================================

class contigViewerClass( Frame ):

	def __init__(self, contigName, rawData, sequences_data, MM_info, hitnum, blastResult, gapInfo, wm):

		global prefix_type
		global g_seqNameCharSpace
		global g_contig_canvas_size

		print "Prefix type: " + `prefix_type`

		# init this class
		self.contigName = contigName
		self.rawData = rawData          # the seq's and the contig data
		self.sequences_data = sequences_data # the seq array
		self.MM_info = MM_info         # the union of D's, I's and S's
		self.queryID = contigName
		self.hitnum = hitnum
		self.blastResult = blastResult
		self.gapInfo = gapInfo

		self.CVLTRWin_open = 0          # the ContigViewer LTR Win open indicator
		self.interestListWin_open = 0   # the interest list Win open indicator
		self.seqNameCharSpace = g_seqNameCharSpace  # how much space the seqName's occupy

		# wm pointer
		self.wm = wm

		# constants for the graph
		# self.graphChartSizeX = 600      # the left part of the image (histogram)
		# self.graphChartSizeX = int(round(g_contig_canvas_size/3))
		self.graphChartSizeX = int(round(g_contig_canvas_size/1))
		if self.graphChartSizeX > 1000:
			self.graphChartSizeX = 1000
		self.textChartSizeX = 150       # the middle part of the image (seq names)
		self.tagChartSizeX = 50         # the right part of the image (tag ID)
		self.hSpace = 50                # horizontal empty space
		### SIZE OF DUMMY SEQUENCE BAR 2007 ###
		# self.vSpace = 5
		self.vSpace = 3                # vertical empty space
		self.viewableSizeY = 500        # vertical size of the contig window
		self.GCContentSizeY = 100       # vertical height of the QC bar chart

		# actual graph chart sizeX
		self.adjustedGraphChartSizeX = self.graphChartSizeX - self.hSpace * 2
		self.barHeight = 8              # the height of the bar of seqs
		self.maxImageSizeX = self.graphChartSizeX + self.textChartSizeX + self.tagChartSizeX
		self.maxImageSizeY = 0          # total Y pixels (not known yet, depends on # of seq's)
		self.maxGeneLen = 0             # end of contig  (not known yet)
		self.num_display = 0            # how many seq needs to be displayed (not known yet)
		self.charSpace = 3              # the # of pixel to display a char (horizontally)

		# calculate the dimensions' parameters
		self.numOfBars = len(self.sequences_data)
		self.maxGeneLen = self.sequences_data[len(self.sequences_data)-1].getEnd() * 1.0
		self.contigIndex = len( self.sequences_data ) - 1
		self.contigName = self.sequences_data[self.contigIndex].getSeqName()
		self.contigBody = self.sequences_data[self.contigIndex].getSeqBody()
		self.contigLength = len(self.contigBody)

  # ---------------------------------------------------

	def generateBlastResultTextWin(self, savefileName="input.txt"):

		# setup up a new window and a new Text object
		self.BlastResultTextWin = Toplevel()
		self.BlastResultTextWin.title("Blast Result *" + self.contigName + "*")
		self.BlastResultTextWin.geometry( "700x500" )
		text_h = self.numOfBars
		if text_h > 20:
			text_h = 20
		### FONT SIZE
		# myFont = tkFont.Font(family="Courier", size="10")
		myFont = tkFont.Font(family="Arial", size="4")
		frame_1 = Frame(self.BlastResultTextWin)
		frame_1.pack(side = TOP, fill = BOTH, expand = True)
		self.BlastResultTextWin_content = Text(frame_1, height=text_h, width=10, wrap=NONE, font=myFont)
		self.BlastResultTextWin_open = 1          # indicate open
		self.BlastResultTextWin.bind('<Destroy>', self.BlastResultTextWinDestroy)
		self.BlastResultTextWin_content.pack(side = LEFT, fill = BOTH, expand = True)

		# insert the text into the text win
		fp_in = open(savefileName, "r")
		lines = fp_in.readlines()
		for i in range( len(lines) ):
			line = lines[i]
			myPos = "%s.0" % (str(i+1))
			self.BlastResultTextWin_content.insert(myPos, line)

		# set up scrollable bars
		vertical_scrollbar = Scrollbar(frame_1, orient=VERTICAL, command=self.BlastResultTextWin_content.yview)
		vertical_scrollbar.pack(side = LEFT, fill = BOTH)

		frame_2 = Frame(self.SeqTextWin)
		frame_2.pack(side = TOP, fill = BOTH)
		horizontal_scrollbar = Scrollbar(frame_2, orient=HORIZONTAL, command=self.BlastResultTextWin_content.xview)
		horizontal_scrollbar.pack(side = BOTTOM, fill = X)
		self.BlastResultTextWin_content.config(yscrollcommand=vertical_scrollbar.set)
		self.BlastResultTextWin_content.config(xscrollcommand=horizontal_scrollbar.set)


	def BlastResultTextWinDestroy(self, o=None):
		self.BlastResultTextWin_open = 0

  # ---------------------------------------------------

	def generateSeqTextWin(self):

		# setup up a new window and a new Text object
		self.SeqTextWin = Toplevel()
		self.SeqTextWin.title("Sequence Text *" + self.contigName + "*")
		self.SeqTextWin.geometry( "750x350" )
		text_h = self.numOfBars
		if text_h > 20:
			text_h = 20
		myFont = tkFont.Font(family="Courier", size="10")
		frame_1 = Frame(self.SeqTextWin)
		frame_1.pack(side = TOP, fill = BOTH, expand = True)
		self.SeqTextWin_content = Text(frame_1, height=text_h, width=10, wrap=NONE, font=myFont)
		self.SeqTextWin_open = 1          # indicate open
		self.SeqTextWin.bind('<Destroy>', self.SeqTextWinDestroy)
		self.SeqTextWin_content.pack(side = LEFT, fill = BOTH, expand = True)

		# insert the ruler
		ruler = ""
		for i in range(self.seqNameCharSpace):
			ruler += " "
		for i in range(self.contigLength):
			if i % 10 == 4:
				ruler += "."
			elif i % 10 == 9:
				ruler += ":"
			else:
				ruler += " "
		self.SeqTextWin_content.insert("1.0", ruler+"\n")

		# insert the text into the text win
		for i in range(self.numOfBars):
			seqBody = self.sequences_data[i].getSeqBody()
			seqName = self.sequences_data[i].getSeqName()
			for j in range(self.seqNameCharSpace-len(seqName)):  # make the names aligned
				seqName += " "
			index = i + 2
			if i == self.numOfBars - 1:   # add a line before the contig
				myPos = "%s.0" % (str(index))
				line = ""
				for line_i in range(self.seqNameCharSpace):
					line += " "
				for line_i in range(self.contigLength):
					line += "-"
				self.SeqTextWin_content.insert(myPos, line+"\n")
				index = index + 1
			myPos = "%s.0" % (str(index))
			self.SeqTextWin_content.insert(myPos, seqName+seqBody+"\n")
			# associate tags to DIS
			self.addDISTag(self.sequences_data[i].getD_info(), 'deletion_tag', index)
			self.addDISTag(self.sequences_data[i].getI_info(), 'insertion_tag', index)
			self.addDISTag(self.sequences_data[i].getS_info(), 'substitution_tag', index)
			# add contig name info binding
			self.addInfoBinding(seqName, i, index)
			self.SeqTextWin_content.update()

		# highlight the tags
		self.SeqTextWin_content.tag_config('spectator_tag', foreground='blue')
		self.SeqTextWin_content.tag_config('deletion_tag', foreground='red')
		self.SeqTextWin_content.tag_config('insertion_tag', foreground='red')
		self.SeqTextWin_content.tag_config('substitution_tag', foreground='red')

		# set up scrollable bars
		vertical_scrollbar = Scrollbar(frame_1, orient=VERTICAL, command=self.SeqTextWin_content.yview)
		vertical_scrollbar.pack(side = LEFT, fill = BOTH)

		frame_2 = Frame(self.SeqTextWin)
		frame_2.pack(side = TOP, fill = BOTH)
		horizontal_scrollbar = Scrollbar(frame_2, orient=HORIZONTAL, command=self.SeqTextWin_content.xview)
		horizontal_scrollbar.pack(side = BOTTOM, fill = X)
		self.SeqTextWin_content.config(yscrollcommand=vertical_scrollbar.set)
		self.SeqTextWin_content.config(xscrollcommand=horizontal_scrollbar.set)

		# save alignment button
		frame_3 = Frame(self.SeqTextWin)
		frame_3.pack(side = TOP, fill = BOTH)
		saveAlignmentButton = Button(frame_3, text="Save Alignment As..", command=self.saveAlignment)
		saveAlignmentButton.pack(side = BOTTOM)

		# search forward text
		frame_search = Frame(self.SeqTextWin)
		frame_search.pack(side = TOP, fill = X)
		self.textSearch_label = Label(frame_search, text="Forward:", width=10)
		self.textSearch_label.pack(side = LEFT)
		self.textSearch_text = Entry(frame_search, name="textSearch_text", width=50)
		# self.textSearch_text.bind( "<Return>", self.showTextSearch)
		self.textSearch_text.pack(side = LEFT)
		self.textSearch_text.insert(0, "ATTTACTGAACTGTTGTTTGATGTGGTTTTG")

		self.caseSensitiveFlag = IntVar()
		self.caseSensitiveCheckBtn = Checkbutton(frame_search, text="Case Sensitive", variable=self.caseSensitiveFlag, width=16)
		self.caseSensitiveCheckBtn.pack(side=LEFT)
		getRevCompButton = Button(frame_search, text="Get Rev-Comp", command=self.showRevComp, width=16)
		getRevCompButton.pack(side = LEFT)

		# search reverse complement text
		frame_search2 = Frame(self.SeqTextWin)
		frame_search2.pack(side = TOP, fill = X)
		self.textSearchRevComp_label = Label(frame_search2, text="Rev-Comp:", width=10)
		self.textSearchRevComp_label.pack(side = LEFT)
		self.textSearchRevComp_text = Entry(frame_search2, name="textSearchRevComp_text", width=50)
		self.textSearchRevComp_text.pack(side = LEFT)
		self.textSearchRevComp_text.insert(0, "")

		searchButton = Button(frame_search2, text="Search", command=self.showTextSearch, width=16, bg="lightgreen")
		searchButton.pack(side = LEFT)

		searchClearButton = Button(frame_search2, text="Clear Selection", command=self.showTextSearchClear, width=16)
		searchClearButton.pack(side = LEFT)

  # ---------------------------------------------------

	def showRevComp(self):
		T = self.textSearch_text.get()
		comp = ""
		for t in T:
			n = t
			if t == 'A':
				n = 'T'
			elif t == 'a':
				n = 't'
			elif t == 'T':
				n = 'A'
			elif t == 't':
				n = 'a'
			elif t == 'G':
				n = 'C'
			elif t == 'g':
				n = 'c'
			elif t == 'C':
				n = 'G'
			elif t == 'c':
				n = 'g'
			comp += n
		revComp = ""
		for c in comp:
			revComp = c + revComp
		self.textSearchRevComp_text.delete(0, END)
		self.textSearchRevComp_text.insert(0, revComp)

	def showTextSearch(self):
		self.showTextSearchEach( self.textSearch_text.get(), 'search_forward_tag', 'purple')
		self.showTextSearchEach( self.textSearchRevComp_text.get(), 'search_revComp_tag', 'green')

	def showTextSearchEach(self, pattern, search_tag, highlightColor):

		if pattern == "":   # no pattern
			return
		if len(pattern) <= 2:  # too short
			return

		start = 1.0
		first_flag = 0
		while 1:
			if self.caseSensitiveFlag.get() == 0: 
				pos = self.SeqTextWin_content.search(pattern, start, stopindex=END, nocase=1)
			else:
				pos = self.SeqTextWin_content.search(pattern, start, stopindex=END)
			if not pos:
				break
			print pos
			if first_flag == 0:   # move the window to the first match
				p_strs = split(pos, '.')
				p = int(p_strs[1])   # get the col 
				self.moveSeqTextWinContentPos(p)
				first_flag = 1
			for i in range( len(pattern) ):
				self.SeqTextWin_content.tag_add(search_tag, pos)
				pos = pos + "+1c"
			# move to the next position
			# start = pos + "+1c"
			start = pos

		# color
		self.SeqTextWin_content.tag_config(search_tag, background=highlightColor)
			
	def showTextSearchClear(self):
		self.SeqTextWin_content.tag_delete('search_forward_tag')
		self.SeqTextWin_content.tag_delete('search_revComp_tag')

  # ---------------------------------------------------

	def addDISTag(self, indexes, tagName, rowNum):

		if rowNum == self.numOfBars+2:  # don't touch the contig
			return
		for i in self.MM_info:        # scan through all the DIS
			myPos = "%d.%d" % (rowNum, i+self.seqNameCharSpace)
			if i in indexes:      # here is the mismatch
				self.SeqTextWin_content.tag_add(tagName, myPos)
			else:                 # this gene is good, the mismatch is at this column
				self.SeqTextWin_content.tag_add('spectator_tag', myPos)

  # ---------------------------------------------------

	def addInfoBinding(self, contigName, seqIndex, rowNum):
		size = self.seqNameCharSpace + self.sequences_data[seqIndex].getStart() + len(self.sequences_data[seqIndex].getSeqBody())
		for i in range(size):
			myPos = "%d.%d" % (rowNum, i)
			self.SeqTextWin_content.tag_add("showinfo_"+contigName, myPos)
		self.SeqTextWin_content.tag_bind("showinfo_"+contigName, '<Button-1>', "showinfo(contigName, contigName)" )

  # ---------------------------------------------------

	def saveAlignment(self):
		str = self.SeqTextWin_content.get("1.0", END)  # all the alignments
		filename = asksaveasfilename()    # save all those
		if filename != "":
			open(filename, 'w').write(str)

  # ---------------------------------------------------
  # SAVE AS POSTSCRIPT FUNCTION ###
	def save_as_post_script(self):
		global ps_X
		global ps_Y
		my_postscript_file = asksaveasfilename(filetypes=[('PostScript', '*.ps')])
		self.pic.postscript(width=ps_X, height=ps_Y, x = '0', y = '0', file = my_postscript_file)


  # ---------------------------------------------------

	def generatePicture(self):

		# update the height of the image
		self.maxImageSizeY = (self.numOfBars) * (self.barHeight+self.vSpace) + \
			(self.hitnum)*(2*self.barHeight+self.vSpace*5) + self.vSpace + 20

		# setup up a new window and a new picture
		self.contigViewerWin = Toplevel()
		self.contigViewerWin.title("Viewer *" + self.contigName + "*")
		pic_h = self.maxImageSizeY + 100
		if pic_h > self.viewableSizeY + 100:
			pic_h = self.viewableSizeY + 100
		frame_1 = Frame(self.contigViewerWin)
		frame_1.pack(side = TOP, fill = BOTH, expand = True)
		self.pic = Canvas(frame_1, width=self.maxImageSizeX, height=pic_h, bg='black')
		self.pic.pack(side = LEFT, fill = BOTH, expand = True)

		### SAVE AS POSTSCRIPT START ###
		global ps_X
		global ps_Y
		ps_X = self.maxImageSizeX
		ps_Y = pic_h + 30
		self.pic.create_rectangle(0, 0, ps_X, ps_Y, tag="Dummy_Black_Rectangle", fill="#000")
		# self.save_as_ps_button = Button(frame_1, text="Save as PostScript", command=self.save_as_post_script, width=24)
		self.save_as_ps_button = Button(self.contigViewerWin, text="Save as PostScript", command=self.save_as_post_script, width=24)
		# self.save_as_ps_button.place(x=ps_X-160,y=ps_Y-120)
		self.save_as_ps_button.pack(side = BOTTOM)
		###  SAVE AS POSTSCRIPT END  ###

		# set up a scrollable bar
		vertical_scrollbar = Scrollbar(frame_1, orient=VERTICAL, command=self.pic.yview)
		vertical_scrollbar.pack(side = LEFT, fill = Y)
		vertical_scrollbar.width = 10
		self.pic.config(yscrollcommand=vertical_scrollbar.set)
		self.pic.config(scrollregion=(0,0,self.maxImageSizeX,self.maxImageSizeY + 120)) 

		# change the mouse icon for this canvas
		self.pic.config(cursor="crosshair")

		# plot it out ------------------------------------

		# draw the sub seqs
		seq_index = 0
		num_seq = len(self.sequences_data)
		for seq in self.sequences_data: # for each seq

			textcolor = 'white'     # pick text color for each seq

			### DEFINE FIRST Y POSITION ###
			posY = self.vSpace + seq_index * (self.vSpace+self.barHeight) + 10
			text_barHeight = posY+(self.barHeight*0.5)     # height for the text

			# decide seq bar color
			# barcolor = 'lightblue'  # this is the initial color
			barcolor = '#555555'  # this is the initial color

			###############################################
			###  DEFINE COLORS FOR DIFFERENT GENOTYPES  ###
			###############################################

			######################################## CUSTOM SETTINGS FOR GENERIC PROJECT #
			#
			# FIRST TWO SYMBOLS FOR DIFFERENT GENOTYPES SHOULD BE "A_" or "B_" or "C_" or "D_"
			#       Type of Prefix 1
			###############################################################################

			global prefix_type

			if prefix_type == 1:

			############################################################
			##### MODIFY VARIABLES ACCORDING TO PARTICULAR PROJECT #####
			############################################################
			### UNIVERSAL 9-PREFIX PROJECT ###
				if seq_index != num_seq-1:
					seq_type = (seq.getSeqName())[0:9]
					if seq_type == "Heli_annu" or seq_type == "HELI_ANNU":
						barcolor = '#FFFF00'
					if seq_type == "Heli_argo" or seq_type == "HELI_ARGO":
						barcolor = '#FFAA00'
					if seq_type == "Heli_peti" or seq_type == "HELI_PETI":
						barcolor = '#FF7700'
					if seq_type == "Heli_cili" or seq_type == "HELI_CILI":
						barcolor = '#FF4400'
					if seq_type == "Heli_exil" or seq_type == "HELI_EXIL":
						barcolor = '#FF00FF'
					if seq_type == "Heli_para" or seq_type == "HELI_PARA":
						barcolor = '#FF0077'
					if seq_type == "Heli_tube" or seq_type == "HELI_TUBE":
						barcolor = '#AA0044'

					if seq_type == "Lact_pere" or seq_type == "LACT_PERE":
						barcolor = '#00FFFF'
					if seq_type == "Lact_sali" or seq_type == "LACT_SALI":
						barcolor = '#00FFAA'
					if seq_type == "Lact_sati" or seq_type == "LACT_SATI":
						barcolor = '#77FFaa'
					if seq_type == "Lact_serr" or seq_type == "LACT_SERR":
						barcolor = '#00FF44'
					if seq_type == "Lact_viro" or seq_type == "LACT_VIRO":
						barcolor = '#00FF00'

					if seq_type == "Prun_arme":
						barcolor = 'orange'
					if seq_type == "Prun_avin":
						barcolor = 'yellow'
					if seq_type == "Prun_cera":
						barcolor = 'green'
					if seq_type == "Prun_dulc":
						barcolor = 'blue'
					if seq_type == "Prun_pers":
						barcolor = 'lightblue'

					if seq_type == "Bras_oler":
						barcolor = 'yellow'
					if seq_type == "Bras_rapa":
						barcolor = 'lightblue'

					if seq_type == "Cich_endi":
						barcolor = 'yellow'
					if seq_type == "Cich_inty":
						barcolor = 'lightblue'

					### ElDorado
					if seq_type == "Lact_eldr":
						barcolor = '#FFFF00'
					if seq_type == "Lact_eldo":
						barcolor = '#FFaa00'

					### Cisco
					if seq_type == "Lact_cisc":
						barcolor = '#FFFFFF'
					if seq_type == "Lact_ciso":
						barcolor = '#aaaaaa'

					### Parade
					if seq_type == "Lact_pard":
						barcolor = '#00FFFF'
					if seq_type == "Lact_para":
						barcolor = '#00FFaa'

					### Pavane
					if seq_type == "Lact_pavn":
						barcolor = '#aaFFaa'
					if seq_type == "Lact_pava":
						barcolor = '#77FF77'

					### Thomson
					if seq_type == "Lact_thmp":
						barcolor = '#00aaFF'
					if seq_type == "Lact_thmo":
						barcolor = '#0077FF'

					### Emperor
					if seq_type == "Lact_empr":
						barcolor = '#FF00FF'
					if seq_type == "Lact_empo":
						barcolor = '#aa00aa'


				else:
					barcolor = 'red'


			if prefix_type == 2:

			############################################################
			##### MODIFY VARIABLES ACCORDING TO PARTICULAR PROJECT #####
			############################################################
			### UNIVERSAL 9-PREFIX PROJECT ###
				if seq_index != num_seq-1:
					seq_type = (seq.getSeqName())[0:9]
					if seq_type == "Heli_annu" or seq_type == "HELI_ANNU":
						barcolor = 'orange'
					if seq_type == "Heli_argo" or seq_type == "HELI_ARGO":
						barcolor = 'yellow'
					if seq_type == "Heli_peti" or seq_type == "HELI_PETI":
						barcolor = 'green'
					if seq_type == "Heli_cili" or seq_type == "HELI_CILI":
						barcolor = 'lightblue'
					if seq_type == "Heli_exil" or seq_type == "HELI_EXIL":
						barcolor = 'blue'
					if seq_type == "Heli_para" or seq_type == "HELI_PARA":
						barcolor = 'violet'
					if seq_type == "Heli_tube" or seq_type == "HELI_TUBE":
						barcolor = 'white'

					if seq_type == "Lact_pere" or seq_type == "LACT_PERE":
						barcolor = 'orange'
					if seq_type == "Lact_sali" or seq_type == "LACT_SALI":
						barcolor = 'yellow'
					if seq_type == "Lact_sati" or seq_type == "LACT_SATI":
						barcolor = 'green'
					if seq_type == "Lact_serr" or seq_type == "LACT_SERR":
						barcolor = 'lightblue'
					if seq_type == "Lact_viro" or seq_type == "LACT_VIRO":
						barcolor = 'blue'

				else:
					barcolor = 'red'
			########################################

			### CUSTOM SETTINGS FOR CGPDB PROJECT ###

			if prefix_type == 3:

			############################################################
			##### MODIFY VARIABLES ACCORDING TO PARTICULAR PROJECT #####
			############################################################
			### UNIVERSAL 9-PREFIX PROJECT ###
				if seq_index != num_seq-1:
					seq_type = (seq.getSeqName())[0:9]
					if seq_type == "Heli_annu" or seq_type == "HELI_ANNU":
						barcolor = '#FFFF00'
					if seq_type == "Heli_argo" or seq_type == "HELI_ARGO":
						barcolor = '#FFAA00'
					if seq_type == "Heli_peti" or seq_type == "HELI_PETI":
						barcolor = '#FF7700'
					if seq_type == "Heli_cili" or seq_type == "HELI_CILI":
						barcolor = '#FF4400'
					if seq_type == "Heli_exil" or seq_type == "HELI_EXIL":
						barcolor = '#FF00FF'
					if seq_type == "Heli_para" or seq_type == "HELI_PARA":
						barcolor = '#FF0077'
					if seq_type == "Heli_tube" or seq_type == "HELI_TUBE":
						barcolor = '#AA0044'

					if seq_type == "Lact_pere" or seq_type == "LACT_PERE":
						barcolor = '#00FFFF'
					if seq_type == "Lact_sali" or seq_type == "LACT_SALI":
						barcolor = '#00FFAA'
					if seq_type == "Lact_sati" or seq_type == "LACT_SATI":
						barcolor = '#00FF77'
					if seq_type == "Lact_serr" or seq_type == "LACT_SERR":
						barcolor = '#00FF44'
					if seq_type == "Lact_viro" or seq_type == "LACT_VIRO":
						barcolor = '#00FF00'

			### CUSTOM SETTINGS FOR CGPDB PROJECT ###

			if prefix_type == 4:

			############################################################
			##### MODIFY VARIABLES ACCORDING TO PARTICULAR PROJECT #####
			############################################################
			### UNIVERSAL 4-PREFIX PROJECT ###
				if seq_index != num_seq-1:
					seq_type = (seq.getSeqName())[0:4]
					if seq_type == "LACT":
						barcolor = '#FFFF00'
					if seq_type == "SAB5":
						barcolor = '#AAFFFF'
					if seq_type == "SAB6":
						barcolor = '#FFAAFF'
					if seq_type == "SAB7":
						barcolor = '#FFFFAA'
					if seq_type == "SAA4" or seq_type == "SAA5":
						barcolor = '#AAAAAA'
					if seq_type == "SAD1":
						barcolor = '#AAFFFF'
					if seq_type == "SAD2":
						barcolor = '#FFAAFF'
					if seq_type == "SAD3":
						barcolor = '#FFFFAA'
					### ARABIDOPSIS ###
					if seq_type == "SAI1":
						barcolor = '#AAAAAA'
					if seq_type == "SAI2":
						barcolor = '#AAFFFF'
					if seq_type == "SAI3":
						barcolor = '#FFAAFF'
					if seq_type == "SAI4":
						barcolor = '#FFFFAA'
					if seq_type == "SAI5":
						barcolor = '#FFFFFF'


			if prefix_type == 5:

				if seq_index != num_seq-1:
					seq_type = (seq.getSeqName())[2]
					if seq_type in "ABCDI":
						barcolor = 'orange'
					if seq_type in "EFGHJ":
						barcolor = 'green'
					if seq_type in "KL":
						barcolor = 'lightblue'
					if seq_type in "MN":
						barcolor = 'yellow'
				else:
					barcolor = 'red'

			###########################################################################

			###### Prefix Type 4 (arabidopsis)

			if prefix_type == 4:

				if seq_index != num_seq-1:
					seq_type = (seq.getSeqName())[0:3]
					if seq_type == "P__":
						barcolor = 'lightblue'
					if seq_type == "Q__":
						barcolor = 'yellow'
					if seq_type == "R__":
						barcolor = 'green'
					if seq_type == "S__":
						barcolor = 'orange'
				else:
					barcolor = 'red'

			############################################################
			#####              END OF MODIFICATION                 #####
			############################################################

			if prefix_type == 5:
				global g_barColors
				global g_prefixes
				global g_position

				if ":" in g_position:
					s, e = split(g_position, ":")
					s = int(s)
					e = int(e)
					if seq_index != num_seq-1:
						seq_type = (seq.getSeqName())[s:e]
						if seq_type == g_prefixes[0]:
							barcolor = g_barColors[0]
						if seq_type == g_prefixes[1]:
							barcolor = g_barColors[1]
						if seq_type == g_prefixes[2]:
							barcolor = g_barColors[2]
						if seq_type == g_prefixes[3]:
							barcolor = g_barColors[3]
						### DEC 2006 ###
						if seq_type == g_prefixes[4]:
							barcolor = g_barColors[4]
						if seq_type == g_prefixes[5]:
							barcolor = g_barColors[5]
						if seq_type == g_prefixes[6]:
							barcolor = g_barColors[6]
						if seq_type == g_prefixes[7]:
							barcolor = g_barColors[7]

					else:
						barcolor = 'red'
				else:    # this is a choice
					pos = int( g_position )
					if seq_index != num_seq-1:
						seq_type = (seq.getSeqName())[pos]
						if seq_type in g_prefixes[0]:
							barcolor = g_barColors[0]
						if seq_type in g_prefixes[1]:
							barcolor = g_barColors[1]
						if seq_type in g_prefixes[2]:
							barcolor = g_barColors[2]
						if seq_type in g_prefixes[3]:
							barcolor = g_barColors[3]
						if seq_type in g_prefixes[4]:
							barcolor = g_barColors[4]
						if seq_type in g_prefixes[5]:
							barcolor = g_barColors[5]
						if seq_type in g_prefixes[6]:
							barcolor = g_barColors[6]
						if seq_type in g_prefixes[7]:
							barcolor = g_barColors[7]


					else:
						barcolor = 'red'

			if prefix_type == 0:

				print "Too Bad"
				exit

			###########################################################################

			# place the seq bar
			posX_start = self.hSpace + (seq.getStart()/self.maxGeneLen)*self.adjustedGraphChartSizeX
			posX_end = self.hSpace + (seq.getEnd()/self.maxGeneLen)*self.adjustedGraphChartSizeX
			posY_start = posY
			posY_end = posY_start + self.barHeight
			self.pic.create_rectangle(posX_start, posY_start, posX_end, posY_end, width=0, fill=barcolor)

			# place the mismatch segment
			self.displayMMError('D', seq.getD_info(), self.hSpace, self.maxGeneLen, \
				self.adjustedGraphChartSizeX, posY, self.barHeight, self.pic)
			self.displayMMError('I', seq.getI_info(), self.hSpace, self.maxGeneLen, \
				self.adjustedGraphChartSizeX, posY, self.barHeight, self.pic)
			self.displayMMError('S', seq.getS_info(), self.hSpace, self.maxGeneLen, \
				self.adjustedGraphChartSizeX, posY, self.barHeight, self.pic)
			self.displayMMError('XN', seq.getXN_info(), self.hSpace, self.maxGeneLen, \
				self.adjustedGraphChartSizeX, posY, self.barHeight, self.pic)

			# place the start index
			start = seq.getStart()
			### DEFINE START POSITION ###
			posX = self.hSpace + (start/self.maxGeneLen)*self.adjustedGraphChartSizeX
			self.pic.create_text(posX-15, text_barHeight, text=str(start), fill=textcolor)

			# place the end index
			end = seq.getEnd()
			# the extra space is used to sparate the bar and the text
			###  DEFINE END POSITION  ###
			posX = self.hSpace + (end/self.maxGeneLen)*self.adjustedGraphChartSizeX
			self.GC_Box_X_end = posX
			self.pic.create_text(posX+12, text_barHeight, text=str(end), fill=textcolor)

			# place the sub seq name
			posX = self.hSpace + self.adjustedGraphChartSizeX + self.hSpace*2
			seqName = seq.getSeqName()
			self.pic.create_text(posX-20, text_barHeight, text=seqName, fill=textcolor, anchor=W)

			# increment the seq index
			seq_index = seq_index + 1
			self.pic.update()

		# enable mouse interaction
		self.pic.bind('<Button-1>', self.onLeftClick)
		self.pic.bind('<Button-2>', self.onMiddleClick)
		self.pic.bind('<Control-Button-1>', self.onMiddleClick)
		self.pic.bind('<Button-3>', self.onRightClick)
		self.pic.bind('<Shift-Button-1>', self.onShiftLeftClick)
		self.pic.bind('<Shift-Button-3>', self.onShiftRightClick)

		# draw the GC content chart
		self.generatePictureGCContent(posY + 20)

		# save the contig Y location
		self.posY_contig = posY
		# draw the blast result
		posY = self.vSpace*2 + seq_index * (self.vSpace+self.barHeight)
		posY += 5
		for hitnum_i in range( self.hitnum ):
			status = self.setupBlastResultGlobalVar(hitnum_i)
			if status != "good":
				print "blast result error: No hits found"
				break
			self.generatePictureBlastResultOverlap(posY+120)
			posY += (2*self.barHeight+self.vSpace*5)

  # ---------------------------------------------------

	def generatePictureGCContent(self, posY):

		baseY = posY + self.GCContentSizeY - 2    # the baseline Y coordinate
		borderColor = 'gray'
		backgroundColor = 'black'
		slidingWindowSize = 20   # how many we are analyzing at a time
		stepSize = 3     # step size (how far we jump to the next)

		# draw a box
		posX_start = self.hSpace / 2
		posX_end = self.GC_Box_X_end
		# posX_end = self.hSpace*3 + (self.graphChartSizeX/self.maxGeneLen)*self.adjustedGraphChartSizeX
		posY_start = posY
		posY_end = posY_start + self.GCContentSizeY
		self.pic.create_rectangle(posX_start, posY_start, posX_end, posY_end, width=0, fill=borderColor)
		self.pic.create_rectangle(posX_start+1, posY_start+1, posX_end-1, posY_end-1, width=0, fill=backgroundColor)
		self.pic.create_text(posX_start+20, posY_start+20, text="GC% content", fill='white', anchor=W)

		# find GC content
		seq = self.sequences_data[self.contigIndex].getSeqBody()
		index_s = 0
		while index_s + slidingWindowSize < len(seq):
			index_e = index_s + slidingWindowSize
			GCContent = seq[index_s:index_e]
			# count number of G's and C's
			numOfGC = 0
			for ch in GCContent:
				if ch == 'G' or ch == 'C' or ch == 'q' or ch == 'c':
					numOfGC += 1
			if GCContent == 0:
				index_s += stepSize
				continue
			percentage = (numOfGC*1.0) / slidingWindowSize
			#print GCContent + str(numOfGC)
			# draw bar
			index_middle = (index_e+index_s)/2
			index_middle_left = index_middle - stepSize/2.0
			index_middle_right = index_middle + stepSize/2.0
			posX_start = self.hSpace + (index_middle_left/self.maxGeneLen)*self.adjustedGraphChartSizeX
			posX_end = self.hSpace + (index_middle_right/self.maxGeneLen)*self.adjustedGraphChartSizeX
			posY_start = baseY
			posY_end = posY_start - percentage*self.GCContentSizeY
			barColor = self.getBarColor(percentage)
			self.pic.create_rectangle(posX_start, posY_start, posX_end, posY_end, width=0, fill=barColor)
			self.pic.update()
			# update index_s
			index_s += stepSize

	def getBarColor(self, percentage):
		hexR = int( 16*percentage)
		# hexG = int( 0.0 )
		hexG = int( 8*(1-percentage))
		hexB = int( 16*(1-percentage))
		return '#' + self.int2Hex(hexR) + self.int2Hex(hexG) + self.int2Hex(hexB)

	def int2Hex(self, i):
		if i < 0:
			return str('0')
		if i >= 0 and i <= 9:
			return str(i)
		if i >= 10 and i <= 15:
			return chr( ord('A') + (i-10) )
		if i >= 16:
			return str('F')

  # ---------------------------------------------------

	def getConsecutiveInfo(self, numList):
		if len(numList) < 2:   # if not much num, just quit
			return numList
		r_l = []   # condensed resulted list
		NaN = -9999999
		firstNum = NaN         # first index
		lastNum = NaN          # the previous index
		count = 0
		for num in numList:
			# this handles the first index, then jump to the next
			if count == 0:    # set the first index
				firstNum = num
				lastNum = num
				count = 1
				continue
			# this is basically the else case, for the next index
			if lastNum == num - 1:
				count += 1
				lastNum = num
			else:
				# append the old info
				info = [firstNum, count]
				r_l.append(info)
				# save the new info
				firstNum = num
				lastNum = num
				count = 1

		# append the old info
		info = [firstNum, count]
		r_l.append(info)

		return r_l


	def setupBlastResultGlobalVar(self, index):

		print ">>>>>>>>>>>>>>>>>>>>>>>>>---------------------------"
		print "TIGR index: " + str(index)
		try:
			[infoData, posData] = self.blastResult[index]
			[hitNum, gapListC, gapListT] = self.gapInfo[index]
		except:
			return "error"
		self.subjectID = infoData[0]
		self.query_first = infoData[1]
		self.query_last = infoData[2]
		self.subject_first = infoData[3]
		self.subject_last = infoData[4]
		self.len_q = infoData[5]
		self.len_s = infoData[6]
		print "infoData: " + str(infoData)
		print "posData: " + str(posData)
		self.gapListC = self.getConsecutiveInfo(gapListC)    # contig gap info
		self.gapListT = gapListT    # tigr gap info
		print "gapListC: " + str(gapListC)
		print "gapListT: " + str(gapListT)

		# change direction
		self.dir_bottom_bar = "F"
		if self.query_first > self.query_last:
			self.dir_bottom_bar = "R"
		if posData[0] == "forward":
			self.dir_top_bar = "F"
		else:
			self.dir_top_bar = "R"

		# store exons info
		positions = posData[1]
		exons_raw = split(positions, "|")
		self.introns = []
		self.exons = []
		for exon_raw in exons_raw:
			index1_str, index2_str = split(exon_raw, "-")
			index1, index2 = int(index1_str), int(index2_str)
			if self.dir_top_bar == "F":
				self.exons.append( [index1, index2] )
			elif self.dir_top_bar == "R":
				self.exons.append( [index2, index1] )
		if self.dir_top_bar == "R":
			self.exons.reverse()
		# store introns info
		if len(self.exons) > 1:
			numExons = len(self.exons)
			for ei in range(numExons-1):
				left_pair = self.exons[ei]
				right_pair = self.exons[ei+1]
				left = left_pair[1]
				right = right_pair[0]
				### CORRECTION BY 1 NUCLEOTIDE ###
				# intron_size = right - left
				intron_size = right - left - 1
				self.introns.append( intron_size )

		return "good"

  # ---------------------------------------------------

	def BlastResult_placeStartEndIndexes(self, start, end, start_str, end_str, posY, textcolor):
		# place the start index
		textcolor = 'cyan'
		if self.dir_top_bar == "F":
			### START INDEX ###
			posX = self.hSpace + (atof(start_str)/self.maxGeneLen)*self.adjustedGraphChartSizeX
			self.pic.create_text(posX-20, posY+self.barHeight*1.5, text=(str(start_str)+" nt"), fill=textcolor)
			###  END INDEX  ###
			posX = self.hSpace + (atof(end_str)/self.maxGeneLen)*self.adjustedGraphChartSizeX
			self.pic.create_text(posX+25, posY+self.barHeight*1.5, text=(str(end_str)+" nt"), fill=textcolor)
		if self.dir_top_bar == "R":
			### START INDEX ###
			posX = self.hSpace + (atof(start_str)/self.maxGeneLen)*self.adjustedGraphChartSizeX
			self.pic.create_text(posX-20, posY+self.barHeight*1.5, text=(str(start_str)+" nt"), fill=textcolor)
			###  END INDEX  ###
			posX = self.hSpace + (atof(end_str)/self.maxGeneLen)*self.adjustedGraphChartSizeX
			self.pic.create_text(posX+25, posY+self.barHeight*1.5, text=(str(end_str)+" nt"), fill=textcolor)


  # ---------------------------------------------------

	def generatePictureBlastResultOverlap(self, posY=0):

		#########################################################################
		### THIS IS A MOST IMPORTANT AND COMPLEX/COMPLICATED FUNCTION         ###
		### SOME CALCULATION OF COORDINATES MAY LOOK REALLY CONFUSING         ###
		### GAPS ON BLAST ALIGNMENT DO NOT ALLOW TO DISPLAY INTRONS PERFECTLY ###
		###                                                                   ###
		### THE PROBLEM IS THAT THE LENGTH OF BLAST ALIGNMENT DOES NOT CORRESPOND
		### TO THE LENGTHS OF ORIGINAL SEQUENCES. IT MAY BE LONGER BUT WE DISPLAY
		### ITS LENTH ACCORDING TO CONTIG (EST) LENGTH                        ###
		#########################################################################

		# constants
		end = float(self.len_s)
		totalLen = (self.graphChartSizeX*1.0)
		totalLen2 = (self.graphChartSizeX*1.0/self.maxGeneLen)*(end)
		textcolor = 'white' # pick text color for each seq
		text_barHeight = self.barHeight   # height for the text

		# decide start and end indexes
		### TOP BAR - SUBJECT (ARABIDOPSIS) ###
		### BOTTOM BAR - QUERY (EST CONTIG) ###
		if self.dir_top_bar == "F":
			start = self.subject_first * 1.0
			end = self.subject_last * 1.0
		else:
			end = self.subject_first * 1.0
			start = self.subject_last * 1.0
		if self.dir_bottom_bar == "F":
			start_str = self.query_first
			end_str = self.query_last
		else:
			end_str = self.query_first
			start_str = self.query_last

		# place the start and end indexes
		self.BlastResult_placeStartEndIndexes(start, end, start_str, end_str, posY, textcolor)

		###  DRAW BLAST HITS  ###
		# place the shorter seq bar
		barcolor = 'lightgreen'
		start = atof(start_str) * 1.0
		end = atof(end_str) * 1.0
		### ARABIDOPSIS HIT START ###
		posX_start = self.hSpace + (start/self.maxGeneLen)*self.adjustedGraphChartSizeX
		###  ARABIDOPSIS HIT END  ###
		posX_end = self.hSpace + (end/self.maxGeneLen)*self.adjustedGraphChartSizeX
		###      Y POSITIONS      ###
		posY_start = posY
		posY_end = posY_start + self.barHeight
		### DRAW THE BLAST HIT BAR ###
		self.pic.create_rectangle(posX_start, posY_start, posX_end, posY_end, width=0, fill=barcolor)


		# put introns and exons ------------------------

		# take off the extrons on the left
		exon_lens = []
		exon_p_list = []
		curr_pos = 0
		### START - END POSITIONS TO DISPLAY INTRONS - EXONS ###
		### MULTIPLY BY 3: PROTEIN LENGTH --> DNA LENGTH
		# start = self.subject_first * 3
		### START CORRECTION BY 2 NUCLEOTIDES ###
		start = self.subject_first * 3 - 2
		end = self.subject_last * 3 
		########################################################
		first_flag = 0
		skip_num = 0
		included_num_list = []
		print "start: " + str(start)
		print "end: " + str(end)
		for exon_pair_i in range( len(self.exons) ):
			exon_pair = self.exons[exon_pair_i]
			### EXON LENGTH CALCULATION ###
			# diff = int( fabs(exon_pair[1] - exon_pair[0]) )
			### CORRECTION BY 1 NUCLEOTIDE ###
			diff = int( fabs(exon_pair[1] - exon_pair[0]) + 1)
			### ? IS IT OK ? ###
			### curr_pos += diff + 1
			curr_pos += diff
			print "curr_pos: " + str(curr_pos)
			if curr_pos < start:
				skip_num += 1
				continue
			elif curr_pos > end:
				if first_flag == 0:
					break
				last_pos = curr_pos - diff
				print "end: " + str(end)
				print "curr_pos: " + str(curr_pos)
				print "diff: " + str(diff)
				print "last_pos: " + str(last_pos)
				exon_p = last_pos + (end-last_pos)/2.0 - start
				print "exon_p: " + str(exon_p)
				exon_p_list.append(exon_p)
				exon_lens.append(end-last_pos)
				break
			else:
				# deal with the first time entry
				if first_flag == 0:
					exon_p = (curr_pos-start)/2.0
					exon_p_list.append(exon_p)
					exon_lens.append(curr_pos-start)
					included_num_list.append( exon_pair_i )
					first_flag = 1
					continue
				exon_p = (curr_pos-start) - diff/2.0
				exon_p_list.append(exon_p)
				exon_lens.append(diff)
				included_num_list.append( exon_pair_i )
		print "exon lens: " + str(exon_lens)
		print "exon p_list: " + str(exon_p_list)

		# take off the introns on the left
		intron_lens = []
		print self.exons
		print included_num_list
		print self.introns
		for included_i in included_num_list:
			intron_lens.append( self.introns[included_i] )
			
		print "intron lens: " + str(intron_lens)

		#== place exons
		if len(exon_lens) > 1:
			for exon_i in range( len(exon_lens) ):
				if self.dir_bottom_bar == "F":
					exon_l = exon_lens[exon_i]
					exon_p = exon_p_list[exon_i] * 1.0
					start = atof(start_str) * 1.0
					start = (start/self.maxGeneLen)*self.adjustedGraphChartSizeX
					exon_p = (exon_p/self.maxGeneLen)*self.adjustedGraphChartSizeX
					### FORWARD COUNTING ###
					posX = self.hSpace + start + exon_p
					self.pic.create_text(posX, posY+text_barHeight+self.barHeight*0.5+1, text=str(exon_l), fill='yellow')
				if self.dir_bottom_bar == "R":
					exon_l = exon_lens[exon_i]
					exon_p = exon_p_list[exon_i] * 1.0
					start = atof(start_str) * 1.0
					start = (start/self.maxGeneLen)*self.adjustedGraphChartSizeX
					end_adj = (end_str/self.maxGeneLen)*self.adjustedGraphChartSizeX
					exon_p = (exon_p/self.maxGeneLen)*self.adjustedGraphChartSizeX
					### REVERSE COUNTING ###
					posX = end_adj + self.hSpace - exon_p
					self.pic.create_text(posX, posY+text_barHeight+self.barHeight*0.5+1, text=str(exon_l), fill='yellow')

		#== place introns
		#-- place vertical lines
		intronLineColor = "red"
		curr_pos = 0
		for intron_i in range( len(intron_lens) ):
			if self.dir_bottom_bar == "F":
				pos = curr_pos + exon_lens[intron_i] * 1.0
				start = atof(start_str) * 1.0
				# INTRON POSITION
				start = (start/self.maxGeneLen)*self.adjustedGraphChartSizeX
				pos = (pos/self.maxGeneLen)*self.adjustedGraphChartSizeX
				posX_start = self.hSpace + start + pos
				posX_end = posX_start + 1
				posY_start = posY
				posY_end = posY_start + self.barHeight
				self.pic.create_rectangle(posX_start, posY_start, posX_end, posY_end, width=0, fill=intronLineColor)
				# draw triangle
				triangle_size = 10
				posX1 = posX_start
				posY1 = posY_end
				posX2 = posX1 - triangle_size
				posY2 = posY1 + triangle_size
				posX3 = posX1 + triangle_size
				posY3 = posY1 + triangle_size
				self.pic.create_line(posX1, posY1, posX2, posY2, fill=intronLineColor)
				self.pic.create_line(posX1, posY1, posX3, posY3, fill=intronLineColor)
				self.pic.create_line(posX2, posY2, posX3, posY3, fill=intronLineColor)
				# place intron value
				intron_val = intron_lens[intron_i]
				posX = posX_start
				self.pic.create_text(posX, posY+text_barHeight+self.barHeight*0.5+triangle_size+2, \
					text=str(intron_val), fill=textcolor)

				# place intron index
				intron_index = skip_num + intron_i + 1
				intron_index_str = "[" + str(intron_index) + "]"
				posX = posX_start
				self.pic.create_text(posX, posY+2*text_barHeight+self.barHeight*0.5+triangle_size+3, \
					text=intron_index_str, fill=textcolor)

				# update curr pos
				curr_pos += exon_lens[intron_i] * 1.0

			if self.dir_bottom_bar == "R":
				pos = curr_pos + exon_lens[intron_i] * 1.0
				start = atof(start_str) * 1.0
				# INTRON POSITION
				start = (start/self.maxGeneLen)*self.adjustedGraphChartSizeX
				end_adj = (end_str/self.maxGeneLen)*self.adjustedGraphChartSizeX
				pos = (pos/self.maxGeneLen)*self.adjustedGraphChartSizeX
				# COUNT FROM THE END
				posX_start = self.hSpace + end_adj - pos
				posX_end = posX_start+1
				posY_start = posY
				posY_end = posY_start + self.barHeight
				self.pic.create_rectangle(posX_start, posY_start, posX_end, posY_end, width=0, fill=intronLineColor)
				# draw triangle
				triangle_size = 10
				posX1 = posX_start
				posY1 = posY_end
				posX2 = posX1 - triangle_size
				posY2 = posY1 + triangle_size
				posX3 = posX1 + triangle_size
				posY3 = posY1 + triangle_size
				self.pic.create_line(posX1, posY1, posX2, posY2, fill=intronLineColor)
				self.pic.create_line(posX1, posY1, posX3, posY3, fill=intronLineColor)
				self.pic.create_line(posX2, posY2, posX3, posY3, fill=intronLineColor)
				# place intron value
				intron_val = intron_lens[intron_i]
				posX = posX_start
				self.pic.create_text(posX, posY+text_barHeight+self.barHeight*0.5+triangle_size+2, \
					text=str(intron_val), fill=textcolor)

				# place intron index
				intron_index = skip_num + intron_i + 1
				intron_index_str = "[" + str(intron_index) + "]"
				posX = posX_start
				self.pic.create_text(posX, posY+2*text_barHeight+self.barHeight*0.5+triangle_size+3, \
					text=intron_index_str, fill=textcolor)

				# update curr pos
				curr_pos += exon_lens[intron_i] * 1.0

		# place tigr gap lines at tigr
		### GAPS ON ARABIDOPSIS ###
		gap_tt_color = "blue"
		for t_pos in self.gapListT:
			start = atof(start_str) * 1.0
			posX_start = self.hSpace + ((start+t_pos)/self.maxGeneLen)*self.adjustedGraphChartSizeX
			print "gap pos start: " + str(posX_start)
			posX_end = posX_start
			posY_start = posY
			posY_end = posY_start + self.barHeight
			self.pic.create_rectangle(posX_start, posY_start, posX_end, posY_end, width=0, fill=gap_tt_color)

		# place contig gap lines at tigr
		### GAPS ON CONTIG CONSENSUS ###
		gap_ct_color = "orange"

		actual_align_length = 0

		for c_info in self.gapListC:
			[c_pos, c_len] = c_info
			start = atof(start_str) * 1.0
			posX_start = self.hSpace + ((start+c_pos)/self.maxGeneLen)*self.adjustedGraphChartSizeX
			print "gap pos start: " + str(posX_start)
			posX_end = posX_start
			posY_start = posY
			posY_end = posY_start + self.barHeight
			self.pic.create_rectangle(posX_start, posY_start, posX_end, posY_end, width=0, fill=gap_ct_color)
			# draw triangle
			triangle_size = 10
			posX1 = posX_start
			posY1 = posY_start
			posX2 = posX1 - triangle_size
			posY2 = posY1 - triangle_size
			posX3 = posX1 + triangle_size
			posY3 = posY1 - triangle_size
			self.pic.create_line(posX1, posY1, posX2, posY2, fill=gap_ct_color)
			self.pic.create_line(posX1, posY1, posX3, posY3, fill=gap_ct_color)
			self.pic.create_line(posX2, posY2, posX3, posY3, fill=gap_ct_color)
			# place gap value
			posX = posX_start
			self.pic.create_text(posX, posY-text_barHeight-triangle_size+3, text=str(c_len), fill='green')
			### INCR BLAST ALIGNMENT ###
			actual_align_length = actual_align_length + c_len
			print actual_align_length
			# draw gap line on the contig line
			posX_contig_start = posX_start
			posX_contig_end = posX_contig_start
			posY_contig_start = self.posY_contig
			posY_contig_end = posY_contig_start + self.barHeight
			self.pic.create_rectangle(posX_contig_start, posY_contig_start, \
				posX_contig_end, posY_contig_end, width=0, fill=gap_ct_color)

		### CREATE MARK FOR ACTUAL LENGTH OF BLAST ALIGNMENT ###
		# ???????????????????????????????????????????????????? #
		########################################################

		aln_end = atof(end_str) * 1.0
		alignX_end = self.hSpace + ((aln_end + actual_align_length)/self.maxGeneLen)*self.adjustedGraphChartSizeX
		self.pic.create_rectangle(alignX_end-1, posY_start, alignX_end+1, posY_end, width=0, fill='pink')

		# place tigr seq id
		### ARABIDOPSIS ID ###
		posX = self.hSpace*2.5 + self.graphChartSizeX
		self.pic.create_text(posX-60, posY+10, text=str(self.subjectID), fill='gold')
		self.pic.update()

  # ---------------------------------------------------

	def moveSeqTextWinContent(self, event):
		x = event.x - self.hSpace
		fraction = (x+20)/(self.graphChartSizeX * 1.0)
		self.moveSeqTextWinContentFraction(fraction)

	def moveSeqTextWinContentPos(self, pos):
		fraction = (pos-20)/(self.maxGeneLen * 1.0)
		self.moveSeqTextWinContentFraction(fraction)

	def moveSeqTextWinContentFraction(self, fraction):
		if fraction < 0:
			fraction = 0
		if fraction > 1:
			fraction = 1
		if self.SeqTextWin_open == 0:    # if text win not open, open it
			self.generateSeqTextWin()
		# move the text to the location of interest
		self.SeqTextWin_content.xview(MOVETO, fraction)

  # ---------------------------------------------------

	def highlightTextWinGenes(self):
		L_str = self.CVLTR_L_text.get()        # left index
		LX_str = self.CVLTR_LX_text.get()      # left excluded index
		R_str = self.CVLTR_R_text.get()        # right index
		RX_str = self.CVLTR_RX_text.get()      # right excluded index
		doLeftFlag = 1   # indicate we should highlight the left one
		doRightFlag = 1   # indicate we should highlight the right one
		if L_str == "" or LX_str == "":   # no input yet, so quit
			doLeftFlag = 0
		if R_str == "" or RX_str == "":   # no input yet, so quit
			doRightFlag = 0
		# clear the old background color
		self.SeqTextWin_content.tag_delete('interested_tag')
		# draw the new background color
		if doLeftFlag == 1:
			L = int(L_str) + self.seqNameCharSpace
			LX = int(LX_str) + self.seqNameCharSpace
			for i in range(1, self.numOfBars+1):
				startingPos = "%d.%d" % (i, LX)
				endingPos = "%d.%d" % (i, L)
				self.SeqTextWin_content.tag_add('interested_tag', startingPos, endingPos)
		if doRightFlag == 1:
			R = int(R_str) + self.seqNameCharSpace
			RX = int(RX_str) + self.seqNameCharSpace
			for i in range(1, self.numOfBars+1):
				startingPos = "%d.%d" % (i, R)
				endingPos = "%d.%d" % (i, RX)
				self.SeqTextWin_content.tag_add('interested_tag', startingPos, endingPos)
		self.SeqTextWin_content.tag_config('interested_tag', background='yellow')

  # ---------------------------------------------------

	def drawLeftBox(self):
		L_str = self.CVLTR_L_text.get()        # left index
		LX_str = self.CVLTR_LX_text.get()      # left excluded index
		if L_str == "" or LX_str == "":   # no input yet, so quit
			return
		L = int(L_str)
		LX = int(LX_str)

		# draw the box
		x0 = self.convert_seqPos_to_pixelPos(LX)
		x1 = self.convert_seqPos_to_pixelPos(L)
		self.drawBox(x0, x1, "boxL")

  # ---------------------------------------------------

	def drawRightBox(self):
		R_str = self.CVLTR_R_text.get()        # right index
		RX_str = self.CVLTR_RX_text.get()      # right excluded index
		if R_str == "" or RX_str == "":   # no input yet, so quit
			return
		R = int(R_str)
		RX = int(RX_str)

		# draw the box
		x0 = self.convert_seqPos_to_pixelPos(R)
		x1 = self.convert_seqPos_to_pixelPos(RX)
		self.drawBox(x0, x1, "boxR")

  # ---------------------------------------------------

	def drawBox(self, x0, x1, tag):
		self.pic.delete(tag)
		y0 = self.vSpace / 2
		y1 = self.maxImageSizeY - (self.vSpace/2) + 100
		if x0 < x1 and y0 < y1:    # valid case
			if x1-x0 >= 30:    # recommended case, box is big enough
				self.pic.create_rectangle(x0, y0, x1, y1, tags=tag, outline='white', width=1)
			else:     # box is small, so display in different color
				self.pic.create_rectangle(x0, y0, x1, y1, tags=tag, outline='yellow', width=2)

  # ---------------------------------------------------

	def onShiftLeftClick(self, event):
		if self.CVLTRWin_open == 0: # if not already open
			self.showContigLTRWin(event) # open a new win
		self.CVLTR_fill_in_left_excluded_index(event)
		self.moveSeqTextWinContent(event) # move the text
		self.highlightTextWinGenes() # highlight the corresponding genes
		self.drawLeftBox() # draw the rectangle
		self.sendToPerlPrimer()  # send data to Perl Primer

  # ---------------------------------------------------

	def onShiftRightClick(self, event):
		if self.CVLTRWin_open == 0: # if not already open
			self.showContigLTRWin(event) # open a new win
		self.CVLTR_fill_in_right_excluded_index(event)
		self.moveSeqTextWinContent(event) # move the text
		self.highlightTextWinGenes() # highlight the corresponding genes
		self.drawRightBox() # draw the rectangle
		self.sendToPerlPrimer()  # send data to Perl Primer

  # ---------------------------------------------------

	def onLeftClick(self, event):
		if self.CVLTRWin_open == 0: # if not already open
			self.showContigLTRWin(event) # open a new win
		self.CVLTR_fill_in_left_index(event)
		self.moveSeqTextWinContent(event) # move the text
		self.highlightTextWinGenes() # highlight the corresponding genes
		self.updateLength() # update LR difference
		self.drawLeftBox() # draw the rectangle
		self.sendToPerlPrimer()  # send data to Perl Primer

  # ---------------------------------------------------

	def onMiddleClick(self, event):
		if self.CVLTRWin_open == 0: # if not already open
			self.showContigLTRWin(event) # open a new win
		self.CVLTR_fill_in_middle_index(event)
		self.moveSeqTextWinContent(event) # move the text
		self.highlightTextWinGenes() # highlight the corresponding genes

  # ---------------------------------------------------

	def onRightClick(self, event):
		if self.CVLTRWin_open == 0: # if not already open
			self.showContigLTRWin(event) # open a new win
		self.CVLTR_fill_in_right_index(event)
		self.moveSeqTextWinContent(event) # move the text
		self.highlightTextWinGenes() # highlight the corresponding genes
		self.updateLength() # update LR difference
		self.drawRightBox() # draw the rectangle
		self.sendToPerlPrimer()  # send data to Perl Primer

  # ---------------------------------------------------

	def SeqTextWinDestroy(self, event):
		self.SeqTextWin_open = 0 # indicate close

  # ---------------------------------------------------

	def LTRWinDestroy(self, event):
		self.CVLTRWin_open = 0 # indicate close

  # ---------------------------------------------------

	def interestListWinDestroy(self, event):
		global g_interestListWin_open
		g_interestListWin_open = 0 # indicate close

  # ---------------------------------------------------

	def showContigLTRWin(self, event):

		# setup up a new window and some components
		self.contigViewerLTRWin = Toplevel()
		self.contigViewerLTRWin.title("Indexes *" + self.contigName + "*")
		self.CVLTRWin_open = 1 # indicate open
		self.contigViewerLTRWin.bind('<Destroy>', self.LTRWinDestroy)

		frame_1 = Frame(self.contigViewerLTRWin)
		frame_1.pack(side = TOP, fill = BOTH, expand = True)

		# contig name label and entry
		self.CVLTR_cID_label = Label(frame_1, text="Contig ID:")
		self.CVLTR_cID_label.pack( side=LEFT, padx = 5)
		self.CVLTR_cID_text = Entry(frame_1, name="contigID_text", width=20)
		self.CVLTR_cID_text.pack( side=LEFT, padx = 5)

		# left index label and entry
		self.CVLTR_L_label = Label(frame_1, text="L")
		self.CVLTR_L_label.pack( side=LEFT, padx = 5)
		self.CVLTR_L_text = Entry(frame_1, name="l_text", width=5)
		self.CVLTR_L_text.pack( side=LEFT, padx = 5)

		# middle index label and entry
		self.CVLTR_M_label = Label(frame_1, text="M")
		self.CVLTR_M_label.pack( side=LEFT, padx = 5)
		self.CVLTR_M_text = Entry(frame_1, name="m_text", width=5)
		self.CVLTR_M_text.pack( side=LEFT, padx = 5)

		# right index label and entry
		self.CVLTR_R_label = Label(frame_1, text="R")
		self.CVLTR_R_label.pack( side=LEFT, padx = 5)
		self.CVLTR_R_text = Entry(frame_1, name="r_text", width=5)
		self.CVLTR_R_text.pack( side=LEFT, padx = 5)

		# length label and entry (R-L)
		self.CVLTR_length_label = Label(frame_1, text="length")
		self.CVLTR_length_label.pack( side=LEFT, padx = 5)
		self.CVLTR_length_text = Entry(frame_1, name="length_text", width=5)
		self.CVLTR_length_text.pack( side=LEFT, padx = 5)

		# left excluded index label and entry
		self.CVLTR_LX_label = Label(frame_1, text="LX")
		self.CVLTR_LX_label.pack( side=LEFT, padx = 5)
		self.CVLTR_LX_text = Entry(frame_1, name="lx_text", width=5)
		self.CVLTR_LX_text.pack( side=LEFT, padx = 5)

		# right excluded index label and entry
		self.CVLTR_RX_label = Label(frame_1, text="RX")
		self.CVLTR_RX_label.pack( side=LEFT, padx = 5)
		self.CVLTR_RX_text = Entry(frame_1, name="rx_text", width=5)
		self.CVLTR_RX_text.pack( side=LEFT, padx = 5)

		# length of the contig (constant)
		self.CVLTR_contigLength_label = Label(frame_1, text="Contig Length")
		self.CVLTR_contigLength_label.pack( side=LEFT, padx = 5)
		self.CVLTR_contigLength_text = Entry(frame_1, name="contigLength_text", width=5)
		self.CVLTR_contigLength_text.pack( side=LEFT, padx = 5)

		frame_2 = Frame(self.contigViewerLTRWin)
		frame_2.pack(side = TOP, fill = BOTH, expand = True)

		# reset button
		self.CVLTR_reset_button = Button(frame_2, text="Reset", command=self.CVLTR_resetIndexes)
		self.CVLTR_reset_button.pack(side=RIGHT, padx = 5)

		# add to interest list button
		self.CVLTR_addToInterestList_button = Button(frame_2, text="Add to list", command=self.addToInterestList)
		self.CVLTR_addToInterestList_button.pack(side=RIGHT, padx = 5)

		# generate file for PerlPrimer program
		self.CVLTR_PerlPrimer_button = Button(frame_2, text="PerlPrimer", command=self.addToPerlPrimer)
		self.CVLTR_PerlPrimer_button.pack(side=RIGHT, padx = 5)

		# fill in the contig name and contig length
		self.CVLTR_fill_in_ContigName_and_contigLength(event)

  # ---------------------------------------------------

	def sendToPerlPrimer(self):

		cont_id = self.CVLTR_cID_text.get()
		excl5A  = self.CVLTR_LX_text.get()
		excl5B  = self.CVLTR_L_text.get()
		excl3A  = self.CVLTR_R_text.get()
		excl3B  = self.CVLTR_RX_text.get()
		contigBody = self.contigBody
		contigBody = contigBody.replace("-", "")

		# don't send while data is not complete
		if cont_id == "" or excl5A == "" or excl5B == "" or excl3A == "" or excl3B == "" or contigBody == "":
			return

		# send packet
		packet = ">" + cont_id + " 5prime_region["
		packet += excl5A + "-" + excl5B + "]"
		packet += " 3prime_region[" + excl3A + "-" + excl3B + "]"
		packet += '\n' + contigBody
		self.clientSend(packet)

	def clientSend(self, packet):
		self.wm.clientSend(packet)

  # ---------------------------------------------------

	def addToPerlPrimer(self):

		global g_use_singleton
		global g_seqNameCharSpace

		if g_use_singleton == "FALSE":
			singleton_flag = 0
		if g_use_singleton == "TRUE":
			singleton_flag = 1

		cont_id = self.CVLTR_cID_text.get()
		excl5B  = self.CVLTR_L_text.get()
		# self.CVLTR_M_text.get()
		excl3A  = self.CVLTR_R_text.get()
		# self.CVLTR_length_text.get()
		excl5A  = self.CVLTR_LX_text.get()
		excl3B  = self.CVLTR_RX_text.get()
		# self.CVLTR_contigLength_text.get()

		print cont_id + '\t' + excl5A + '\t' + excl5B + '\t' + excl3A + '\t' + excl3B + '\n'

		start = 1.0
		if singleton_flag == 0:
			# pattern = "Contig"
			pattern = "------------------------------------------------------------"
		if singleton_flag == 1:
			pattern = "------------------------------------------------------------"

		find_me = self.SeqTextWin_content.search(pattern, start, stopindex=END)

		seq = self.SeqTextWin_content.get(find_me, END)
		atgc = seq
		atgc_clean = ""
		for t in atgc:
			n = t
			if t == '-':
				n = ''
			if t == '\n':
				n = ''
			atgc_clean += n
		# print seq
		# print atgc
		atgc_clean = atgc_clean[g_seqNameCharSpace:]
		print atgc_clean + '\n'

		filename = asksaveasfilename() # save all those
		open(filename, 'w').write(">" + cont_id + " 5prime_region[" + excl5A + "-" + excl5B + "]" \
						+ " 3prime_region[" + excl3A + "-" + excl3B + "]" \
						+ " page[1] " + '\n' + atgc_clean + '\n')

  # ---------------------------------------------------

	def showInterestListWin(self):

		global g_interestListWin
		global g_interestListWin_open
		global g_interestListIndex
		global g_interestList_content

		# setup up a new window and some components
		g_interestListWin = Toplevel()
		g_interestListWin.title("Interest List")
		g_interestListWin.geometry("500x200")
		g_interestListWin_open = 1   # indicate open
		g_interestListIndex = 1      # beginning row location for insertion
		g_interestListWin.bind('<Destroy>', self.interestListWinDestroy)
		g_interestListWin.resizable(height=True, width=True)

		# set up textarea
		frame_1 = Frame(g_interestListWin)
		frame_1.pack(side = TOP, fill = BOTH, expand = True)
		g_interestList_content = Text(frame_1, height=2, width=10, wrap=NONE)
		g_interestList_content.pack(side = LEFT, fill = BOTH, expand = True)

		# set up scrollable bars
		vertical_scrollbar = Scrollbar(frame_1, orient=VERTICAL, command=g_interestList_content.yview)
		vertical_scrollbar.pack(side = LEFT, fill = Y)

		frame_2 = Frame(g_interestListWin)
		frame_2.pack(side = TOP, fill = X)
		horizontal_scrollbar = Scrollbar(frame_2, orient=HORIZONTAL, command=g_interestList_content.xview)
		horizontal_scrollbar.pack(fill = X)
		g_interestList_content.config(xscrollcommand=horizontal_scrollbar.set)
		g_interestList_content.config(yscrollcommand=vertical_scrollbar.set)

		# save alignment button
		frame_3 = Frame(g_interestListWin)
		frame_3.pack(side = TOP, fill = X)
		saveInterestListButton = Button(frame_3, text="Save as file", command=self.saveInterestList)
		saveInterestListButton.pack()

  # ---------------------------------------------------

	def addToInterestList(self):

		global g_interestListWin
		global g_interestListWin_open
		global g_interestListIndex
		global g_interestList_content

		if g_interestListWin_open == 0: # if not already open
			self.showInterestListWin() # open a new win

		# construct the string
		sep = "\t"
		str = ""
		str = str + self.CVLTR_cID_text.get() + sep
		str = str + self.CVLTR_L_text.get() + sep
		str = str + self.CVLTR_M_text.get() + sep
		str = str + self.CVLTR_R_text.get() + sep
		str = str + self.CVLTR_length_text.get() + sep
		str = str + self.CVLTR_LX_text.get() + sep
		str = str + self.CVLTR_RX_text.get() + sep
		str = str + self.CVLTR_contigLength_text.get()

		# insert the text into the interest text win
		myPos = "%s.0" % (g_interestListIndex)
		g_interestList_content.insert(myPos, str+"\n")
		g_interestListIndex = g_interestListIndex + 1

		# move the textarea downward if there are too many
		if g_interestListIndex > 4:
			g_interestList_content.yview(SCROLL, 1, UNITS)

  # ---------------------------------------------------

	def saveInterestList(self):

		global g_interestListWin
		global g_interestListWin_open
		global g_interestListIndex
		global g_interestList_content

		str = g_interestList_content.get("1.0", END) # all the interesting indexes
		filename = asksaveasfilename() # save all those
		open(filename, 'w').write(str)

  # ---------------------------------------------------

	def updateLength(self): # update LR difference
		if self.CVLTR_L_text.get() == "" or self.CVLTR_R_text.get() == "":
			return    # quit if data not ready
		self.CVLTR_length_text.delete(0, END) # clear it first
		left = int( self.CVLTR_L_text.get() )
		right = int( self.CVLTR_R_text.get() )
		diff = right - left
		self.CVLTR_length_text.insert(0, str(diff)) # fill it in

  # ---------------------------------------------------

	def CVLTR_resetIndexes(self):
		# clear out the indexes
		self.CVLTR_L_text.delete(0, 'end')
		self.CVLTR_M_text.delete(0, 'end')
		self.CVLTR_R_text.delete(0, 'end')
		self.CVLTR_length_text.delete(0, 'end')
		self.CVLTR_LX_text.delete(0, 'end')
		self.CVLTR_RX_text.delete(0, 'end')
		# erase the boxes in the pic
		self.pic.delete('boxL')
		self.pic.delete('boxR')
		# clear the highlighted area
		self.SeqTextWin_content.tag_delete('interested_tag')

  # ---------------------------------------------------

	def CVLTR_fill_in_ContigName_and_contigLength(self, event):
		print "X=%s Y=%s" % (event.x, event.y)
		self.CVLTR_cID_text.delete(0, END) # clear it first
		self.CVLTR_cID_text.insert(0, self.contigName) # fill it in
		self.CVLTR_contigLength_text.delete(0, END) # clear it first
		self.CVLTR_contigLength_text.insert(0, self.contigLength)  # fill it in

  # ---------------------------------------------------

	def CVLTR_fill_in_left_excluded_index(self, event):
		print "X=%s Y=%s" % (event.x, event.y)
		self.CVLTR_LX_text.delete(0, END) # clear it first
		pos = self.convert_pixelPos_to_seqPos(event.x)
		self.CVLTR_LX_text.insert(0, str(int(pos))) # fill it in

  # ---------------------------------------------------

	def CVLTR_fill_in_right_excluded_index(self, event):
		print "X=%s Y=%s" % (event.x, event.y)
		self.CVLTR_RX_text.delete(0, END) # clear it first
		pos = self.convert_pixelPos_to_seqPos(event.x)
		self.CVLTR_RX_text.insert(0, str(int(pos))) # fill it in

  # ---------------------------------------------------

	def CVLTR_fill_in_left_index(self, event):
		print "X=%s Y=%s" % (event.x, event.y)
		self.CVLTR_L_text.delete(0, END) # clear it first
		pos = self.convert_pixelPos_to_seqPos(event.x)
		self.CVLTR_L_text.insert(0, str(int(pos))) # fill it in

  # ---------------------------------------------------

	def CVLTR_fill_in_middle_index(self, event):
		print "X=%s Y=%s" % (event.x, event.y)
		self.CVLTR_M_text.delete(0, END) # clear it first
		pos = self.convert_pixelPos_to_seqPos(event.x)
		self.CVLTR_M_text.insert(0, str(int(pos))) # fill it in

  # ---------------------------------------------------

	def CVLTR_fill_in_right_index(self, event):
		print "X=%s Y=%s" % (event.x, event.y)
		self.CVLTR_R_text.delete(0, END) # clear it first
		pos = self.convert_pixelPos_to_seqPos(event.x)
		self.CVLTR_R_text.insert(0, str(int(pos))) # fill it in

  # ---------------------------------------------------

	def convert_pixelPos_to_seqPos(self, x):
		return ( (x-self.hSpace)*1.0 / self.adjustedGraphChartSizeX ) * self.maxGeneLen

  # ---------------------------------------------------

	def convert_seqPos_to_pixelPos(self, x):
		return ((x*1.0)/self.maxGeneLen) * self.adjustedGraphChartSizeX + self.hSpace

  # ---------------------------------------------------

	def displayMMError(self, type, info, hS, mGL, aGCSX, pY, bH, p):

		# pick the color according to which DIS
		barcolorMM = 'yellow'    # initial color
		if type == 'D':
			barcolorMM = 'blue'
		if type == 'I':
			barcolorMM = 'darkgreen'
		if type == 'S':
			barcolorMM = 'red'
		if type == 'XN':
			barcolorMM = 'gray'

		# draw it out
		for myPos in info:
			posX_start = hS + (myPos / mGL) * aGCSX
			posX_end = posX_start
			posY_start = pY
			posY_end = posY_start + bH
			p.create_rectangle(posX_start, posY_start, posX_end, posY_end, width=0, fill=barcolorMM)


#########################################

def main():
	contigViewerUserInputWindow().mainloop()

if __name__ == "__main__":
	main()

############## THE END ##################
