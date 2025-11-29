#include "json_export.h"
#include "block.h"
#include <fstream>
#include <sstream>
#include <iomanip>
#include <iostream>

std::string JSONExport::escapeJSON(const std::string& input) {
    std::ostringstream ss;
    for (char c : input) {
        switch (c) {
            case '"': ss << "\\\""; break;
            case '\\': ss << "\\\\"; break;
            case '\b': ss << "\\b"; break;
            case '\f': ss << "\\f"; break;
            case '\n': ss << "\\n"; break;
            case '\r': ss << "\\r"; break;
            case '\t': ss << "\\t"; break;
            default: ss << c; break;
        }
    }
    return ss.str();
}

std::string JSONExport::blockToJSON(const Block& block, int index) {
    std::ostringstream json;
    json << "    {\n"
         << "      \"index\": " << index << ",\n"
         << "      \"data\": \"" << escapeJSON(block.data) << "\",\n"
         << "      \"prevHash\": \"" << escapeJSON(block.prevHash) << "\",\n"
         << "      \"hash\": \"" << escapeJSON(block.hash) << "\",\n"
         << "      \"timestamp\": " << block.timestamp << ",\n"
         << "      \"nonce\": " << block.nonce << "\n"
         << "    }";
    return json.str();
}

std::string JSONExport::chainToJSON(const std::vector<Block>& chain) {
    if (chain.empty()) {
        return "[]";
    }

    std::ostringstream json;
    json << "[\n";
    
    for (size_t i = 0; i < chain.size(); ++i) {
        json << blockToJSON(chain[i], i);
        if (i < chain.size() - 1) {
            json << ",";
        }
        json << "\n";
    }
    
    json << "]";
    return json.str();
}

bool JSONExport::saveToFile(const std::vector<Block>& chain, const std::string& filename) {
    try {
        std::string jsonData = chainToJSON(chain);
        std::ofstream file(filename);
        if (!file.is_open()) {
            std::cerr << "✗ Cannot open file: " << filename << std::endl;
            return false;
        }
        file << jsonData;
        file.close();
        std::cout << "✓ Blockchain exported to: " << filename << std::endl;
        return true;
    } catch (const std::exception& e) {
        std::cerr << "✗ Error exporting blockchain: " << e.what() << std::endl;
        return false;
    }
}

void JSONExport::printChainJSON(const std::vector<Block>& chain) {
    std::string jsonData = chainToJSON(chain);
    std::cout << jsonData << std::endl;
}