#include "rsa_signer.h"
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <openssl/bio.h>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <vector>
#include <stdexcept>

RSASigner::RSASigner() : pkey(nullptr) {
    generateKeyPair();
}

RSASigner::~RSASigner() {
    if (pkey) {
        EVP_PKEY_free(static_cast<EVP_PKEY*>(pkey));
    }
}

void RSASigner::generateKeyPair() {
    EVP_PKEY_CTX* ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, nullptr);
    if (!ctx) {
        throw std::runtime_error("Failed to create RSA context");
    }

    if (EVP_PKEY_keygen_init(ctx) <= 0) {
        EVP_PKEY_CTX_free(ctx);
        throw std::runtime_error("Failed to initialize RSA key generation");
    }

    if (EVP_PKEY_CTX_set_rsa_keygen_bits(ctx, 2048) <= 0) {
        EVP_PKEY_CTX_free(ctx);
        throw std::runtime_error("Failed to set RSA key bits to 2048");
    }

    EVP_PKEY* key = nullptr;
    if (EVP_PKEY_keygen(ctx, &key) <= 0) {
        EVP_PKEY_CTX_free(ctx);
        throw std::runtime_error("Failed to generate RSA key pair");
    }

    EVP_PKEY_CTX_free(ctx);
    pkey = key;
    std::cout << "✓ RSA-2048 key pair generated successfully" << std::endl;
}

std::string RSASigner::signMessage(const std::string& message) {
    if (!pkey) {
        throw std::runtime_error("RSA key not initialized");
    }

    EVP_PKEY* key = static_cast<EVP_PKEY*>(pkey);
    EVP_MD_CTX* ctx = EVP_MD_CTX_new();
    if (!ctx) {
        throw std::runtime_error("Failed to create signing context");
    }

    // Initialize signing operation
    if (EVP_DigestSignInit(ctx, nullptr, EVP_sha256(), nullptr, key) <= 0) {
        EVP_MD_CTX_free(ctx);
        throw std::runtime_error("Failed to initialize RSA signing");
    }

    // Provide the message to be signed
    if (EVP_DigestSignUpdate(ctx, message.c_str(), message.length()) <= 0) {
        EVP_MD_CTX_free(ctx);
        throw std::runtime_error("Failed to update RSA signing with message");
    }

    // Determine signature length
    size_t signatureLength = 0;
    if (EVP_DigestSignFinal(ctx, nullptr, &signatureLength) <= 0) {
        EVP_MD_CTX_free(ctx);
        throw std::runtime_error("Failed to determine RSA signature length");
    }

    // Allocate buffer for signature
    std::vector<unsigned char> signature(signatureLength);
    
    // Create signature
    if (EVP_DigestSignFinal(ctx, signature.data(), &signatureLength) <= 0) {
        EVP_MD_CTX_free(ctx);
        throw std::runtime_error("Failed to create RSA signature");
    }

    EVP_MD_CTX_free(ctx);

    // Convert binary signature to hex string
    std::stringstream ss;
    for (size_t i = 0; i < signatureLength; i++) {
        ss << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(signature[i]);
    }
    
    return ss.str();
}

bool RSASigner::verifySignature(const std::string& message, const std::string& signatureHex) {
    if (!pkey) {
        throw std::runtime_error("RSA key not initialized");
    }

    // Convert hex signature back to binary
    std::vector<unsigned char> signature;
    for (size_t i = 0; i < signatureHex.length(); i += 2) {
        std::string byteString = signatureHex.substr(i, 2);
        unsigned char byte = static_cast<unsigned char>(std::stoul(byteString, nullptr, 16));
        signature.push_back(byte);
    }

    EVP_PKEY* key = static_cast<EVP_PKEY*>(pkey);
    EVP_MD_CTX* ctx = EVP_MD_CTX_new();
    if (!ctx) {
        throw std::runtime_error("Failed to create verification context");
    }

    // Initialize verification operation
    if (EVP_DigestVerifyInit(ctx, nullptr, EVP_sha256(), nullptr, key) <= 0) {
        EVP_MD_CTX_free(ctx);
        throw std::runtime_error("Failed to initialize RSA verification");
    }

    // Provide the message to be verified
    if (EVP_DigestVerifyUpdate(ctx, message.c_str(), message.length()) <= 0) {
        EVP_MD_CTX_free(ctx);
        throw std::runtime_error("Failed to update RSA verification with message");
    }

    // Verify signature
    int result = EVP_DigestVerifyFinal(ctx, signature.data(), signature.size());
    EVP_MD_CTX_free(ctx);

    return result == 1;
}

std::string RSASigner::getPublicKeyPEM() {
    if (!pkey) return "";
    
    EVP_PKEY* key = static_cast<EVP_PKEY*>(pkey);
    BIO* bio = BIO_new(BIO_s_mem());
    
    if (PEM_write_bio_PUBKEY(bio, key) != 1) {
        BIO_free(bio);
        throw std::runtime_error("Failed to write public key to PEM format");
    }
    
    char* pemData = nullptr;
    long pemLength = BIO_get_mem_data(bio, &pemData);
    std::string pemString(pemData, pemLength);
    
    BIO_free(bio);
    return pemString;
}