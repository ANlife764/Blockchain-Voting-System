#ifndef BLOCKCHAIN_H
#define BLOCKCHAIN_H

#include <vector>
#include <string>
#include "block.h"

class Blockchain {
private:
    std::vector<Block> chain;
    int difficulty;
    std::vector<std::vector<Block>> nodeChains;

public:
    Blockchain(int diff = 3);
    void addBlock(const std::string& data);
    void printChain() const;
    bool isValid() const;
    
    // Consensus methods
    void simulateNetwork(bool forceDivergence = true);
    bool checkConsensus() const;
    const std::vector<std::vector<Block>>& getNodeChains() const { return nodeChains; }
    
    // ADD THIS METHOD for JSON export
    const std::vector<Block>& getChain() const { return chain; }
};

#endif