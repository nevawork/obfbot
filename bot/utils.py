"""File handling utilities."""

import os
import zipfile
from pathlib import Path
from typing import Optional, List, Tuple
from bot.config import config
from bot.logger import logger


class FileHandler:
    """Handle file operations for obfuscation."""

    ALLOWED_EXTENSIONS = {".lua", ".luau", ".txt"}
    MAX_FILE_SIZE = config.MAX_FILE_SIZE_BYTES

    @staticmethod
    def validate_file(filename: str, file_size: int) -> Tuple[bool, Optional[str]]:
        """Validate uploaded file.

        Args:
            filename: Filename
            file_size: File size in bytes

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file size
        if file_size > FileHandler.MAX_FILE_SIZE:
            return False, f"File too large. Max size: {config.MAX_FILE_SIZE_MB}MB"

        # Check extension
        ext = Path(filename).suffix.lower()
        if ext not in FileHandler.ALLOWED_EXTENSIONS:
            return False, f"Invalid file type. Allowed: {', '.join(FileHandler.ALLOWED_EXTENSIONS)}"

        return True, None

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename
        """
        # Remove path traversal attempts
        filename = os.path.basename(filename)
        # Remove special characters
        filename = "".join(c for c in filename if c.isalnum() or c in "._-")
        return filename or "unnamed.lua"

    @staticmethod
    def save_file(content: bytes, job_id: str, filename: str) -> Path:
        """Save file to temp storage.

        Args:
            content: File content
            job_id: Job ID
            filename: Filename

        Returns:
            Path to saved file
        """
        job_dir = config.TEMP_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        file_path = job_dir / FileHandler.sanitize_filename(filename)
        file_path.write_bytes(content)
        logger.info(f"File saved: {file_path}")
        return file_path

    @staticmethod
    def read_file(path: Path) -> bytes:
        """Read file.

        Args:
            path: File path

        Returns:
            File content
        """
        return path.read_bytes()

    @staticmethod
    def save_output(content: str, job_id: str, filename: str) -> Path:
        """Save obfuscated output.

        Args:
            content: Obfuscated code
            job_id: Job ID
            filename: Output filename

        Returns:
            Path to output file
        """
        job_dir = config.OUTPUT_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        output_path = job_dir / FileHandler.sanitize_filename(filename)
        output_path.write_text(content, encoding="utf-8")
        logger.info(f"Output saved: {output_path}")
        return output_path

    @staticmethod
    def extract_zip(zip_path: Path, job_id: str) -> List[Tuple[str, bytes]]:
        """Extract ZIP archive.

        Args:
            zip_path: Path to ZIP file
            job_id: Job ID

        Returns:
            List of (filename, content) tuples
        """
        files = []
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_file:
                for file_info in zip_file.infolist():
                    if file_info.is_dir():
                        continue
                    ext = Path(file_info.filename).suffix.lower()
                    if ext in FileHandler.ALLOWED_EXTENSIONS:
                        content = zip_file.read(file_info.filename)
                        if len(content) <= FileHandler.MAX_FILE_SIZE:
                            files.append((file_info.filename, content))
                            logger.info(f"Extracted: {file_info.filename}")
        except Exception as e:
            logger.error(f"Failed to extract ZIP: {e}")
            raise
        return files

    @staticmethod
    def cleanup_job(job_id: str) -> None:
        """Clean up job files.

        Args:
            job_id: Job ID
        """
        import shutil
        job_temp = config.TEMP_DIR / job_id
        if job_temp.exists():
            shutil.rmtree(job_temp)
            logger.info(f"Cleaned up temp files: {job_temp}")
