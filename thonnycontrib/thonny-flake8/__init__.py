#!/bin/env python3
"""Thonny-flake8, adds flake8 warnings to Thonny"""
import logging
import re
import subprocess

from thonny import get_workbench, ui_utils
from thonny.assistance import SubprocessProgramAnalyzer, add_program_analyzer


def processFlakeOutput(line):
    """Breaks output of the flake8 command into filename, line, col, and explanation"""
    regexForSplitting = (
        r"(?P<filename>.*?)\:(?P<line>\d+)\:"
        + r"(?P<col>\d+)\: (?P<id>.\d+) (?P<explanation>.*)"
    )
    matches = re.match(regexForSplitting, line)
    return (
        matches.group("filename"),
        matches.group("line"),
        matches.group("col"),
        matches.group("id"),
        matches.group("explanation"),
    )


class Flake8Analyzer(SubprocessProgramAnalyzer):
    """The analyzer itself"""

    def is_enabled(self):
        """Returns if the user has the option enabled"""
        enabled = get_workbench().get_option("assistance.use_flake8")
        if enabled == None:
            enabled = True
        return enabled

    def start_analysis(self, main_file_path, imported_file_paths):
        """Runs flake8 on the currently open file."""
        self._proc = ui_utils.popen_with_ui_thread_callback(
            ["flake8"] + [main_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            on_completion=self._parse_and_output_warnings,
        )

    def _parse_and_output_warnings(self, _, out_lines, err_lines):
        """Parses the flake8 output and sends it to thonny"""
        warnings = []
        for error in err_lines:
            logging.getLogger("thonny").error("Flake8: %s", error)

        for line in out_lines:
            file, line, col, warnId, explanation = processFlakeOutput(line.strip())
            if warnId.strip() != "F401":
                # Ignores F401 because Thonny handles already unused imports.
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
    """Adds the Flake8 analyzer"""
    add_program_analyzer(Flake8Analyzer)
