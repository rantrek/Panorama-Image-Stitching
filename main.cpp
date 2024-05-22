// Panorama_Stitching.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "Panorama.h"

using namespace std;

int main()
{
	string imageFolder( "city/*.jpg");
    vector<string> imagePath;
    glob(imageFolder, imagePath);
	vector<Mat> images;
    Mat stitchedImg;
    Panorama *panorama = new Panorama();

    for (size_t i = 0; i < imagePath.size(); ++i)
    {
        // Read the ith argument or image 
        // and push into the image array
        Mat img = panorama->loadImage(imagePath[i]);
        img.resize(400);
        images.push_back(img);
    }

    stitchedImg = panorama->stitchPanorama(images);
   

    //Visualize the images
    //imshow("Original 1", images[0]);
    //imshow("Original 2", images[1]);
	
    imshow("Panorama", stitchedImg);
	waitKey(0);

	return 0;
}

