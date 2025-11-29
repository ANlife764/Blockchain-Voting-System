#pragma once
#include <unordered_set>
#include <string>

class VoterAuth {
public:
    bool registerVoter(const std::string& voterID);
    bool verifyVoter(const std::string& voterID) const;
    
private:
    std::unordered_set<std::string> _voters;
};