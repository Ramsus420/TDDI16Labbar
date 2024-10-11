#pragma once
#include <iostream>
#include <cmath>

/**
 * An immutable data type for points in the plane.
 */
class Point {
public:
    // No default constructor.
    Point() = delete;

    // Initialize with coordinates.
    Point(double x, double y) : x{x}, y{y} {}

    // Position
    double x;
    double y;

    // Compute the slope to another point.
    //
    // If the points are the same, negative infinity is returned
    // Otherwise, the angle between this and 'to', in radians, is returned
    double slopeTo(const Point &to) const;

    // Compare slopes to two other points and see if they are the same, given
    // the specified tolerance.
    bool sameSlope(const Point &a, const Point &b, double tolerance) const;

    // Is this point lexicographically smaller than p?
    // Comparing x-coordinates and breaking ties by y-coordinates
    bool operator <(const Point&) const;
    bool operator >(const Point&) const;

    // Output.
    friend std::ostream& operator<<(std::ostream&, const Point&);
};

/**
 * Determine if two slopes are the same, given a tolerance.
 */
bool sameSlope(double slopeA, double slopeB, double tolerance);

/**
 * Sort points according to their slope relative to 'origin'.
 */
class PolarSorter {
public:
    PolarSorter(const Point &origin) : origin{origin} {}

    bool operator() (const Point& p1, const Point& p2) const {
        return origin.slopeTo(p1) < origin.slopeTo(p2);
    }

private:
    Point origin;
};
