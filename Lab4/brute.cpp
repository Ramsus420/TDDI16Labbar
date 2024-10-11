/*
 * brute < input.txt
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

    auto begin = chrono::high_resolution_clock::now();

    // Iterate through all possible origins:
    for (int o{0}; o < N; ++o) {
        // Then, select all combinations of other points:
        for (int i{0}; i < N - 2; ++i) {
            // If o and i are the same, skip this iteration:
            if (i == o)
                continue;

            for (int j{i + 1}; j < N - 1; j++) {
                // Only try to find a fourth point if the first three are on the same slope
                if (points[o].sameSlope(points[i], points[j], tolerance)) {
                    for (int k{j + 1}; k < N; k++) {
                        // Check if the new point is on the same slope!
                        if (points[o].sameSlope(points[i], points[k], tolerance)) {
                            window->draw_line({points[o], points[i], points[j], points[k]});
                        }
                    }
                }
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
