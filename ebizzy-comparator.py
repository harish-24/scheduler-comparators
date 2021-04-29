import os
import json
import sys
import glob


def file_to_dict(json_file):
    with open(json_file) as js_file:
        return json.load(js_file)


def compare(baseline, test):
    ret = {}
    baseline_dict = file_to_dict(baseline)
    test_dict = file_to_dict(test)
    for key in baseline_dict.keys():
        baseline_val = baseline_dict[key]
        test_val = test_dict[key]
        diff = float(test_val) - float(baseline_val)
        pct = 0.0
        if baseline_val != 0:
            pct = float(diff)*100/float(baseline_val)
        ret[key] = pct
    return ret


def get_file_list(folder):
    return glob.glob(folder + "/*")


def compare_folders(base_folder, test_folder):
    results = []
    for file1, file2 in zip(base_file_list, test_file_list):
        results.append(compare(file1, file2))
    return results


def usage():
    print("Usage: python ebizzy-comparator.py <baseline-folder/file> <test-folder/file>")


def print_comparison(baseline_dict, test_dict, result_dict):
    for key in baseline_dict.keys():
        bops = float(baseline_dict[key])
        tops = float(test_dict[key])
        pct = result_dict[key]

        print("{:20s} {:20f} {:20f} {:20f}".format(key, bops, tops, pct))


if __name__ == "__main__":
    nr_args = len(sys.argv)
    if nr_args < 3:
        usage()
        exit()
    baseline = sys.argv[1]
    test = sys.argv[2]
    result_list = []
    base_file_list = []
    test_file_list = []

    if os.path.isfile(baseline):
        base_file_list.append(baseline)
        test_file_list.append(test)
        result_list.append(compare(baseline, test))
    else:
        base_file_list = get_file_list(baseline)
        test_file_list = get_file_list(test)
        result_list = compare_folders(base_file_list, test_file_list)

    for ite, result_dict in enumerate(result_list):
        baseline_dict = file_to_dict(base_file_list[ite])
        test_dict = file_to_dict(test_file_list[ite])
        print("Iteration %s" % (ite + 1))
        print("{:25s} {:25s} {:25s} {:20s}".format("Fields", "Baseline", "Test", "Pct diff"))
        print("-------------------------------------------------------------------------------------")
        print_comparison(baseline_dict, test_dict, result_dict)
        print("-------------------------------------------------------------------------------------")
        print("\n")
