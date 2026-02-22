#include <iostream>
#include <fstream>
#include <string>
#include <cstdio>  

using namespace std;

//              Function to overwrites files add zero
bool overwriteFile(const string& path, int passes) {
    
    fstream file(path, ios::in | ios::out | ios::binary);
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << path << endl;
        return false;
    }

    // file is big?????????????
    file.seekg(0, ios::end);
    long fileSize = file.tellg();

    // 3.shredd it*************************
    for (int p = 0; p < passes; p++) {
        file.seekp(0, ios::beg); 
        for (long i = 0; i < fileSize; i++) {
            file.put('\0'); //         overwrite with zero
        }
        file.flush(); // ///////////////force write to disk
    }

    file.close();
    return true;
}

int main(int argc, char* argv[]) {
   
    if (argc < 3) {
        cout << "Usage: shredder <filePath> <passes>" << endl;
        return 1;
    }

    string filePath = argv[1];
    int passes = stoi(argv[2]);

    // ///////shred
    if (overwriteFile(filePath, passes)) {
        // //// delete the file
        if (remove(filePath.c_str()) == 0) {
            cout << "OK" << endl;
            return 0;
        } else {
            cerr << "Error: Could not delete file " << filePath << endl;
        }
    }

    cout << "FAILED" << endl;
    return 1;
}