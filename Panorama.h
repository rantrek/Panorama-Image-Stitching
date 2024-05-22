#pragma once
#include <iostream>
#include <fstream>
#include<vector>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/stitching.hpp>


using namespace cv;
using namespace std;

class Panorama
{
public:
	string path;
	vector<Mat> imgs;

	Panorama(); //default constructor
	~Panorama(); //destructor

	//Methods
	Mat loadImage(string path);

	Mat stitchPanorama(vector<Mat> imgs);

	



};



