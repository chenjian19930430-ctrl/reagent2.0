"""Media assembly module — FFmpeg-based video/image composition (Phase 1 MVP)."""

from __future__ import annotations

import asyncio
import uuid
from pathlib import Path
from typing import Optional

from loguru import logger

from reagent.shared.config import settings


class MediaAssembler:
    """Media assembly engine.

    Phase 1 MVP: FFmpeg-based video/image concatenation and overlay.
    Phase 2+: MiniMax video generation API integration.
    """

    def __init__(self):
        self._ffmpeg_path = settings.ffmpeg_path
        self._output_dir = Path(settings.content_output_dir) / "media"
        self._output_dir.mkdir(parents=True, exist_ok=True)

    async def concat_videos(
        self,
        input_paths: list[str],
        output_filename: Optional[str] = None,
        transition: str = "fade",
    ) -> str:
        """Concatenate multiple video clips using FFmpeg.

        Args:
            input_paths: List of video file paths.
            output_filename: Optional output filename (auto-generated if not provided).
            transition: Transition type ('fade', 'dissolve', 'none').

        Returns:
            Path to the assembled video.
        """
        if not input_paths:
            raise ValueError("At least one input path is required")

        filename = output_filename or f"video_{uuid.uuid4().hex[:8]}.mp4"
        output_path = str(self._output_dir / filename)

        # Build FFmpeg filter for concatenation
        # Using concat demuxer for same-codec clips
        concat_file = self._output_dir / f"concat_{uuid.uuid4().hex[:8]}.txt"
        with open(concat_file, "w") as f:
            for path in input_paths:
                f.write(f"file '{path}'\n")

        cmd = [
            self._ffmpeg_path,
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            "-y",
            output_path,
        ]

        logger.info(f"Running FFmpeg concat: {' '.join(cmd)}")
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        # Clean up temp concat file
        concat_file.unlink(missing_ok=True)

        if proc.returncode != 0:
            logger.error(f"FFmpeg concat failed: {stderr.decode()}")
            raise RuntimeError(f"FFmpeg concat failed: {stderr.decode()[:500]}")

        logger.info(f"Video assembled: {output_path}")
        return output_path

    async def overlay_text(
        self,
        video_path: str,
        text: str,
        output_filename: Optional[str] = None,
        position: str = "center",
    ) -> str:
        """Overlay text on a video using FFmpeg drawtext.

        Args:
            video_path: Input video path.
            text: Text to overlay.
            output_filename: Optional output filename.
            position: Text position ('center', 'top', 'bottom').

        Returns:
            Path to the output video.
        """
        filename = output_filename or f"text_{uuid.uuid4().hex[:8]}.mp4"
        output_path = str(self._output_dir / filename)

        # Position mapping
        pos_map = {
            "center": "(w-text_w)/2:(h-text_h)/2",
            "top": "(w-text_w)/2:20",
            "bottom": "(w-text_w)/2:h-60",
        }
        xy = pos_map.get(position, pos_map["center"])

        # SAFETY: Use drawtext textfile instead of inline text to prevent
        # command injection via user-provided text content.
        text_file = self._output_dir / f"text_content_{uuid.uuid4().hex[:8]}.txt"
        text_file.write_text(text, encoding="utf-8")

        cmd = [
            self._ffmpeg_path,
            "-i", video_path,
            "-vf", f"drawtext=textfile={text_file}:fontsize=48:fontcolor=white:x={xy}:y={xy}:shadowy=2",
            "-c:a", "copy",
            "-y",
            output_path,
        ]

        logger.info("Running FFmpeg overlay (textfile mode)")
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()

        # Clean up temp text file
        text_file.unlink(missing_ok=True)

        if proc.returncode != 0:
            logger.error(f"FFmpeg overlay failed: {stderr.decode()}")
            raise RuntimeError(f"FFmpeg overlay failed: {stderr.decode()[:500]}")

        logger.info(f"Text overlay complete: {output_path}")
        return output_path
