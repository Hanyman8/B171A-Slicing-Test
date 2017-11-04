import pathlib


def report_feature(solution_stats, student_stats):
    ret = []
    flag = True

    for line1, line2 in zip(solution_stats, student_stats):
        if line1 != line2:
            line1 = line1.strip()
            line2 = line2.strip()
            ret.append(f'"{line2.rstrip()}" (should have been "{line1}") :warning:\n')
            flag = False

    return flag, ret


def format_gcode(gcode_name):
    input = open(gcode_name, "r")

    ret = []

    for i, line in enumerate(input):
        # I don't want first line - info when was gcode generated
        if i == 0:
            continue
        if line.startswith(";"):
            ret.append(line)

    return ret


def test(student_repo_path, solution_repo_path, **kwargs):
    good = True
    messages = []

    for gcode in solution_repo_path.glob('*.gcode'):
        messages.append(f'### {gcode.name}')
        messages.append('')

        solution_stats = format_gcode(gcode)
        student_stats = format_gcode(student_repo_path / gcode.name)

        #print(solution_stats)

        status, msg = report_feature(solution_stats, student_stats)
        if not status:
            messages.append(f' * {msg}')
        else:
            messages.append(f'Everything OK')

        good = good and status

    return {
        'title': 'Mesh statistics',
        'markdowns': messages,
        'labels': ['success' if good else 'failure'],
        'exitcode': int(not good),
    }


# MIROS HACKING (to be removed):

if __name__ == '__main__':
    import pprint

    student = pathlib.Path('../B171A-Slicing-hanusji8')
    solution = pathlib.Path('../B171A-Slicing-Solution')
    pprint.pprint(test(student_repo_path=student, solution_repo_path=solution,
                       student_repo_commit='xxxx'))
