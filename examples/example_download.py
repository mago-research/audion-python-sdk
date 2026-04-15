#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- MAGO

"""
자막 파일 다운로드 예제

이 예제는 오디오/비디오를 처리하고 자막 파일(SRT/VTT)을 다운로드하는 방법을 보여줍니다.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from audion import AudionClient


def main():
    api_key = os.getenv("AUDION_API_KEY")

    if not api_key:
        print("에러: AUDION_API_KEY 환경 변수를 설정해주세요.")
        print("\n사용법:")
        print("  export AUDION_API_KEY='your-api-key-here'")
        print("  python examples/example_download.py <file_path_or_url> [format] [output_path]")
        return

    if len(sys.argv) < 2:
        print("에러: 파일 경로 또는 URL을 지정해주세요.")
        print("\n사용법:")
        print("  python examples/example_download.py <file_path_or_url> [format] [output_path]")
        print("\n예시:")
        print("  python examples/example_download.py samples/audio.wav")
        print("  python examples/example_download.py samples/audio.wav srt ./output/")
        print("  python examples/example_download.py samples/audio.wav vtt ./result.vtt")
        print("  python examples/example_download.py https://youtu.be/abc123 srt")
        return

    input_value = sys.argv[1]
    fmt = sys.argv[2] if len(sys.argv) >= 3 else "srt"
    output_path = sys.argv[3] if len(sys.argv) >= 4 else None

    is_url = input_value.startswith("http://") or input_value.startswith("https://")

    if is_url:
        input_type = "url"
        print(f"✓ 처리할 URL: {input_value}")
    else:
        input_type = "file"
        if not os.path.exists(input_value):
            print(f"에러: 파일을 찾을 수 없습니다: {input_value}")
            return
        print(f"✓ 파일 발견: {input_value}")
        print(f"✓ 파일 크기: {os.path.getsize(input_value) / 1024 / 1024:.2f} MB")

    print(f"✓ 다운로드 포맷: {fmt}")
    if output_path:
        print(f"✓ 저장 경로: {output_path}")

    client = AudionClient(api_key=api_key)

    try:
        print("\nAudion API 호출 및 자막 다운로드 중...")
        saved_path = client.download(
            input_type=input_type,
            input=input_value,
            format=fmt,
            output_path=output_path,
        )

        print(f"\n다운로드 완료!")
        print(f"저장 경로: {saved_path}")

    except ValueError as e:
        print(f"\n입력 오류: {e}")
    except Exception as e:
        print(f"\n처리 오류: {e}")


if __name__ == "__main__":
    main()
