#include <iostream>
#include <fstream>
#include <string>
#include <sys/types.h>
#include <dirent.h>

int increase_label_num;

void replaceFirstNumber(std::string& line) {
    size_t spacePos = line.find(' ');
    if (spacePos != std::string::npos) {
        std::string firstNumber = line.substr(0, spacePos);
        try {
            int num = std::stoi(firstNumber);
            num += increase_label_num;
            line.replace(0, spacePos, std::to_string(num));
        } catch (...) {
            std::cerr << "Error converting first number to integer: " << firstNumber << std::endl;
        }
    }
}

void processFile(const std::string& filename) {
    std::ifstream infile(filename);
    std::ofstream outfile(filename + ".tmp");

    if (!infile) {
        std::cerr << "Error opening input file: " << filename << std::endl;
        return;
    }
    if (!outfile) {  
        std::cerr << "Error creating output file: " << filename + ".tmp" << std::endl;
        infile.close();
        return;
    }

    std::string line;
    while (std::getline(infile, line)) {
        replaceFirstNumber(line);
        outfile << line << '\n';
    }

    infile.close();
    outfile.close();

    remove(filename.c_str());
    rename((filename + ".tmp").c_str(), filename.c_str());
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << "<folder_path> <increase_label_number>" << std::endl;
        return EXIT_FAILURE;
    }

    std::string folderPath = argv[1]; //Path
    std::string increase_label_num_temp = argv[2]; //Increase label number

    try {
        increase_label_num = std::stoi(increase_label_num_temp);
    } catch (...) {
        std::cerr << "Error converting increase label number to integer: " << increase_label_num_temp << std::endl;
        return EXIT_FAILURE;
    }

    DIR *dir;
    struct dirent *ent;
    if ((dir = opendir(folderPath.c_str())) != nullptr) {
        while ((ent = readdir(dir)) != nullptr) {
            std::string filename = ent->d_name;
            if (filename != "." && filename != "..") {
                std::string filepath = folderPath + "/" + filename;
                processFile(filepath);
            }
        }
        closedir(dir);
    } else {
        std::cerr << "Error opening directory: " << folderPath << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "Processing complete." << std::endl;
    return EXIT_SUCCESS;
}
