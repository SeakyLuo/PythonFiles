maxSize = 25
maxRandomVarLength = 10
columnLabelWidth = 1

defaultVar = 'x'

MATRIX, DETERMINANT, VECTOR, IDENTITY_MATRIX = 'Matrix', 'Determinant', 'Vector', 'Identity Matrix'
resultTypeOptions = [MATRIX, DETERMINANT, VECTOR]
LATEX, ARRAY = 'LaTeX', 'Array'
resultFormatOptions = [LATEX, ARRAY]
ROW = 'Row'
COL = 'Column'
ROWS = 'Rows'
COLS = 'Columns'
LEFT, RIGHT, UP, DOWN = 'Left', 'Right', 'Up', 'Down'
directions = [LEFT, RIGHT, UP, DOWN]
CLEAR_ZEROS, CLEAR_ENTRIES, CLEAR_ALL = 'Clear Zeros', 'Clear Entries', 'Clear All'
NONE = 'None'
clearOptions = [CLEAR_ENTRIES, CLEAR_ALL, NONE]
GENERATE_CLEAR_OPTION = 'GenerateClearOption'
CALCULATE_CLEAR_OPTION = 'CalculateClearOption'
VECTOR_OPTION = 'VectorOption'
ARRAY_VECTOR = 'ArrayVector'
COLUMN_VECTOR, OVERRIGHTARROW = 'Column Vector', 'OverRightArrow'
vectorOptions = [COLUMN_VECTOR, OVERRIGHTARROW,  VECTOR]
ARRAY_OPTION = 'ArrayOption'
NORMAL_ARRAY, NUMPY_ARRAY, NP_ARRAY = 'Normal Array', 'Numpy Array', 'Np Array'
arrayOptions = [NORMAL_ARRAY, NUMPY_ARRAY, NP_ARRAY]
REMEMBER_SIZE = 'RememberSize'
SHOW_RESULT = 'Show Result'
SHOW_CALCULATION_RESULT = 'ShowCalculationResult'
SHOW_GENERATION_RESULT = 'ShowGenerationResult'
COPY_RESULT = 'Copy Result'
COPY_CALCULATION_RESULT = 'CopyCalculationResult'
COPY_GENERATION_RESULT = 'CopyGenerationResult'
RESULT_TYPE = 'ResultType'
RESULT_FORMAT = 'ResultFormat'
ZERO_MATRIX = 'Zero Matrix'
APPEND_START = 'Append Start'
APPEND_END = 'Append End'
APPEND_INDEX = 'Append Index'
FIND_VALUE = 'Find Value'
FIND_LOCATION = 'Find Location'
REPLACE = 'Replace'
CALCULATE = 'Calculate'
UNIT_MATRIX = 'Unit Matrix'
PERMUTATION_MATRIX = 'Permutation Matrix'
PERMUTATION_VECTOR = 'Permutation Vector'
ADD = 'Add'
MULTIPLY = 'Multiply'
TRANSPOSE = 'Transpose'
RANDOM = 'Random'
RANDOM_MATRIX = 'Random Matrix'
RANDOM_REORDER = 'Random Reorder'
RANDOM_INT_MATRIX = 'Random Int Matrix'
RANDOM_VAR_MATRIX = 'Random Var Matrix'
RANDOM_MULTIVAR_MATRIX = 'Random Multi-Var Matrix'
RANDOM_MATRIX_OPTION = 'RandomMatrixOption'
randomMatrixOptions = [RANDOM_INT_MATRIX, RANDOM_VAR_MATRIX, RANDOM_MULTIVAR_MATRIX]
RANDOM_MIN = 'RandomMin'
RANDOM_MAX = 'RandomMax'
RANDOM_VAR = 'RandomVar'
GENERATE = 'Generate'
UNDO = 'Undo'
REDO = 'Redo'
SORT = 'Sort'
REVERSE = 'Reverse'
RESHAPE = 'Reshape'
LOWER = 'Lower'
UPPER = 'Upper'
LOWER_TRIANGULAR = 'Lower Triangular'
UPPER_TRIANGULAR = 'Upper Triangular'
ONE_TO_N = '1 to N'
A_TO_Z = 'A to Z'
FROM_ARRAY = 'From ' + ARRAY
FROM_LATEX = 'From ' + LATEX
EXIT = 'Exit'
ENTRY_WIDTH = 'EntryWidth'
NEWLINE_ENDING = 'Newline Row Ending'
LATEX_NEWLINE = 'LaTexNewline'
ARRAY_NEWLINE = 'ArrayNewline'
UNKNOWN_MATRIX = 'UnknownMatrix'
SWITCH_ROWS = 'Switch Rows'
SWITCH_COLUMNS = 'Switch Columns'
FILL_ROW = 'Fill Rows'
FILL_COLUMN = 'Fill Columns'
PERMUTATION_VECTOR_TO_MATRIX = 'Permutation Vector To Matrix'
PERMUTATION_MATRIX_TO_VECTOR = 'Permutation Matrix To Vector'
LATEX_OPTION = 'LatexOption'
SQUARE_BRACKET = 'Square Bracket'
PARENTHESE = 'Parentheses'
UNIQUE_RANDOM = 'UniqueRandom'
ALL = 'All'

## Settings
settingOptions = [RESULT_TYPE, RESULT_FORMAT, REMEMBER_SIZE, VECTOR_OPTION, RANDOM_VAR, RANDOM_MIN, RANDOM_MAX, RANDOM_MATRIX_OPTION, ENTRY_WIDTH, \
                  SHOW_GENERATION_RESULT, SHOW_CALCULATION_RESULT, COPY_GENERATION_RESULT, COPY_CALCULATION_RESULT, GENERATE_CLEAR_OPTION, CALCULATE_CLEAR_OPTION, \
                  ARRAY_VECTOR, LATEX_NEWLINE, ARRAY_NEWLINE, ARRAY_OPTION, UNKNOWN_MATRIX]

## Shortcuts
shortcuts = { GENERATE: 'Enter/Return', ADD: 'Ctrl+=', ZERO_MATRIX: 'Ctrl+0', IDENTITY_MATRIX: 'Ctrl+I', RANDOM_MATRIX: 'Ctrl+R', UNIT_MATRIX: 'Ctrl+U', EXIT: 'Ctrl+W', \
              MULTIPLY: 'Ctrl+M', PERMUTATION_MATRIX: 'Ctrl+P', PERMUTATION_VECTOR: 'Ctrl+P', FIND_VALUE: 'Ctrl+F', REPLACE: 'Ctrl+H', REDO: 'Ctrl+Y', UNDO: 'Ctrl+Z', \
              CLEAR_ALL: 'Ctrl+Shift+A', CALCULATE: 'Ctrl+Shift+C', CLEAR_ENTRIES: 'Ctrl+Shift+E', FIND_LOCATION: 'Ctrl+Shift+F', LOWER_TRIANGULAR: 'Ctrl+Shift+L', PERMUTATION_MATRIX_TO_VECTOR: 'Ctrl+Shift+P', PERMUTATION_VECTOR_TO_MATRIX: 'Ctrl+Shift+P', RANDOM_REORDER: 'Ctrl+Shift+R', UPPER_TRIANGULAR: 'Ctrl+Shift+U', CLEAR_ZEROS: 'Ctrl+Shift+Z', \
              A_TO_Z: 'Alt+A', SWITCH_COLUMNS: 'Alt+C',APPEND_END: 'Alt+E', APPEND_INDEX: 'Alt+I', ONE_TO_N: 'Alt+N', SWITCH_ROWS: 'Alt+R', APPEND_START: 'Alt+S', TRANSPOSE: 'Alt+T', \
              FROM_ARRAY: 'Alt+Shift+A', FILL_COLUMN: 'Alt+Shift+C', FROM_LATEX: 'Alt+Shift+L', FILL_ROW: 'Alt+Shift+R'}
otherShortcutFormatter = lambda command, shortcut: '{:<25}{:<15}'.format(command, shortcut)
otherShortcuts = '\n'.join([otherShortcutFormatter(command, shortcut) for command, shortcut in \
                           [('Switch Result Type', 'Ctrl+[ Ctrl+]'), ('Switch Result Format', 'Alt+[ Alt+]'), ('Exit', 'Ctrl+W')]])
