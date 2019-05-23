// myWork.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>


int main()
{	
	cv::Mat edges3, blur, edges5, edges6, edges7, gray, binary, gray2, binary2;
	std::string fileName = "C:\\GreenFox\\Hackaton\\fingerprint_gy1.jpg";
	std::string fileName2 = "C:\\GreenFox\\Hackaton\\fingerprint_gy2.jpg";
	cv::Mat src = cv::imread(fileName, cv::IMREAD_REDUCED_COLOR_8);
	cv::Mat src2 = cv::imread(fileName2, cv::IMREAD_REDUCED_COLOR_8);

	//BGR COLOR space
	// Setup ranges
	cv::Scalar low(30, 30, 145);
	cv::Scalar high(250, 250, 255);

	// Get binary mask
	cv::Mat1b mask;
	inRange(src, low, high, mask);
	cv::Mat1b mask2;
	inRange(src2, low, high, mask2);

	// Initialize result image (all black)
	cv::Mat3b res(src.rows, src.cols, cv::Vec3b(0, 0, 0));
	cv::Mat3b res2(src2.rows, src2.cols, cv::Vec3b(0, 0, 0));

	// Copy masked part to result image
	src.copyTo(res, mask);
	src2.copyTo(res2, mask2);

	cv::cvtColor(res, gray, cv::COLOR_BGR2GRAY);
	cv::cvtColor(res2, gray2, cv::COLOR_BGR2GRAY);

	cv::Mat structElement = cv::getStructuringElement(2, cv::Size(3, 3));
	
	cv::adaptiveThreshold(gray, binary, 255,
		cv::ADAPTIVE_THRESH_MEAN_C, cv::THRESH_BINARY, 7, 0);
	cv::adaptiveThreshold(gray2, binary2, 255,
		cv::ADAPTIVE_THRESH_MEAN_C, cv::THRESH_BINARY, 7, 0);

	cv::Mat harris_corners, harris_normalised;
	harris_corners = cv::Mat::zeros(binary.size(), CV_32FC1);
	cornerHarris(binary, harris_corners, 2, 3, 0.04, cv::BORDER_DEFAULT);
	normalize(harris_corners, harris_normalised, 0, 255, cv::NORM_MINMAX, CV_32FC1, cv::Mat());

	int threshold_harris = 125;
	std::vector<cv::KeyPoint> keypoints;

	cv::Mat rescaled;
	cv::convertScaleAbs(harris_normalised, rescaled);
	cv::Mat harris_c(rescaled.rows, rescaled.cols, CV_8UC3);
	cv::Mat in[] = {rescaled, rescaled, rescaled};
	int from_to[] = {0,0, 1,1, 2,2};
	mixChannels(in, 3, &harris_c, 1, from_to, 3);
	for (int x = 0; x < harris_normalised.cols; x++) {
		for (int y = 0; y < harris_normalised.rows; y++) {
			if ((int)harris_normalised.at<float>(y, x) > threshold_harris) {
				// Draw or store the keypoint location here, just like you decide. In our case we will store the location of the keypoint
				circle(harris_c, cv::Point(x, y), 5, cv::Scalar(0, 255, 0), 1);
				circle(harris_c, cv::Point(x, y), 1, cv::Scalar(0, 0, 255), 1);
				keypoints.push_back(cv::KeyPoint(x, y, 1));
			}
		}
	}
	imshow("temp", harris_c);
	cv::waitKey(0);

	// Compare both
	cv::Mat ccontainer(src.rows, src.cols * 2, CV_8UC3);
	cv::Mat binary_c = binary.clone();
	cvtColor(binary_c, binary_c, cv::COLOR_GRAY2BGR);
	binary_c.copyTo(ccontainer(cv::Rect(0, 0, src.cols, src.rows)));
	harris_c.copyTo(ccontainer(cv::Rect(src.cols, 0, src.cols, src.rows)));
	imshow("thinned versus selected corners", ccontainer); cv::waitKey(0);

	// Calculate the ORB descriptor based on the keypoint
	cv::Ptr<cv::Feature2D> orb_descriptor = cv::ORB::create();
	cv::Mat descriptors;
	orb_descriptor->compute(binary, keypoints, descriptors);

	// You can now store the descriptor in a matrix and calculate all for each image.
	// Since we just got the hamming distance brute force matching left, we will take another image and calculate the descriptors also.
	// Removed as much overburden comments as you can find them above

	cv::Mat harris_corners2, harris_normalised2;
	harris_corners2 = cv::Mat::zeros(binary2.size(), CV_32FC1);
	cornerHarris(binary2, harris_corners2, 2, 3, 0.04, cv::BORDER_DEFAULT);
	normalize(harris_corners2, harris_normalised2, 0, 255, cv::NORM_MINMAX, CV_32FC1, cv::Mat());
	std::vector<cv::KeyPoint> keypoints2;
	cv::Mat rescaled2;
	convertScaleAbs(harris_normalised2, rescaled2);
	cv::Mat harris_c2(rescaled2.rows, rescaled2.cols, CV_8UC3);
	cv::Mat in2[] = {rescaled2, rescaled2, rescaled2};
	int from_to2[] = {0,0, 1,1, 2,2};
	mixChannels(in2, 3, &harris_c2, 1, from_to2, 3);
	for (int x = 0; x < harris_normalised2.cols; x++) {
		for (int y = 0; y < harris_normalised2.rows; y++) {
			if ((int)harris_normalised2.at<float>(y, x) > threshold_harris) {
				// Draw or store the keypoint location here, just like you decide. In our case we will store the location of the keypoint
				circle(harris_c2, cv::Point(x, y), 5, cv::Scalar(0, 255, 0), 1);
				circle(harris_c2, cv::Point(x, y), 1, cv::Scalar(0, 0, 255), 1);
				keypoints2.push_back(cv::KeyPoint(x, y, 1));
			}
		}
	}
	cv::imshow("temp2", harris_c2); cv::waitKey(0);
	cv::Mat descriptors2;
	orb_descriptor->compute(binary2, keypoints2, descriptors2);

	// Now lets match both descriptors
	// Create the matcher interface
	cv::Ptr<cv::DescriptorMatcher> matcher = cv::DescriptorMatcher::create("BruteForce-Hamming");
	std::vector< cv::DMatch > matches;
	matcher->match(descriptors, descriptors2, matches);

	// Loop over matches and multiply
	// Return the matching certainty score
	float score = 0.0;
	for (int i = 0; i < matches.size(); i++) {
		cv::DMatch current_match = matches[i];
		score = score + current_match.distance;
	}
	std::cerr << std::endl << "Current matching score = " << score << std::endl;

	return 0;
}