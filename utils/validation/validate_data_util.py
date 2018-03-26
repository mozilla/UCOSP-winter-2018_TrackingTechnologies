import re

from urllib.parse import urlparse

class SchemaDataValidator:
    """Facilitates checking if s3 json objects are valid and
    storing error messages when those json objects are invalid.
    """
    # crawl_id should always be 1 for our current crawl data.
    EXPECTED_CRAWL_ID = 1

    def __init__(self):
        """Initializes private variables for the class."""
        self._error_message = ""

        # Increase performance by only compiling regular expressions
        # once and then storing them as private class variables.
        self._call_stack_row_and_col_regex = re.compile(":[0-9]*:[0-9]*$")
        self._call_stack_at_sign_regex = re.compile("([^@])*(@)")
        self._script_loc_eval_format_regex = re.compile("^(line [0-9]* > (eval|Function)[ ]?)*$")
        self._time_stamp_format = re.compile("^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z$")

    def get_error_message(self):
        """Returns the error message string."""
        return self._error_message

    def reset_error_message(self):
        """Resets the error message to the empty string."""
        self._error_message = ""

    def is_valid_schema_data(self, data_frame):
        """Checks a pandas object, generated from a s3 json file, for validity.
        If the pandas object is invalid then the error message property is set
        and can be checked to get a description of specifically what portion of
        the schema object is invalid.
        Keyword arguments:
        data_frame -- a pandas data frame that contains s3 json data from a single file.
        """
        if not self._is_call_stack_valid(data_frame.call_stack):
            return False
        if not self._is_crawl_id_valid(data_frame.crawl_id):
            return False
        if not self._is_func_name_valid(data_frame.func_name):
            return False
        if not self._is_in_iframe_valid(data_frame.in_iframe):
            return False
        if not self._is_location_valid(data_frame.location):
            return False
        if not self._is_operation_valid(data_frame.operation):
            return False
        if not self._is_script_col_valid(data_frame.script_col):
            return False
        if not self._is_script_line_valid(data_frame.script_line):
            return False
        if not self._is_script_loc_eval_valid(data_frame.script_loc_eval):
            return False
        if not self._is_script_url_valid(data_frame.script_url):
            return False
        if not self._is_symbol_valid(data_frame.symbol):
            return False
        if not self._is_time_stamp_valid(data_frame.time_stamp):
            return False
        # since arguments and value can be any value, including an empty string, we do not validate them.

        return True

    def _is_call_stack_valid(self, call_stack_series):
        """Checks if all of the call_stack rows are valid call stacks for a single s3 json object.
        Keyword arguments:
        call_stack_series -- Pandas Series object containing all of the call_stack values for a single s3 json object.
        """
        for call_stack in call_stack_series:
            # some call_stacks are empty, which is expected.
            if len(call_stack) == 0:
                continue

            # Javascripts stacks property of the Error object will sometimes
            # return undefined. This is why some of the call stacks values
            # are undefined instead of emtpy.
            #
            # Since this was not an expected value for the call_stack in
            # the crawler we mark the call stack as having an error.
            # This comment in the crawler's codebase mentions what the
            # crawler's authors expected the call stack values format to be:
            # https://github.com/groovecoder/data-leak/blob/master/src/content.js#L195
            if call_stack == "undefined":
                self._error_message = "call stack value is 'undefined'."
                return False

            # To simplify the analysis, we split the entire call stack into
            # seperate frames. This is possible since each frame on the
            # call stack is seperated by the \n character.
            call_stack_frames = re.split('\n', call_stack)

            for call_stack_frame in call_stack_frames:
                # check to make sure that each frame on the call stack ends
                # with a line number and column number, seperated by colons.
                row_and_column_at_end_of_frame = self._call_stack_row_and_col_regex.search(call_stack_frame)

                # If we cannot find the end of line information then the
                # call stack frame is invalid.
                if not row_and_column_at_end_of_frame:
                    self._error_message = "Invalid call stack format: row and column information was not present at the end of a call stack frame."
                    return False

                # check to make sure that each call stack frame
                # has the @ symbol before the url section.
                at_sign_at_start_of_frame = self._call_stack_at_sign_regex.match(call_stack_frame)

                if not at_sign_at_start_of_frame:
                    self._error_message = "Invalid call stack format: @ sign was not present in the middle of a call stack frame."
                    return False

                # given that the URL section can contain almost any characters,
                # we do not check it for validity.

        return True

    def _is_crawl_id_valid(self, crawl_id_series):
        """Checks if all of the crawl_id rows are valid crawl id's for a single s3 json object.
        crawl_id_series -- Pandas Series object containing all of the crawl_id values for a single s3 json object.
        """
        for crawl_id in crawl_id_series:
            if crawl_id != SchemaDataValidator.EXPECTED_CRAWL_ID:
                self._error_message = (
                    "Invalid crawl id. crawl_id = (" + str(crawl_id) + ") when it should be (" +
                    str(SchemaDataValidator.EXPECTED_CRAWL_ID) + ")."
                )
                return False

        return True

    def _is_func_name_valid(self, func_name_series):
        """Checks if all of the func_name rows are valid function names for a single s3 json object.
        func_name_series -- Pandas Series object containing all of the func_name values for a single s3 json object.
        """
        for func_name in func_name_series:
            # function names cannot start with numbers.
            if len(func_name) > 0 and func_name[0].isdigit():
                self._error_message = "Invalid function name: Function name starts with a number '" + func_name + "'."
                return False

        return True

    def _is_in_iframe_valid(self, in_iframe_series):
        """Checks if all of the in_iframe rows are boolean values for a single s3 json object.
        in_iframe_series -- Pandas Series object containing all of the in_iframe values for a single s3 json object.
        """
        for in_iframe in in_iframe_series:
            if not isinstance(in_iframe, bool):
                self._error_message = "Invalid in_iframe type: in_iframe should be a boolean value, but it was " + str(type(in_iframe)) + "."
                return False

        return True

    def _is_location_valid(self, location_series):
        """Checks if all of the location rows are valid urls for a single s3 json object.
        location_series -- Pandas Series object containing all of the location values for a single s3 json object.
        """
        valid_url_schemes = ['https', 'http']

        for location in location_series:
            parsed_url = urlparse(location)

            # if the url scheme is not http or https, and the 
            # network location is empty then the url is invalid.
            if parsed_url.scheme not in valid_url_schemes or not parsed_url.netloc:
                self._error_message = "Location url is invalid '" + location + "'."
                return False

        return True

    def _is_operation_valid(self, operation_series):
        """Checks if all of the operation values are one of the valid operation values for a single s3 json object.
        operation_series -- Pandas Series object containing all of the operation values for a single s3 json object.
        """
        valid_operations = ['get', 'call', 'set']

        for operation in operation_series:
            if operation not in valid_operations:
                self._error_message = "Invalid operator value: Received '" + operation + "' when the only valid values are " + str(valid_operations) + "."
                return False

        return True

    def _is_script_col_valid(self, script_col_series):
        """Check if all of the script_col values are positive integers for a single s3 json object.
        script_col_series -- Pandas Series object containing all of the script_col values for a single s3 json object.
        """
        # check if all the values in the series are integers.
        if script_col_series.dtype.kind not in 'i':
            # If all the values are not integers then the format is incorrect.
            # we then locate a script_col whos value is not an integer in order to
            # generate an error message.
            for script_col in script_col_series:
                if not script_col.isdigit():
                    self._error_message = "script_col is '" + script_col + "' when it should be a number."
                    return False

        return True

    def _is_script_line_valid(self, script_line_series):
        """Check if all of the script_line values are positive integers for a single s3 json object.
        script_line_series -- Pandas Series object containing all of the script_line values for a single s3 json object.
        """
        # check if all the values in the series are integers.
        if script_line_series.dtype.kind not in 'i':
            # If all the values are not integers then the format is incorrect.
            # we then locate a script_line whos value is not an integer in order to
            # generate an error message.
            for script_line in script_line_series:
                if not script_line.isdigit():
                    self._error_message = "script_line is '" + script_line + "' when it should be a number."
                    return False

        return True

    def _is_script_loc_eval_valid(self, script_loc_eval_series):
        """Check if all of the script_loc_eval values are properly formatted for a single s3 json object.
        script_loc_eval_series -- Pandas Series object containing all of the script_loc_eval values for a single s3 json object.
        """
        for script_loc_eval in script_loc_eval_series:
            match = self._script_loc_eval_format_regex.match(script_loc_eval)
            if not match:
                self._error_message = "script_loc_eval is '" + script_loc_eval + "' which is not in the correct format."
                return False

        return True

    def _is_script_url_valid(self, script_url_series):
        """Checks if all of the script_url values are valid urls for a single s3 json object.
        script_url_series -- Pandas Series object containing all of the script_url values for a single s3 json object.
        """
        for script_url in script_url_series:
            # script_url can be any string, so we only
            # check to make sure the script_url is not empty.
            if not script_url:
                self._error_message = "script_url is empty."
                return False

        return True

    def _is_symbol_valid(self, symbol_series):
        """Checks if all of the symbol values are not empty for a single s3 json object.
        symbol_series -- Pandas Series object containing all of the symobl values for a single s3 json object.
        """
        for symbol in symbol_series:
            # Given the number of possible symbols, we do not
            # check to make sure the symbol is one of these values.
            # We simply check to make sure the symbol is not empty.
            if not symbol:
                self._error_message = "symbol is empty."
                return False

        return True

    def _is_time_stamp_valid(self, time_stamp_series):
        """Checks if all of the time_stamp values are valid time stamps for a single s3 json object.
        time_stamp_series -- Pandas Series object containing all of the time_stamp values for a single s3 json object.
        """
        for time_stamp in time_stamp_series:
            if not self._time_stamp_format.match(time_stamp):
                self._error_message = "time_stamp format is invalid '" + time_stamp + "'."
                return False

        return True

