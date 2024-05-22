
#include "Panorama.h"

Panorama::Panorama() {}

Panorama::~Panorama(){}


Mat Panorama::loadImage(string path)
{   
	Mat img = imread(path, IMREAD_COLOR);

	if (img.empty()) // Check for invalid input
	{
		cout << "Could not open or find the image" << std::endl;
		return Mat();
	}
	return img;
}

Mat Panorama::stitchPanorama(vector<Mat> imgs)
{
	Stitcher::Mode mode = Stitcher::PANORAMA;
	Ptr<Stitcher> pano = Stitcher::create(mode);
	Stitcher::Status status;

	Mat stitched;

	status = pano ->stitch(imgs,stitched);

	if (status == Stitcher::OK) {
		cout << "Success!" << endl;
		return stitched;

	}
   
	else {
		cout << "Can't stitch images, error code = " << int(status) << endl;
		return Mat();
	}
	
}



/*vector<Point> Panorama::findBiggestContour(Mat img)
{
	//Detects all external contours in the threshold image
	//Extracts the * largest * contour which will be the contour/outline of the stitched image
	

	Mat drawing = img.clone();
	vector<vector<Point>> cnts;
	vector<Point> max_c;
	//Rect bbox;

	findContours(img.clone(),cnts, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
	sort(cnts.begin(), cnts.end(),[](const vector<Point>& a, const vector<Point>& b) { return contourArea(a) > contourArea(b); });
	max_c = cnts.at(0);//extracting the largest contour
	//bbox = boundingRect(max_c);

	return max_c;
}*/


