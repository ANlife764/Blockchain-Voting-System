#include "voter.h"
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <stdexcept>

class RSASigner {
private:
    RSA* privateKey;
    RSA* publicKey;

public:
    RSASigner() {
        generateKeyPair();
    }

    void generateKeyPair() {
        RSA* rsa = RSA_new();
        BIGNUM* bn = BN_new();
        BN_set_word(bn, RSA_F4);
        
        RSA_generate_key_ex(rsa, 2048, bn, NULL);
        
        privateKey = rsa;
        publicKey = RSAPublicKey_dup(privateKey);
        BN_free(bn);
    }

    std::string signMessage(const std::string& message) {
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256(reinterpret_cast<const unsigned char*>(message.c_str()), message.length(), hash);
        
        unsigned char signature[4096];
        unsigned int signatureLength;
        
        int result = RSA_sign(NID_sha256, hash, SHA256_DIGEST_LENGTH, 
                             signature, &signatureLength, privateKey);
        
        if (result != 1) {
            throw std::runtime_error("RSA signing failed");
        }
        
        return std::string(reinterpret_cast<char*>(signature), signatureLength);
    }

    bool verifySignature(const std::string& message, const std::string& signature) {
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256(reinterpret_cast<const unsigned char*>(message.c_str()), message.length(), hash);
        
        int result = RSA_verify(NID_sha256, hash, SHA256_DIGEST_LENGTH,
                               reinterpret_cast<const unsigned char*>(signature.c_str()),
                               signature.length(), publicKey);
        
        return result == 1;
    }
};

bool VoterAuth::registerVoter(const std::string& voterID) {
    return _voters.insert(voterID).second;
}

bool VoterAuth::verifyVoter(const std::string& voterID) const {
    return _voters.find(voterID) != _voters.end();
}