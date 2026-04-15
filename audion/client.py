#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- MAGO
# AUTHORS:
# Sukbong Kwon (Galois)

from typing import Optional
from .base import BaseAudionClient

class AudionClient(BaseAudionClient):
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        """
        Initialize the Audion client.

        Args:
            api_key: The API key for user authentication. (required)
            base_url: The base URL of the server.
            timeout: The timeout of the request.
        """
        if not api_key:
            raise ValueError("api_key is required")
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )

def main():
    import os
    client = AudionClient(api_key=os.environ.get("AUDION_API_KEY", ""))
    result = client.flow(
        flow="audion_vu",
        input_type="file",
        input="test/audio/sample_10s.flac",
    )
    print(result)

if __name__ == "__main__":
    main()
