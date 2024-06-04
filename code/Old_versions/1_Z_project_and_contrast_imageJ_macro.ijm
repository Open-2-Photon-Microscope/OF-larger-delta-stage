/* Simple macro used to average the slices in the original .tiff files and tweek intensity and contrast
to improve image quality. It also sets pixel size.
Takes as input the raw .tiff stacks, 
Outputs the flattened image as a .tiff in a subfolder in the same directory as the input files*/

// set batch mode on to remove unecessary visualisation of data and improve processing speed
setBatchMode(true); 

// choose input directory, and create output directory
	inputDirectory= getDirectory("Location of the raw .tiff files");
	print(inputDirectory);
	
	outputDirectory = inputDirectory + File.separator + "Z_proj";
	File.makeDirectory(outputDirectory);
	
// get list of files in the input directory
	fileList = getFileList(inputDirectory);
	//Array.print(fileList);
	
	  output_file_nbr = 0;
	  
// apply Z project function on .tiff files only
	for (i = 0; i < fileList.length; i++) {
  
		if(endsWith(fileList[i], ".tiff")) {

		        imageFile = inputDirectory + fileList[i];
		        print("Processing: ", imageFile);
		        z_project_contrast(imageFile);
		}
	}

//switch batch mode off
setBatchMode(false);

input_file_nbr = fileList.length;
showMessage("End of script", output_file_nbr + " .tiff files created from " + input_file_nbr + " input files");
 
 
// Z project function for each tiff image

function z_project_contrast(imageFile)
{

//open image and get file name
	open(imageFile);
	fileName=getTitle(); 
	fileName=replace(fileName, ".tiff", "");
	split_name = split(fileName, "_");
	//Array.print(split_name);
	image_id = split_name[1];
	//print(image_id);
	//run functions if the number of slices is correct (aborted images are often the expected number of slices, here 300)
		if(nSlices==300){
			 
		// 1 - create an average intensity projection, start at slice 2 because the 1st one often shows missing data
			run("Z Project...", "start=2 projection=[Average Intensity]");
		// 2 - enhance contrast, saturation value can be changed to fit needs, and add a normalisation
			run("Enhance Contrast", "saturated=0.35 normalize");
		// 3 - Apply known pixel size, here 0.512 pixel/µm
			run("Set Scale...", "distance=256 known=500 unit=µm");

		//create output name with image ID as the first element
			outputName = outputDirectory + File.separator + image_id + "_flat_"+ fileName + ".tiff";
			print("output name = " , outputName);
		// Save the results data under output name in the output folder
			saveAs("tiff", outputName);
			output_file_nbr++;		
		}
		
	// Closes all opened images
    close("*");  
}
