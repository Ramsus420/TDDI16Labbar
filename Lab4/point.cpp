#include <limits>
#include <iostream>
#include "point.h"

/**
 * Slope between this point and p
 *
 * If the points are the same, negative infinity is returned
 * Otherwise, the angle between this and 'to' is returned.
 */
double Point::slopeTo(const Point &p) const {
    if (x == p.x && y == p.y)
        return -std::numeric_limits<double>::infinity();
    else
        return std::atan2(p.y - y, p.x - x);
}

/**
 * Check if the slopes to two other points are the same.
 */
bool Point::sameSlope(const Point &a, const Point &b, double tolerance) const {
    double slopeA = slopeTo(a);
    double slopeB = slopeTo(b);
    return ::sameSlope(slopeA, slopeB, tolerance);
}

// Value for pi.
static const double pi = acos(-1);

bool sameSlope(double slopeA, double slopeB, double tolerance) {
    // See if slopeA and slopeB are close together.
    double difference = std::abs(slopeA - slopeB);
    // Also consider the case where they are close to 2*pi radians apart.
    double modPi = std::abs(difference - 2*pi);
    return difference <= tolerance || modPi <= tolerance;
}


/**
 * Is this point lexicographically smaller than p?
 * Comparing x-ccordinates and breaking ties by y-coordinates
 */
bool Point::operator<(const Point &other) const {
    if (x == other.x)
        return y < other.y;
    else
        return x < other.x;
}

bool Point::operator>(const Point &other) const {
    return other < *this;
}

std::ostream &operator<<(std::ostream &out, const Point& p) {
    return out << "(" << p.x << ", " << p.y << ")";
}
