# AI Content Generator - Submission Report

> **Author:** Melkam  
> **Date:** February 2, 2026  
> **Challenge:** 10 Academy - AI Content Generation Exploration

---

## Table of Contents

1. [Environment Setup Documentation](#1-environment-setup-documentation)
2. [Codebase Understanding](#2-codebase-understanding)
3. [Generation Log](#3-generation-log)
4. [Challenges & Solutions](#4-challenges--solutions)
5. [Insights & Learnings](#5-insights--learnings)
6. [Generated Content Summary](#6-generated-content-summary)
7. [Links](#7-links)

---

## 1. Environment Setup Documentation

### APIs Configured

| Provider | API Key Variable | Status | Purpose |
|----------|-----------------|--------|---------|
| **Google Gemini** | `GEMINI_API_KEY` | ✅ Working | Lyria (music), Veo (video), Imagen (image) |
| **AIMLAPI** | `AIMLAPI_KEY` | ⚠️ Requires Verification | MiniMax music with vocals |
| **KlingAI** | `KLINGAI_API_KEY`, `KLINGAI_SECRET_KEY` | ❌ Auth Failed | High-quality video generation |

### Setup Process

```bash
# 1. Clone and enter the repository
cd trp1-ai-artist

# 2. Install dependencies with uv
uv sync

# 3. Configure environment variables
cp .env.example .env
# Edit .env with API keys
```

### Issues Encountered During Setup

#### Issue 1: MiniMax API Verification Required
- **Error:** `403 Forbidden - Complete verification to using the API`
- **Cause:** AIMLAPI requires card verification before using the MiniMax music API
- **Resolution:** Could not resolve without completing verification at https://aimlapi.com/app/verification
- **Workaround:** Used Lyria provider instead (instrumental only)

#### Issue 2: KlingAI Authentication Failed
- **Error:** `Authentication failed. Check API key.`
- **Cause:** JWT token generation or API key format issue
- **Resolution:** Verified keys were correctly set but authentication still failed
- **Workaround:** Attempted to use Veo instead

#### Issue 3: Veo API Changes
- **Error:** `module 'google.genai.types' has no attribute 'GenerateVideoConfig'`
- **Cause:** Google GenAI SDK updated, API changed
- **Resolution:** Fixed code to use `GenerateVideosConfig` (plural) and `generate_videos()` method

#### Issue 4: Veo Rate Limiting
- **Error:** `429 RESOURCE_EXHAUSTED - You exceeded your current quota`
- **Cause:** Free tier quota exhausted after multiple attempts
- **Resolution:** Would need to wait for quota reset or upgrade plan

---

## 2. Codebase Understanding

### Architecture Overview

```
src/ai_content/
├── core/                 # Core abstractions
│   ├── provider.py       # Protocol definitions (MusicProvider, VideoProvider, ImageProvider)
│   ├── registry.py       # ProviderRegistry - decorator-based provider registration
│   ├── result.py         # GenerationResult dataclass
│   └── exceptions.py     # Custom exceptions
│
├── config/               # Configuration management
│   ├── settings.py       # Pydantic Settings for all providers
│   └── loader.py         # YAML config loading
│
├── providers/            # Provider implementations
│   ├── google/
│   │   ├── lyria.py      # Real-time music streaming (instrumental)
│   │   ├── veo.py        # Video generation
│   │   └── imagen.py     # Image generation
│   ├── aimlapi/
│   │   ├── client.py     # Shared AIMLAPI HTTP client
│   │   └── minimax.py    # MiniMax music with vocals
│   └── kling/
│       └── direct.py     # KlingAI video (highest quality)
│
├── presets/              # Pre-configured styles
│   ├── music.py          # 11 music presets (jazz, blues, ethiopian-jazz, etc.)
│   └── video.py          # 7 video presets (nature, urban, space, etc.)
│
├── pipelines/            # Orchestration
│   ├── base.py           # PipelineResult, PipelineConfig
│   ├── music.py          # Music-only pipeline
│   ├── video.py          # Video-only pipeline
│   └── full.py           # Full music video pipeline
│
└── cli/                  # Command-line interface
    └── main.py           # Typer-based CLI commands
```

### Key Insights About the Provider System

1. **Protocol-Based Design**: Uses Python's `Protocol` for structural subtyping instead of ABC, enabling duck typing with type safety.

2. **Decorator Registration**: Providers register themselves using decorators:
   ```python
   @ProviderRegistry.register_music("lyria")
   class GoogleLyriaProvider:
       ...
   ```

3. **Lazy Instantiation**: Provider instances are created on-demand and cached as singletons.

4. **Capability Flags**: Each provider declares capabilities:
   - `supports_vocals` - Can generate vocals/lyrics
   - `supports_realtime` - Real-time streaming support
   - `supports_reference_audio` - Style transfer from audio
   - `supports_image_to_video` - Can animate images

### Provider Comparison

| Provider | Type | Vocals | Real-time | Reference Audio | Max Duration |
|----------|------|--------|-----------|-----------------|--------------|
| Lyria | Music | ❌ | ✅ | ❌ | 30s+ |
| MiniMax | Music | ✅ | ❌ | ✅ | ~60s |
| Veo | Video | - | ❌ | - | 8s |
| Kling | Video | - | ❌ | - | 10s |

### Pipeline Orchestration

The `FullContentPipeline` orchestrates end-to-end content creation:

```
1. Music Generation ──┬── (parallel) ──► 3. Video Generation
2. Image Generation ──┘                        │
                                               ▼
                                    4. Audio/Video Merge
                                               │
                                               ▼
                                    5. Export/Upload
```

---

## 3. Generation Log

### Successful Generations

#### Audio 1: Jazz Instrumental (Lyria)

| Property | Value |
|----------|-------|
| **Command** | `uv run ai-content music -p "A relaxing jazz piano piece with smooth bass" --style jazz --provider lyria` |
| **Prompt Used** | Preset: `[Smooth Jazz Fusion] [Walking Bass Line, Brushed Drums, Mellow Saxophone] [Warm Piano Chords, Vinyl Crackle Texture] Late night radio feel, nostalgic and contemplative` |
| **Provider** | Google Lyria (lyria-realtime-exp) |
| **Preset** | `jazz` |
| **BPM** | 95 |
| **Duration** | 30 seconds |
| **Output File** | `exports/lyria_20260202_122717.wav` |
| **File Size** | 3.30 MB |
| **Creative Decision** | Used jazz preset for its nostalgic, late-night radio aesthetic |

#### Audio 2: Ethiopian Jazz Fusion (Lyria)

| Property | Value |
|----------|-------|
| **Command** | `uv run python examples/lyria_example_ethiopian.py --style ethio-jazz --duration 30` |
| **Prompt Used** | Weighted prompts: Ethiopian Jazz (1.0), Vibraphon Melodic (0.9), African Rhythms (0.8), Brass Section (0.7), Groovy Bass (0.6) |
| **Provider** | Google Lyria with custom weighted prompts |
| **Preset** | Custom `ethio-jazz` |
| **BPM** | 110 |
| **Temperature** | 0.85 |
| **Duration** | 30 seconds |
| **Output File** | `exports/ethio_jazz_instrumental.wav` |
| **File Size** | 5.13 MB |
| **Creative Decision** | Explored Ethiopian jazz (Mulatu Astatke inspired) to create unique Ethio-jazz fusion |

#### Audio 3: Lo-fi Hip Hop Instrumental (Lyria)

| Property | Value |
|----------|-------|
| **Command** | `uv run ai-content music -p "ethiapian amharic gospel song" --provider lyria --lyrics amharic-lyrics.txt` |
| **Prompt Used** | "ethiapian amharic gospel song" (lyrics ignored by Lyria) |
| **Provider** | Google Lyria |
| **Duration** | 30 seconds |
| **Output File** | `exports/lyria_20260202_125324.wav` |
| **File Size** | 5.13 MB |
| **Note** | Lyria does not support vocals - lyrics were ignored |

#### Audio 4: Lo-fi Chill Beats (Lyria)

| Property | Value |
|----------|-------|
| **Command** | `uv run ai-content music -p "Lo-fi hip hop, chill beats" --provider lyria --lyrics lyrics.txt` |
| **Provider** | Google Lyria |
| **Duration** | 30 seconds |
| **Output File** | `exports/lyria_20260202_131222.wav` |
| **File Size** | 5.13 MB |

### Failed Generations

#### Video Generation (Veo) - API Issues

```bash
uv run ai-content video -p "A majestic lion slowly walks through tall savanna grass..." --provider veo
```

**Errors encountered:**
1. `GenerateVideoConfig` → Fixed to `GenerateVideosConfig`
2. `allow_adult for personGeneration is currently not supported` → Fixed to `allow_all`
3. `429 RESOURCE_EXHAUSTED` → Quota exceeded, could not resolve

#### Music with Vocals (MiniMax) - Verification Required

```bash
uv run ai-content music -p "Lo-fi hip hop" --provider minimax --lyrics lyrics.txt
```

**Error:** `403 Forbidden - Complete verification to using the API`

---

## 4. Challenges & Solutions

### Challenge 1: CLI Requires Prompt Even with Preset

**What happened:** Running `ai-content music --style jazz --provider lyria` failed with "Missing option '--prompt'"

**Solution:** Always provide `--prompt` even when using a preset. The preset overrides the prompt value.

```bash
# Correct usage
uv run ai-content music -p "placeholder" --style jazz --provider lyria
```

### Challenge 2: Veo API Changes (GenerateVideoConfig)

**What happened:** `module 'google.genai.types' has no attribute 'GenerateVideoConfig'`

**Troubleshooting:**
1. Searched Google GenAI documentation
2. Found API changed from `GenerateVideoConfig` to `GenerateVideosConfig`
3. Method changed from `generate_video()` to `generate_videos()`

**Solution:** Updated `src/ai_content/providers/google/veo.py`:
```python
# Before
config = types.GenerateVideoConfig(...)
operation = await client.aio.models.generate_video(...)

# After
config = types.GenerateVideosConfig(...)
operation = await client.aio.models.generate_videos(...)
```

### Challenge 3: Veo personGeneration Parameter

**What happened:** `400 INVALID_ARGUMENT - allow_adult for personGeneration is currently not supported`

**Solution:** Veo 3.1 requires different values based on mode:
- Text-to-video: `allow_all`
- Image-to-video: `allow_adult`

Updated code to auto-select based on whether `first_frame_url` is provided.

### Challenge 4: Rate Limiting

**What happened:** After fixing the API issues, hit `429 RESOURCE_EXHAUSTED`

**Workaround discovered:**
- Wait for quota reset (daily reset)
- Use different API key
- Upgrade to paid tier

### Challenge 5: Lyria Doesn't Support Vocals

**What happened:** Attempted to use lyrics with Lyria, got warning "Lyria does not support vocals/lyrics"

**Workaround:** 
- Lyria is instrumental only
- For vocals, need MiniMax (requires verification) or future Suno/Udio providers

---

## 5. Insights & Learnings

### What Surprised Me About the Codebase

1. **Well-Structured Architecture**: The Protocol + Registry pattern makes adding new providers extremely clean. Just decorate a class and it's registered.

2. **Comprehensive Preset System**: The presets include not just prompts but also BPM, mood, and tags - very thoughtful for music generation.

3. **Pipeline Abstraction**: The full pipeline can orchestrate music + image + video + merge in parallel where possible.

4. **Async-First Design**: All I/O operations are async, which is essential for real-time streaming like Lyria.

### What I Would Improve

1. **Make `--prompt` Optional with Presets**: When a preset is specified, the prompt should be optional since the preset provides one.

2. **Better Error Messages**: Some errors (like the GenerateVideoConfig issue) took time to debug. More descriptive errors would help.

3. **Provider Health Check Command**: A command like `ai-content check-providers` to verify API keys and quota before attempting generation.

4. **Retry Logic for Rate Limits**: Auto-retry with exponential backoff when hitting 429 errors.

5. **Progress Indicators**: Long-running video generation (Kling: 5-14 min) could use progress updates.

### Comparison to Other AI Tools

| Aspect | This Codebase | Other Tools (e.g., Runway, Pika) |
|--------|--------------|----------------------------------|
| **Flexibility** | High - multiple providers, presets | Limited to their own models |
| **CLI Interface** | Excellent - full CLI with options | Usually web-only or limited CLI |
| **Customization** | BPM, temperature, lyrics, presets | Preset-heavy, less control |
| **Transparency** | Open source, can see/modify code | Black box |
| **Cost** | API-based, pay per use | Subscription-based |

### Key Takeaways

1. **AI Music Generation is Mature**: Lyria produces high-quality instrumentals with precise BPM control and style transfer.

2. **Video Generation Has Friction**: Rate limits, API changes, and authentication issues made video generation challenging.

3. **Vocals Require Specific Providers**: Not all music AI supports vocals - need to choose the right provider for the task.

4. **Presets Are Powerful**: Well-designed presets (like ethio-jazz) can produce culturally-specific content.

---

## 6. Generated Content Summary

### Audio Files Generated

| File | Style | Duration | Size | Provider |
|------|-------|----------|------|----------|
| `lyria_20260202_122717.wav` | Jazz | 30s | 3.3 MB | Lyria |
| `ethio_jazz_instrumental.wav` | Ethiopian Jazz | 30s | 5.1 MB | Lyria |
| `lyria_20260202_125324.wav` | Gospel-inspired | 30s | 5.1 MB | Lyria |
| `lyria_20260202_131222.wav` | Lo-fi Hip Hop | 30s | 5.1 MB | Lyria |

**Total Audio Generated:** 4 files, ~18.6 MB, 2 minutes of content

### Video Files Generated

| Status | Reason |
|--------|--------|
| ❌ Not Generated | Veo quota exhausted after fixing API issues |
| ❌ Not Generated | KlingAI authentication failed |

### Requirements Checklist

| Requirement | Status | Notes |
|-------------|--------|-------|
| At least 1 audio file | ✅ | 4 audio files generated |
| Different styles/providers | ✅ | Jazz, Ethiopian Jazz, Lo-fi styles |
| At least 1 video file | ⚠️ | Blocked by rate limits |
| (Bonus) Combined video | ❌ | Requires video first |

---

## 7. Links

### Repository
- **GitHub:** [trp1-ai-artist](https://github.com/[username]/trp1-ai-artist)

### Generated Content
- Audio files located in `exports/` directory
- No video generated due to API quota limitations

### YouTube
- N/A - Video generation was blocked by rate limits

### Documentation Referenced
- [Google Veo API Documentation](https://ai.google.dev/gemini-api/docs/video)
- [Google Lyria Documentation](https://ai.google.dev/gemini-api/docs/music-generation)
- [AIMLAPI Documentation](https://docs.aimlapi.com/)

---

## Appendix: Commands Reference

### Music Generation
```bash
# With preset
uv run ai-content music -p "any text" --style jazz --provider lyria

# Custom prompt
uv run ai-content music -p "Smooth jazz fusion with piano" --bpm 95 --duration 30 --provider lyria

# With lyrics (MiniMax only)
uv run ai-content music -p "Lo-fi beats" --provider minimax --lyrics lyrics.txt
```

### Video Generation
```bash
# Basic video
uv run ai-content video -p "Lion in savanna" --provider veo

# With preset
uv run ai-content video -p "any" --style nature --provider veo --aspect 16:9
```

### Utility Commands
```bash
# List all providers
uv run ai-content list-providers

# List all presets
uv run ai-content list-presets

# Check job status
uv run ai-content jobs
```


