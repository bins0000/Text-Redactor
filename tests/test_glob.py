import glob


def test_glob():
    for name in glob.glob('*/*.txt'):
        path = name

    expectedOutputInTests = "project1/common_names.txt"
    expectedOutputInRoot = "docs/common_names.txt"

    assert path == expectedOutputInTests or path == expectedOutputInRoot

    
    
