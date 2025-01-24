import re
import json
import boto3
from app import app
from openai import OpenAI


AWS_REGION = 'us-west-2'
s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
)


textract = boto3.client('textract',
                        aws_access_key_id=app.config['S3_KEY'],
                        aws_secret_access_key=app.config['S3_SECRET'],
                        region_name=AWS_REGION)


def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)


def read_text_from_file(filename):
    """Reads text from a file on disk.

    Args:
        filename: The path to the file.

    Returns:
        The text content of the file, or None if an error occurs.
    """
    try:
        with open(filename, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


def write_text_to_file(text, filename):
    """Writes the given text to a file with the specified filename.

    Args:
        text: The text to write to the file.
        filename: The name of the file to create or overwrite.
    """
    try:
        with open(filename, 'w') as file:
            file.write(text)
        print(f"Text successfully written to '{filename}'")
    except Exception as e:
        print(f"An error occurred: {e}")


def python_object_to_json_file(python_object, filename):
    """Converts a Python object to JSON and writes it to a file.

    Args:
        python_object: The Python object to convert.
        filename: The name of the file to write the JSON data to.
    """
    try:
        with open(filename, 'w') as f:
            # Use indent for pretty printing
            json.dump(python_object, f, indent=4)
        print(f"JSON data written to '{filename}' successfully.")
    except (TypeError, OverflowError) as e:
        print(f"Error converting object to JSON: {e}")
    except OSError as e:
        print(f"Error writing to file: {e}")


def get_chat_completion(system_prompt, user_prompt):
    """
    Generates a chat completion using the OpenAI API.

    Args:
        system_prompt: The system-level instructions for the chat model.
        user_prompt: The user's message to the chat model.

    Returns:
        The chat model's response as a string.
        Returns an error message if the API call fails.
    """

    try:
        client = OpenAI(api_key="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")

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        print(completion.choices[0].message)
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


system_prompt = """
### Prompt:

"I have a JSON string that is invalid because it doesn't follow standard JSON formatting rules (e.g., it uses single quotes instead of double quotes, has trailing commas, or other minor issues). Please correct the JSON string to make it valid and return **only** the fixed JSON wrapped in triple backticks. Do not include any explanation or additional text in your response.

Here is the malformed JSON:

```
{'key': 'value', 'anotherKey': 123,}
```

Return only the corrected JSON."

---

### Expected Response:

```json
{
  "key": "value",
  "anotherKey": 123
}
```
"""


def create_gpt_json(unstructured_json):
    gpt_json = get_chat_completion(system_prompt, unstructured_json)
    return gpt_json


def extract_json(gpt_output):
    unstructured_json = gpt_output
    if "```json" in unstructured_json:
        unstructured_json = unstructured_json.replace("```json", "```")
    json_string = ""
    if "```" in unstructured_json:
        # Extract JSON using regular expression
        match = re.search(r"```(.*?)```", unstructured_json, re.DOTALL)
        if match:
            json_string = match.group(1).strip()
        else:
            json_string = unstructured_json.strip()
    else:
        json_string = unstructured_json
    return json_string
