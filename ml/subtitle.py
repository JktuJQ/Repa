import whisper
from datetime import timedelta

MODEL_TYPE = "medium"
whisper_model = None


def format_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def gen_subtitles(input_path, output_file):
    ##############################################################
    # DELETE IN PROD 
    whisper_model = whisper.load_model("medium")
    ###############################################################
    result = whisper_model.transcribe(input_path, word_timestamps=True)
    with open(output_file, "w", encoding="utf-8") as f:
        counter = 1
        for segment in result["segments"]:
            for word in segment["words"]:
                start = format_time(word["start"])
                end = format_time(word["end"])
                f.write(f"{counter}\n{start} --> {end}\n{word['word'].strip()}\n\n")
                counter += 1

if __name__ == "__main__":
    whisper_model = whisper.load_model(MODEL_TYPE)
