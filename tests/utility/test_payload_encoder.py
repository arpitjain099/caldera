import pytest

from app.utility.payload_encoder import DEFAULT_KEY, xor_bytes, xor_file


PAYLOAD = b'hello payload contents\n'


class TestXorBytes:
    def test_default_key(self):
        assert xor_bytes(PAYLOAD) != PAYLOAD
        assert xor_bytes(xor_bytes(PAYLOAD)) == PAYLOAD

    def test_explicit_int_list_key(self):
        assert xor_bytes(PAYLOAD, key=DEFAULT_KEY) == xor_bytes(PAYLOAD)

    @pytest.mark.parametrize('key', ['ABCD', 'a', 'longer-text-key'])
    def test_string_key(self, key):
        """The -key argument is text, so a str key has to work."""
        encoded = xor_bytes(PAYLOAD, key=key)

        assert encoded != PAYLOAD
        assert xor_bytes(encoded, key=key) == PAYLOAD

    def test_string_and_bytes_keys_agree(self):
        assert xor_bytes(PAYLOAD, key='ABCD') == xor_bytes(PAYLOAD, key=b'ABCD')


class TestXorFile:
    def test_round_trip_with_string_key(self, tmp_path):
        source = tmp_path / 'in.bin'
        encoded = tmp_path / 'in.bin.xored'
        decoded = tmp_path / 'out.bin'
        source.write_bytes(PAYLOAD)

        xor_file(str(source), output_file=str(encoded), key='ABCD')
        xor_file(str(encoded), output_file=str(decoded), key='ABCD')

        assert encoded.read_bytes() != PAYLOAD
        assert decoded.read_bytes() == PAYLOAD
