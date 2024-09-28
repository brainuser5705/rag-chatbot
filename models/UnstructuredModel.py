import os
from dotenv import load_dotenv

import unstructured_client
from unstructured_client.models import operations, shared

from models.ChunkModel import Chunk

load_dotenv()

UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
UNSTRUCTURED_API_URL = os.getenv("UNSTRUCTURED_API_URL")

class Unstructured:
    def __init__(self):
        self.client = unstructured_client.UnstructuredClient(
            api_key_auth=UNSTRUCTURED_API_KEY,
            server_url=UNSTRUCTURED_API_URL
        )

    def ingest_document(self, file_path):

        print(f"Beginning ingestion for {file_path}...")
        try:
            with open(file_path, "rb") as file:
                file_data = file.read()
        except Exception as e:
            return f"{file_path} cannot be ingested."
        
        print(f"\tCreating partition request...")
        partition_request = operations.PartitionRequest(
            partition_parameters=shared.PartitionParameters(
                files=shared.Files(
                    content=file_data,
                    file_name=file_path,
                ),
                strategy=shared.Strategy.HI_RES,
                languages=['eng'],
                split_pdf_page=True,            # If True, splits the PDF file into smaller chunks of pages.
                split_pdf_allow_failed=True,    # If True, the partitioning continues even if some pages fail.
                split_pdf_concurrency_level=15  # Set the number of concurrent request to the maximum value: 15.
            ),
        )
        
        print(f"\tExtracting chunks from Unstructured...")
        # converts JSON output into a Chunk object representing the partition 
        try:
            res = self.client.general.partition(request=partition_request)

            chunks = []
            for elem in res.elements:
                chunks.append(
                    Chunk(
                        id=elem["element_id"],
                        text=elem["text"],
                        file_name=elem["metadata"]["filename"])
                )

            return chunks

        except Exception as e:
            raise IngestionException(f"IngestionException - Could not ingest document {file_path}: {e}")
    
class IngestionException(Exception):
    pass