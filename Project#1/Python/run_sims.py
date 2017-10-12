import subprocess
import math

gem5_dir   = '/usr/local/gem5/'
gem5_exec  = gem5_dir + 'build/X86/gem5.opt' 
gem5_se    = gem5_dir + 'configs/example/se.py' 
bench_dir  = '/home/011/k/kx/kxm162730/comp_arch/Prj1/Project1_SPEC/'

test_name  = ['401.bzip2','429.mcf','456.hmmer','458.sjeng','470.lbm','scimark']
test_true_name  = ['bzip2','mcf','hmmer','sjeng','lbm','scimark'] 
test=[]
for test_var in test_name:
	test.append(bench_dir + test_var + '/src/benchmark')
test_arg=[]
test_arg.append(bench_dir + str(test_name[0]) + '/data/input.program 10')
test_arg.append(bench_dir + str(test_name[1]) +'/data/inp.in')
test_arg.append('--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 '+ bench_dir + str(test_name[2]) + '/data/bombesin.hmm')
test_arg.append(bench_dir + str(test_name[3])+'/data/test.txt') 
test_arg.append('20 ' + bench_dir +str(test_name[4]) +'/data/reference.dat 0 1 ' + bench_dir +str(test_name[4]) + '/data/100_100_130_cf_a.of')
test_arg.append('')
test_dir=[]

for test_var in test_name:
	test_dir.append( bench_dir + test_var+'/')
output_dir=[]
for out_var in test_dir:
	output_dir.append(out_var+'m5out')	

cpu_type   = 'timing'	
l1size    = [1,2,4,8,32,128]
l1assoc   = [1,2,4,8]
l2size     = [1,2,4,8,16,128,512,1024]
l2assoc    = [1,2,4,8]
linesize   = [16,32,64,128]
inst_cnt   = '500000000'

l1dsize_set 	=[]
l1isize_set 	=[]
l1assoc_set 	=[]
l2size_set 		=[]
l2assoc_set 	=[]
linesize_set 	=[]

def powTwoBit(number):
	return (number & (number-1) == 0) and (number != 0)

for linesize_var in linesize:
	for l1isize_var in l1size:
		for l1dsize_var in l1size:
			for l1assoc_var in l1assoc:
				for l2size_var in l2size: 
					for l2assoc_var in l2assoc:
						if( (l2size_var >= l1isize_var) & (l2size_var >= l1dsize_var) & (l2size_var >= (l1isize_var+l1dsize_var)) ):
							l1i_num_lines = int(l1isize_var*1024)/int(linesize_var)
							l1d_num_lines = int(l1dsize_var*1024)/int(linesize_var)
							l2_num_lines  = int(l2size_var*1024)/int(linesize_var)
							l1i_num_sets = int(l1i_num_lines)/int(l1assoc_var)
							l1d_num_sets = int(l1d_num_lines)/int(l1assoc_var)
							l2_num_sets  = int(l2_num_lines)/int(l2assoc_var)
							if ( (l1i_num_lines >= l1assoc_var) & (l1d_num_lines >= l1assoc_var) & (l2_num_lines >= l2assoc_var) ):
								if(  powTwoBit((int(l1isize_var)*1024)/(int(linesize_var)*int(l1assoc_var))) ):
									if(  powTwoBit((int(l1dsize_var)*1024)/(int(linesize_var)*int(l1assoc_var)))  ):
										if(  powTwoBit((int(l2size_var)*1024)/(int(linesize_var)*int(l2assoc_var))) ):
											if( ( l1isize_var + l1dsize_var ) <= 256 ):
												l2size_set.append(l2size_var)
												l2assoc_set.append(l2assoc_var)
												l1dsize_set.append(l1dsize_var)	
												l1isize_set.append(l1isize_var)
												l1assoc_set.append(l1assoc_var)
												linesize_set.append(linesize_var)


print len(l1dsize_set)
for index in range(len(test_name)):
	for number in range(len(l1dsize_set)):
		final_out_dir = str(output_dir[index])+'/'+str(test_true_name[index])+'_'+str(l1isize_set[number])+'kBiCache'+'_'+str(l1dsize_set[number])+'kBdCache'+'_'+str(l1assoc_set[number])+'way'+'_'+str(l2size_set[number])+'kBL2'+'_'+str(l2assoc_set[number])+'way'+'_'+str(linesize_set[number])+'cache'
		subprocess.call([gem5_exec,'-d',final_out_dir,gem5_se,'-c',str(test[index]),'-o',str(test_arg[index]),'-I',inst_cnt,'--cpu-type='+cpu_type,'--caches','--l2cache','--l1d_size='+str(l1dsize_set[number])+'kB','--l1i_size='+str(l1isize_set[number])+'kB','--l2_size='+str(l2size_set[number])+'kB','--l1d_assoc='+str(l1assoc_set[number]),'--l1i_assoc='+str(l1assoc_set[number]),'--l2_assoc='+str(l2assoc_set[number]),'--cacheline_size='+str(linesize_set[number])])

