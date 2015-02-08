#include <iostream>
#include <cassert>

#include "opencv2/opencv.hpp"

cv::Mat ellipse(int center_i, int center_j, double r_i, double r_j, int height, int width){
	cv::Mat y = cv::Mat(cv::Size(height, 1), CV_32SC1);
	for(int i = 0; i < height; ++i)
		y.at<int>(i) = i - center_i;
	cv::Mat x = cv::Mat(cv::Size(1, width), CV_8UC1);
	for(int j = 0; j < width; ++j)
		x.at<int>(j) = j - center_j;
	cv::Mat ret = x.mul(x) / (r_j*r_j) + y.mul(y) / (r_i*r_i);
	for(int i = 0; i < height; ++i){
		for(int j = 0; j < width; ++j){
			if(ret.at<int>(i, j) <= 1) ret.at<int>(i, j) = 1;
			else ret.at<int>(i, j) = 0;
		}
	}
	return ret;
}

void test(){
	cv::VideoCapture cap("videos/roomba.mp4");
	assert(cap.isOpened());
	//double width = cap.get(CV_CAP_PROP_FRAME_WIDTH);
	//double height = cap.get(CV_CAP_PROP_FRAME_HEIGHT);
	double fps = cap.get(CV_CAP_PROP_FPS);
	cv::Mat frame_color, frame_gray, frame;
	bool flag = cap.read(frame_color);
	assert(flag);
	cv::cvtColor(frame_color, frame_gray, CV_BGR2GRAY);
	cv::resize(frame_gray, frame, cv::Size(), 0.1, 0.1);
	cv::Size size = frame.size();
	int width = size.width;
	int height = size.height;

	//int fourcc = CV_FOURCC('m', 'p', '4', 'v');
	int fourcc = static_cast<int>(cap.get(CV_CAP_PROP_FOURCC));
	cv::VideoWriter writer("result.mp4", fourcc, fps, size, true);
	assert(writer.isOpened());

	//int center_i = 894, center_j = 515;
	//int r_i = 300, r_j = 310;
	int center_i = 89, center_j = 52;
	int r_i = 30, r_j = 31;

	cv::Mat mask = ellipse(center_i, center_j, r_i, r_j, height, width);
	cv::Mat kernel = frame.mul(mask);

	for(int count = 0; count < 1000; ++count){
	//int count = 0;
	//while(flag){
		//++count;
		std::cout << count << '\n';
		flag = cap.read(frame_color);
		cv::resize(frame_color, frame, cv::Size(), 0.1, 0.1);
		cv::cvtColor(frame, frame_gray, CV_BGR2GRAY);
		cv::Mat res;
		cv::filter2D(frame_gray, res, -1, kernel);
		cv::Point maxLoc;
		cv::minMaxLoc(res, NULL, NULL, NULL, &maxLoc);
		int i = maxLoc.y, j = maxLoc.x;
		//if(40 < i && i < height - 40 && 40 < j && j < width - 40){
		//	cv::Range ranges[] = {cv::Range(i - 40, i + 40), cv::Range(j - 15, j + 15), cv::Range::all()};
		//	cv::Mat(frame, ranges);
		//	ranges = {cv::Range(i - 15, i + 15), cv::Range(j - 40, j + 40), cv::Range::all()};
		//	cv::Mat(frame, ranges);
		//}

		if(6 < i && i < height - 6 && 6 < j && j < width - 6){
			cv::Range ranges_y[] = {cv::Range(i - 6, i + 6), cv::Range(j - 2, j + 2), cv::Range::all()};
			cv::Mat(frame, ranges_y);
			cv::Range ranges_x[] = {cv::Range(i - 2, i + 2), cv::Range(j - 6, j + 6), cv::Range::all()};
			cv::Mat(frame, ranges_x);
		}

		writer.write(frame);
	}
	writer.release();
}

int main(){
	test();
}

