"""Job queue management system."""

import uuid
import asyncio
from typing import Optional, Dict, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from bot.logger import logger
from bot.config import config


class JobStatus(str, Enum):
    """Job status enumeration."""

    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    """Job representation in queue."""

    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int = 0
    filename: str = ""
    input_data: bytes = b""
    status: JobStatus = JobStatus.QUEUED
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[bytes] = None
    error: Optional[str] = None
    progress: int = 0  # 0-100
    settings: Dict = field(default_factory=dict)

    @property
    def processing_time(self) -> Optional[float]:
        """Get processing time in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class JobQueue:
    """Asynchronous job queue for processing obfuscation tasks."""

    def __init__(self, max_queue_size: int = 500, max_concurrent: int = 10):
        """Initialize job queue.

        Args:
            max_queue_size: Maximum jobs in queue
            max_concurrent: Maximum concurrent jobs
        """
        self.max_queue_size = max_queue_size
        self.max_concurrent = max_concurrent
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.jobs: Dict[str, Job] = {}  # job_id -> Job
        self.workers: set = set()
        self.process_callback: Optional[Callable] = None
        logger.info(
            f"JobQueue initialized: max_queue={max_queue_size}, max_concurrent={max_concurrent}"
        )

    async def add_job(self, job: Job) -> bool:
        """Add job to queue.

        Args:
            job: Job to add

        Returns:
            True if added, False if queue is full
        """
        if self.queue.full():
            logger.warning(f"Queue full, cannot add job {job.job_id}")
            return False

        await self.queue.put(job)
        self.jobs[job.job_id] = job
        logger.info(f"Job {job.job_id} added to queue (size: {self.queue.qsize()})")
        return True

    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a job.

        Args:
            job_id: Job ID to cancel

        Returns:
            True if cancelled, False if not found or already done
        """
        if job_id not in self.jobs:
            logger.warning(f"Job {job_id} not found")
            return False

        job = self.jobs[job_id]
        if job.status in (JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED):
            logger.warning(f"Cannot cancel job {job_id}, status: {job.status}")
            return False

        job.status = JobStatus.CANCELLED
        logger.info(f"Job {job_id} marked for cancellation")
        return True

    async def get_job_status(self, job_id: str) -> Optional[Job]:
        """Get job status.

        Args:
            job_id: Job ID

        Returns:
            Job object or None if not found
        """
        return self.jobs.get(job_id)

    async def get_user_jobs(self, user_id: int) -> list:
        """Get all jobs for a user.

        Args:
            user_id: User ID

        Returns:
            List of Job objects
        """
        return [job for job in self.jobs.values() if job.user_id == user_id]

    async def process_jobs(self, processor: Callable) -> None:
        """Start processing jobs with provided processor function.

        Args:
            processor: Async function to process jobs
        """
        self.process_callback = processor
        for _ in range(self.max_concurrent):
            worker = asyncio.create_task(self._worker(processor))
            self.workers.add(worker)
            worker.add_done_callback(self.workers.discard)
            logger.info(f"Worker started (total: {len(self.workers)})")

    async def _worker(self, processor: Callable) -> None:
        """Worker coroutine to process jobs.

        Args:
            processor: Async function to process jobs
        """
        while True:
            try:
                job = await asyncio.wait_for(
                    self.queue.get(), timeout=config.JOB_TIMEOUT_SECONDS
                )

                if job.status == JobStatus.CANCELLED:
                    logger.info(f"Job {job.job_id} skipped (cancelled)")
                    continue

                job.status = JobStatus.PROCESSING
                job.started_at = datetime.utcnow()
                logger.info(f"Processing job {job.job_id}")

                try:
                    result = await processor(job)
                    job.result = result
                    job.status = JobStatus.COMPLETED
                    job.completed_at = datetime.utcnow()
                    logger.info(
                        f"Job {job.job_id} completed in {job.processing_time:.2f}s"
                    )
                except Exception as e:
                    job.error = str(e)
                    job.status = JobStatus.FAILED
                    job.completed_at = datetime.utcnow()
                    logger.error(f"Job {job.job_id} failed: {e}")

            except asyncio.TimeoutError:
                logger.warning("Worker timeout, restarting")
            except Exception as e:
                logger.error(f"Worker error: {e}")

    async def cleanup_old_jobs(self, max_age_hours: int = 24) -> None:
        """Clean up old completed/failed jobs.

        Args:
            max_age_hours: Maximum age in hours
        """
        now = datetime.utcnow()
        removed = []
        for job_id, job in list(self.jobs.items()):
            if job.completed_at:
                age = (now - job.completed_at).total_seconds() / 3600
                if age > max_age_hours:
                    del self.jobs[job_id]
                    removed.append(job_id)

        if removed:
            logger.info(f"Cleaned up {len(removed)} old jobs")

    async def shutdown(self) -> None:
        """Shutdown queue and workers."""
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
        logger.info("JobQueue shutdown complete")
