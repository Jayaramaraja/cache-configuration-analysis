import os
import sys
import re
import csv
import math
import glob
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
#########################################################################################

def plot_graphs_l1i(filename,testname):
	# open the file in universal line ending mode
	plot_dir = './plots/'+testname+'/l1i/'
	with open(filename, 'rU') as infile:
	# read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					data[header].append(value)
				except KeyError:
					data[header] = [value]
	
	# extract the variables you want
	l1i_size_set = [float(i) for i in data['l1i_size']]
	l1d_size_set = [float(i) for i in data['l1d_size']]
	l1_assoc_set = [float(i) for i in data['l1_assoc']]
	l2_size_set  = [float(i) for i in data['l2_size']]
	l2_assoc_set = [float(i) for i in data['l2_assoc']]
	line_size_set= [float(i) for i in data['line_size']]
	total_cost_set=[float(i) for i in data['total_cost']]
	cpi_set 	 = [float(i) for i in data['cpi']]
	cpi_vs_cost_set = [float(i) for i in data['CPIvsCOST_weighted']]
	l1d_l1i_sum_set = [x + y for x, y in zip(l1d_size_set, l1i_size_set)]
	l1d_l1i_sum_set_uniq = list(set(l1d_l1i_sum_set))
	line_size_uniq = list(set(line_size_set))
	l1i_size_uniq = list(set(l1i_size_set))
	l1d_size_uniq = list(set(l1d_size_set))
	l1_assoc_uniq = list(set(l1_assoc_set))
	l2_assoc_uniq = list(set(l2_assoc_set))
	l2_size_uniq = list(set(l2_size_set))
	full_list = zip(l1i_size_set, l1d_size_set, l1d_l1i_sum_set, l1_assoc_set, l2_size_set, l2_assoc_set, line_size_set, total_cost_set, cpi_set, cpi_vs_cost_set)
####################  		l1i 		################################
	for linesize_var in line_size_uniq:
		for l1dsize_var in l1d_size_uniq:
			for l1assoc_var in l1_assoc_uniq:
				for l2size_var in l2_size_uniq: 
					for l2assoc_var in l2_assoc_uniq:
						index_set = []
						sorted_index = []
						needed_list = []
						needed_l1i = []
						needed_cpi = []
						needed_cost = []
						needed_wc = []
						for index in range(len(line_size_set)):
							if ( (linesize_var == line_size_set[index]) & (l1dsize_var == l1d_size_set[index]) & (l1assoc_var == l1_assoc_set[index]) & (l2size_var == l2_size_set[index]) & (l2assoc_var == l2_assoc_set[index]) ):
								index_set.append(index)
								needed_list.append((index,full_list[index]))
						if len(index_set)>=3:
							needed_list = sorted(needed_list, key=lambda x:x[1][0])
							sorted_index = [item[0] for item in needed_list]
							for index in sorted_index:
								needed_l1i.append(l1i_size_set[index])
								needed_cpi.append(cpi_set[index])
								needed_cost.append(total_cost_set[index])
								needed_wc.append(cpi_vs_cost_set[index])
							print 'l1d=',l1dsize_var,'linesize=',linesize_var,'l1assoc=',l1assoc_var,'l2size=',l2size_var,'l2assoc=',l2assoc_var,'\n','indexes=',index_set,sorted_index
							print needed_list
							print needed_l1i
							print needed_cpi
							print needed_cost
							#fig, ax1 = plt.subplots()
							#ax1.plot(needed_l1i, needed_cpi, 'b*-')
							#ax1.set_xlabel('l1i size with l1dsize='+str(int(l1dsize_var))+'kB '+str(int(l1assoc_var))+'way l2size='+str(int(l2size_var))+'kB '+str(int(l2assoc_var))+'way line_size='+str(int(linesize_var))+'B')
							## Make the y-axis label and tick labels match the line color.
							#ax1.set_ylabel('CPI', color='b')
							#for tl in ax1.get_yticklabels():
							    #tl.set_color('b')
							
							#ax2 = ax1.twinx()
							#ax2.plot(needed_l1i, needed_cost, 'r*-')
							#ax2.set_ylabel('COST', color='r')
							#for tl in ax2.get_yticklabels():
							    #tl.set_color('r')
							
							host = host_subplot(111, axes_class=AA.Axes)
							plt.subplots_adjust(right=0.75)
							
							par1 = host.twinx()
							par2 = host.twinx()
							
							offset = 60
							new_fixed_axis = par2.get_grid_helper().new_fixed_axis
							par2.axis["right"] = new_fixed_axis(loc="right",
							                                    axes=par2,
							                                    offset=(offset, 0))
							
							par2.axis["right"].toggle(all=True)
							
							#host.set_xlim(min(needed_l1i), max(needed_l1i))
							#host.set_ylim(min(needed_cpi), max(needed_cpi))
							#host.set_xticks(needed_l1i)
							host.set_xlabel('l1i size with l1d='+str(int(l1dsize_var))+'kB_'+str(int(l1assoc_var))+'way_l2='+str(int(l2size_var))+'kB_'+str(int(l2assoc_var))+'way_line='+str(int(linesize_var))+'B')
							host.set_ylabel("CPI")
							par1.set_ylabel("COST")
							par2.set_ylabel("Weighted_COST")
							
							p1, = host.plot(needed_l1i, needed_cpi, '*-', label="CPI")
							p2, = par1.plot(needed_l1i, needed_cost, '+-',label="COST")
							p3, = par2.plot(needed_l1i, needed_wc, '.-',label="Weighted_COST")
							
							par1.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							par2.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							
							#host.legend(loc='upper left')
							
							host.axis["left"].label.set_color(p1.get_color())
							par1.axis["right"].label.set_color(p2.get_color())
							par2.axis["right"].label.set_color(p3.get_color())
							plt.savefig(plot_dir+testname+"_L1isize_l1d="+str(int(l1dsize_var))+"kB_"+str(int(l1assoc_var))+"way_l2="+str(int(l2size_var))+"kB_"+str(int(l2assoc_var))+"way_line="+str(int(linesize_var))+"B"+".png")
							plt.close('all')

########################################################################

def plot_graphs_l1d(filename,testname):
	# open the file in universal line ending mode 
	plot_dir = './plots/'+testname+'/l1d/'
	with open(filename, 'rU') as infile:
	# read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					data[header].append(value)
				except KeyError:
					data[header] = [value]
	
	# extract the variables you want
	l1i_size_set = [float(i) for i in data['l1i_size']]
	l1d_size_set = [float(i) for i in data['l1d_size']]
	l1_assoc_set = [float(i) for i in data['l1_assoc']]
	l2_size_set  = [float(i) for i in data['l2_size']]
	l2_assoc_set = [float(i) for i in data['l2_assoc']]
	line_size_set= [float(i) for i in data['line_size']]
	total_cost_set=[float(i) for i in data['total_cost']]
	cpi_set 	 = [float(i) for i in data['cpi']]
	cpi_vs_cost_set = [float(i) for i in data['CPIvsCOST_weighted']]
	l1d_l1i_sum_set = [x + y for x, y in zip(l1d_size_set, l1i_size_set)]
	l1d_l1i_sum_set_uniq = list(set(l1d_l1i_sum_set))
	line_size_uniq = list(set(line_size_set))
	l1i_size_uniq = list(set(l1i_size_set))
	l1d_size_uniq = list(set(l1d_size_set))
	l1_assoc_uniq = list(set(l1_assoc_set))
	l2_assoc_uniq = list(set(l2_assoc_set))
	l2_size_uniq = list(set(l2_size_set))
	full_list = zip(l1i_size_set, l1d_size_set, l1d_l1i_sum_set, l1_assoc_set, l2_size_set, l2_assoc_set, line_size_set, total_cost_set, cpi_set, cpi_vs_cost_set)

####################  		l1d 		################################
	for linesize_var in line_size_uniq:
		for l1isize_var in l1i_size_uniq:
			for l1assoc_var in l1_assoc_uniq:
				for l2size_var in l2_size_uniq: 
					for l2assoc_var in l2_assoc_uniq:
						index_set = []
						sorted_index = []
						needed_list = []
						needed_l1d = []
						needed_cpi = []
						needed_cost = []
						needed_wc = []
						for index in range(len(line_size_set)):
							if ( (linesize_var == line_size_set[index]) & (l1isize_var == l1i_size_set[index]) & (l1assoc_var == l1_assoc_set[index]) & (l2size_var == l2_size_set[index]) & (l2assoc_var == l2_assoc_set[index]) ):
								index_set.append(index)
								needed_list.append((index,full_list[index]))
						if len(index_set)>=3:
						  	print needed_list
							needed_list = sorted(needed_list, key=lambda x:x[1][1])
							sorted_index = [item[0] for item in needed_list]
							for index in sorted_index:
								needed_l1d.append(l1d_size_set[index])
								needed_cpi.append(cpi_set[index])
								needed_cost.append(total_cost_set[index])
								needed_wc.append(cpi_vs_cost_set[index])
							print 'l1i=',l1isize_var,'linesize=',linesize_var,'l1assoc=',l1assoc_var,'l2size=',l2size_var,'l2assoc=',l2assoc_var,'\n','indexes=',index_set,sorted_index
							print needed_list
							print needed_l1d
							print needed_cpi
							print needed_cost
							
							host = host_subplot(111, axes_class=AA.Axes)
							plt.subplots_adjust(right=0.75)
							
							par1 = host.twinx()
							par2 = host.twinx()
							
							offset = 60
							new_fixed_axis = par2.get_grid_helper().new_fixed_axis
							par2.axis["right"] = new_fixed_axis(loc="right",
							                                    axes=par2,
							                                    offset=(offset, 0))
							
							par2.axis["right"].toggle(all=True)
							
							host.set_xlabel('l1d size with l1i='+str(int(l1isize_var))+'kB_'+str(int(l1assoc_var))+'way_l2='+str(int(l2size_var))+'kB_'+str(int(l2assoc_var))+'way_line='+str(int(linesize_var))+'B')
							host.set_ylabel("CPI")
							par1.set_ylabel("COST")
							par2.set_ylabel("Weighted_COST")
							
							p1, = host.plot(needed_l1d, needed_cpi, '*-', label="CPI")
							p2, = par1.plot(needed_l1d, needed_cost, '+-',label="COST")
							p3, = par2.plot(needed_l1d, needed_wc, '.-',label="Weighted_COST")
							
							par1.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							par2.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							
							#host.legend(loc='upper left')
							
							host.axis["left"].label.set_color(p1.get_color())
							par1.axis["right"].label.set_color(p2.get_color())
							par2.axis["right"].label.set_color(p3.get_color())
							plt.savefig(plot_dir+testname+"_L1dsize_l1i="+str(int(l1isize_var))+"kB_"+str(int(l1assoc_var))+"way_l2="+str(int(l2size_var))+"kB_"+str(int(l2assoc_var))+"way_line="+str(int(linesize_var))+"B"+".png")
							plt.close('all')

########################################################################
def plot_graphs_l1(filename,testname):
	plot_dir = './plots/'+testname+'/l1/'
	# open the file in universal line ending mode 
	with open(filename, 'rU') as infile:
	# read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					data[header].append(value)
				except KeyError:
					data[header] = [value]
	
	# extract the variables you want
	l1i_size_set = [float(i) for i in data['l1i_size']]
	l1d_size_set = [float(i) for i in data['l1d_size']]
	l1_assoc_set = [float(i) for i in data['l1_assoc']]
	l2_size_set  = [float(i) for i in data['l2_size']]
	l2_assoc_set = [float(i) for i in data['l2_assoc']]
	line_size_set= [float(i) for i in data['line_size']]
	total_cost_set=[float(i) for i in data['total_cost']]
	cpi_set 	 = [float(i) for i in data['cpi']]
	cpi_vs_cost_set = [float(i) for i in data['CPIvsCOST_weighted']]
	l1d_l1i_sum_set = [x + y for x, y in zip(l1d_size_set, l1i_size_set)]
	l1d_l1i_sum_set_uniq = list(set(l1d_l1i_sum_set))
	line_size_uniq = list(set(line_size_set))
	l1i_size_uniq = list(set(l1i_size_set))
	l1d_size_uniq = list(set(l1d_size_set))
	l1_assoc_uniq = list(set(l1_assoc_set))
	l2_assoc_uniq = list(set(l2_assoc_set))
	l2_size_uniq = list(set(l2_size_set))
	full_list = zip(l1i_size_set, l1d_size_set, l1d_l1i_sum_set, l1_assoc_set, l2_size_set, l2_assoc_set, line_size_set, total_cost_set, cpi_set, cpi_vs_cost_set)

####################  		l1 total 		################################
	for linesize_var in line_size_uniq:
		for l1assoc_var in l1_assoc_uniq:
			for l2size_var in l2_size_uniq: 
				for l2assoc_var in l2_assoc_uniq:
					index_set = []
					sorted_index = []
					needed_list = []
					needed_l1 = []
					needed_cpi = []
					needed_cost = []
					needed_wc = []
					for index in range(len(line_size_set)):
						if ( (linesize_var == line_size_set[index]) & (l1assoc_var == l1_assoc_set[index]) & (l2size_var == l2_size_set[index]) & (l2assoc_var == l2_assoc_set[index]) ):
							index_set.append(index)
							needed_list.append((index,full_list[index]))
					if len(index_set)>=3:
						needed_list = sorted(needed_list, key=lambda x:x[1][2])
						sorted_index = [item[0] for item in needed_list]
						for index in sorted_index:
							needed_l1.append(l1d_l1i_sum_set[index])
							needed_cpi.append(cpi_set[index])
							needed_cost.append(total_cost_set[index])
							needed_wc.append(cpi_vs_cost_set[index])
						print 'linesize=',linesize_var,'l1assoc=',l1assoc_var,'l2size=',l2size_var,'l2assoc=',l2assoc_var,'\n','indexes=',index_set,sorted_index
						print needed_list
						print needed_l1
						print needed_cpi
						print needed_cost
						
						host = host_subplot(111, axes_class=AA.Axes)
						plt.subplots_adjust(right=0.75)
						
						par1 = host.twinx()
						par2 = host.twinx()
						
						offset = 60
						new_fixed_axis = par2.get_grid_helper().new_fixed_axis
						par2.axis["right"] = new_fixed_axis(loc="right",
						                                    axes=par2,
						                                    offset=(offset, 0))
						
						par2.axis["right"].toggle(all=True)
						
						host.set_xlabel('Total l1 size_'+str(int(l1assoc_var))+'way_l2='+str(int(l2size_var))+'kB_'+str(int(l2assoc_var))+'way_line='+str(int(linesize_var))+'B')
						host.set_ylabel("CPI")
						par1.set_ylabel("COST")
						par2.set_ylabel("Weighted_COST")
						
						p1, = host.plot(needed_l1, needed_cpi, '*-', label="CPI")
						p2, = par1.plot(needed_l1, needed_cost, '+-',label="COST")
						p3, = par2.plot(needed_l1, needed_wc, '.-',label="Weighted_COST")
						
						par1.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
						par2.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
						
						#host.legend(loc='upper left')
						
						host.axis["left"].label.set_color(p1.get_color())
						par1.axis["right"].label.set_color(p2.get_color())
						par2.axis["right"].label.set_color(p3.get_color())
						plt.savefig(plot_dir+testname+"_L1size_"+str(int(l1assoc_var))+"way_l2="+str(int(l2size_var))+"kB_"+str(int(l2assoc_var))+"way_line="+str(int(linesize_var))+"B"+".png")
						plt.close('all')

########################################################################

########################################################################

def plot_graphs_l1a(filename,testname):
	# open the file in universal line ending mode 
	plot_dir = './plots/'+testname+'/l1a/'
	with open(filename, 'rU') as infile:
	# read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					data[header].append(value)
				except KeyError:
					data[header] = [value]
	
	# extract the variables you want
	l1i_size_set = [float(i) for i in data['l1i_size']]
	l1d_size_set = [float(i) for i in data['l1d_size']]
	l1_assoc_set = [float(i) for i in data['l1_assoc']]
	l2_size_set  = [float(i) for i in data['l2_size']]
	l2_assoc_set = [float(i) for i in data['l2_assoc']]
	line_size_set= [float(i) for i in data['line_size']]
	total_cost_set=[float(i) for i in data['total_cost']]
	cpi_set 	 = [float(i) for i in data['cpi']]
	cpi_vs_cost_set = [float(i) for i in data['CPIvsCOST_weighted']]
	l1d_l1i_sum_set = [x + y for x, y in zip(l1d_size_set, l1i_size_set)]
	l1d_l1i_sum_set_uniq = list(set(l1d_l1i_sum_set))
	line_size_uniq = list(set(line_size_set))
	l1i_size_uniq = list(set(l1i_size_set))
	l1d_size_uniq = list(set(l1d_size_set))
	l1_assoc_uniq = list(set(l1_assoc_set))
	l2_assoc_uniq = list(set(l2_assoc_set))
	l2_size_uniq = list(set(l2_size_set))
	full_list = zip(l1i_size_set, l1d_size_set, l1d_l1i_sum_set, l1_assoc_set, l2_size_set, l2_assoc_set, line_size_set, total_cost_set, cpi_set, cpi_vs_cost_set)

####################  		l1d 		################################
	for linesize_var in line_size_uniq:
		for l1isize_var in l1i_size_uniq:
			for l1dsize_var in l1d_size_uniq:
				for l2size_var in l2_size_uniq: 
					for l2assoc_var in l2_assoc_uniq:
						index_set = []
						sorted_index = []
						needed_list = []
						needed_l1a = []
						needed_cpi = []
						needed_cost = []
						needed_wc = []
						for index in range(len(line_size_set)):
							if ( (linesize_var == line_size_set[index]) & (l1dsize_var == l1d_size_set[index]) & (l1isize_var == l1i_size_set[index]) & (l2size_var == l2_size_set[index]) & (l2assoc_var == l2_assoc_set[index]) ):
								index_set.append(index)
								needed_list.append((index,full_list[index]))
						if len(index_set)>=3:
						  	print needed_list
							needed_list = sorted(needed_list, key=lambda x:x[1][3])
							sorted_index = [item[0] for item in needed_list]
							for index in sorted_index:
								needed_l1a.append(l1_assoc_set[index])
								needed_cpi.append(cpi_set[index])
								needed_cost.append(total_cost_set[index])
								needed_wc.append(cpi_vs_cost_set[index])
							print 'l1i=',l1isize_var,'l1d=',l1dsize_var,'linesize=',linesize_var,'l2size=',l2size_var,'l2assoc=',l2assoc_var,'\n','indexes=',index_set,sorted_index
							print needed_list
							print needed_l1a
							print needed_cpi
							print needed_cost
							
							host = host_subplot(111, axes_class=AA.Axes)
							plt.subplots_adjust(right=0.75)
							
							par1 = host.twinx()
							par2 = host.twinx()
							
							offset = 60
							new_fixed_axis = par2.get_grid_helper().new_fixed_axis
							par2.axis["right"] = new_fixed_axis(loc="right",
							                                    axes=par2,
							                                    offset=(offset, 0))
							
							par2.axis["right"].toggle(all=True)
							
							host.set_xlabel('l1a with l1i='+str(int(l1isize_var))+'kB_'+'l1d='+str(int(l1dsize_var))+'kB_l2='+str(int(l2size_var))+'kB_'+str(int(l2assoc_var))+'way_line='+str(int(linesize_var))+'B')
							host.set_ylabel("CPI")
							par1.set_ylabel("COST")
							par2.set_ylabel("Weighted_COST")
							
							p1, = host.plot(needed_l1a, needed_cpi, '*-', label="CPI")
							p2, = par1.plot(needed_l1a, needed_cost, '+-',label="COST")
							p3, = par2.plot(needed_l1a, needed_wc, '.-',label="Weighted_COST")
							
							par1.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							par2.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							
							#host.legend(loc='upper left')
							
							host.axis["left"].label.set_color(p1.get_color())
							par1.axis["right"].label.set_color(p2.get_color())
							par2.axis["right"].label.set_color(p3.get_color())
							plt.savefig(plot_dir+testname+"_L1a_l1i="+str(int(l1isize_var))+"kB_l1d="+str(int(l1dsize_var))+"kB_l2="+str(int(l2size_var))+"kB_"+str(int(l2assoc_var))+"way_line="+str(int(linesize_var))+"B"+".png")
							plt.close('all')

########################################################################
########################################################################

def plot_graphs_l2(filename,testname):
	# open the file in universal line ending mode 
	plot_dir = './plots/'+testname+'/l2/'
	with open(filename, 'rU') as infile:
	# read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					data[header].append(value)
				except KeyError:
					data[header] = [value]
	
	# extract the variables you want
	l1i_size_set = [float(i) for i in data['l1i_size']]
	l1d_size_set = [float(i) for i in data['l1d_size']]
	l1_assoc_set = [float(i) for i in data['l1_assoc']]
	l2_size_set  = [float(i) for i in data['l2_size']]
	l2_assoc_set = [float(i) for i in data['l2_assoc']]
	line_size_set= [float(i) for i in data['line_size']]
	total_cost_set=[float(i) for i in data['total_cost']]
	cpi_set 	 = [float(i) for i in data['cpi']]
	cpi_vs_cost_set = [float(i) for i in data['CPIvsCOST_weighted']]
	l1d_l1i_sum_set = [x + y for x, y in zip(l1d_size_set, l1i_size_set)]
	l1d_l1i_sum_set_uniq = list(set(l1d_l1i_sum_set))
	line_size_uniq = list(set(line_size_set))
	l1i_size_uniq = list(set(l1i_size_set))
	l1d_size_uniq = list(set(l1d_size_set))
	l1_assoc_uniq = list(set(l1_assoc_set))
	l2_assoc_uniq = list(set(l2_assoc_set))
	l2_size_uniq = list(set(l2_size_set))
	full_list = zip(l1i_size_set, l1d_size_set, l1d_l1i_sum_set, l1_assoc_set, l2_size_set, l2_assoc_set, line_size_set, total_cost_set, cpi_set, cpi_vs_cost_set)

####################  		l2 		################################
	for linesize_var in line_size_uniq:
		for l1isize_var in l1i_size_uniq:
			for l1dsize_var in l1d_size_uniq:
				for l1assoc_var in l1_assoc_uniq: 
					for l2assoc_var in l2_assoc_uniq:
						index_set = []
						sorted_index = []
						needed_list = []
						needed_l2 = []
						needed_cpi = []
						needed_cost = []
						needed_wc = []
						for index in range(len(line_size_set)):
							if ( (linesize_var == line_size_set[index]) & (l1dsize_var == l1d_size_set[index]) & (l1isize_var == l1i_size_set[index]) & (l1assoc_var == l1_assoc_set[index]) & (l2assoc_var == l2_assoc_set[index]) ):
								index_set.append(index)
								needed_list.append((index,full_list[index]))
						if len(index_set)>=3:
						  	print needed_list
							needed_list = sorted(needed_list, key=lambda x:x[1][4])
							sorted_index = [item[0] for item in needed_list]
							for index in sorted_index:
								needed_l2.append(l2_size_set[index])
								needed_cpi.append(cpi_set[index])
								needed_cost.append(total_cost_set[index])
								needed_wc.append(cpi_vs_cost_set[index])
							print 'l1i=',l1isize_var,'l1d=',l1dsize_var,'l1a=',l1assoc_var,'linesize=',linesize_var,'l2assoc=',l2assoc_var,'\n','indexes=',index_set,sorted_index
							print needed_list
							print needed_l2
							print needed_cpi
							print needed_cost
							
							host = host_subplot(111, axes_class=AA.Axes)
							plt.subplots_adjust(right=0.75)
							
							par1 = host.twinx()
							par2 = host.twinx()
							
							offset = 60
							new_fixed_axis = par2.get_grid_helper().new_fixed_axis
							par2.axis["right"] = new_fixed_axis(loc="right",
							                                    axes=par2,
							                                    offset=(offset, 0))
							
							par2.axis["right"].toggle(all=True)
							
							host.set_xlabel('l2 size with l1i='+str(int(l1isize_var))+'kB_'+'l1d='+str(int(l1dsize_var))+'kB_l2='+str(int(l2assoc_var))+'way_line='+str(int(linesize_var))+'B')
							host.set_ylabel("CPI")
							par1.set_ylabel("COST")
							par2.set_ylabel("Weighted_COST")
							
							p1, = host.plot(needed_l2, needed_cpi, '*-', label="CPI")
							p2, = par1.plot(needed_l2, needed_cost, '+-',label="COST")
							p3, = par2.plot(needed_l2, needed_wc, '.-',label="Weighted_COST")
							
							par1.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							par2.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							
							#host.legend(loc='upper left')
							
							host.axis["left"].label.set_color(p1.get_color())
							par1.axis["right"].label.set_color(p2.get_color())
							par2.axis["right"].label.set_color(p3.get_color())
							plt.savefig(plot_dir+testname+"_L2size_with_l1i="+str(int(l1isize_var))+"kB_l1d="+str(int(l1dsize_var))+"kB_"+str(int(l1assoc_var))+"way_l2="+str(int(l2assoc_var))+"way_line="+str(int(linesize_var))+"B"+".png")
							plt.close('all')

########################################################################
########################################################################

def plot_graphs_l2a(filename,testname):
	# open the file in universal line ending mode 
	plot_dir = './plots/'+testname+'/l2a/'
	with open(filename, 'rU') as infile:
	# read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					data[header].append(value)
				except KeyError:
					data[header] = [value]
	
	# extract the variables you want
	l1i_size_set = [float(i) for i in data['l1i_size']]
	l1d_size_set = [float(i) for i in data['l1d_size']]
	l1_assoc_set = [float(i) for i in data['l1_assoc']]
	l2_size_set  = [float(i) for i in data['l2_size']]
	l2_assoc_set = [float(i) for i in data['l2_assoc']]
	line_size_set= [float(i) for i in data['line_size']]
	total_cost_set=[float(i) for i in data['total_cost']]
	cpi_set 	 = [float(i) for i in data['cpi']]
	cpi_vs_cost_set = [float(i) for i in data['CPIvsCOST_weighted']]
	l1d_l1i_sum_set = [x + y for x, y in zip(l1d_size_set, l1i_size_set)]
	l1d_l1i_sum_set_uniq = list(set(l1d_l1i_sum_set))
	line_size_uniq = list(set(line_size_set))
	l1i_size_uniq = list(set(l1i_size_set))
	l1d_size_uniq = list(set(l1d_size_set))
	l1_assoc_uniq = list(set(l1_assoc_set))
	l2_assoc_uniq = list(set(l2_assoc_set))
	l2_size_uniq = list(set(l2_size_set))
	full_list = zip(l1i_size_set, l1d_size_set, l1d_l1i_sum_set, l1_assoc_set, l2_size_set, l2_assoc_set, line_size_set, total_cost_set, cpi_set, cpi_vs_cost_set)

####################  		l2 assoc		################################
	for linesize_var in line_size_uniq:
		for l1isize_var in l1i_size_uniq:
			for l1dsize_var in l1d_size_uniq:
				for l1assoc_var in l1_assoc_uniq: 
					for l2size_var in l2_size_uniq:
						index_set = []
						sorted_index = []
						needed_list = []
						needed_l2a = []
						needed_cpi = []
						needed_cost = []
						needed_wc = []
						for index in range(len(line_size_set)):
							if ( (linesize_var == line_size_set[index]) & (l1dsize_var == l1d_size_set[index]) & (l1isize_var == l1i_size_set[index]) & (l1assoc_var == l1_assoc_set[index]) & (l2size_var == l2_size_set[index]) ):
								index_set.append(index)
								needed_list.append((index,full_list[index]))
						if len(index_set)>=3:
						  	print needed_list
							needed_list = sorted(needed_list, key=lambda x:x[1][5])
							sorted_index = [item[0] for item in needed_list]
							for index in sorted_index:
								needed_l2a.append(l2_assoc_set[index])
								needed_cpi.append(cpi_set[index])
								needed_cost.append(total_cost_set[index])
								needed_wc.append(cpi_vs_cost_set[index])
							print 'l1i=',l1isize_var,'l1d=',l1dsize_var,'l1a=',l1assoc_var,'linesize=',linesize_var,'l2size=',l2size_var,'\n','indexes=',index_set,sorted_index
							print needed_list
							print needed_l2a
							print needed_cpi
							print needed_cost
							
							host = host_subplot(111, axes_class=AA.Axes)
							plt.subplots_adjust(right=0.75)
							
							par1 = host.twinx()
							par2 = host.twinx()
							
							offset = 60
							new_fixed_axis = par2.get_grid_helper().new_fixed_axis
							par2.axis["right"] = new_fixed_axis(loc="right",
							                                    axes=par2,
							                                    offset=(offset, 0))
							
							par2.axis["right"].toggle(all=True)
							
							host.set_xlabel('l2a with l1i='+str(int(l1isize_var))+'kB_'+'l1d='+str(int(l1dsize_var))+'kB_'+str(int(l1assoc_var))+'way_l2='+str(int(l2size_var))+'kB_line='+str(int(linesize_var))+'B')
							host.set_ylabel("CPI")
							par1.set_ylabel("COST")
							par2.set_ylabel("Weighted_COST")
							
							p1, = host.plot(needed_l2a, needed_cpi, '*-', label="CPI")
							p2, = par1.plot(needed_l2a, needed_cost, '+-',label="COST")
							p3, = par2.plot(needed_l2a, needed_wc, '.-',label="Weighted_COST")
							
							par1.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							par2.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							
							#host.legend(loc='upper left')
							
							host.axis["left"].label.set_color(p1.get_color())
							par1.axis["right"].label.set_color(p2.get_color())
							par2.axis["right"].label.set_color(p3.get_color())
							plt.savefig(plot_dir+testname+"_L2a_with_l1i="+str(int(l1isize_var))+"kB_l1d="+str(int(l1dsize_var))+"kB_"+str(int(l1assoc_var))+"way_l2"+str(int(l2size_var))+"kB_line="+str(int(linesize_var))+"B"+".png")
							plt.close('all')

########################################################################


########################################################################

def plot_graphs_line(filename,testname):
	# open the file in universal line ending mode 
	plot_dir = './plots/'+testname+'/linesize/'
	with open(filename, 'rU') as infile:
	# read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					data[header].append(value)
				except KeyError:
					data[header] = [value]
	
	# extract the variables you want
	l1i_size_set = [float(i) for i in data['l1i_size']]
	l1d_size_set = [float(i) for i in data['l1d_size']]
	l1_assoc_set = [float(i) for i in data['l1_assoc']]
	l2_size_set  = [float(i) for i in data['l2_size']]
	l2_assoc_set = [float(i) for i in data['l2_assoc']]
	line_size_set= [float(i) for i in data['line_size']]
	total_cost_set=[float(i) for i in data['total_cost']]
	cpi_set 	 = [float(i) for i in data['cpi']]
	cpi_vs_cost_set = [float(i) for i in data['CPIvsCOST_weighted']]
	l1d_l1i_sum_set = [x + y for x, y in zip(l1d_size_set, l1i_size_set)]
	l1d_l1i_sum_set_uniq = list(set(l1d_l1i_sum_set))
	line_size_uniq = list(set(line_size_set))
	l1i_size_uniq = list(set(l1i_size_set))
	l1d_size_uniq = list(set(l1d_size_set))
	l1_assoc_uniq = list(set(l1_assoc_set))
	l2_assoc_uniq = list(set(l2_assoc_set))
	l2_size_uniq = list(set(l2_size_set))
	full_list = zip(l1i_size_set, l1d_size_set, l1d_l1i_sum_set, l1_assoc_set, l2_size_set, l2_assoc_set, line_size_set, total_cost_set, cpi_set, cpi_vs_cost_set)

####################  		line size		################################
	for l2assoc_var in l2_assoc_uniq:
		for l1isize_var in l1i_size_uniq:
			for l1dsize_var in l1d_size_uniq:
				for l1assoc_var in l1_assoc_uniq: 
					for l2size_var in l2_size_uniq:
						index_set = []
						sorted_index = []
						needed_list = []
						needed_line = []
						needed_cpi = []
						needed_cost = []
						needed_wc = []
						for index in range(len(line_size_set)):
							if ( (l2assoc_var == l2_assoc_set[index]) & (l1dsize_var == l1d_size_set[index]) & (l1isize_var == l1i_size_set[index]) & (l1assoc_var == l1_assoc_set[index]) & (l2size_var == l2_size_set[index]) ):
								index_set.append(index)
								needed_list.append((index,full_list[index]))
						if len(index_set)>=3:
						  	print needed_list
							needed_list = sorted(needed_list, key=lambda x:x[1][6])
							sorted_index = [item[0] for item in needed_list]
							for index in sorted_index:
								needed_line.append(line_size_set[index])
								needed_cpi.append(cpi_set[index])
								needed_cost.append(total_cost_set[index])
								needed_wc.append(cpi_vs_cost_set[index])
							print 'l1i=',l1isize_var,'l1d=',l1dsize_var,'l1a=',l1assoc_var,'l2size=',l2size_var,'l2assoc=',l2assoc_var,'\n','indexes=',index_set,sorted_index
							print needed_list
							print needed_line
							print needed_cpi
							print needed_cost
							
							host = host_subplot(111, axes_class=AA.Axes)
							plt.subplots_adjust(right=0.75)
							
							par1 = host.twinx()
							par2 = host.twinx()
							
							offset = 60
							new_fixed_axis = par2.get_grid_helper().new_fixed_axis
							par2.axis["right"] = new_fixed_axis(loc="right",
							                                    axes=par2,
							                                    offset=(offset, 0))
							
							par2.axis["right"].toggle(all=True)
							
							host.set_xlabel('line size with l1i='+str(int(l1isize_var))+'kB_'+'l1d='+str(int(l1dsize_var))+'kB_'+str(int(l1assoc_var))+'way_l2='+str(int(l2size_var))+'kB_'+str(int(l2assoc_var))+'way')
							host.set_ylabel("CPI")
							par1.set_ylabel("COST")
							par2.set_ylabel("Weighted_COST")
							
							p1, = host.plot(needed_line, needed_cpi, '*-', label="CPI")
							p2, = par1.plot(needed_line, needed_cost, '+-',label="COST")
							p3, = par2.plot(needed_line, needed_wc, '.-',label="Weighted_COST")
							
							par1.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							par2.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
							
							#host.legend(loc='upper left')
							
							host.axis["left"].label.set_color(p1.get_color())
							par1.axis["right"].label.set_color(p2.get_color())
							par2.axis["right"].label.set_color(p3.get_color())
							plt.savefig(plot_dir+testname+"_Linesize_with_l1i="+str(int(l1isize_var))+"kB_l1d="+str(int(l1dsize_var))+"kB_"+str(int(l1assoc_var))+"way_l2"+str(int(l2size_var))+"kB_"+str(int(l2assoc_var))+"way"+".png")
							plt.close('all')

########################################################################

#########################################################################################

for filename in glob.glob("./bench*.csv"):
	(f_path, f_name) = os.path.split(filename)
	(f_short_name, f_extension) = os.path.splitext(f_name)
	f_short_name = f_short_name.replace("bench_","",1)
	print f_short_name
	print filename
	if not os.path.exists("./plots/"+f_short_name):
		os.makedirs("./plots/"+f_short_name)
	if not os.path.exists("./plots/"+f_short_name+"/l1i"):
		os.makedirs("./plots/"+f_short_name+"/l1i")
	if not os.path.exists("./plots/"+f_short_name+"/l1d"):
		os.makedirs("./plots/"+f_short_name+"/l1d")
	if not os.path.exists("./plots/"+f_short_name+"/l1"):
		os.makedirs("./plots/"+f_short_name+"/l1")
	if not os.path.exists("./plots/"+f_short_name+"/l1a"):
		os.makedirs("./plots/"+f_short_name+"/l1a")
	if not os.path.exists("./plots/"+f_short_name+"/l2"):
		os.makedirs("./plots/"+f_short_name+"/l2")
	if not os.path.exists("./plots/"+f_short_name+"/l2a"):
		os.makedirs("./plots/"+f_short_name+"/l2a")
	if not os.path.exists("./plots/"+f_short_name+"/linesize"):
		os.makedirs("./plots/"+f_short_name+"/linesize")
	plot_graphs_l1i(filename,f_short_name)
	plot_graphs_l1d(filename,f_short_name)
	plot_graphs_l1(filename,f_short_name)
	plot_graphs_l1a(filename,f_short_name)
	plot_graphs_l2(filename,f_short_name)
	plot_graphs_l2a(filename,f_short_name)
	plot_graphs_line(filename,f_short_name)


