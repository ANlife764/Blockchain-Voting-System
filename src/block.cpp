#include "block.h"
#include "sha256.h"
#include <iostream>

// FIXED: Constructor implementation
Block::Block(const std::string& data, const std::string& prevHash) 
    : data(data), prevHash(prevHash), timestamp(time(nullptr)), nonce(0) {
    calculateHash();
}

void Block::calculateHash() {
    std::string input = prevHash + data + std::to_string(timestamp) + std::to_string(nonce);
    hash = SHA256::hash(input);
}

void Block::mineBlock(int difficulty) {
    std::string target(difficulty, '0');
    while(hash.substr(0, difficulty) != target) {
        nonce++;
        calculateHash();
    }
}