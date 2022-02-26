from thonny.assistance import SubprocessProgramAnalyzer, add_program_analyzer
from thonny import ui_utils, get_workbench
import subprocess
import logging
import re


def processFlakeOutput(line):
    regexForSplitting = (
        r"(?P<filename>.*?)\:(?P<line>\d+)\:"
        + r"(?P<col>\d+)\: (?P<explanation>.\d+ .*)"
    )
    matches = re.match(regexForSplitting, line)
    return (
        matches.group("filename"),
        matches.group("line"),
        matches.group("col"),
        matches.group("explanation"),
    )


def getCurrentFile():
    thonnyEditor = get_workbench().get_editor_notebook().get_current_editor()
    if thonnyEditor is None:
        return None
    else:
        return thonnyEditor.get_filename()


class flake8Analyzer(SubprocessProgramAnalyzer):
    def is_enabled(self):
        return get_workbench().get_option("assistance.use_flake8")

    def start_analysis(self, main_file_path, imported_file_paths):

        self._proc = ui_utils.popen_with_ui_thread_callback(
            ["flake8"] + [main_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            on_completion=self._parse_and_output_warnings,
        )

    def _parse_and_output_warnings(self, _, out_lines, err_lines):
        warnings = []
        for error in err_lines:
            logging.getLogger("thonny").error("Flake8: " + error)

        for line in out_lines:
            file, line, col, explanation = processFlakeOutput(line.strip())
            atts = {}
            atts["explanation"] = explanation
            atts["explanation_rst"] = explanation
            atts["filename"] = file
            atts["lineno"] = int(line)
            atts["col_offset"] = int(col)
            atts["msg"] = explanation

            warnings.append(atts)

        self.completion_handler(self, warnings)


def load_plugin():
    add_program_analyzer(flake8Analyzer)
