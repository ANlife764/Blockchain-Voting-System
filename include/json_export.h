#ifndef JSON_EXPORT_H
#define JSON_EXPORT_H

#include <string>
#include <vector>

class Block; // Forward declaration

class JSONExport {
public:
    static std::string escapeJSON(const std::string& input);
    static std::string blockToJSON(const Block& block, int index);
    static std::string chainToJSON(const std::vector<Block>& chain);
    static bool saveToFile(const std::vector<Block>& chain, const std::string& filename);
    static void printChainJSON(const std::vector<Block>& chain);
};

#endif