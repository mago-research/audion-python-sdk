<div align="center">
  <!-- <img src="https://audion.magovoice.com/static/media/logo.10d2cf1b78c4088112afa09c702c5c2d.svg" width="200">
  <h1>Audion Python SDK</h1> -->

  <p>
    <strong>음성 AI 구현의 복잡함을 없애고, 비즈니스 가능성을 확장하세요.</strong>
  </p>

  <p>
    <a href="https://github.com/magovoice/audion-python-sdk/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
    <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python version"></a>
  </p>
</div>

# Audion Python SDK

> Repository: https://github.com/holamago/audion-python-sdk

## 목차

- [특징](#특징)
- [요구사항](#요구사항)
- [설치](#설치)
- [빠른 시작](#빠른-시작)
- [API 문서](#api-문서)
- [지원 파일 형식](#지원-파일-형식)
- [문서](#문서)
- [라이선스](#라이선스)
- [지원](#지원)
- [버전 히스토리](#버전-히스토리)

## 특징

- **간편한 음성 AI 통합**: 몇 줄의 코드로 강력한 음성 AI 기능을 애플리케이션에 추가
- **다양한 입력 지원**: 로컬 파일 및 URL을 통한 음성/비디오 처리
- **광범위한 파일 형식**: 주요 오디오 및 비디오 형식 지원
- **유연한 Flow 시스템**: 다양한 음성 AI 워크플로우 지원
- **간단한 API**: 직관적이고 사용하기 쉬운 Python 인터페이스

## 요구사항

- Python 3.10+
- API 키 ([Audion 서비스 등록](https://audion.magovoice.com/signup) 필요)
  - 회원가입 후 API Key 발급 받아야 합니다.

## 설치

pip을 사용하여 설치:

```bash
pip install audion-sdk
```

또는 개발용으로 레포를 클론하여 editable 모드로 설치:

```bash
git clone https://github.com/holamago/audion-python-sdk.git
cd audion-python-sdk

python -m venv venv
source venv/bin/activate

pip install -e .
```

## 빠른 시작

### 1. 클라이언트 초기화

```python
from audion import AudionClient

# API 키로 클라이언트 초기화
client = AudionClient(api_key="your-api-key-here")
```

### 2. 로컬 파일 처리

- 오디오/비디오 업로드

```python
# 로컬 오디오/비디오 파일 처리
result = client.flow(
    flow="audion_vu",
    input_type="file",
    input="path/to/your/audio.wav"
)
print(result)
```

### 3. URL 처리

```python
# YouTube URL 처리
result = client.flow(
    flow="audion_vu",
    input_type="url",
    input="https://youtu.be/your-video-id"
)
print(result)
```

### 4. 자막 다운로드

```python
# 로컬 파일을 처리하고 SRT 자막 파일로 다운로드
saved_path = client.download(
    input_type="file",
    input="path/to/your/audio.wav",
    format="srt"
)
print(f"저장 경로: {saved_path}")

# URL을 처리하고 SRT 자막 파일로 다운로드 (저장 경로 지정)
saved_path = client.download(
    input_type="url",
    input="https://youtu.be/your-video-id",
    format="srt",
    output_path="./output/subtitle.srt"
)
print(f"저장 경로: {saved_path}")
```

## API 문서

### AudionClient

Audion 서비스의 메인 클라이언트 클래스입니다.

#### 초기화

```python
AudionClient(
    api_key: str,           # 필수: API 인증 키
    base_url: str = None,   # 선택: 서버 기본 URL
    timeout: float = 300    # 선택: 요청 타임아웃 (초)
)
```

**매개변수:**

- `api_key` (str, 필수): Audion 서비스 인증을 위한 API 키
- `base_url` (str, 선택): 서버의 기본 URL. 기본값은 프로덕션 서버
- `timeout` (float, 선택): HTTP 요청 타임아웃. 기본값은 300초

**예외:**

- `ValueError`: api_key가 제공되지 않은 경우

#### 메서드

##### `flow(flow, input_type, input)`

지정된 플로우로 음성/비디오 처리를 실행합니다.

```python
client.flow(
    flow: str,        # 실행할 플로우 이름
    input_type: str,  # 입력 타입: "file" 또는 "url"
    input: str        # 파일 경로 또는 URL
)
```

**매개변수:**

- `flow` (str): 실행할 플로우의 이름
  - 현재 지원하는 플로우:
    - `audion_vu`: Voice Understanding
    - `audion_vh`: Voice Highlight
  - Custom Flow 지원 가능 (email:contact@holamago.com)
- `input_type` (str): 입력 타입. `"file"` 또는 `"url"`
- `input` (str): 처리할 파일의 경로 또는 URL

**반환값:**

- `dict`: 처리 결과를 포함하는 JSON 응답

**예외:**

- `ValueError`: 지원하지 않는 input_type인 경우
- `Exception`: API 호출 실패 시

##### `download(input_type, input, format, output_path)`

오디오/비디오를 처리하고 자막 파일(SRT/VTT)을 다운로드합니다. 내부적으로 `audion_vu` 플로우를 실행한 뒤 결과를 자막 파일로 저장합니다.

```python
client.download(
    input_type: str,        # 입력 타입: "file" 또는 "url"
    input: str,             # 파일 경로 또는 URL
    format: str = "srt",    # 자막 포맷: "srt" 또는 "vtt"
    output_path: str = None # 저장 경로 (선택)
)
```

**매개변수:**

- `input_type` (str): 입력 타입. `"file"` 또는 `"url"`
- `input` (str): 처리할 파일의 경로 또는 URL
- `format` (str, 선택): 다운로드할 자막 포맷. `"srt"` 또는 `"vtt"`. 기본값은 `"srt"`
- `output_path` (str, 선택): 파일 저장 경로
  - `None`인 경우: 현재 디렉토리에 `{원본파일명}_{documentId}.{format}`으로 저장
  - 디렉토리 경로인 경우: 해당 디렉토리에 `{원본파일명}_{documentId}.{format}`으로 저장
  - 파일 경로인 경우: 지정된 경로에 저장

**반환값:**

- `str`: 저장된 파일의 절대 경로

**예외:**

- `ValueError`: 지원하지 않는 format이거나 서버 응답에서 documentId를 추출할 수 없는 경우
- `Exception`: API 호출 또는 파일 다운로드 실패 시

## 지원 파일 형식

### 오디오 형식

- `.wav` - WAV (Waveform Audio File Format)
- `.mp3` - MP3 (MPEG-1 Audio Layer III)
- `.m4a` - M4A (MPEG-4 Audio)
- `.ogg` - OGG (Ogg Vorbis)
- `.flac` - FLAC (Free Lossless Audio Codec)
- `.aac` - AAC (Advanced Audio Coding)
- `.wma` - WMA (Windows Media Audio)
- `.m4b`, `.m4p`, `.m4r`, `.m4v` - 기타 MPEG-4 오디오 형식

### 비디오 형식

- `.mp4` - MP4 (MPEG-4 Part 14)
- `.mov` - MOV (QuickTime File Format)
- `.avi` - AVI (Audio Video Interleave)
- `.mkv` - MKV (Matroska Video)
- `.webm` - WebM
- `.wmv` - WMV (Windows Media Video)
- `.flv` - FLV (Flash Video)
- `.mpeg`, `.mpg` - MPEG (Moving Picture Experts Group)

### 지원하는 Flow

- `audion_vu`: Voice Understanding - 음성 인식 및 분석
- `audion_vh`: Voice Highlight - 주요 음성 구간 추출
- Custom Flow도 지원 가능합니다 (contact@holamago.com)


## 문서

- **GitHub**: [github.com/holamago/audion-python-sdk](https://github.com/holamago/audion-python-sdk)
- **예제**: [examples/](https://github.com/holamago/audion-python-sdk/tree/main/examples) 디렉토리

## 라이선스

이 프로젝트는 [Apache License 2.0](LICENSE) 하에 라이선스됩니다.

## 지원

- **문서**: [Audion 공식 문서](https://audion.magovoice.com)
- **이슈**: [GitHub Issues](https://github.com/holamago/audion-python-sdk/issues)
- **이메일**: contact@holamago.com

## 버전 히스토리

<details>
<summary><b>v0.1.7</b></summary>

- `output_path`에 존재하지 않는 디렉토리 경로 지정 시 자동 생성 처리 개선
- 다운로드 파일명에 원본 파일명 포함 (`{원본파일명}_{documentId}.{format}`)
- flow 응답 구조(`content.documentId`) 대응 수정
- URL 입력 검증 추가
- 자막 다운로드 기능 추가 (`download` 메서드)
- SRT/VTT 포맷 자막 파일 다운로드 지원
- 자막 다운로드 예제 추가

</details>

<details>
<summary><b>v0.1.2</b></summary>

- PyPI 패키지 구성 정리 (`pyproject.toml` 기반 빌드)
- SDK 내부 구조 정리 (로그 유틸과 코어/헬퍼 모듈 리팩토링)
- 문서 개선 (README 정리 및 예제 링크 정리)

</details>

<details>
<summary><b>v0.1.0</b></summary>

- 초기 릴리스
- 기본 flow API 지원
- 파일 및 URL 입력 지원
- 다중 오디오/비디오 형식 지원

</details>

<div align="center">
  <p>Made with ❤️ by <a href="https://magovoice.com">MAGO</a></p>
</div>
