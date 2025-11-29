cmake_minimum_required(VERSION 3.10)
project(BlockchainVotingSystem)

set(CMAKE_CXX_STANDARD 11)

# Find OpenSSL
find_package(OpenSSL REQUIRED)

# Include directories
include_directories(include)

# Add executable
add_executable(blockchain_voting
    src/main.cpp
    src/block.cpp
    src/blockchain.cpp
    src/consensus.cpp
    src/sha256.cpp
    src/voter.cpp
    src/json_export.cpp
    src/rsa_signer.cpp
)

# Link libraries
target_link_libraries(blockchain_voting OpenSSL::SSL OpenSSL::Crypto)