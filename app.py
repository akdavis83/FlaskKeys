from flask import Flask, render_template, request, jsonify
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1
from kyber import Kyber512, Kyber768, Kyber1024
import base58

app = Flask(__name__)

class BTCETHKeyGen:
    def __init__(self):
        self.kyber = Kyber512
        self.kyber = Kyber768
        self.kyber = Kyber1024

    def generate_btc_keypair(self):
        """
        Generate a Bitcoin private and public key pair using Kyber.
        """
        # Generate Kyber keys
        _, sk = self.kyber.keygen()

        # Derive a 32-byte private key for Bitcoin from the Kyber secret key
        priv_key = sha256(sk).digest()[:32]

        # Generate the Bitcoin public key using ECDSA (SECP256k1 curve)
        sk_ecdsa = SigningKey.from_string(priv_key, curve=SECP256k1)
        vk_ecdsa = sk_ecdsa.get_verifying_key()
        pub_key = b"\x04" + vk_ecdsa.to_string()  # Uncompressed public key

        # Generate the Bitcoin address
        pub_key_hash = sha256(pub_key).digest()
        btc_address = base58.b58encode_check(b"\x00" + pub_key_hash[:20])

        return priv_key.hex(), btc_address.decode()

    def generate_eth_keypair(self):
        """
        Generate an Ethereum private and public key pair using Kyber.
        """
        # Generate Kyber keys
        _, sk = self.kyber.keygen()

        # Derive a 32-byte private key for Ethereum from the Kyber secret key
        priv_key = sha256(sk).digest()[:32]

        # Generate the Ethereum public key using ECDSA (SECP256k1 curve)
        sk_ecdsa = SigningKey.from_string(priv_key, curve=SECP256k1)
        vk_ecdsa = sk_ecdsa.get_verifying_key()
        pub_key = vk_ecdsa.to_string()  # Compressed public key not needed for Ethereum

        # Derive the Ethereum address (last 20 bytes of the Keccak-256 hash of the public key)
        eth_address = sha256(pub_key).digest()[-20:]

        return priv_key.hex(), "0x" + eth_address.hex()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_keys():
    key_type = request.json.get('keyType')
    keygen = BTCETHKeyGen()

    if key_type == 'btc':
        priv_key, address = keygen.generate_btc_keypair()
    elif key_type == 'eth':
        priv_key, address = keygen.generate_eth_keypair()
    else:
        return jsonify({'error': 'Invalid key type'}), 400

    return jsonify({'privateKey': priv_key, 'address': address})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
