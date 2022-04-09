import glob


def test_glob():
    for name in glob.glob('*/*.txt'):
        path = name

    expectedOutput = "project1/common_names.txt"

    assert path == expectedOutput

    
    
