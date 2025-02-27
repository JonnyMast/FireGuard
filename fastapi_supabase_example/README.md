# FastAPI Supabase Example

This project uses FastAPI to connect to our Supabase.

## Running the Project

1. Navigate to the `fastapi_supabase_example` folder:
    ```sh
    cd ././fastapi_supabase_example
    ```

2. Run the following command:
    ```sh
    poetry run python run.py
    ```


    # Python Package Structure

    The project is structured as a Python package, where different directories (folders) contain `__init__.py` files. These files mark the directories as Python packages, which enables importing modules from them.

    ## About `__init__.py` Files

    - These files are intentionally left empty as per standard (best) practice
    - They should not be removed as they are important for the Python package system to work correctly
    - They allow Python to recognize directories as packages, enabling imports like `from directory_name import module_name`