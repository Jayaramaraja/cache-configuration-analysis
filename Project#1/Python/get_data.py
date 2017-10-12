import os
import sys
import re
import csv
import math
walk_dir = ['401.bzip2/m5out/','429.mcf/m5out/','456.hmmer/m5out/','458.sjeng/m5out/','470.lbm/m5out/','scimark/m5out/']
test_true_name  = ['bzip2','mcf','hmmer','sjeng','lbm','scimark'] 

l1i_cost_factor = 8.0
l1d_cost_factor = 8.0
l2_cost_factor  = l1i_cost_factor/8.0

l1i_miss_rate = '.*system.cpu.icache.overall_misses::total\s+(\S+)\s+' 
l1d_miss_rate = '.*system.cpu.dcache.overall_misses::total\s+(\S+)\s+' 
l2_miss_rate  = '.*system.l2.overall_misses::total\s+(\S+)\s+'
inst_cnt_re   = '.*sim_insts\s+(\S+)\s+'

for index in range(len(walk_dir)):
	line_match = '.*'+test_true_name[index]+'_(\d+)kBiCache_(\d+)kBdCache_(\d+)way_(\d+)kBL2_(\d+)way_(\d+)cache'
	resultFile = open("./results/bench_"+test_true_name[index]+".csv",'wb')
	wr = csv.writer(resultFile, dialect='excel')
	wr.writerow(["l1i_size", "l1d_size", "l1_assoc", "l2_size", "l2_assoc", "line_size", "$_cost", "misc_cost", "total_cost", "cpi", "CPIvsCOST_weighted"])
	for root, subdirs, files in os.walk(walk_dir[index]):
		print('--\nroot = ' + root)
		for filename in files:
			file_path = os.path.join(root, filename)
			if ( filename == 'stats.txt'):
				line_matched = re.match(line_match, root)
				l1isize = float(line_matched.groups()[0])
				l1dsize = float(line_matched.groups()[1])
				l1assoc = float(line_matched.groups()[2])
				l2size  = float(line_matched.groups()[3])
				l2assoc = float(line_matched.groups()[4])
				linesize= float(line_matched.groups()[5])
				print('\t- file %s (full path: %s)' % (filename, file_path))
				l1i_num_lines = (l1isize*1024)/linesize
				l1d_num_lines = (l1dsize*1024)/linesize
				l2_num_lines  = (l2size*1024)/linesize
				l1i_num_sets = l1i_num_lines/l1assoc
				l1d_num_sets = l1d_num_lines/l1assoc
				l2_num_sets  = l2_num_lines/l2assoc
				l1i_cost = (l1i_cost_factor*l1isize) + ((l1i_cost_factor/4)*l1assoc)
				l1d_cost = (l1d_cost_factor*l1dsize) + ((l1d_cost_factor/4)*l1assoc)
				l2_cost  = (l2_cost_factor*l2size) + ((l2_cost_factor/4)*l2assoc)
				l1i_misc = (l1i_cost_factor*((32+1-(math.log(linesize,2))-(math.log(l1i_num_sets,2)))*(1/(1024*8))*(l1i_num_lines) ) ) + ( ( (l1i_cost_factor/250) * l1i_num_sets) if l1assoc!=1 else 0 )
				l1d_misc = (l1d_cost_factor*((32+1-(math.log(linesize,2))-(math.log(l1d_num_sets,2)))*(1/(1024*8))*(l1d_num_lines))) + ( ( (l1d_cost_factor/250) * l1d_num_sets) if l1assoc!=1 else 0 ) 
				l2_misc  = (l2_cost_factor*((32+1-(math.log(linesize,2))-(math.log(l2_num_sets,2)))*(1/(1024*8))*(l2_num_lines))) + ( ( (l2_cost_factor/500) * l2_num_sets) if l2assoc!=1 else 0 )
				misc_cost = l1i_misc + l1d_misc + l2_misc
				cache_cost = l1i_cost + l1d_cost + l2_cost
				total_cost = cache_cost + misc_cost
				with open(file_path) as f:
					for line in f:
						l1i_miss_match = re.match(l1i_miss_rate, line)
						l1d_miss_match = re.match(l1d_miss_rate, line)
						l2_miss_match  = re.match(l2_miss_rate, line)
						inst_cnt_match = re.match(inst_cnt_re, line)
						if inst_cnt_match:
							inst_cnt = float(inst_cnt_match.groups()[0])
						if l1d_miss_match:
							l1d_miss_value = float(l1d_miss_match.groups()[0])
							print 'l1i_size = ',l1isize
							print 'l1d_size = ',l1dsize
							print 'l1_assoc = ',l1assoc
							print 'l2_size  = ',l2size
							print 'l2_assoc = ',l2assoc
							print 'linesize = ',linesize
							print 'inst_cnt = ',inst_cnt
							print 'l1d_miss =',l1d_miss_value
						if l1i_miss_match:
							l1i_miss_value = float(l1i_miss_match.groups()[0])
							print 'l1i_miss =',l1i_miss_value
						if l2_miss_match:
							l2_miss_value = float(l2_miss_match.groups()[0])
							print 'l2_miss =',l2_miss_value
							cpi = 1 + ((((l1i_miss_value+l1d_miss_value)*4)+(l2_miss_value*80))/float(inst_cnt))
							cpi_vs_cost = (cpi*0.8) + (cache_cost*0.2) 
							print 'cache_cost =',cache_cost
							print 'misc_cost  =',misc_cost
							print 'Total_cost =',total_cost
							print 'CPI =',cpi
							print 'CPI Vs COST weighted =',cpi_vs_cost,'\n\n'
							wr.writerow([l1isize,l1dsize,l1assoc,l2size,l2assoc,linesize,cache_cost,misc_cost,total_cost,cpi,cpi_vs_cost])


