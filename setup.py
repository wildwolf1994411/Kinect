import cx_Freeze


executables = [cx_Freeze.Executable("test.py")]



cx_Freeze.setup(
    name="analysis tool",
    version = "0.1",
    author = 'An-Ti Chaing',
    options={"build_exe": {"packages":["Tkinter","tkFileDialog","openpyxl",
                           "pandas"],
                           "excludes": ["collections.abc"]},
                           
                           },
    executables = executables

    )