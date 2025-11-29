#ifndef BLOCK_H
#define BLOCK_H

#include <string>
#include <ctime>

class Block {
public:
    std::string data;
    std::string prevHash;
    std::string hash;
    time_t timestamp;
    int nonce;

    // FIXED: Constructor with proper parameters
    Block(const std::string& data, const std::string& prevHash);
    
    void calculateHash();
    void mineBlock(int difficulty);
    
    bool operator==(const Block& other) const {
        return hash == other.hash && 
               prevHash == other.prevHash &&
               data == other.data &&
               timestamp == other.timestamp;
    }
};

#endif