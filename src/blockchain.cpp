#include "blockchain.h"
#include "block.h"
#include <iostream>

Blockchain::Blockchain(int diff) : difficulty(diff) {
    chain.emplace_back("Genesis Block", "");
    chain[0].mineBlock(difficulty);
    simulateNetwork();
}

void Blockchain::addBlock(const std::string& data) {
    Block newBlock(data, chain.back().hash);
    newBlock.mineBlock(difficulty);
    chain.push_back(newBlock);
    simulateNetwork(); // Update network after each block
}

void Blockchain::simulateNetwork(bool forceDivergence) {
    nodeChains.clear();
    
    // Create 3 node versions
    nodeChains.push_back(chain); // Node 0 (original)
    nodeChains.push_back(chain); // Node 1
    nodeChains.push_back(chain); // Node 2
    
    /*if (forceDivergence && chain.size() > 1) {
        // Node 1: Remove last block
        nodeChains[1].pop_back();
        
        // Node 2: Tamper with last block
        auto& lastBlock = nodeChains[2].back();
        lastBlock.data = "MALICIOUS_TAMPERING_" + lastBlock.data;
        lastBlock.calculateHash();
    }*/
}

bool Blockchain::checkConsensus() const {
    if (nodeChains.size() < 3) return false;
    
    // Compare hashes only for efficiency
    const auto& chain0 = nodeChains[0];
    const auto& chain1 = nodeChains[1];
    const auto& chain2 = nodeChains[2];
    
    // Check if at least two chains agree
    bool match01 = (chain0.size() == chain1.size());
    bool match02 = (chain0.size() == chain2.size());
    bool match12 = (chain1.size() == chain2.size());
    
    if (match01) {
        for (size_t i = 0; i < chain0.size(); ++i) {
            if (chain0[i].hash != chain1[i].hash) {
                match01 = false;
                break;
            }
        }
    }
    
    if (match02) {
        for (size_t i = 0; i < chain0.size(); ++i) {
            if (chain0[i].hash != chain2[i].hash) {
                match02 = false;
                break;
            }
        }
    }
    
    if (match12) {
        for (size_t i = 0; i < chain1.size(); ++i) {
            if (chain1[i].hash != chain2[i].hash) {
                match12 = false;
                break;
            }
        }
    }
    
    return (match01 || match02 || match12);
}

// ADD THIS METHOD for blockchain validation
bool Blockchain::isValid() const {
    for (size_t i = 1; i < chain.size(); ++i) {
        const Block& current = chain[i];
        const Block& previous = chain[i - 1];
        
        // Check if current block's previous hash matches actual previous block's hash
        if (current.prevHash != previous.hash) {
            return false;
        }
        
        // Check if current block's hash is valid
        Block temp = current;
        temp.calculateHash(); // Recalculate hash without mining
        if (temp.hash != current.hash) {
            return false;
        }
    }
    return true;
}

void Blockchain::printChain() const {
    for (const auto& block : chain) {
        std::cout << "Data: " << block.data << "\n"
                  << "Hash: " << block.hash << "\n"
                  << "Prev: " << block.prevHash << "\n"
                  << "Nonce: " << block.nonce << "\n"
                  << "-----------------\n";
    }
}
