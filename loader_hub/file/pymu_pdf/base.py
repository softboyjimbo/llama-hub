"""Read PDF files using PyMuPDF library."""
from pathlib import Path
from typing import Dict, List, Optional, Union

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class PyMuPDFReader(BaseReader):
    """Read PDF files using PyMuPDF library."""

    def load(
        self,
        file_path: Union[Path, str],
        metadata: bool = True,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
        """Loads list of documents from PDF file and also accepts extra information in dict format.

        Args:
            file_path (Union[Path, str]): file path of PDF file (accepts string or Path).
            metadata (bool, optional): if metadata to be included or not. Defaults to True.
            extra_info (Optional[Dict], optional): extra information related to each document in dict format. Defaults to None.

        Raises:
            TypeError: if extra_info is not a dictionary.
            TypeError: if file_path is not a string or Path.

        Returns:
            List[Document]: list of documents.
        """
        import fitz

        # check if file_path is a string or Path
        if not isinstance(file_path, str) and not isinstance(file_path, Path):
            raise TypeError("file_path must be a string or Path.")

        # open PDF file
        doc = fitz.open(file_path)

        # if extra_info is not None, check if it is a dictionary
        if extra_info:
            if not isinstance(extra_info, dict):
                raise TypeError("extra_info must be a dictionary.")

        # if metadata is True, add metadata to each document
        if metadata:
            metadata_dict = {}
            metadata_dict["total_pages"] = len(doc)
            metadata_dict["file_path"] = self.file_path

            # add extra_info to metadata_dict
            if not extra_info:
                extra_info = metadata_dict
            else:
                extra_info = dict(extra_info, **metadata_dict)

            # return list of documents
            return [
                Document(
                    page.get_text().encode("utf-8"),
                    extra_info=dict(
                        extra_info,
                        **{
                            metadata_dict["source"]: f"{page.number+1}",
                        },
                    ),
                )
                for page in doc
            ]

        else:
            return [
                Document(page.get_text().encode("utf-8"), extra_info=extra_info)
                for page in doc
            ]
