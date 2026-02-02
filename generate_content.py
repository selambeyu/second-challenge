#!/usr/bin/env python3
"""
Quick script to generate required content for the challenge.

Run with: uv run python generate_content.py
"""

import asyncio
from pathlib import Path

from ai_content.core.registry import ProviderRegistry
from ai_content import providers  # noqa: F401 - registers providers


async def generate_video():
    """Generate a video with Veo."""
    print("\n" + "=" * 60)
    print("🎬 Generating Video with Veo")
    print("=" * 60)

    provider = ProviderRegistry.get_video("veo")
    result = await provider.generate(
        prompt="""A majestic lion slowly walks through tall savanna grass,
golden hour sunlight casting long shadows,
cinematic slow motion with tracking dolly shot,
nature documentary style, 8K resolution, shallow depth of field""",
        aspect_ratio="16:9",
    )

    if result.success:
        print(f"✅ Video saved to: {result.file_path}")
    else:
        print(f"❌ Video generation failed: {result.error}")

    return result


async def generate_music_with_lyrics():
    """Generate music with vocals using MiniMax."""
    print("\n" + "=" * 60)
    print("🎵 Generating Music with Vocals (MiniMax)")
    print("=" * 60)

    lyrics = """[Verse 1]
Late night vibes, coffee getting cold
Stories in my mind waiting to be told
Rain against the window, soft and slow
Let the music take me where I need to go

[Chorus]
Drifting through the hours
Lost in mellow sounds
Finding peace in quiet moments
Where the calm is found"""

    provider = ProviderRegistry.get_music("minimax")
    result = await provider.generate(
        prompt="Lo-fi hip hop, chill beats, mellow piano, vinyl crackle",
        lyrics=lyrics,
    )

    if result.success:
        print(f"✅ Music saved to: {result.file_path}")
    else:
        print(f"❌ Music generation failed: {result.error}")

    return result


async def combine_audio_video(audio_path: Path, video_path: Path):
    """Combine audio and video using FFmpeg."""
    print("\n" + "=" * 60)
    print("🔀 Combining Audio + Video")
    print("=" * 60)

    try:
        from ai_content.integrations.media import MediaProcessor

        processor = MediaProcessor()
        output_path = Path("exports/combined_music_video.mp4")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        await processor.merge_audio_video(
            audio_path=audio_path,
            video_path=video_path,
            output_path=output_path,
        )
        print(f"✅ Combined video saved to: {output_path}")
        return output_path

    except ImportError:
        print("⚠️ FFmpeg/moviepy not available for merging")
        return None
    except Exception as e:
        print(f"❌ Merge failed: {e}")
        return None


async def main():
    print("=" * 60)
    print("🚀 AI Content Generation Challenge")
    print("=" * 60)

    # Use existing audio or generate new
    existing_audio = Path("exports/ethio_jazz_instrumental.wav")

    # Generate video
    video_result = await generate_video()

    if video_result.success and existing_audio.exists():
        # Combine existing audio with new video
        await combine_audio_video(existing_audio, video_result.file_path)

    print("\n" + "=" * 60)
    print("📋 Summary")
    print("=" * 60)
    print("Check your exports/ folder for generated content!")


if __name__ == "__main__":
    asyncio.run(main())
