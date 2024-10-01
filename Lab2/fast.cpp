#include "image.h"
#include "window.h"
#include "load.h"
#include <chrono>
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

using std::cout;
using std::cerr;
using std::endl;
using std::string;
using std::vector;
using std::unordered_map;

/**
 * Class that stores a summary of an image.
 *
 * This summary is intended to contain a high-level representation of the
 * important parts of an image. I.e. it shall contain what a human eye would
 * find relevant, while ignoring things that the human eye would find
 * irrelevant.
 *
 * To approximate human perception, we store a series of booleans that indicate
 * if the brightness of the image has increased or not. We do this for all
 * horizontal lines and vertical lines in a downsampled version of the image.
 *
 * See the lab instructions for more details.
 *
 * Note: You will need to use this data structure as the key in a hash table. As
 * such, you will need to implement equality checks and a hash function for this
 * data structure.
 */
class Image_Summary {
public:
    // Horizontal increases in brightness.
    vector<bool> horizontal;

    // Vertical increases in brightness.
    vector<bool> vertical;

    bool operator==(const Image_Summary &other) const {
        return horizontal == other.horizontal && vertical == other.vertical;
    }

};

namespace std {
    // Definiera en typ som specialiserar std::hash för vår typ:
    template <>
    class hash<Image_Summary> {
    public:
    // Typen ska kunna användas som ett funktionsobjekt.
    // Vi behöver därför överlagra funktionsanropsoperatorn (operator ()).
    size_t operator ()(const Image_Summary &to_hash) const {
        size_t hash = 0;
        for (const auto& h : to_hash.horizontal) {
            hash = hash * 2 + h;
        }
        for (const auto& v : to_hash.vertical) {
            hash = hash * 2 + v;
        }
        std::cout << hash << std::endl;
        return hash;
    }
    };
}

// Compute an Image_Summary from an image. This is described in detail in the
// lab instructions.
Image_Summary compute_summary(const Image &image) {
    const size_t summary_size = 8;
    Image_Summary result;

    for(size_t x = 0; x < summary_size; x++){
        for(size_t y = 0; y < summary_size; y++){
            if(image.pixel(x, y).brightness() < image.pixel(x + 1, y).brightness()){
                result.horizontal.push_back(false);
            } else {
                result.horizontal.push_back(true);
            }
            if(image.pixel(x, y).brightness() < image.pixel(x, y + 1).brightness()){
                result.vertical.push_back(false);
            } else {
                result.vertical.push_back(true);
            }
        }
    }

    return result;
}

int main(int argc, const char *argv[]) {
    WindowPtr window = Window::create(argc, argv);

    int summary_size{8};
    int duplicate_amount{0};

    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " [--nopause] [--nowindow] <directory>" << endl;
        cerr << "Missing directory containing files!" << endl;
        return 1;
    }

    vector<string> files = list_files(argv[1], ".jpg");
    cout << "Found " << files.size() << " image files." << endl;

    if (files.size() <= 0) {
        cerr << "No files found! Make sure you entered a proper path!" << endl;
        return 1;
    }

    auto begin = std::chrono::high_resolution_clock::now();

    unordered_map<Image_Summary, vector<string>> duplicates;
    std::vector<Image> images;

    //load images
    for(const auto &file : files){
        images.push_back(load_image(file).shrink(summary_size + 1, summary_size + 1));
    }

    auto load_time = std::chrono::high_resolution_clock::now();
    cout << "Loading images took: "
         << std::chrono::duration_cast<std::chrono::milliseconds>(load_time - begin).count()
         << " milliseconds." << endl;

    //compute summaries and find duplicates
    for (size_t i = 0; i < images.size(); i++) {
        duplicates[compute_summary(images.at(i))].push_back(files.at(i));
    }

    //report duplicates
    for(auto const& image : duplicates){
        if(image.second.size() > 1){
            window->report_match(image.second);
            duplicate_amount += image.second.size();
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    cout << "Total time: "
         << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count()
         << " milliseconds." << endl;

    cout << "Calculating duplicates took: "
         << std::chrono::duration_cast<std::chrono::milliseconds>(end - load_time).count()
         << " milliseconds." << endl;

    cout << "Found " << duplicate_amount << " duplicates." << endl;

    return 0;
}
