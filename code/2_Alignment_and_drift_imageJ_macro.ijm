/* 
This script select the correct files for alignment according to user input ( All zeros, X displacement, Y displacement or ALL)  
It assumes that each direction (x, -x, y, -y) has 2 repeats, and that only the relevant files are in the input folder.
i.e. user needs to place all the incorrect files (non filtered out by the previous macro) in a different folder or subfolder for it to work
it then uses the the "Linear Stack Alignment with SIFT" plugin to align tiles.
Exports translation values as a .csv file for each subset of data, and a tile image showing the displacement


 */
 
// set batch mode on to remove unecessary visualisation of data and improve processing speed
setBatchMode(true); 

// choose input directory, and create output directory
	inputDirectory= getDirectory("Location of the flat .tiff files");
	print(inputDirectory);
	outerDirectory = File.getParent(inputDirectory);
	
	outputDirectory = outerDirectory + File.separator + "Alignment";
	File.makeDirectory(outputDirectory);
	
// get list of files in the input directory
	fileList = getFileList(inputDirectory);
	//Array.print(fileList);
	
// Create empty arrays and index values correspondind to each possible user input
zero_index = 0;
Zero_file_list = newArray;

x_index = 0;
x_file_list = newArray;

x_minus_index = 0;
x_minus_file_list = newArray;

y_index = 0;
y_file_list = newArray;

y_minus_index = 0;
y_minus_file_list = newArray;

/* Create subset lists of files sorted by movement direction :  
	-All 0  all files where X==0, Y==0, Z==0
	- All X movement  all files where Y==0, Z==0, and X > 0 OR X < 0
		+ closest 0,0,0 per sequence (i.e. image number closest to the smallest image number in the list)
	- All Y movement  all files where X==0, Z==0, and Y > 0 OR Y < 0
		+ closest 0,0,0 per sequence (i.e. image number closest to the smallest image number in the list)
*/


// Sort file list numerically by image ID
fileList= sort_array_numerically(fileList);
	//Array.print(fileList);
	
	for (i = 0; i < fileList.length; i++) {
 			
		if(endsWith(fileList[i], ".tiff")) {
		
		fileName=replace(fileList[i], ".tiff", "");
		split_name = split(fileName, "_");
		image_id = split_name[0];
		
		x_loc = split(split_name[2], "y");
		y_loc = split(x_loc[1], "z");
		
		x = replace(x_loc[0], "x","");	
		y = y_loc[0];
		z = y_loc[1];
	
			if( (x == 0) & (y == 0) & (z == 0) ){

				Zero_file_list[zero_index] = fileList[i];	
				//print("Location is 0 for file " + Zero_file_list[zero_index] + " at index " + zero_index);
				zero_index = zero_index + 1;
			}
			
			if( (x > 0) & (y == 0) & (z == 0) ){
				x_file_list[x_index] = fileList[i];	
				//print("Location is X = " + x + " for file " + x_file_list[x_index]+ " at index "+ x_index);
				x_index = x_index + 1;
			}
			
			if( (x < 0) & (y == 0) & (z == 0) ){
				x_minus_file_list[x_minus_index] = fileList[i];	
				//print("Location is X = " + x + " for file " + x_minus_file_list[x_minus_index]+ " at index "+ x_minus_index);
				x_minus_index = x_minus_index + 1;
			}
			
			if( (x == 0) & (y > 0) & (z == 0) ){
				y_file_list[y_index] = fileList[i];	
				//print("Location is Y = " + y + " for file " + y_file_list[y_index], " at index "+ y_index);
				y_index = y_index + 1;
			}
			
			if( (x == 0) & (y < 0) & (z == 0) ){
				y_minus_file_list[y_minus_index] = fileList[i];	
				//print("Location is Y = " + y + " for file " + y_minus_file_list[y_minus_index]+ " at index "+ y_minus_index);
				y_minus_index = y_minus_index + 1;
			}			
	}
}	
	

/*  For each array : 
	1 - Split in 2 to separate duplicate sequences
	2 - add the corresponding 0 to the array
*/

print("\n All 0 files");
experiment1 = "Zero_only";
Array.print(Zero_file_list);

print("\n All positive X files");
//Array.print(x_file_list);
experiment2 = "X_positive_1";
x_file_list_1 = split_sequence(x_file_list, 1);
x_file_list_1 = attach_zero(x_file_list_1);
experiment3 = "X_positive_2";
x_file_list_2 = split_sequence(x_file_list, 2);
x_file_list_2 = attach_zero(x_file_list_2);
Array.print(x_file_list_1);
Array.print(x_file_list_2);

print("\n All negative X files");
//Array.print(x_minus_file_list);
experiment4 = "X_negative_1";
x_minus_file_list_1 = split_sequence(x_minus_file_list, 1);
x_minus_file_list_1 = attach_zero(x_minus_file_list_1);
experiment5 = "X_negative_2";
x_minus_file_list_2 = split_sequence(x_minus_file_list, 2);
x_minus_file_list_2 = attach_zero(x_minus_file_list_2);
Array.print(x_minus_file_list_1);
Array.print(x_minus_file_list_2);

print("\n All positive Y");
//Array.print(y_file_list);		
experiment6 = "Y_positive_1";
y_file_list_1 = split_sequence(y_file_list, 1);
y_file_list_1 = attach_zero(y_file_list_1);
experiment7 = "Y_positive_2";
y_file_list_2 = split_sequence(y_file_list, 2);
y_file_list_2 = attach_zero(y_file_list_2);
Array.print(y_file_list_1);
Array.print(y_file_list_2);

print("\n All negative Y");
//Array.print(y_minus_file_list);
experiment8 = "Y_negative_1";
y_minus_file_list_1 = split_sequence(y_minus_file_list, 1);
y_minus_file_list_1 = attach_zero(y_minus_file_list_1);
experiment9 = "Y_negative_2";
y_minus_file_list_2 = split_sequence(y_minus_file_list, 2);
y_minus_file_list_2 = attach_zero(y_minus_file_list_2);
Array.print(y_minus_file_list_1);
Array.print(y_minus_file_list_2);

//Let the user decide which dataset they want to analyze

analysis_array = newArray(); //create an array to store checkbox results
rows = 2;
columns = 2;
n=4;
labels = newArray("Zero only", "All X", "All Y", "All directions");
defaults = newArray(n);
Array.fill(defaults, "false");
Dialog.create("Which set of images should be used for alignment");
Dialog.addCheckboxGroup(rows,columns,labels, defaults);
Dialog.show();
  for (i=0; i<n; i++){
  	 result = Dialog.getCheckbox();
     print(labels[i]+": "+result);
     analysis_array[i]= result;
  }
  

//Set correct dataset to be used
	if(analysis_array[0]==1){
		align_and_save_table(Zero_file_list, experiment1);
			}
	if(analysis_array[1]==1){
		align_and_save_table(x_file_list_1, experiment2);
		align_and_save_table(x_file_list_2, experiment3);
		align_and_save_table(x_minus_file_list_1, experiment4);
		align_and_save_table(x_minus_file_list_2, experiment5);		
			}
	if(analysis_array[2]==1){
		align_and_save_table(y_file_list_1, experiment6);
		align_and_save_table(y_file_list_2, experiment7);
		align_and_save_table(y_minus_file_list_1, experiment8);
		align_and_save_table(y_minus_file_list_2, experiment9);
			}
	if(analysis_array[3]==1){
		align_and_save_table(Zero_file_list, experiment1);
		align_and_save_table(x_file_list_1, experiment2);
		align_and_save_table(x_file_list_2, experiment3);		
		align_and_save_table(x_minus_file_list_1, experiment4);		
		align_and_save_table(x_minus_file_list_2, experiment5);				
		align_and_save_table(y_file_list_1, experiment6);		
		align_and_save_table(y_file_list_2, experiment7);
		align_and_save_table(y_minus_file_list_1, experiment8);
		align_and_save_table(y_minus_file_list_2, experiment9);
			}
			
print("\\Clear"); 			
print("All files processed");

/*  Function performing alignment and retrieving values in a .csv table, as well as a summary image 
*/
function align_and_save_table(a, experiment){ // "a" is the input array
	
	// create table to store results
	Table.create("Images_translation");

	// open correct dataset
	for(i=0; i<a.length; i++){

		imageFile = inputDirectory + a[i];
		open(imageFile);
		filename= getTitle();
		fileName=replace(filename, ".tiff", "");
		split_name = split(fileName, "_");
		x_loc = split(split_name[2], "y");
		y_loc = split(x_loc[1], "z");
		
		x = replace(x_loc[0], "x","");	
		y = y_loc[0];
		z = y_loc[1];
		
		Table.set("File_id", i, a[i]);
		Table.set("x_theoretical", i, x);
		Table.set("y_theoretical", i, y);
	}
	
	//create stack of images, run alignment
	run("Images to Stack", "use");		
	print("\\Clear"); 
	run("Linear Stack Alignment with SIFT", "initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Translation interpolate show_transformation_matrix");
	close("Stack");
	//change colour settings for labels
	setForegroundColor(255, 255, 255);
	setBackgroundColor(0, 0, 0);
	//save stack
	outputName = outputDirectory + File.separator + experiment + "_aligned_stack.tiff";
	saveAs("tiff", outputName);
	//collect log information
	logString = getInfo("log");
	print("\\Clear"); 
	split_log = split(logString, "\n");
	transform_matrix = newArray;
	matrix_index=0;
	//Split log into array and select transformation matrixes only
	for(i=0; i<split_log.length; i++){
		if(startsWith(split_log[i], "Transformation") == true){	
				transform_matrix[matrix_index] = split_log[i];
				matrix_index++;
		}
	}
	
	//From transformation matrixes, extract X and Y translation
	for(i=0; i<transform_matrix.length; i++){
			print("Line " + i + " is : " + transform_matrix[i]);
			split_matrix = split(transform_matrix[i], "[[");
			x_values = split(split_matrix[1], ",");
			x_translation = replace(x_values[2], "]", "");
			y_values = split(split_matrix[2], ",");
			y_translation = replace(y_values[2], "]", "");
			print(x_translation);
			print(y_translation);
		// add values to table
		Table.set("x_recorded", i+1, x_translation);
		Table.set("y_recorded", i+1, y_translation);
		//create label on each slice of the stack
}

for(i=0; i<a.length; i++){	
slice_number = i+1;	
x_translation = Table.get("x_recorded", i);
y_translation = Table.get("y_recorded", i);
Label_translation = a[i] + "\ntX_" + x_translation + "\ntY_" + y_translation;
print(Label_translation);
run("Label...", "format=Text starting=0 interval=1 x=5 y=10 font=18 text=" + Label_translation + " range=" + slice_number +"-"+ slice_number+"");	
}

//save stack
run("blue_orange_icb");
outputName = outputDirectory + File.separator + experiment + "_aligned_stack_annotation.tiff";
saveAs("tiff", outputName);

montage_row_nbr = -Math.floor(-(a.length/3));
run("Make Montage...", "columns=3 rows="+montage_row_nbr+" scale=1");
outputName = outputDirectory + File.separator + experiment + "_aligned_montage.png";
saveAs("PNG", outputName);

selectWindow("Images_translation");
outputName = outputDirectory + File.separator + experiment + "_translation.csv";
saveAs("Results", outputName);
close(experiment + "_translation.csv");
run("Close All");
}



// Function used to reorder arrays numerically by image ID

function sort_array_numerically(a) { // "a" is the input array
	arr2 = newArray; //return array containing digits
	for (i = 0; i < a.length; i++) {
		str = a[i];
		digits = "";
		str=replace(str, ".tiff", "");
		split_name = split(str, "_");
		//Array.print(split_name);
		image_id = split_name[0];
		//print(image_id);
		
		if(!isNaN(parseInt(image_id)))
		digits += image_id;

		arr2[i] = parseInt(digits);
	}
	//Array.print(arr2);
	Array.sort(arr2, a);
	return a;
}

// Function used to split each array into 2 since the same movement were recorded twice

function split_sequence(a, seq) { // "a" is the input array, "seq" is the sequence number (should be 1 or 2)
	repeat_nbr = 2;
	slice_index = (a.length/repeat_nbr);
	if(seq == 1){
		split_a = Array.slice(a,0,slice_index);
		return split_a;
		}
	else(seq == 2){
		split_a = Array.slice(a,slice_index,a.length);
		return split_a;
		}

	}

// Function used to attach the corresponding 0 file to each sequence
function attach_zero(a) { 
	arr2 = newArray; //return array containing image id
	arr_diff = newArray; //return array containing difference in id number
	//find smallest id in input array
	str = a[0];
	str=replace(str, ".tiff", "");
	split_name = split(str, "_");
	smallest_id = parseInt(split_name[0]);		

	// in zero file list, find closest matching id to smallest id
	for (i = 0; i < Zero_file_list.length; i++) {
		str = Zero_file_list[i];
		digits = "";
		str=replace(str, ".tiff", "");
		split_name = split(str, "_");
		image_id = split_name[0];
		arr2[i] = parseInt(image_id);
		
		arr_diff[i] = Math.abs(smallest_id - arr2[i]);
		}	
	//Array.print(arr_diff);
	min_diff = Array.findMinima(arr_diff, 0);
	min_diff_index = min_diff[0];
	a = Array.concat(Zero_file_list[min_diff_index], a);
	return a;
}







