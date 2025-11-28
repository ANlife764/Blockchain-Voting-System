#ifndef CONSENSUS_H
#define CONSENSUS_H

#include "block.h"
#include <vector>
#include <unordered_map>

class Consensus {
public:
    static bool verifyBlock(const Block& newBlock, const std::vector<Block>& chain);
    static bool achieveConsensus(const std::vector<std::vector<Block>>& nodeChains);
    
private:
    static bool validateBlockStructure(const Block& block);
};

#endif