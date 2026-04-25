# envoy-cli

> A CLI tool for managing and syncing `.env` files across environments with encryption support.

---

## Installation

```bash
pip install envoy-cli
```

Or with pipx for isolated installs:

```bash
pipx install envoy-cli
```

---

## Usage

Initialize a new envoy project in your repo:

```bash
envoy init
```

Push your local `.env` to a remote environment:

```bash
envoy push --env production
```

Pull and decrypt the latest secrets to your local `.env`:

```bash
envoy pull --env staging
```

Encrypt a `.env` file before committing or sharing:

```bash
envoy encrypt .env --output .env.enc
```

Decrypt a previously encrypted file:

```bash
envoy decrypt .env.enc --output .env
```

---

## Configuration

Envoy reads from an `envoy.toml` file in your project root. Run `envoy init` to generate one automatically.

---

## Requirements

- Python 3.8+
- An optional remote backend (S3, GCS, or HTTP endpoint) for syncing

---

## License

This project is licensed under the [MIT License](LICENSE).