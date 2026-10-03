import hashlib
import zipfile
import io
import json
import sys
from Crypto.Cipher import AES


def decrypt(input_path, output_path=None, key_str="com.ijsoft.cpul", entry_name="cpus_db"):
    password_hex = hashlib.md5(key_str.encode()).hexdigest()
    key_bytes = password_hex.encode("utf-8")  # 32 bytes

    # IV: reverse odd-indexed bytes
    iv_bytes = bytearray(16)
    for i in range(0, len(key_bytes), 2):
        iv_bytes[i // 2] = key_bytes[31 - i]

    with open(input_path, "rb") as f:
        encrypted = f.read()

    cipher = AES.new(key_bytes, AES.MODE_CFB, iv=bytes(iv_bytes), segment_size=8)
    decrypted = cipher.decrypt(encrypted)

    zf = zipfile.ZipFile(io.BytesIO(decrypted))
    json_content = zf.read(entry_name)
    data = json.loads(json_content)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Written {len(json_content):,} bytes to {output_path}")

    return data


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "cpus"
    out = sys.argv[2] if len(sys.argv) > 2 else None

    # Auto-detect key based on filename
    if "gpu" in inp.lower():
        key = "com.ijsoft.gpul"
        entry = "gpus_db"
        default_out = "gpus_decrypted.json"
    else:
        key = "com.ijsoft.cpul"
        entry = "cpus_db"
        default_out = "cpus_decrypted.json"

    out = out or default_out
    decrypt(inp, out, key, entry)
