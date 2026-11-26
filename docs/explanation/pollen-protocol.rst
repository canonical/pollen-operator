.. meta::
   :description: Pollen protocol used in the Pollen service.

.. _explanation_pollen_protocol:

Pollen protocol
===============

Pollen uses the standard HTTP/HTTPS protocol.

The Pollen client (Pollinate) will initiate the protocol and send an HTTP POST request to the Pollen server with form-encoded data containing one field, ``challenge``. The value of the ``challenge`` field is a 128-character random hex string.

.. code-block:: http

    POST / HTTP/1.1
    Content-Type: application/x-www-form-urlencoded

    challenge=<challenge>

The Pollen server will respond with two lines of plain text. The first line will be the SHA-512 digest of the request challenge, encoded in hexadecimal. The second line will be the SHA-512 digest of the challenge concatenated with 64 random bytes, encoded in hexadecimal.

.. code-block:: text

    HTTP/1.1 200 OK
    Content-Type: text/plain; charset=utf-8

    HEX(SHA512(challenge))
    HEX(SHA512(challenge || random_bytes))
