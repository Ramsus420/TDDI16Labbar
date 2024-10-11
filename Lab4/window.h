#pragma once
#include <vector>
#include <memory>
#include "point.h"

/**
 * Window allowing us to draw points and lines easily.
 */
class Window {
public:
    // Create.
    Window() = default;

    // No copy.
    Window(const Window &) = delete;
    Window &operator =(const Window &) = delete;

    // Destructor.
    virtual ~Window() = default;

    // Draw a number of points.
    virtual void draw_points(const std::vector<Point> &points) = 0;

    // Draw a line.
    virtual void draw_line(Point from, Point to) = 0;

    // Draw a line from a number of points that are assumed to be on the same line.
    // Determines which points are furthest apart and draws a single line.
    void draw_line(std::vector<Point> points);

    // Run the main-loop until the window is closed.
    virtual void run() = 0;
};

using WindowPtr = std::unique_ptr<Window>;

// Create a window given the command line.
WindowPtr create_window(int argc, const char **argv);
