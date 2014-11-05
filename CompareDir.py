import os
import hashlib
import fnmatch
import itertools


def hash_lines(file_path):
	'''
	Don't worry, file will be close properly as http://legacy.python.org/dev/peps/pep-0343/
	'''
	with open(file_path, "rt") as op: 
		return [ hashlib.sha224(line).hexdigest() for line in op ]


def save_hashcodes(file_path, combined_str):
	#print "Save to %s" % file_path
	with open(file_path, "wt") as ip:
		ip.write(combined_str)

def convert_file(file_path):
	#print "Convert %s" % file_path
	
	hash_list = hash_lines(file_path)
	
	hash_list.sort()
	save_file_path = "%s.hash" % file_path
	combined_str = "\n".join(hash_list)
	#save_hashcodes(save_file_path, combined_str)

	return hashlib.sha224(combined_str).hexdigest()


def convert_files(base_dir):

	file_pattern = "*.csv"
	hash_list = [ (file , convert_file(file)) for file in matching_file_interator(base_dir, file_pattern)]
	#hash_list.sort()

	return dict(hash_list)
 
def compare_bas_reg(base):
	'''
	Input: a dir that compare two directories that contain files with same file names.
	Output: Print With same file name, file contents sorted by line are not hashcode same.
	'''

	for diff in compare_bas_reg_dirs(base):
		print diff
		print "\n"
 
 
def compare_bas_reg_dirs(base):

	#matching bas/reg dirs
	bas_dirs = [bas_dir for bas_dir in matching_dir_interator(base,"*_bas")]
	reg_dirs = [reg_dir for reg_dir in matching_dir_interator(base,"*_reg")]
	# As a bas with a reg, there are bas/reg pairs
	assert(len(bas_dirs) == len(reg_dirs))

	bas_dirs.sort()
	reg_dirs.sort()
#Comparing each bas/reg pair
	for (bas_dir, reg_dir) in zip(bas_dirs, reg_dirs):
		for diff in compare_bas_reg_dir(bas_dir, reg_dir):
			yield diff
 
def compare_bas_reg_dir(bas_dir, reg_dir):
#comparing files in directory
	bas_dict = convert_files(bas_dir)
	reg_dict = convert_files(reg_dir)
	bkeys = bas_dict.keys()
	bkeys.sort()
	rkeys = reg_dict.keys()
	rkeys.sort()
	for (bk ,rk) in zip(bkeys, rkeys):
		if not bas_dict[bk] == reg_dict[rk]:
			yield (bk, bas_dict[bk], rk, reg_dict[rk])
 
def matching_file_interator(base_dir,file_pattern):
	#find matching files in given directory
	for path, dirlist, filelist in os.walk(base_dir):
		for file in fnmatch.filter(filelist,file_pattern):
			yield os.path.join(path,file)

def matching_dir_interator(base_dir,dir_pattern):
	#find matching sub-directories in given directory
	for path, dirlist, filelist in os.walk(base_dir):
		for dir in fnmatch.filter(dirlist,dir_pattern):
			yield os.path.join(path, dir)
 
if __name__ == '__main__':
	
	base =  "./reports"
	compare_bas_reg(base)
