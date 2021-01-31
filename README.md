
# pretty-wgkey

## Introdution
This script generates a keypair for WireGuard VPN.

Its specific purpose is to ask the user a name (base64, 10 characters maximum) which will be present in the public key.

WireGuard has not yet implemented a solution to identify peers, so this script is, I believe, a way to identify peers from their public key.

## Usage
```text
pretty-wgkey.py [-h] [-p {anywhere,beginning}] [-dt] string

positional arguments:
  string                The string to find in the public key

optional arguments:
  -h, --help            show this help message and exit
  -p {anywhere,startswith}, --place {anywhere,startswith}
                        The place where to find the chosen string in the
                        public key
  -dt, --doctest        Launch internal tests (provided by doctest)
```

## Requirements
The script requires `pynacl` module, available [here](https://github.com/pyca/pynacl/).

It has been written and tested with Python 3.8.2.

## Performance
Execution time obviously depends on your computer's performances.

On a laptop with an Intel Core i9-8950HK CPU, I get an average 30k keys/sec generated.

I will work on updating this tool to take advantage of multicore CPU, when I'll have time and knowledge to do so.

## Disclaimer
Run this at your own risk.
This script is provided as is, and I am not responsible in any way for any damage that may appear after using it in a prodution environment.
The key generated **may** be weaker than purely random ones, because of the predictable part that is included in them (the name/string that is searched in the public key).

I know there are other tools doing the same thing (see references).
As I am currently learning Python, and using WIreGuard, I took this as learning project, and already learned a lot !

If I made typos or if my english is not correct, that's because it's not my native language ;)
Feel free to correct my mistakes!

## References
WireGuard website : https://www.wireguard.com

This script has been inspired by :
* `wireguard-vanity-address` from `warner` : https://github.com/warner/wireguard-vanity-address
* `Wireguard-Vanity-Key-Searcher` from `volleybus` : https://github.com/volleybus/Wireguard-Vanity-Key-Searcher
