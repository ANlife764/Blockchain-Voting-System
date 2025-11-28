#include <iostream>
#include <chrono>
#include "blockchain.h"
#include "voter.h"
#include "json_export.h"
#include "rsa_signer.h"  // Include the fixed RSA signer

int main() {
    try {
        // Initialize blockchain
        Blockchain chain(3);
        VoterAuth auth;
        
        // Test RSA signing
        std::cout << "=== RSA SIGNING TEST ===" << std::endl;
        RSASigner signer;
        
        std::string testVote = "Alice123 voted for CandidateA";
        std::string signature = signer.signMessage(testVote);
        
        std::cout << "✓ Message: " << testVote << std::endl;
        std::cout << "✓ Signature: " << signature.substr(0, 64) << "..." << std::endl;
        std::cout << "✓ Verification: " 
                  << (signer.verifySignature(testVote, signature) ? "PASS" : "FAIL") 
                  << std::endl;
        
        // Register voters and cast votes
        std::cout << "\n=== VOTING PROCESS ===" << std::endl;
        auth.registerVoter("Alice123");
        auth.registerVoter("Bob456");
        
        auto start = std::chrono::high_resolution_clock::now();
        
        if (auth.verifyVoter("Alice123")) {
            chain.addBlock("Alice123 voted for CandidateA");
        }
        
        if (auth.verifyVoter("Bob456")) {
            chain.addBlock("Bob456 voted for CandidateB");
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        
        // Display results
        std::cout << "\n=== BLOCKCHAIN ===" << std::endl;
        chain.printChain();
        
        std::cout << "\nProcessed in " 
                  << std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count()
                  << "ms\n";
        
        // Export to JSON
        JSONExport::saveToFile(chain.getChain(), "blockchain.json");
        
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}