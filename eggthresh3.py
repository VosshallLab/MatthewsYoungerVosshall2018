### script should take a directory name as input, and then run the thresholding function on all .png files in that directory that don't start with THRESH
### Uses cv2 for image processing, numpy for thresholding in cv2, all other libraries are standard.
import cv2
import os
import csv
import numpy as np
import sys
### run_directory() is a function that requires a directory and two sets of thresholding values: EGG_MIN and EGG_MAX
### these thresholds are in terms of hue, saturation, and value

### plate_pref takes the csv file output of run_directory as input, ordering does not matter, file naming does (uses formating from the bash script)
### uses csv file to create prefernce indices based on the platelayout, saves the file names, pixel counts, and preference to a csv file

### main is a function that can more easily be called from bash with inputs
### it does not requre input but takes system arguments sent to it similar to commands in bash, allowing for as many or as few arguments as each function needs
print("Argument 0 is " + sys.argv[0])
print("Argument 1 is " + sys.argv[1])
print("Argument 2 is " + sys.argv[2])
def main():
	print("starting main") #Print for diagnostics
	method = sys.argv[1]
	if method == "run_directory":
		print("Starting run_directory")
		path = sys.argv[2]
		EGG_MIN = np.array([0, 0, 0],np.uint8)
		EGG_MAX = np.array([173, 46, 201],np.uint8)
		run_directory(path,EGG_MIN,EGG_MAX)
	if method == "plate_pref":
		print("Starting plate_pref")
		csvfile = sys.argv[2]
		plate_pref(csvfile)
	if method == "full_analysis":
		path = sys.argv[2]
		EGG_MIN = np.array([0, 0, 0],np.uint8)
		EGG_MAX = np.array([173, 46, 201],np.uint8)
		run_directory(path,EGG_MIN,EGG_MAX)
		csvfilename = (os.path.basename(os.path.normpath(path)) + '.csv') #csv file to save to
		csvfile = (path + '/' + csvfilename) #full path of csv file
		#plate_pref(csvfile)

def run_directory(path, EGG_MIN, EGG_MAX):
	pixel_count = [['filename','egg_pixels']] #File Header
	filelist = os.listdir(path) #get all the files in the directory
	png_files = [] #create empty list of png files
	#error_file=open('Error.txt','w')
	print("Path is " + path)
	#error_file.close()

	for item in filelist:
		#error_file=open('Error.txt','w')
		#print(item)
		#error_file.close()
		if item.endswith(".png") and not os.path.isfile(path + '/' + 'THRESH' + item): #if the file is a png and doesn't have a threshold png already
			png_files.append(item) #add it to png list
	for input_file in png_files: #for all the files in that list create a thresholded version and count the pixels
		#print(path + '/' + input_file)
		current_working = cv2.imread(path + '/' + input_file)
		hsv = cv2.cvtColor(current_working, cv2.COLOR_BGR2HSV) 
		frame_threshed = cv2.inRange(hsv, EGG_MIN, EGG_MAX)
		cv2.imwrite(path + '/' + 'THRESH_' + input_file, frame_threshed)
		pixel_count.append([input_file,cv2.countNonZero(frame_threshed)])
	csvfilename = (os.path.basename(os.path.normpath(path)) + '.csv') #csv file to save to
	writename = (path + '/' + csvfilename) #full path of csv file
	with open(writename, 'wb') as csvwrite: #open the csv
		writer = csv.writer(csvwrite, delimiter=',') #create an object to write to
		for row in pixel_count:
			writer.writerow(row) #write each row in pixel_count to a csv
		csvwrite.close #close the csv
	#error_file.close()

def plate_pref(csvfile):
	#Create an array of control and test ()
	plate_layout = [['a1','a2'],['a3','a4'],['b2','b1'],['b4','b3'],['c1','c2'],['c3','c4'],['d2','d1'],['d4','d3'],['e1','e2'],['e3','e4'],['f2','f1'],['f4','f3'],['g1','g2'],['g3','g4']]
	pixel_dict = {}
	preference_csv = []
	writename = (csvfile[0:len(csvfile)-4] + '_Preference.csv')
	pixel_array=[]
	try: #Try to open the processlist
		with open(csvfile, 'rU') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',')
			pixel_array = [row for row in csvreader]
	except: #if it can't, throw an error
		sys.exit(1)

	for row in pixel_array:
		if row[1] != 'egg_pixels':
			pixel_dict[row[0][len(row[0])-6:len(row[0])-4]] = [row[1],row[0]]
	for plate_set in plate_layout:
		apix=(float(pixel_dict[plate_set[0]][0]))
		bpix=(float(pixel_dict[plate_set[1]][0]))
		if apix+bpix == 0:
			preference=0
		else:
			preference = float((apix-bpix)/(apix+bpix))
		a = pixel_dict[plate_set[0]]
		b = pixel_dict[plate_set[1]]
		preference_csv.append([a[1],a[0],b[1],b[0],preference])
	with open(writename, 'wb') as csvwrite:
		writer = csv.writer(csvwrite, delimiter=',')
		for row in preference_csv:
			writer.writerow(row)
		csvwrite.close  

# for test_dir in INPUT_DIRECTORY:
#    os.chdir(test_dir)
#    png_files = [f for f in os.listdir(test_dir) if (f.endswith('.png') and not f.startswith('THRESH'))]
#    print('working on directory ' + test_dir + ":\n")
#    run_directory(png_files, EGG_MIN, EGG_MAX)
main()
