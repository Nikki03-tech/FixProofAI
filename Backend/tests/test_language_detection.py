from Backend.services.language_detection import detect_language


def test_detects_python_source():
    code = "def greet(name):\n    print('hello', name)\n"
    assert detect_language(code) == "python"


def test_detects_javascript_source():
    code = "const greet = (name) => {\n  console.log(name);\n};"
    assert detect_language(code) == "javascript"


def test_ambiguous_code_does_not_trigger_language_warning():
    assert detect_language("result = value") is None
