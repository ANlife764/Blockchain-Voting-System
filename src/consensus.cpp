#include "consensus.h"
#include <algorithm>

bool Consensus::verifyBlock(const Block& newBlock, const std::vector<Block>& chain) {
    // Verify block structure
    if (!validateBlockStructure(newBlock)) return false;
    
    // Verify PoW
    std::string target(newBlock.hash.size() >= 3 ? 3 : newBlock.hash.size(), '0');
    if (newBlock.hash.substr(0, target.length()) != target) return false;
    
    // Verify previous hash
    if (!chain.empty() && newBlock.prevHash != chain.back().hash) return false;
    
    return true;
}

bool Consensus::achieveConsensus(const std::vector<std::vector<Block>>& nodeChains) {
    if (nodeChains.empty()) return false;
    
    // FIXED: Use explicit types instead of 'auto' in lambda
    const auto& longestChain = *std::max_element(
        nodeChains.begin(),
        nodeChains.end(),
        [](const std::vector<Block>& a, const std::vector<Block>& b) {
            return a.size() < b.size();
        }
    );
    
    // Verify all blocks in the longest chain
    for (size_t i = 1; i < longestChain.size(); ++i) {
        // Create a sub-vector for the chain up to current block
        std::vector<Block> subChain(longestChain.begin(), longestChain.begin() + i);
        if (!verifyBlock(longestChain[i], subChain)) {
            return false;
        }
    }
    
    return true;
}

bool Consensus::validateBlockStructure(const Block& block) {
    return !block.data.empty() && 
           !block.hash.empty() && 
           block.timestamp > 0;
}