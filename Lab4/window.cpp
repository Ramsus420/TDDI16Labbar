#include "window.h"
#include "gui_window.h"
#include "text_window.h"
#include <iostream>
#include <string>
#include <algorithm>

WindowPtr create_window(int argc, const char **argv) {
    if (argc == 2 && std::string(argv[1]) == "--text") {
        return WindowPtr{new Text_Window{}};
    } else if (argc == 1) {
        return WindowPtr{new Gui_Window{}};
    } else {
        std::cout << "Usage:" << std::endl;
        std::cout << argv[0] << " < input.txt" << std::endl;
        std::cout << "or:" << std::endl;
        std::cout << argv[0] << " --text < input.txt" << std::endl;
        return WindowPtr{};
    }
}

void Window::draw_line(std::vector<Point> points) {
    if (points.size() < 2) {
        std::cerr << "WARNING: Passed fewer than 2 points to 'draw_line'. Cannot draw a line!" << std::endl;
        return;
    }

    Point origin = points[0];
    Point direction{points[1].x - origin.x, points[1].y - origin.y};

    // Compute the (signed) distance from 'origin' along 'direction' (i.e. dot product).
    // Note: Not scaled to any particular length, since we only use it for sorting.
    auto distance = [origin, direction](Point p){
        Point delta{p.x - origin.x, p.y - origin.y};
        return delta.x*direction.x + delta.y*direction.y;
    };

    // Sort based on the (signed) distance from origin along 'direction':
    std::sort(points.begin(), points.end(), [&distance](Point a, Point b){
        return distance(a) < distance(b);
    });

    // Draw from the first to the last.
    draw_line(points.front(), points.back());
}
