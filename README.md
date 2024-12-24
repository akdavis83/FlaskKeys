# Flask Site and Key Pair Generation Documentation

## Overview
This documentation provides details about the Flask-based web application and the implementation of Bitcoin (BTC) and Ethereum (ETH) key pair generation using Kyber cryptography.

### Features
- **Web Interface**: Allows users to generate BTC and ETH key pairs through a simple form.
- **API Endpoint**: Provides an endpoint for key pair generation.
- **Cryptographic Security**: Uses Kyber post-quantum cryptography and ECDSA (SECP256k1) for key generation.

---

## Flask Application

### Project Structure
```
project/
├── app.py                  # Flask application
├── templates/
│   └── index.html          # Frontend template
├── static/                 # Static files (if needed)
└── requirements.txt        # Python dependencies
```

### Installation and Setup

1. **Install Dependencies**:
   ```bash
   pip install flask ecdsa base58
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Web Interface**:
   Open a browser and navigate to `http://127.0.0.1:5000`.

4. **Deploy to Production**:
   Use a platform like Heroku or Render. Install `gunicorn` and create a `Procfile`:
   ```bash
   pip install gunicorn
   ```
   Add this to `Procfile`:
   ```
   web: gunicorn app:app
   ```

---

## API Endpoints

### `/generate`
- **Method**: POST
- **Description**: Generates a key pair for Bitcoin or Ethereum.
- **Request Body**:
  ```json
  {
      "keyType": "btc" | "eth"
  }
  ```
- **Response**:
  - Success:
    ```json
    {
        "privateKey": "<private_key>",
        "address": "<address>"
    }
    ```
  - Error:
    ```json
    {
        "error": "Invalid key type"
    }
    ```

---

## Key Pair Generation

### BTC and ETH Key Generation Using Kyber

#### Class: `BTCETHKeyGen`
This class handles the generation of BTC and ETH private keys and addresses.

#### Dependencies
- **Kyber**: For post-quantum cryptography.
- **ECDSA**: For SECP256k1 curve operations.
- **Base58**: For Bitcoin address encoding.
- **SHA256**: For cryptographic hashing.

#### Methods

1. **`generate_btc_keypair()`**
   - Generates a Bitcoin private key and address.
   - **Steps**:
     1. Generate Kyber key pair.
     2. Derive a 32-byte private key using SHA256.
     3. Use ECDSA (SECP256k1) to generate the public key.
     4. Create the Bitcoin address using Base58Check encoding.
   - **Returns**:
     - Private key (hex format)
     - Bitcoin address

2. **`generate_eth_keypair()`**
   - Generates an Ethereum private key and address.
   - **Steps**:
     1. Generate Kyber key pair.
     2. Derive a 32-byte private key using SHA256.
     3. Use ECDSA (SECP256k1) to generate the public key.
     4. Derive the Ethereum address from the last 20 bytes of the SHA256 hash of the public key.
   - **Returns**:
     - Private key (hex format)
     - Ethereum address (hex format)

---

## Example Workflow

### Bitcoin Key Pair
1. **Private Key**: Generated using Kyber secret key and SHA256.
2. **Public Key**: Generated using SECP256k1 curve.
3. **Address**: Encoded using Base58Check.

### Ethereum Key Pair
1. **Private Key**: Generated using Kyber secret key and SHA256.
2. **Public Key**: Generated using SECP256k1 curve.
3. **Address**: Derived from the last 20 bytes of the SHA256 hash of the public key.

---

## Frontend Interface

### `index.html`
- **Purpose**: Provides a user-friendly interface for key generation.
- **Features**:
  - Radio buttons to select BTC or ETH.
  - Button to trigger key pair generation.
  - Displays the generated private key and address.

#### Example HTML Structure
```html
<form onsubmit="event.preventDefault(); generateKeys();">
    <label>
        <input type="radio" name="keyType" value="btc" required> Bitcoin
    </label>
    <label>
        <input type="radio" name="keyType" value="eth"> Ethereum
    </label>
    <button type="submit">Generate</button>
</form>
<div id="result"></div>
```

---

## Security Considerations
- **Private Key Safety**: Ensure private keys are never logged or exposed.
- **HTTPS**: Use HTTPS in production to secure communication.
- **Rate Limiting**: Prevent abuse of the `/generate` endpoint.

---

## Future Enhancements
- Add support for additional cryptocurrencies.
- Implement user authentication for secure access.
- Provide a download option for generated keys.

