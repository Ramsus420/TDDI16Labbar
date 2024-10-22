/*
 * fast < input.txt
 *
 * Compute and plot all line segments involving 4 points in input.txt
 */

#include <iostream>
#include <algorithm>
#include <vector>
#include <chrono>
#include "point.h"
#include "window.h"

using namespace std;

int main(int argc, const char* argv[]) {
    WindowPtr window = create_window(argc, argv);
    if (!window)
        return 1;

    // The array of points
    vector<Point> points;

    // Read tolerance from cin
    double tolerance{};
    cin >> tolerance;

    // Read points from cin
    int N{};
    cin >> N;

    for (int i{0}; i < N; ++i) {
        double x{}, y{};
        cin >> x >> y;
        points.push_back(Point{x, y});
    }

    // draw points to screen all at once
    window->draw_points(points);

    // Sort points by their natural order. Makes finding endpoints a bit easier.
   // sort(points.begin(), points.end());

    auto begin = chrono::high_resolution_clock::now();

    sort(points.begin(), points.end());

    // Iterate through all possible origins:
    for (int o{0}; o < N; ++o) {
        // Select a point p from the set of all points
        Point p = points[o];

        //sortera resten av punkterna efter lutning
        sort(points.begin() + o, points.end(), [p](const Point& a, const Point& b) {
            return p.slopeTo(a) < p.slopeTo(b);
        });

        // kolla om 3 punkter
        for (int i = o + 1; i < N - 2; ++i) {
            if (p.slopeTo(points[i]) == p.slopeTo(points[i + 2])) {
                window->draw_line(p, points[i + 2]);
            }
        }
    }


    auto end = chrono::high_resolution_clock::now();
    cout << "Computing line segments took "
         << std::chrono::duration_cast<chrono::milliseconds>(end - begin).count()
         << " milliseconds." << endl;

    // wait for user to terminate program
    window->run();

    return 0;
}
