#include "text_window.h"
#include <iostream>

Text_Window::Text_Window() {}

void Text_Window::draw_points(const std::vector<Point> &) {}

void Text_Window::draw_line(Point from, Point to) {
    std::cout << "LINE: " << from << " - " << to << std::endl;
}

void Text_Window::run() {}
