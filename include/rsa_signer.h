#ifndef RSA_SIGNER_H
#define RSA_SIGNER_H

#include <string>
#include <stdexcept>

class RSASigner {
private:
    void* pkey; // Opaque pointer to avoid including OpenSSL in header

public:
    RSASigner();
    ~RSASigner();
    
    void generateKeyPair();
    std::string signMessage(const std::string& message);
    bool verifySignature(const std::string& message, const std::string& signature);
    std::string getPublicKeyPEM();
};

#endif