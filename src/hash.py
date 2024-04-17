import HashTools
from os import urandom

secret = urandom(16)
original_data = b"&admin=False"
sig = HashTools.new(algorithm="sha256", raw=secret+original_data).hexdigest()

# attack
append_data = b"&admin=True"
magic = HashTools.new("sha256")
new_data, new_sig = magic.extension(
    secret_length=16, original_data=original_data,
    append_data=append_data, signature=sig
)

print(f"Original data: {original_data}")
print(f"Original signature: {sig}")
print(f"New data: {new_data}")
print(f"New signature: {new_sig}")