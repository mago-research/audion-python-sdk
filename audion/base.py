# Copyright (c) 2025- MAGO

import json
import os
import requests
from typing import Optional
from pydantic import BaseModel, Field

from .config import PRODUCTION_URL, TIMEOUT
from .helper.constants import SUPPORTED_DOWNLOAD_FORMATS
from .helper.logs import get_logger
from .helper.utils import get_media_type, validate_url

logger = get_logger(__name__)

class BaseAudionConfig(BaseModel):
    api_key: str = Field(..., description="The API key of the server")
    base_url: str = Field(default=PRODUCTION_URL, description="The base URL of the server")
    timeout: int = Field(default=TIMEOUT, description="The timeout of the server")


class BaseAudionClient(BaseAudionConfig):
    """
    Base class for all Audion clients.
    """
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        # Use default values if None is provided
        base_url = base_url or PRODUCTION_URL
        timeout = timeout or TIMEOUT

        super().__init__(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )
        logger.info(f"Initialized Audion client with base URL: {self.base_url}")

    def flow(
        self,
        flow: str,
        input_type: str,
        input: str,
    ):
        """
        Call the API with the given flow, input type, and input.

        Args:
            flow: The flow to call.
            input_type: The type of the input.
            input: The input to the flow.
        """
        # Set Authorization header with api_key
        headers = {
            "Authorization": f"Audion {self.api_key}"
        }

        # Define url
        url = f"{self.base_url}/flow"
        print(url)

        response = None
        try:
            # If input is a file, upload the file to the server
            if input_type == "file":
                logger.info(f"Uploading file: {input}")
                media_type = get_media_type(input)
                print(media_type, input)

                response = requests.post(
                    url,
                    headers=headers,
                    data={
                        "flow": flow,
                        "input_type": input_type,
                        "input": input,
                    },
                    files={
                        "file": (input, open(input, "rb"), media_type)
                    },
                )
                print(response.json())
            elif input_type == "url":
                validate_url(input)
                response = requests.post(
                    url,
                    headers=headers,
                    data={
                        "flow": flow,
                        "input_type": input_type,
                        "input": input,
                    },
                )
            else:
                raise ValueError(f"Unsupported input type: {input_type}")

            if response and response.status_code != 200:
                # Save the response to a file
                with open("rsp.json", "w") as f:
                    json.dump(response.json(), f)

            return response.json() if response else None
        except Exception as e:
            logger.error(f"Failed to call the API: {e}")
            raise e


    def download(
        self,
        input_type: str,
        input: str,
        format: str = "srt",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Process audio/video through the audion_vu flow and download the result
        as a subtitle file (SRT or VTT).

        Args:
            input_type: The type of the input. "file" or "url".
            input: The file path or URL to process.
            format: The subtitle format to download. "srt" or "vtt". Defaults to "srt".
            output_path: The path to save the downloaded file. If None, saves to
                         the current directory as {documentId}.{format}.

        Returns:
            The absolute path to the saved file.

        Raises:
            ValueError: If the format is not supported or documentId is missing from the response.
        """
        if format not in SUPPORTED_DOWNLOAD_FORMATS:
            raise ValueError(
                f"Unsupported format: '{format}'. "
                f"Supported formats: {SUPPORTED_DOWNLOAD_FORMATS}"
            )

        logger.info(f"Starting download: input_type={input_type}, format={format}")

        flow_result = self.flow("audion_vu", input_type, input)

        content = flow_result.get("content", {}) if flow_result else {}
        document_id = content.get("documentId")

        if not document_id:
            raise ValueError(
                "Failed to extract documentId from flow response. "
                f"Response: {flow_result}"
            )

        upload_filename = content.get("uploadFilename", "")
        logger.info(f"Obtained documentId: {document_id}, uploadFilename: {upload_filename}")

        return self._download_file(document_id, format, output_path, upload_filename)

    def _download_file(
        self,
        document_id: str,
        format: str,
        output_path: Optional[str] = None,
        upload_filename: str = "",
    ) -> str:
        """
        Download a subtitle file from the server.

        Args:
            document_id: The document ID returned from the flow response.
            format: The subtitle format. "srt" or "vtt".
            output_path: The path to save the file. If None, saves to
                         ./{document_id}.{format}.

        Returns:
            The absolute path to the saved file.
        """
        headers = {
            "Authorization": f"Audion {self.api_key}"
        }

        url = f"{self.base_url}/flow/download/{document_id}"
        logger.info(f"Downloading file from: {url}?format={format}")

        try:
            response = requests.get(
                url,
                headers=headers,
                params={"format": format},
                stream=True,
                timeout=self.timeout,
            )
            response.raise_for_status()

            resolved_path = self._resolve_output_path(
                document_id, format, output_path, upload_filename
            )

            parent_dir = os.path.dirname(resolved_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)

            with open(resolved_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            absolute_path = os.path.abspath(resolved_path)
            logger.info(f"File saved to: {absolute_path}")
            return absolute_path

        except requests.HTTPError as e:
            logger.error(f"Download failed with HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to download file: {e}")
            raise

    @staticmethod
    def _resolve_output_path(
        document_id: str,
        format: str,
        output_path: Optional[str] = None,
        upload_filename: str = "",
    ) -> str:
        if upload_filename:
            safe_name = "".join(
                c if c not in r'\/:*?"<>|' else "_" for c in upload_filename
            )
            default_filename = f"{safe_name}_{document_id}.{format}"
        else:
            default_filename = f"{document_id}.{format}"

        if output_path is None:
            return default_filename

        if os.path.isdir(output_path) or output_path.endswith(os.sep):
            return os.path.join(output_path, default_filename)

        return output_path

    def get_flows(self):
        """
        Get the flow from the server.
        """
        logger.info("Getting flows from the server")
        return self.get("/flow")






