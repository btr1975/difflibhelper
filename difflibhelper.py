#!/usr/bin/env python3
import logging
import difflib
import itertools
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = ''
__version__ = '1.0.0'
__version_info__ = tuple([int(num) for num in __version__.split('.')])
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'
__status__ = 'Development'
LOGGER = logging.getLogger(__name__)
GLOBAL_LINE_NUMBER_FORMAT = '%04d'


def list_of_diffs_pre_post(pre_list, post_list, pre_list_file_name=None, post_list_file_name=None):
    """
    Function to take a pre_list, and a post_list, and diff them with real line numbers
    :param pre_list:
    :param post_list:
    :param pre_list_file_name: The name of the pre file
    :param post_list_file_name: The name of the post file name
    :return:
        pre_list_diff, post_list_diff, combined_list_diff
    """
    LOGGER.debug('Starting Function list_of_diffs_pre_post')
    combined_list_diff = list()
    pre_list_diff = list()
    post_list_diff = list()
    line_number_fix = None
    line_number_pre_fix = None
    line_number_post_fix = None

    # Creates a pre file diff

    differ = difflib.Differ()
    diffs = differ.compare(pre_list, post_list)
    line_number = 0

    pre_list_diff.append('------------- PRE FILE LINES DIFFERENT FROM POST -------------\n')

    if pre_list_file_name:
        pre_list_diff.append('CHANGES IN PRE FILE {file_name}'.format(file_name=pre_list_file_name))

    else:
        pre_list_diff.append('PRE LINES')

    for line in diffs:
        # split off "  ", "+ ", "- "
        add_subtract_same_code = line[:2]
        # if the line is in pre and post files or just pre, increment the line number.
        if add_subtract_same_code in ("  ", "- "):
            line_number += 1
            line_number_fix = GLOBAL_LINE_NUMBER_FORMAT % (line_number,)
        # if the line is only in pre, print the line number and the text on the line
        if add_subtract_same_code == "- ":
            pre_list_diff.append("{} {}".format(line_number_fix, line[2:].strip()))

    pre_list_diff.append('\n')

    # Creates a post file diff

    differ = difflib.Differ()
    diffs = differ.compare(pre_list, post_list)
    line_number = 0

    post_list_diff.append('------------- POST FILE LINES DIFFERENT FROM PRE -------------\n')

    if post_list_file_name:
        post_list_diff.append('CHANGES IN POST FILE {file_name}'.format(file_name=post_list_file_name))

    else:
        post_list_diff.append('POST LINES')

    for line in diffs:
        # split off "  ", "+ ", "- "
        add_subtract_same_code = line[:2]
        # if the line is in pre and post files or just post, increment the line number.
        if add_subtract_same_code in ("  ", "+ "):
            line_number += 1
            line_number_fix = GLOBAL_LINE_NUMBER_FORMAT % (line_number,)
        # if the line is only in post, print the line number and the text on the line
        if add_subtract_same_code == "+ ":
            post_list_diff.append("{} {}".format(line_number_fix, line[2:].strip()))

    post_list_diff.append('\n')

    # Creates a combined diff

    differ = difflib.Differ()
    diffs = differ.compare(pre_list, post_list)
    line_number_pre = 0
    line_number_post = 0

    combined_list_diff.append('------------- PRE AND POST COMBINED DIFF -------------\n')

    if pre_list_file_name and post_list_file_name:
        combined_list_diff.append('< - = {pre_file_name}, + = '
                                  '{post_file_name} >'.format(pre_file_name=pre_list_file_name,
                                                              post_file_name=post_list_file_name))

    else:
        combined_list_diff.append('< - = PRE, + = POST >')

    for line in diffs:
        # split off "  ", "+ ", "- "
        add_subtract_same_code = line[:2]

        # if the line is in pre and post files or just pre, increment the line number.
        if add_subtract_same_code in ("  ", "- "):
            line_number_pre += 1
            line_number_pre_fix = GLOBAL_LINE_NUMBER_FORMAT % (line_number_pre,)

        # if the line is in pre and post files or just post, increment the line number.
        if add_subtract_same_code in ("  ", "+ "):
            line_number_post += 1
            line_number_post_fix = GLOBAL_LINE_NUMBER_FORMAT % (line_number_post,)

        # if the line is only in pre, print the line number and the text on the line
        if add_subtract_same_code == "- ":
            combined_list_diff.append("-{} {}".format(line_number_pre_fix, line[2:].strip()))

        # if the line is only in post, print the line number and the text on the line
        if add_subtract_same_code == "+ ":
            combined_list_diff.append("+{} {}".format(line_number_post_fix, line[2:].strip()))

    combined_list_diff.append('\n')

    return pre_list_diff, post_list_diff, combined_list_diff


def list_with_line_numbers(orig_list):
    """
    Function to add line numbers to a list
    :param orig_list:
    :return:
        A List
    """
    LOGGER.debug('Starting Function list_with_line_numbers')
    temp_list = list()
    for index, line in enumerate(orig_list):
        line_num = GLOBAL_LINE_NUMBER_FORMAT % (index + 1,)
        temp_list.append('{line_num} {line_data}'.format(line_num=line_num, line_data=line))

    return temp_list


def extract_just_line_number(orig_list):
    """
    Function to get only a list of changed line numbers
    :param orig_list:
    :return:
        A List

    """
    LOGGER.debug('Starting Function extract_just_line_number')
    temp_list = list()
    for line in orig_list:
        if line[:4] == '----':
            continue

        elif line[:4] in ('PRE ', 'POST'):
            continue

        elif line[:4] == '\n':
            continue

        temp_list.append(line[:4])

    return temp_list


def get_a_csv_diff(pre_list, post_list, pre_list_file_name=None, post_list_file_name=None):
    """
    Function to build a csv of pre and post files
    :param pre_list:
    :param post_list:
    :param pre_list_file_name:
    :param post_list_file_name:
    :return:
        A CSV formatted list

    """
    LOGGER.debug('Starting Function get_a_csv_diff')
    temp_csv_list = list()

    numbered_orig_pre_list = list_with_line_numbers(pre_list)
    numbered_orig_post_list = list_with_line_numbers(post_list)
    pre_list_diff, post_list_diff, *garbage = list_of_diffs_pre_post(pre_list, post_list, pre_list_file_name,
                                                                     post_list_file_name)

    pre_line_changes = extract_just_line_number(pre_list_diff)

    post_line_changes =  extract_just_line_number(post_list_diff)

    temp_csv_list.append('CHANGE_PRE,CHANGE_PRE_LINE_NUMBER,CHANGE_PRE_LINE_DATA,CHANGE_POST,CHANGE_POST_LINE_NUMBER,CHANGE_POST_LINE_DATA')

    for line_numbered_orig_pre_list, line_numbered_orig_post_list in itertools.zip_longest(numbered_orig_pre_list, numbered_orig_post_list):
        try:
            if line_numbered_orig_pre_list[:4] not in pre_line_changes and line_numbered_orig_post_list[:4] not in post_line_changes:
                temp_csv_list.append(',"{pre_line}","{pre_line_data}",,"{post_line}","{post_line_data}"'.format(
                    pre_line=line_numbered_orig_pre_list[:4], pre_line_data=line_numbered_orig_pre_list[5:],
                    post_line=line_numbered_orig_post_list[:4], post_line_data=line_numbered_orig_post_list[5:]))

            elif line_numbered_orig_pre_list[:4] in pre_line_changes and line_numbered_orig_post_list[:4] in post_line_changes:
                temp_csv_list.append('changed,"{pre_line}","{pre_line_data}",changed,"{post_line}","{post_line_data}"'.format(
                    pre_line=line_numbered_orig_pre_list[:4], pre_line_data=line_numbered_orig_pre_list[5:],
                    post_line=line_numbered_orig_post_list[:4], post_line_data=line_numbered_orig_post_list[5:]))

            try:
                line_numbered_orig_pre_list[:4]

            except TypeError as e:
                LOGGER.warning('Function get_a_csv_diff error with pre_list not able to get numbers {e}'.format(e=e))
                temp_csv_list.append('changed,,,changed,"{post_line}","{post_line_data}"'.format(
                    post_line=line_numbered_orig_post_list[:4], post_line_data=line_numbered_orig_post_list[5:]))

            try:
                line_numbered_orig_post_list[:4]

            except TypeError as e:
                LOGGER.warning('Function get_a_csv_diff error with post_list not able to get numbers {e}'.format(e=e))
                temp_csv_list.append('changed,"{pre_line}","{pre_line_data}",changed,,'.format(
                    pre_line=line_numbered_orig_pre_list[:4], pre_line_data=line_numbered_orig_pre_list[5:]))

        except TypeError as e:
            LOGGER.warning('Function get_a_csv_diff error {e}'.format(e=e))


    return temp_csv_list



