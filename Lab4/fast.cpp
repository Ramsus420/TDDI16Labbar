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
    vector<Point> input_points;

    // Read tolerance from cin
    double tolerance{};
    cin >> tolerance;

    // Read points from cin
    int N{};
    cin >> N;

    for (int i{0}; i < N; ++i) {
        double x{}, y{};
        cin >> x >> y;
        input_points.push_back(Point{x, y});
    }

    // draw points to screen all at once
    window->draw_points(input_points);

    auto begin = chrono::high_resolution_clock::now();

    std::vector<Point> points = input_points;

    // Iterate through all possible origins:
    for (int o{0}; o < N; ++o) {
        // Select a point p from the set of all points
        Point p = input_points[o];
        vector<Point> result{p};

        //antar nlogn tid
        sort(points.begin(), points.end(), [p](const Point& a, const Point& b) {
            return p.slopeTo(a) < p.slopeTo(b);
        });

        for(int j = 1; j < N-2; j++)
        {
            if(p.sameSlope(points[j], points[j+2], tolerance))
            {
                result.push_back(points[j]);
                result.push_back(points[j + 1]);
                result.push_back(points[j + 2]);
            }
            else
            {
                if(result.size() > 3)
                {
                    window->draw_line(result);
                }
                result.clear();
                result.push_back(p);
            }
        }
        if(result.size() >= 3){
            window->draw_line(result);
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
