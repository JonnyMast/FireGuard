# Running the Backend

1. Create a `.env` file in the root directory with your Supabase credentials:
    * See .env requirements

2. Navigate to `Backend` folder -> Install the required dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Run the following command:
    ```sh
    poetry run python run.py
    ```


# .env requirements

## Database info
SUPABASE_URL=

SUPABASE_KEY=

## JWT master key
JWT_SECRET=




# General Info

## Python Package Structure

    The project is structured as a Python package, where different directories (folders) contain `__init__.py` files. These files mark the directories as Python packages, which enables importing modules from them.

### About `__init__.py` Files

    - These files are intentionally left empty as per standard (best) practice
    - They should not be removed as they are important for the Python package system to work correctly
    - They allow Python to recognize directories as packages, enabling imports like `from directory_name import module_name`
